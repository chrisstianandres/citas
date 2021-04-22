var logotipo;
var datatable;
var action = 'add';
var pk = '';

function datatable_fun() {
    datatable = $("#datatable").DataTable({
        responsive: true,
        autoWidth: false,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {'action': 'list'},
            dataSrc: ""
        },
        columns: [
            {"data": "full_name_list"},
            {"data": "cedula"},
            {"data": "correo"},
            {"data": "telefono"},
            {"data": "celular"},
            {"data": "direccion"},
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
        dom: "<'row'<'clearfix'<'pull-right tableTools-container'<'dt-buttons btn-overlap btn-group' B>>>>" +
            "<'row'<'col-sm-12 col-md-3'l>>" +
            "<'row'<'col-sm-12 col-md-12'f>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        buttons: {
            dom: {
                button: {
                    className: 'btn',

                },
                container: {
                    className: 'buttons-container'
                }
            },
            buttons: [
                {
                    text: '<span><i class="fa fa-print bigger-110 grey"></i> PDF</span>',
                    className: 'dt-button buttons-print btn btn-white btn-primary btn-bold',
                    extend: 'pdfHtml5',
                    //filename: 'dt_custom_pdf',
                    orientation: 'landscape', //portrait
                    pageSize: 'A4', //A3 , A5 , A6 , legal , letter
                    // download: 'open',
                    exportOptions:
                        {
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

            ]
        },
        columnDefs: [
            {
                targets: '_all',
                class: 'text-center',
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var edit = '<a style="color: white" type="button" class="btn btn-primary btn-xs" rel="edit" ' +
                        'data-toggle="tooltip" title="Editar Datos"><i class="fa fa-pencil"></i></a>' + ' ';
                    var del = '<a type="button" class="btn btn-danger btn-xs"  style="color: white" rel="del" ' +
                        'data-toggle="tooltip" title="Eliminar"><i class="fa fa-trash"></i></a>' + ' ';
                    var est = '<a type="button" class="btn btn-success btn-xs"  style="color: white" rel="est" ' +
                        'data-toggle="tooltip" title="Cambiar estado"><i class="fa fa-cog"></i></a>' + ' ';
                    return edit + del + est;

                }
            },
            {
                targets: [-2],
                render: function (data, type, row) {
                    return '<span>' + data + '</span>'

                }
            },
        ],
        createdRow: function (row, data, dataIndex) {
            if (data.estado === 1) {
                $('td', row).eq(6).find('span').addClass("label label-danger arrowed-in");
            } else if (data.estado === 0) {
                $('td', row).eq(6).find('span').addClass("label label-success arrowed");
            }

        }

    });
}

$(function () {

    datatable_fun();
    $('#datatable tbody')
        .on('click', 'a[rel="del"]', function () {
            action = 'delete';
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            var parametros = {'id': data.id};
            parametros['action'] = action;
            save_estado('Alerta',
                '/empleado/eliminar/' + data.id, 'Esta seguro que desea eliminar este empleado?', parametros,
                function () {
                    menssaje_ok('Exito!', 'Exito al eliminar este empleado!', 'far fa-smile-wink', function () {
                        datatable.ajax.reload(null, false);
                    })
                })
        })
        .on('click', 'a[rel="edit"]', function () {
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            window.location.href = '/empleado/editar/' + data.id
        })
        .on('click', 'a[rel="est"]', function () {
            action = 'estado';
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            var parametros = {'id': data.id};
            parametros['action'] = action;
            save_estado('Alerta',
                window.location.pathname, 'Esta seguro que desea cambiar el estado de este empleado?', parametros,
                function () {
                    menssaje_ok('Exito!', 'Exito al cambiar de estado a este empleado!', 'far fa-smile-wink', function () {
                        datatable.ajax.reload(null, false);
                    })
                })
        });
});
