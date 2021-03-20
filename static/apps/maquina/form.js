var datatable_search;
$(document).ready(function () {
    $('#id_tipo').select2({
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
            url: window.location.pathname,
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
        placeholder: 'Busca un Equipo',
        minimumInputLength: 1,
    });

    validador();
    $("#form").validate({
        rules: {
            tipo: {
                required: true,
            },
            serie: {
                required: true,
                minlength: 3,
                maxlength: 50
            },
        },
        messages: {
            tipo: {
                required: "Por favor escoje un tipo de maquina",
            },
            serie: {
                required: "Por favor ingresa una serie",
                minlength: "Debe ingresar al menos 3 caracteres",
                maxlength: "Debe ingresar hasta 50 caracteres"
            },
        },
    });

    $("#form_tipo").validate({
        rules: {
            nombre: {
                required: true,
                minlength: 3,
                maxlength: 50
            },
            descripcion: {
                required: true,
                minlength: 3,
                maxlength: 50
            },
        },
        messages: {
            nombre: {
                required: "Este valor es requerido",
                minlength: "Debe ingresar al menos 3 caracteres",
                maxlength: "Debe ingresar hasta 50 caracteres"
            },
            descripcion: {
                required: "Por favor ingresa una descripcion",
                minlength: "Debe ingresar al menos 3 caracteres",
                maxlength: "Debe ingresar hasta 50 caracteres"
            },
        },
    });

    $('#id_new_tipo').on('click', function () {
        $('#modal-table').modal('show');
        action = 'add';
        pk = '';
    });

    $('#modal-table').on('hidden.bs.modal', function () {
        reset('#form_tipo');
    });


    $('#form_tipo').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', 'add_tipo');
        parametros.append('id', '');
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                window.location.pathname, 'Esta seguro que desea guardar este tipo de equipo?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar tipo de equipo!', 'far fa-smile-wink', function () {
                        $('#modal-table').modal('hide');
                        var newOption = new Option(response.tipo['nombre'], response.tipo['id'], false, true);
                        $('#id_tipo').append(newOption).trigger('change');
                    });
                });
        }
    });

    $('#form').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', $('#action').val());
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                window.location.pathname, 'Esta seguro que desea guardar este Equipo?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar esta Equipo!', 'far fa-smile-wink', function () {
                        $('#modal-table').modal('hide');
                        window.location.href = '/equipos/lista'
                    });
                });
        }
    });


    $('#search_maquina').on('click', function () {
        $('#modal-table_search').modal('show');
        datatable_search = $("#table_search").DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {'action': 'list_search'},
                dataSrc: ""
            },
            columns: [
                {"data": "nombre"},
                {"data": "descripcion"},
                {"data": "id"}
            ],
            language:
                {
                    url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
                },
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a style="color: white" type="button" class="btn btn-xs btn-success" rel="check" ' +
                            'data-toggle="tooltip" title="Editar Datos"><i class="ace-icon fa fa-check"></i></a>';

                    }
                },
            ],
        });
    });


    $('#table_search tbody')
        .on('click', 'a[rel="check"]', function () {
            var tr = datatable_search.cell($(this).closest('td, li')).index();
            var data = datatable_search.row(tr.row).data();
            $('#modal-table_search').modal('hide');
            var newOption = new Option(data.nombre, data.id, false, true);
            $('#id_tipo').append(newOption).trigger('change');

        });


});

