var datatable;

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
            {"data": "nombre"},
            {"data": "descripcion"},
            {"data": "categoria.nombre"},
            {"data": "precio"},
            {"data": "duracion"},
            {"data": "imagen"},
            {"data": "id"}
        ],
        language:
            {
                url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
            },
        columnDefs: [
            {
                targets: [-4],
                class: 'text-center',
                render: function (data, type, row) {
                    return '$ '+ data

                }

            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var tiempo = data/60;
                    var hora;
                    if(tiempo>1){hora= ' Horas'}
                    else {hora= ' Hora'}
                    return tiempo+ hora;
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data) {
                    return '<img src="' + data + '" width="50" height="50" class="img-circle elevation-2" alt="Image">';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var edit = '<a style="color: white" type="button" class="btn btn-primary btn-xs" rel="edit" ' +
                        'data-toggle="tooltip" title="Editar Datos"><i class="fa fa-edit"></i></a>' + ' ';
                    var del = '<a type="button" class="btn btn-danger btn-xs"  style="color: white" rel="del" ' +
                        'data-toggle="tooltip" title="Eliminar"><i class="fa fa-trash"></i></a>' + ' ';
                    return edit + del

                }
            },
        ]
    });
}

$(function () {
    datatable_fun();
    $('#datatable tbody')
        .on('click', 'a[rel="del"]', function () {
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            var parametros = {'id': data.id};
            parametros['action'] = 'delete';
            save_estado('Alerta',
               '/servicio/eliminar/'+data.id, 'Esta seguro que desea eliminar este servicio?', parametros,
                function () {
                    menssaje_ok('Exito!', 'Exito al eliminar este servicio!', 'far fa-smile-wink', function () {
                        datatable.ajax.reload(null, false)
                    })
                })
        })
        .on('click', 'a[rel="edit"]', function () {
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            window.location.href = '/servicio/editar/'+data.id
        });
});