
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
            {"data": "stock"}
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
                    text: '<span><i class="fa fa-print bigger-110 grey"></i> PDF</span>',
                    className: 'dt-button buttons-print btn btn-white btn-primary btn-bold',
                    extend: 'pdfHtml5',
                    //filename: 'dt_custom_pdf',
                    orientation: 'landscape', //portrait
                    pageSize: 'A4', //A3 , A5 , A6 , legal , letter
                    download: 'open',
                    exportOptions: {
                        columns: [0, 1, 2, 3, 5],
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
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="' + data + '" width="30" height="30" alt="image" class="img-circle elevation-2">';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var span;
                    if (data === 0){
                         span = '<span class="badge badge-danger">'+data+'</span>';
                    } else if (data > 1 && data <= 5){
                        span = '<span class="badge badge-warning">'+data+'</span>';
                    } else if(data>5){
                        span = '<span class="badge badge-success">'+data+'</span>';
                    }
                    return span
                }
            },
        ]
    });
}

$(function () {
    datatable_fun();
});