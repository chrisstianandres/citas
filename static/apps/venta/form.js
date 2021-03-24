var dt_detalle;
var tbl_productos;
var tbl_servicios;
var iva_emp = $('#iva_emp').val();
var ventas = {
    items: {
        fecha: '',
        cliente: '',
        duracion: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        detalle: [],
        empleado: []
    },
    get_ids: function () {
        var ids = [];
        $.each(this.items.detalle, function (key, value) {
            if (value.tipo === 'Producto') {
                ids.push(value.id)
            }
        });
        return ids;
    },
    get_ids_empleado: function () {
        var ids = [];
        $.each(this.items.empleado, function (key, value) {
            ids.push(value.id)
        });
        return ids;
    },
    get_ids_serv: function () {
        var ids_s = [];
        $.each(this.items.detalle, function (key, value) {
            if (value.tipo === 'Servicio') {
                ids_s.push(value.id)
            }
        });
        return ids_s;
    },
    calculate: function () {
        var subtotal = 0.00;
        $.each(this.items.detalle, function (pos, dict) {
            dict.subtotal = dict.cantidad * parseFloat(dict.precio).toFixed(2);
            subtotal += dict.subtotal;
        });
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * (iva_emp / 100);
        this.items.total = this.items.subtotal + this.items.iva;
        $('#sub_gen').text('$' + this.items.subtotal.toFixed(2));
        $('#iva_gen').text('$' + this.items.iva.toFixed(2));
        $('#tot_gen').text('$' + this.items.total.toFixed(2));
    },
    calculate_duracion: function () {
        var duracion = 0.00;
        $.each(this.items.detalle, function (pos, dict) {
            if (value.tipo === 'Servicio') {
                duracion += dict.duracion
            }
        });
        this.items.duracion = duracion;
    },
    add: function (data) {
        var array;
        if (data.tipo === 'Producto') {
            array = {
                'nombre': data.nombre,
                'tipo': data.tipo,
                'duracion': 'N/A',
                'categoria': data.categoria.nombre,
                'presentacion': data.presentacion.nombre,
                'stock': data.stock,
                'cantidad': 1,
                'precio': data.precio_venta,
                'subtotal': 1,
                'id': data.id_det,
            };
            this.items.detalle.push(array);
        } else {
            array = {
                'nombre': data.nombre,
                'tipo': data.tipo,
                'duracion': data.duracion,
                'categoria': data.categoria.nombre,
                'presentacion': 'N/A',
                'stock': 'N/A',
                'cantidad': 1,
                'precio': data.precio,
                'subtotal': 1,
                'id': data.id,
            };
            this.items.detalle.push(array);
        }
        this.list();
    },
    list: function () {
        this.calculate();
        dt_detalle = $("#table_detalle").DataTable({
            destroy: true,
            responsive: true,
            autoWidth: false,
            dom: 'tipr',
            data: this.items.detalle,
            columns: [
                {data: "nombre"},
                {data: "tipo"},
                {data: "duracion"},
                {data: "categoria"},
                {data: "presentacion"},
                {data: "stock"},
                {data: "cantidad"},
                {data: "precio"},
                {data: "subtotal"},
                {data: "id"}
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
                    targets: [2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.tipo === 'Servicio') {
                            return '<input type="text" class="form-control input-sm" value="' + data + '" name="duracion">';
                        } else {
                            return data
                        }
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var quitar = '<a type="button" rel="remove" class="btn btn-danger btn-xs btn-round" ' +
                            'style="color: white" data-toggle="tooltip" title="Quitar"><i class="fa fa-times"></i>' +
                            '</a>';
                        var empleado = '<a type="button" rel="det" class="btn btn-info btn-xs btn-round" ' +
                            'style="color: white" data-toggle="tooltip" title="Detalle de Empleado"><i class="fa fa-search"></i>' +
                            '</a>' + ' ';
                        return empleado + quitar
                    }
                },
                {
                    targets: [-4],
                    render: function (data, type, row) {
                        if (row.tipo === 'Producto') {
                            return '<input type="text" class="form-control input-sm" value="' + data + '" name="cantidad">';
                        } else {
                            return '<input type="text" class="form-control input-sm" value="' + data + '" name="cantidad_serv">';
                        }
                    }
                },
                {
                    targets: [-3],
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control input-sm" value="' + data + '" name="precio">';
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
                    max: data.stock,
                    step: 1,
                    buttondown_class: 'btn btn-white btn-danger btn-bold btn-xs',
                    buttonup_class: 'btn btn-white btn-danger btn-bold btn-xs',
                });
                $(row).find('input[name="cantidad_serv"]').TouchSpin({
                    min: 1,
                    max: 100,
                    step: 1,
                    buttondown_class: 'btn btn-white btn-danger btn-bold btn-xs',
                    buttonup_class: 'btn btn-white btn-danger btn-bold btn-xs',
                });
                $(row).find('input[name="precio"]').TouchSpin({
                    min: 0.50,
                    max: 500.00,
                    step: 0.01,
                    decimals: 2,
                    buttondown_class: 'btn btn-white btn-info btn-bold btn-xs',
                    buttonup_class: 'btn btn-white btn-info btn-bold btn-xs',
                });
                $(row).find('input[name="duracion"]').TouchSpin({
                    min: 15,
                    max: 60,
                    step: 1,
                    buttondown_class: 'btn btn-white btn-success btn-bold btn-xs',
                    buttonup_class: 'btn btn-white btn-success btn-bold btn-xs',
                });
                if (data.tipo === 'Producto') {
                    $(row).find('a[rel="det"]').hide();
                }
            }
        });
    },

};
$(function () {
    buscar_productos();
    //seccion Medcicinas
    $('#table_detalle tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = dt_detalle.cell($(this).closest('td, li')).index();
            borrar_todo_alert('Alerta de Eliminación',
                'Esta seguro que desea eliminar esta elemento de tu detalle de venta?', function () {
                    var p = ventas.items.detalle[tr.row];
                    ventas.items.detalle.splice(tr.row, 1);
                    menssaje_ok('Confirmacion!', 'Elemento eliminado', 'far fa-smile-wink', function () {
                        ventas.list();
                        buscar_servicios();
                        buscar_productos();
                    });
                })
        })
        .on('change', 'input[name="cantidad"]', function () {
            var cantidad = parseInt($(this).val());
            var tr = dt_detalle.cell($(this).closest('td, li')).index();
            ventas.items.detalle[tr.row].cantidad = cantidad;
            ventas.calculate();
            $('td:eq(8)', dt_detalle.row(tr.row).node()).html('$' + ventas.items.detalle[tr.row].subtotal.toFixed(2));
        })
        .on('change', 'input[name="cantidad_serv"]', function () {
            var cantidad = parseInt($(this).val());
            var tr = dt_detalle.cell($(this).closest('td, li')).index();
            ventas.items.detalle[tr.row].cantidad = cantidad;
            ventas.calculate();
            $('td:eq(8)', dt_detalle.row(tr.row).node()).html('$' + ventas.items.detalle[tr.row].subtotal.toFixed(2));
        })
        .on('change', 'input[name="duracion"]', function () {
            var duracion = parseInt($(this).val());
            var tr = dt_detalle.cell($(this).closest('td, li')).index();
            ventas.items.detalle[tr.row].duracion = duracion;
            ventas.calculate_duracion();
        })
        .on('change', 'input[name="precio"]', function () {
            var precio = parseFloat($(this).val()).toFixed(2);
            var tr = dt_detalle.cell($(this).closest('td, li')).index();
            ventas.items.detalle[tr.row].precio = precio;
            ventas.calculate();
            $('td:eq(8)', dt_detalle.row(tr.row).node()).html('$' + ventas.items.detalle[tr.row].subtotal.toFixed(2));
        });

    $('input[name="duracion_servicio"]').TouchSpin({
        min: 1,
        max: 480,
        step: 1,
        prefix: 'Minutos',
        buttondown_class: 'btn btn-white btn-info btn-bold btn-sm',
        buttonup_class: 'btn btn-white btn-info btn-bold btn-sm',
    });
    $('#vaciar')
        .on('click', function () {
            if (ventas.items.detalle.length === 0) return false;
            borrar_todo_alert('Alerta de Eliminación',
                'Esta seguro que desea eliminar todos los elementos seleccionadas?', function () {
                    ventas.items.detalle = [];
                    menssaje_ok('Confirmacion!', 'Elementos eliminados', 'far fa-smile-wink', function () {
                        ventas.list();
                        buscar_servicios();
                        buscar_productos();
                    });
                });
        });

    $('#productos_buscador tbody')
        .on('click', 'a[rel="take"]', function () {
            var tr = tbl_productos.cell($(this).closest('td, li')).index();
            var data = tbl_productos.row(tr.row).data();
            ventas.add(data);
            buscar_productos();
        });

    $('#servicios_buscador tbody')
        .on('click', 'a[rel="take"]', function () {
            var tr = tbl_servicios.cell($(this).closest('td, li')).index();
            var data = tbl_servicios.row(tr.row).data();
            ventas.add(data);
            menssaje_ok('Elegir un empleado', 'A seleccionado un servicio, por favor elija un empleado que ' +
                'brindara este servicio', 'fa fa', function () {
                $('#modal_empleado').modal({backdrop: 'static', keyboard: false});
                buscar_empleados();
            });
            buscar_servicios();
        });

    $('#tbl_empleados tbody')
        .on('click', 'a[rel="take"]', function () {
            var tr = tbl_productos.cell($(this).closest('td, li')).index();
            var data = tbl_productos.row(tr.row).data();
            // ventas.add(data);
            // buscar_productos();
        });

    $('#id_new_cliente')
        .on('click', function () {
            $('#Modal_person').modal('show');
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
                    '/cliente/nuevo', 'Esta seguro que desea guardar este cliente?', parametros,
                    function (response) {
                        menssaje_ok('Exito!', 'Exito al guardar este cliente!', 'far fa-smile-wink', function () {
                            $('#Modal_person').modal('hide');
                            var newOption = new Option(response.cliente['full_name'], response.cliente['id'], false, true);
                            $('#id_cliente').append(newOption).trigger('change');
                        });
                    });
            }

        });

    $('#id_user').chosen({no_results_text: "No se encontraron resultados para: "});


    $('#Modal_person')
        .on('hidden.bs.modal', function (e) {
            reset('#form_person');
            $('#form_person').trigger("reset");
        });

    $('#save')
        .on('click', function () {
            if ($('select[name="user"]').val() === "") {
                menssaje_error('Error!', "Debe seleccionar un Cliente", 'far fa-times-circle');
                return false
            } else if (ventas.items.detalle.length === 0) {
                menssaje_error('Error!', "Debe seleccionar al menos un producto o servicio", 'far fa-times-circle');
                return false
            } else {
                var parametros;
                ventas.items.fecha = $('#id_fecha_venta').val();
                ventas.items.cliente = $('#id_user').val();
                ventas.items.duracion = $('#id_duracion_servicio').val();
                parametros = {'ventas': JSON.stringify(ventas.items)};
                parametros['action'] = 'add';
                save_with_ajax('Alerta',
                    window.location.pathname, 'Esta seguro que desea guardar esta Venta?', parametros, function (response) {
                        printpdf('Alerta!', '¿Desea generar el comprobante en PDF?', function () {
                            window.open('/venta/printpdf/' + response['id'], '_blank');
                            window.location.href = '/transaccion/venta/lista'
                        }, function () {
                            window.location.href = '/transaccion/venta/lista'
                        })
                    });
            }
        });

    $('#id_buscador_select').on('change', function () {
        var productos_container = $('#productos_buscador');
        var servicios_container = $('#servicios_buscador');
        if ($(this).val() === '0') {
            productos_container.attr('style', 'display:true');
            servicios_container.attr('style', 'display:none');
            buscar_productos();
        } else {
            productos_container.attr('style', 'display:none');
            servicios_container.attr('style', 'display:true');
            buscar_servicios();
        }
    });

    function buscar_productos() {
        tbl_productos = $("#table_productos").DataTable({
            destroy: true,
            autoWidth: false,
            dataSrc: "",
            responsive: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {'action': 'search_prod', 'ids': JSON.stringify(ventas.get_ids())},
                dataSrc: ""
            },
            language: {
                "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
            },
            columns: [
                {data: "nombre"},
                {data: "categoria.nombre"},
                {data: "presentacion.nombre"},
                {data: "stock"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    width: '10%',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a style="color: white" type="button" class="btn btn-success btn-round btn-xs" rel="take" ' +
                            'data-toggle="tooltip" title="Seleccionar"><i class="fa fa-check"></i></a>' + ' '

                    }
                },
                {
                    targets: [-2],
                    orderable: false,
                    render: function (data, type, row) {
                        return '<span class="badge badge-primary">' + data + '</span>'

                    }
                },

            ]
        });
    }


    function buscar_servicios() {
        tbl_servicios = $("#table_servicios").DataTable({
            destroy: true,
            autoWidth: false,
            dataSrc: "",
            responsive: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {'action': 'search_serv', 'ids': JSON.stringify(ventas.get_ids_serv())},
                dataSrc: ""
            },
            language: {
                "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
            },
            columns: [
                {data: "nombre"},
                {data: "categoria.nombre"},
                {data: "duracion"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    width: '10%',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a style="color: white" type="button" class="btn btn-success btn-round btn-xs" rel="take" ' +
                            'data-toggle="tooltip" title="Seleccionar"><i class="fa fa-check"></i></a>' + ' '

                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return data + ' Mts'

                    }
                },
            ]
        });
    }

    function buscar_empleados() {
        tbl_empleados = $("#table_empleado").DataTable({
            destroy: true,
            autoWidth: false,
            dataSrc: "",
            responsive: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {'action': 'search_empleados', 'ids': JSON.stringify(ventas.get_ids_empleado())},
                dataSrc: ""
            },
            language: {
                "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
            },
            columns: [
                {data: "full_name_list"},
                {data: "sexo"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    width: '10%',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a style="color: white" type="button" class="btn btn-success btn-round btn-xs" rel="take" ' +
                            'data-toggle="tooltip" title="Seleccionar"><i class="fa fa-check"></i></a>' + ' '

                    }
                },
            ]
        });
    }

});

