var datos = {
    fechas: {
        'start_date': '',
        'end_date': '',
        'tipo': 0,
        'action': 'report'
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
$(function () {
    daterange();
    datatable = $("#datatable").DataTable({
        destroy: true,
        responsive: true,
        autoWidth: false,
        order: [[2, "asc"]],
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: datos.fechas,
            dataSrc: ""
        },
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
                    footer: true,
                    filename: 'Reporte de Ventas por productos',
                    orientation: 'landscape', //portrait
                    pageSize: 'A4', //A3 , A5 , A6 , legal , letter
                    download: 'open',
                    exportOptions: {
                        columns: [0, 1, 2, 3, 4, 5, 6],
                        search: 'applied',
                        order: 'applied'
                    },
                    customize: customize_report,
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
                targets: [-2, -3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-1],
                width: '20%',
                render: function (data, type, row) {
                    return '$ ' + data;
                }
            },
        ],
        footerCallback: function (row, data, start, end, display) {
            var api = this.api(), data;
            // Remove the formatting to get integer data for summation
            var intVal = function (i) {
                return typeof i === 'string' ?
                    i.replace(/[\$,]/g, '') * 1 :
                    typeof i === 'number' ?
                        i : 0;
            };
            // Total over this page
            cantidad = api.column(3, {page: 'current'}).data().reduce(function (a, b) {
                return intVal(a) + intVal(b);
            }, 0);
            cantidad_full = api.column(3).data().reduce(function (a, b) {
                return intVal(a) + intVal(b);
            }, 0);

            sin_iva = api.column(4, {page: 'current'}).data().reduce(function (a, b) {
                return intVal(a) + intVal(b);
            }, 0);
            siniva_full = api.column(4).data().reduce(function (a, b) {
                return intVal(a) + intVal(b);
            }, 0);


            iva = api.column(5, {page: 'current'}).data().reduce(function (a, b) {
                return intVal(a) + intVal(b);
            }, 0);
            iva_full = api.column(5).data().reduce(function (a, b) {
                return intVal(a) + intVal(b);
            }, 0);

            con_iva = api.column(6, {page: 'current'}).data().reduce(function (a, b) {
                return intVal(a) + intVal(b);
            }, 0);
            con_iva_full = api.column(6).data().reduce(function (a, b) {
                return intVal(a) + intVal(b);
            }, 0);

            // Update footer
            $(api.column(3).footer()).html(parseInt(cantidad) + '( ' + parseInt(cantidad_full) + ')');
            $(api.column(4).footer()).html(
                '$' + parseFloat(sin_iva).toFixed(2) + '(    $ ' + parseFloat(siniva_full).toFixed(2) + ')'
                // parseFloat(data).toFixed(2)
            );
            $(api.column(5).footer()).html(
                '$' + parseFloat(iva).toFixed(2) + '(    $ ' + parseFloat(iva_full).toFixed(2) + ')'
                // parseFloat(data).toFixed(2)
            );
            $(api.column(6).footer()).html(
                '$' + parseFloat(con_iva).toFixed(2) + '(    $ ' + parseFloat(con_iva_full).toFixed(2) + ')'
                // parseFloat(data).toFixed(2)
            );
        },

    });
});

function daterange() {
    var hoy = new  Date;
    // $("div.toolbar").html('<br><div class="col-lg-3"><input type="text" name="fecha" class="form-control form-control-sm input-sm"></div> <br>');
    $('input[name="fecha"]').daterangepicker({
        locale: {
            format: 'YYYY-MM-DD',
            applyLabel: '<i class="fa fa-search"></i> Buscar',
            cancelLabel: '<i class="fa fa-ban"></i> Cancelar',
        },
        showDropdowns: true,
        maxYear: hoy.getFullYear(),
        minYear: (hoy.getFullYear())-5,
    }).on('apply.daterangepicker', function (ev, picker) {
        picker['key'] = 1;
        datos.add(picker);
        // filter_by_date();

    }).on('cancel.daterangepicker', function (ev, picker) {
        picker['key'] = 0;
        datos.add(picker);
    });

}
