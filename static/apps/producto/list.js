
var datatable;

function datatable_fun() {
    datatable = $("#datatable").DataTable({
        responsive: true,
        autoWidth: false,
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
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {'action': 'list'},
            dataSrc: ""
        },
        columns: [
            {"data": "nombre"},
            {"data": "categoria.nombre"},
            {"data": "presentacion.nombre"},
            {"data": "descripcion"},
            {"data": "imagen"},
            {"data": "qr"},
            {"data": "id"}
        ],
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
                text: '<i class="fa fa-qrcode"></i> Exportar codigos QR</i>',
                className: 'dt-button btn btn-white btn-danger btn-bold',
                action: function () {
                    window.location.href = '/transaccion/printQR'
                }
            },
                {
                    text: '<span><i class="fa fa-print bigger-110 grey"></i> PDF</span>',
                    className: 'dt-button buttons-print btn btn-white btn-primary btn-bold',
                    extend: 'pdfHtml5',
                    //filename: 'dt_custom_pdf',
                    orientation: 'landscape', //portrait
                    pageSize: 'A4', //A3 , A5 , A6 , legal , letter
                    download: 'open',
                    exportOptions: {
                        columns: [1, 2, 3],
                        search: 'applied',
                        order: 'applied'
                    },
                    customize,
                },
                {
                    text: '<i class="fa fa-copy bigger-110 pink"></i> Copiar</span>',
                    className: 'dt-button buttons-copy buttons-html5 btn btn-white btn-primary btn-bold',
                    extend: 'copy',
                }
            ],
        },

        dom: "<'row'<'clearfix'<'pull-right tableTools-container'<'dt-buttons btn-overlap btn-group' B>>>>" +
            "<'row'<'col-sm-12 col-md-3'l>>" +
            "<'row'<'col-sm-12 col-md-12'f>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        columnDefs: [
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data) {
                    return '<img src="' + data + '" width="50" height="50" alt="image" class="img-circle elevation-2">';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                width: '10%',
                orderable: false,
                render: function (data, type, row) {
                    var edit = '<a style="color: white" type="button" class="btn btn-primary btn-xs" rel="edit" ' +
                        'data-toggle="tooltip" title="Editar Datos"><i class="fa fa-edit"></i></a>' + ' ';
                    var del = '<a type="button" class="btn btn-danger btn-xs"  style="color: white" rel="del" ' +
                        'data-toggle="tooltip" title="Eliminar"><i class="fa fa-trash"></i></a>' + ' ';
                    return edit + del
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data) {
                    return '<img src="' + data + '" width="80" alt="qr_code" height="80"  rel="qr_code" class="img-responsive">';
                }
            },
        ]
    });
}

$(function () {
    datatable_fun();
    //Botones dentro de datatable
    $('#datatable tbody')
        .on('click', 'a[rel="del"]', function () {
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            var parametros = {'id': data.id, 'action': 'delete'};
            save_estado('Alerta',
                window.location.pathname, 'Esta seguro que desea eliminar este producto?', parametros,
                function () {
                    menssaje_ok('Exito!', 'Exito al eliminar el producto!', 'far fa-smile-wink', function () {
                        datatable.ajax.reload(null, false);
                    })
                });
        })
        .on('click', 'a[rel="edit"]', function () {
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            window.location.href = '/producto/editar/'+data.id
        })
        .on('click', 'img[rel="qr_code"]', function () {
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            $('#titulo_modal').html('<i class="fa fa-qrcode"> Codigo QR</i>');
            $('#body_fluid').html('<img src="' + data.qr + '" width="300" alt="qr_code" height="300"  class="img-responsive">');
            $('#modal_image').modal('show');
        })
        .on('click', 'img[alt="image"]', function () {
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            $('#titulo_modal').html('<i class="fa fa-image"> '+data.nombre+'</i>');
            $('#body_fluid').html('<img src="' + data.imagen + '" width="300" alt="qr_code" height="300"  class="img-responsive">');
            $('#modal_image').modal('show');
        });

    //botones de formulario
    $('#nuevo').on('click', function () {
        window.location.href = '/producto/nuevo'
    });

});