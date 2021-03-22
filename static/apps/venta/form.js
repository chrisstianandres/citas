var dt_detalle;
var tbl_productos;
var tbl_servicios;
var tipo_venta = $('#id_tipo_venta');
var iva_emp = $('#iva_emp').val();
var ventas = {
    items: {
        fecha: '',
        cliente: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        detalle: []
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
    get_ids_serv: function () {
        var ids = [];
        $.each(this.items.detalle, function (key, value) {
             if (value.tipo === 'Servicio') {
                 ids.push(value.id)
             }
        });
        return ids;
    },
    calculate: function () {
        var subtotal = 0.00;
        $.each(this.items.lotes, function (pos, dict) {
            dict.subtotal = dict.cantidad * parseFloat(dict.valor_ave).toFixed(2);
            subtotal += dict.subtotal;
        });
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * (iva_emp / 100);
        this.items.total = this.items.subtotal + this.items.iva;
        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="iva"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    calculate_por_menor: function () {
        var subtotal = 0.00;
        $.each(this.items.lotes, function (pos, dict) {
            dict.subtotal = dict.peso_promedio * dict.cantidad * parseFloat(dict.valor_libra).toFixed(2);
            dict.valor_ave = dict.peso_promedio * parseFloat(dict.valor_libra).toFixed(2);
            subtotal += dict.subtotal;
        });
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * (iva_emp / 100);
        this.items.total = this.items.subtotal + this.items.iva;
        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="iva"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    add: function (data) {
        var array;
        if (data.tipo === 'Producto') {
            array = {
                'nombre': data.producto.nombre,
                'tipo': data.tipo,
                'duracion': 'N/A',
                'categoria': data.producto.categoria.nombre,
                'presentacion': data.producto.presentacion.nombre,
                'stock': data.stock_actual,
                'cantidad': 1,
                'precio': data.precio_venta,
                'subtotal': 1,
                'id': data.producto.id,
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
                'precio': 1.00,
                'subtotal': 1,
                'id': data.id,
            };
            this.items.detalle.push(array);
        }
        // this.items..push(data);
        this.list();
    },
    list: function () {
        // this.calculate();
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
            // columnDefs: [
            //     {
            //         targets: '_all',
            //         class: 'text-center',
            //
            //     },
            //     {
            //         targets: [1],
            //         class: 'text-center',
            //         render: function (data, type, row) {
            //             return parseFloat(data).toFixed(2) + ' Lbs';
            //         }
            //     },
            //     {
            //         targets: [2],
            //         class: 'text-center',
            //         render: function (data, type, row) {
            //             return '<input type="text" class="form-control input-sm" value="' + parseFloat(data).toFixed(2) + '" name="v_libra">';
            //         }
            //     },
            //     {
            //         targets: [-1],
            //         class: 'text-center',
            //         render: function (data, type, row) {
            //             return '<a type="button" rel="remove" class="btn btn-danger btn-xs btn-round" ' +
            //                 'style="color: white" data-toggle="tooltip" title="Quitar"><i class="fa fa-times"></i>' +
            //                 '</a>';
            //         }
            //     },
            //     {
            //         targets: [-4],
            //         render: function (data, type, row) {
            //             return '$ ' + parseFloat(data).toFixed(2);
            //         }
            //     },
            //     {
            //         targets: [-3],
            //         render: function (data, type, row) {
            //             return '<input type="text" class="form-control input-sm" value="' + data + '" name="cantidad">';
            //         }
            //     },
            //     {
            //         targets: [-2],
            //         render: function (data, type, row) {
            //             return '$ ' + parseFloat(data).toFixed(2);
            //         }
            //     },
            // ],
            // createdRow: function (row, data, dataIndex) {
            //     $(row).find('input[name="cantidad"]').TouchSpin({
            //         min: 1,
            //         max: data.stock_actual,
            //         step: 1
            //     });
            //     $(row).find('input[name="v_libra"]').TouchSpin({
            //         min: 0.01,
            //         decimals: 2,
            //         max: 100000000,
            //         step: 0.01,
            //         prefix: '$'
            //     });
            //
            // }
        });
    },

};
$(function () {
    buscar_productos();
    //seccion Medcicinas
    $('#datatable_detalle tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = dt_detalle.cell($(this).closest('td, li')).index();
            borrar_todo_alert('Alerta de Eliminación',
                'Esta seguro que desea eliminar esta ave de tu detalle de venta?', function () {
                    var p = ventas.items.lotes[tr.row];
                    ventas.items.lotes.splice(tr.row, 1);
                    menssaje_ok('Confirmacion!', 'Ave Eliminada eliminada', 'far fa-smile-wink', function () {
                        ventas.list();
                    });
                })
        })
        .on('change', 'input[name="cantidad"]', function () {
            var cantidad = parseInt($(this).val());
            var tr = dt_detalle.cell($(this).closest('td, li')).index();
            ventas.items.lotes[tr.row].cantidad = cantidad;
            ventas.calculate();
            $('td:eq(8)', dt_detalle.row(tr.row).node()).html('$' + ventas.items.lotes[tr.row].subtotal.toFixed(2));
        })
        .on('change', 'input[name="peso"]', function () {
            var peso = parseFloat($(this).val()).toFixed(2);
            var tr = dt_detalle.cell($(this).closest('td, li')).index();
            ventas.items.lotes[tr.row].peso_promedio = peso;
            ventas.calculate_por_menor();
            $('td:eq(8)', dt_detalle.row(tr.row).node()).html('$' + ventas.items.lotes[tr.row].subtotal.toFixed(2));
            $('td:eq(6)', dt_detalle.row(tr.row).node()).html('$' + ventas.items.lotes[tr.row].valor_ave.toFixed(2));
        })
        .on('change', 'input[name="v_libra"]', function () {
            var valor_libra = parseFloat($(this).val()).toFixed(2);
            var tr = dt_detalle.cell($(this).closest('td, li')).index();
            ventas.items.lotes[tr.row].valor_libra = valor_libra;
            ventas.calculate_por_menor();
            $('td:eq(8)', dt_detalle.row(tr.row).node()).html('$' + ventas.items.lotes[tr.row].subtotal.toFixed(2));
            $('td:eq(6)', dt_detalle.row(tr.row).node()).html('$' + ventas.items.lotes[tr.row].valor_ave.toFixed(2));
        })
        .on('change', 'input[name="precio"]', function () {
            var precio = parseFloat($(this).val()).toFixed(2);
            var tr = dt_detalle.cell($(this).closest('td, li')).index();
            ventas.items.lotes[tr.row].valor_ave = precio;
            ventas.calculate();
            $('td:eq(8)', dt_detalle.row(tr.row).node()).html('$' + ventas.items.lotes[tr.row].subtotal.toFixed(2));
        });
    $('#vaciar_detalle')
        .on('click', function () {
            if (ventas.items.lotes.length === 0) return false;
            borrar_todo_alert('Alerta de Eliminación',
                'Esta seguro que desea eliminar todos las aves seleccionadas?', function () {
                    ventas.items.lotes = [];
                    menssaje_ok('Confirmacion!', 'Aves eliminados', 'far fa-smile-wink', function () {
                        ventas.list();
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
            buscar_servicios();
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

    $('#id_cliente')
        .select2({
            theme: "classic",
            language: {
                inputTooShort: function () {
                    return "Ingresa al menos un caracter...";
                },
                "noResults": function () {
                    return "Sin resultados";
                },
                "searching": function () {
                    return "Buscando...";
                }
            },
            allowClear: true,
            ajax: {
                delay: 250,
                type: 'POST',
                url: '/cliente/lista',
                data: function (params) {
                    return {
                        term: params.term,
                        'action': 'search'
                    };
                },
                processResults: function (data) {
                    return {
                        results: data
                    };

                },

            },
            placeholder: 'Busca un Cliente',
            minimumInputLength: 1,
        });

    $('#id_lote')
        .select2({
            theme: "classic",
            language: {
                inputTooShort: function () {
                    return "Ingresa al menos un caracter...";
                },
                "noResults": function () {
                    return "Sin resultados";
                },
                "searching": function () {
                    return "Buscando...";
                }
            },
            allowClear: true,
            ajax: {
                delay: 250,
                type: 'POST',
                url: '/lote/lista',
                data: function (params) {
                    return {
                        term: params.term,
                        'action': 'search_ave',
                        'ids': JSON.stringify(ventas.get_ids())
                    };
                },
                processResults: function (data) {
                    return {
                        results: data
                    };

                },

            },
            placeholder: 'Busca un tipo de Ave',
            minimumInputLength: 1,
        })
        .on('select2:select', function (e) {
            $.ajax({
                type: "POST",
                url: '/lote/lista',
                data: {
                    "id": $('#id_lote option:selected').val(),
                    "action": 'get'
                },
                dataType: 'json',
                success: function (data) {
                    ventas.add(data[0]);
                    $('#id_lote').val(null).trigger('change');

                },
                error: function (xhr, status, data) {
                    alert(data['0']);
                },

            })
        });


    $('#Modal_person')
        .on('hidden.bs.modal', function (e) {
            reset('#form_person');
            $('#form_person').trigger("reset");
        });

    $('#save')
        .on('click', function () {
            if ($('select[name="cliente"]').val() === "") {
                menssaje_error('Error!', "Debe seleccionar un Cliente", 'far fa-times-circle');
                return false
            } else if (ventas.items.lotes.length === 0) {
                menssaje_error('Error!', "Debe seleccionar al menos una tipo de Ave", 'far fa-times-circle');
                return false
            } else {
                var parametros;
                ventas.items.fecha = $('#id_fecha_venta').val();
                ventas.items.cliente = $('#id_cliente option:selected').val();
                parametros = {'ventas': JSON.stringify(ventas.items)};
                parametros['action'] = 'add';
                save_with_ajax('Alerta',
                    '/venta/nuevo', 'Esta seguro que desea guardar esta Venta?', parametros, function (response) {
                        printpdf('Alerta!', '¿Desea generar el comprobante en PDF?', function () {
                            window.open('/venta/printpdf/' + response['id'], '_blank');
                            listado.fadeIn();
                            formulario.fadeOut();
                            $('#id_cliente').val(null).trigger('change');
                            ventas.items.lotes = [];
                            datatable.ajax.reload(null, false);
                        }, function () {
                            listado.fadeIn();
                            formulario.fadeOut();
                            $('#id_cliente').val(null).trigger('change');
                            ventas.items.lotes = [];
                            datatable.ajax.reload(null, false);
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
                {data: "producto.nombre"},
                {data: "producto.categoria.nombre"},
                {data: "producto.presentacion.nombre"},
                {data: "stock_actual"},
                {data: "id"},
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
                        return '<a style="color: white" type="button" class="btn btn-success btn-xs" rel="take" ' +
                            'data-toggle="tooltip" title="Seleccionar Insumo"><i class="fa fa-check"></i></a>' + ' '

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

});

