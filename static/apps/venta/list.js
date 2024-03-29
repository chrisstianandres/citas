var datatable;
var datos = {
    fechas: {
        'start_date': '',
        'end_date': '',
        'action': 'list'
    },
    add: function (data) {
        if (data.key === 1) {
            this.fechas['start_date'] = data.startDate.format('YYYY-MM-DD');
            this.fechas['end_date'] = data.endDate.format('YYYY-MM-DD');
        } else {
            this.fechas['start_date'] = '';
            this.fechas['end_date'] = '';
        }
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: this.fechas,
            success: function (data) {
                datatable.clear();
                datatable.rows.add(data).draw();
            }
        });

    },
};

function datatable_fun() {
    datatable = $("#datatable").DataTable({
        destroy: true,
        scrollX: true,
        autoWidth: false,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: datos.fechas,
            dataSrc: ""
        },
        columns: [
            {"data": "fecha_factura"},
            {"data": "user.full_name"},
            {"data": "subtotal"},
            {"data": "iva"},
            {"data": "total"},
            {"data": "id"},
            {"data": "estado_text"},
            {"data": "id"}
        ],
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json',
            buttons: {
                copyTitle: 'Copiado al Portapapeles',
                copySuccess: {
                    _: '%d Lineas copiadas',
                    1: '1 Linea copiada'
                }
            }
        },
        order: [[4, "desc"]],
        dom: "<'row'<'clearfix'<'pull-right tableTools-container'<'dt-buttons btn-overlap btn-group' B>>>>" +
            "<'row'<'col-sm-12 col-md-3'l>>" +
            "<'row'<'col-sm-12 col-md-12'f>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        buttons: {
            dom: {
                button: {
                    className: '',

                },
                container: {
                    className: 'buttons-container float-md-right'
                }
            },
            buttons: [
                {
                    text: '<span><i class="fa fa-print bigger-110 grey"></i> PDF</span>',
                    className: 'dt-button buttons-print btn btn-white btn-primary btn-bold',
                    extend: 'pdfHtml5',
                    filename: 'Listado de Compras',
                    orientation: 'landscape', //portrait
                    pageSize: 'A4', //A3 , A5 , A6 , legal , letter
                    download: 'open',
                    exportOptions: {
                        columns: [0, 1, 2, 3, 4, 5, 6],
                        search: 'applied',
                        order: 'applied'
                    },
                    customize: customize
                },
                {
                    text: '<i class="fa fa-copy bigger-110 pink"></i> Copiar</span>',
                    className: 'dt-button buttons-copy buttons-html5 btn btn-white btn-primary btn-bold',
                    extend: 'copy',
                }
            ],
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
                    var detalle = '<a type="button" rel="detalle" class="btn btn-success btn-xs btn-round" style="color: white" data-toggle="tooltip" title="Detalle de Venta" ><i class="fa fa-search"></i></a>' + ' ';
                    var devolver = row.user.tipo===0? '<a type="button" rel="devolver" class="btn btn-danger btn-xs btn-round" style="color: white" data-toggle="tooltip" title="Anular"><i class="fa fa-times"></i></a>'+' ':' ';
                    var pdf = '<a type="button" href= "/transaccion/printpdf/' + data + '" rel="pdf" ' +
                        'class="btn btn-primary btn-xs btn-round" style="color: white" data-toggle="tooltip" ' +
                        'title="Reporte PDF"><i class="fa fa-file-pdf-o"></i></a>';
                    return detalle + devolver + pdf;
                }
            },
            {
                targets: [-2],
                render: function (data, type, row) {
                    return row.estado_text;
                }
            },
            {
                targets: [-3],
                render: function (data, type, row) {
                    return pad(data, 10);
                }
            },
            {
                targets: [2, 3, 4],
                render: function (data, type, row) {
                    return '$ ' + data;
                }
            },
        ],
        createdRow: function (row, data, dataIndex) {
            if (data.estado === 1) {
                $('td', row).eq(6).html('<span class = "badge badge-success" style="color: white ">' + data.estado_text + ' </span>');
            } else {
                $('td', row).eq(6).html('<span class = "badge badge-danger" style="color: white "> ' + data.estado_text + ' </span>');
                $('td', row).eq(7).find('a[rel="devolver"]').hide();
                $('td', row).eq(7).find('a[rel="pdf"]').hide();
            }

        }
    });
}


function daterange() {
    $('#fecha').daterangepicker({
        locale: {
            format: 'YYYY-MM-DD',
            applyLabel: '<i class="fa fa-search"></i> Buscar',
            cancelLabel: '<i class="fa fa-times"></i> Cancelar',
        }
    }).on('apply.daterangepicker', function (ev, picker) {
        picker['key'] = 1;
        datos.add(picker);
        // filter_by_date();

    }).on('cancel.daterangepicker', function (ev, picker) {
        picker['key'] = 0;
        datos.add(picker);

    });

}

function pad(str, max) {
    str = str.toString();
    return str.length < max ? pad("0" + str, max) : str;
}

$(function () {
    daterange();
    datatable_fun();
    $('#datatable tbody')
        .on('click', 'a[rel="devolver"]', function () {
            $('.tooltip').remove();
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            var parametros = {'id': data.id, 'action': 'estado'};
            save_estado('Alerta',
                window.location.pathname, 'Esta seguro que desea anular esta venta?', parametros,
                function () {
                    menssaje_ok('Exito!', 'Exito al anular la Venta', 'far fa-smile-wink', function () {
                        datatable.ajax.reload(null, false);
                    })
                });

        })
        .on('click', 'a[rel="detalle"]', function () {
            $('.tooltip').remove();
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            $('#Modal').modal('show');
            $("#tbldetalle_venta").DataTable({
                responsive: true,
                autoWidth: false,
                language: {
                    "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
                },
                destroy: true,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'detalle',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: 'nombre'},
                    {data: 'tipo'},
                    {data: 'duracion'},
                    {data: 'categoria'},
                    {data: 'presentacion'},
                    {data: 'cantidad'},
                    {data: 'precio'},
                    {data: 'subtotal'},
                ],
                columnDefs: [
                    {
                        targets: '_all',
                        class: 'text-center'
                    },
                    {
                        targets: [-1, -2],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            console.log(row);
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    }
                ],
            });
        });

    $('#nuevo').on('click', function () {
       window.location.href = '/transaccion/venta/nuevo'
    });
});

