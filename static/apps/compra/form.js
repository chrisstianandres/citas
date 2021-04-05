var dt_detalle;
var indice = $('#indice').val();
var compras = {
    items: {
        fecha: '',
        comprobante: '',
        proveedor: '',
        subtotal: 0.00,
        pvp: 0.00,
        iva: 0.00,
        tasa_iva: 12.00,
        total: 0.00,
        productos: [],
    },
    get_ids: function () {
        var ids = [];
        $.each(this.items.productos, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    calculate: function () {
        var subtotal = 0.00;
        $.each(this.items.productos, function (pos, dict) {
            dict.subtotal = dict.cantidad * parseFloat(dict.precio);
            dict.pvp = parseFloat(dict.precio) * parseFloat(1 + (indice / 100));
            subtotal += dict.subtotal;
        });
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * (this.items.tasa_iva / 100);
        this.items.total = this.items.subtotal + this.items.iva;
        $('#sub_gen').text('$' + this.items.subtotal.toFixed(2));
        $('#iva_gen').text('$' + this.items.iva.toFixed(2));
        $('#tot_gen').text('$' + this.items.total.toFixed(2));
    },
    add: function (data) {
        this.items.productos.push(data);
        this.list();
    },

    list: function () {
        this.calculate();
        dt_detalle = $("#table_detalle").DataTable({
            destroy: true,
            responsive: true,
            autoWidth: false,
            dom: 'tipr',
            data: this.items.productos,
            columns: [
                {"data": "nombre"},
                {"data": "categoria.nombre"},
                {"data": "presentacion.nombre"},
                {"data": "cantidad"},
                {"data": "precio"},
                {"data": "subtotal"},
                {"data": "id"}
            ],
            language: {
                url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json',
            },
            columnDefs: [
                {
                    targets: '_all',
                    class: 'text-center',
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a type="button" rel="remove" class="btn btn-danger btn-xs btn-round" ' +
                            'style="color: white" data-toggle="tooltip" title="Quitar"><i class="fa fa-times"></i>' +
                            '</a>';
                    }
                },
                {
                    targets: [-3],
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control input-sm" value="' + data + '" name="precio">';
                    }
                },
                {
                    targets: [-4],
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control input-sm" value="' + data + '" name="cantidad">';
                    }
                },
                {
                    targets: [-2],
                    render: function (data, type, row) {
                        return '$ ' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            createdRow: function (row, data, dataIndex) {
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: 1000000,
                    step: 1,
                    buttondown_class: 'btn btn-white btn-info btn-bold btn-xs',
                    buttonup_class: 'btn btn-white btn-info btn-bold btn-xs',
                }).keypress(function (e) {
                    if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
                        return false;
                    }
                });
                $(row).find('input[name="precio"]').TouchSpin({
                    min: 0.50,
                    decimals: 2,
                    max: 100000000,
                    step: 0.01,
                    buttondown_class: 'btn btn-white btn-info btn-bold btn-sm',
                    buttonup_class: 'btn btn-white btn-info btn-bold btn-sm',
                }).keypress(function (e) {
                    if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
                        return false;
                    }
                });
            }
        });
    }
};
$(function () {
    buscar();
    //Iva porcentaje
    $('#id_tasa_iva')
        .TouchSpin({
            min: 0.00,
            decimals: 2,
            max: 100,
            step: 0.01,
            val: 12.00,
            buttondown_class: 'btn btn-white btn-info btn-bold btn-sm',
            buttonup_class: 'btn btn-white btn-info btn-bold btn-sm',
            prefix: '%'
        }).val('12.00').keypress(function (e) {
        if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
            return false;
        }
    }).on('change keyup', function () {
        compras.items.tasa_iva = parseFloat($(this).val());
        compras.calculate();
    })
    ;

    //seccion Productos
    $('#table_detalle tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = dt_detalle.cell($(this).closest('td, li')).index();
            borrar_todo_alert('Alerta de Eliminación',
                'Esta seguro que desea eliminar esta medicina de tu detalle?', function () {
                    var p = compras.items.productos[tr.row];
                    compras.items.productos.splice(tr.row, 1);
                    menssaje_ok('Confirmacion!', 'Productos eliminado', 'far fa-smile-wink', function () {
                        compras.list();
                        buscar();
                    });
                })
        })
        .on('change', 'input[name="cantidad"]', function () {
            var cantidad = parseInt($(this).val());
            var tr = dt_detalle.cell($(this).closest('td, li')).index();
            compras.items.productos[tr.row].cantidad = cantidad;
            compras.calculate();
            $('td:eq(5)', dt_detalle.row(tr.row).node()).html('$' + compras.items.productos[tr.row].subtotal.toFixed(2));
        })
        .on('change', 'input[name="precio"]', function () {
            var precio = parseFloat($(this).val()).toFixed(2);
            var tr = dt_detalle.cell($(this).closest('td, li')).index();
            compras.items.productos[tr.row].precio = precio;
            compras.calculate();
            $('td:eq(5)', dt_detalle.row(tr.row).node()).html('$' + compras.items.productos[tr.row].subtotal.toFixed(2));
        });

    $('#vaciar')
        .on('click', function () {
            if (compras.items.productos.length === 0) return false;
            borrar_todo_alert('Alerta de Eliminación',
                'Esta seguro que desea eliminar todos los productos seleccionadas?', function () {
                    compras.items.productos = [];
                    menssaje_ok('Confirmacion!', 'Productos eliminados', 'far fa-smile-wink', function () {
                        compras.list();
                        buscar();
                    });
                });
        });

    function buscar() {
        tbl_productos = $("#table_productos").DataTable({
            destroy: true,
            autoWidth: false,
            dataSrc: "",
            responsive: true,
            ajax: {
                url: '/producto/lista',
                type: 'POST',
                data: {'action': 'list_list', 'ids': JSON.stringify(compras.get_ids())},
                dataSrc: ""
            },
            language: {
                "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
            },
            info: false,
            columns: [
                {data: "nombre"},
                {data: "categoria.nombre"},
                {data: "presentacion.nombre"},
                {data: "id"}
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    width: '10%',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a style="color: white" type="button" class="btn btn-success btn-xs" rel="take" ' +
                            'data-toggle="tooltip" title="Seleccionar Insumo"><i class="fa fa-check"></i></a>' + ' '

                    }
                },
            ]
        });
    }


    $('#table_productos tbody')
        .on('click', 'a[rel="take"]', function () {
            var tr = tbl_productos.cell($(this).closest('td, li')).index();
            var data = tbl_productos.row(tr.row).data();
            compras.add(data);
            buscar();
        });

    $('#id_new_prov')
        .on('click', function () {
            $('#modal_person').modal('show');
        });

    $('#modal_person').on('hidden.bs.modal', function () {
        reset('#form_person');
    });

    $('#form_person')
        .on('submit', function (e) {
            e.preventDefault();
            var parametros = new FormData(this);
            parametros.append('action', 'add');
            parametros.append('id', '');
            var isvalid = $(this).valid();
            if (isvalid) {
                save_with_ajax2('Alerta',
                    '/proveedor/nuevo', 'Esta seguro que desea guardar este proveedor?', parametros,
                    function (response) {
                        menssaje_ok('Exito!', 'Exito al guardar este proveedor!', 'far fa-smile-wink', function () {
                            $('#modal_person').modal('hide');
                            $('#id_proveedor')
                                .append("<option value='" + response.proveedor['id'] + "' selected='selected'>" + response.proveedor['nombre'] + "</option>")
                                .trigger("chosen:updated");
                            search_info(response.proveedor['id']);
                        });
                    });
            }

        });

    $('#id_proveedor').chosen({no_results_text: "No se encontraron resultados para: "})
        .on('change', function () {
            var id = $(this).val();
            if (id >= 1) {
                search_info(id);
            } else {
                $('#direccion_prov').html('Sin Direccion');
                $('#telefono_prov').html('09xxxxxxxx');
            }

        });

    $('#Modal_person')
        .on('hidden.bs.modal', function (e) {
            reset('#form_person');
            $('#form_person').trigger("reset");
        });

    $('#save')
        .on('click', function () {
            if ($('select[name="proveedor"]').val() === "") {
                menssaje_error('Error!', "Debe seleccionar un proveedor", 'far fa-times-circle');
                return false
            } else if ($('input[name="comprobante"]').val() === "") {
                menssaje_error('Error!', "Debe ingresar un numero de comprobante", 'far fa-times-circle');
                return false
            } else if (compras.items.productos.length === 0) {
                menssaje_error('Error!', "Debe seleccionar al menos un Producto", 'fa fa-ban');
                return false
            } else {
                var parametros;
                compras.items.fecha = $('input[name="fecha"]').val();
                compras.items.proveedor = $('#id_proveedor').val();
                compras.items.comprobante = $('#id_comprobante').val();
                parametros = {'compras': JSON.stringify(compras.items)};
                parametros['action'] = 'add';
                console.log(compras.items);
                save_with_ajax('Alerta',
                    window.location.pathname, 'Esta seguro que desea guardar esta compra?', parametros, function (response) {
                        $('#id_proveedor').val(null).trigger('change');
                        window.location.href = '/compra/lista'
                    });
            }
        });

    $("#id_comprobante").keypress(function (e) {
        //if the letter is not digit then display error and don't type anything
        if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
            //display error message
            $("#errmsg").html("Solo numeros").show().fadeOut("slow");
            return false;
        }
    });

    var ano = new Date();
    $('#id_fecha').daterangepicker({
        locale: {
            format: 'YYYY-MM-DD',
            applyLabel: '<i class="fa fa-check"></i> Selccionar',
            cancelLabel: '<i class="fa fa-times"></i> Cancelar',
        },
        singleDatePicker: true,
        showDropdowns: true,
        maxDate: new Date(),
        minYear: ano.getFullYear() - 1,
        minDate: ano.getFullYear() - 1 + '-01-01'
    });

});


function search_info(id) {
    $.ajax({
        dataType: 'JSON',
        type: 'POST',
        url: window.location.pathname,
        data: {'id': id, 'action': 'get_prov'},
    })
        .done(function (data) {
            if (!data.hasOwnProperty('error')) {
                $('#direccion_prov').html(data[0].direccion);
                $('#telefono_prov').html(data[0].telefono);
                return false;
            }
            menssaje_error('Error', data.error, 'fas fa-exclamation-circle');

        })
        .fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        });

}
