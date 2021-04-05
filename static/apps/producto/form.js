var indice;
$(document).ready(function () {
    validador();
    $("#form_producto").validate({
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
            categoria: {
                required: true
            },
            presentacion: {
                required: true
            }
        },
        messages: {
            nombre: {
                required: "Por favor ingresa un valor",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            descripcion: {
                required: "Por favor ingresa un valor",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            categoria: {
                required: "Por favor selecciona una categoria"
            },
            presentacion: {
                required: "Por favor selecciona una presentacion"
            },
        },
    });
    $('#id_nombre_producto').keyup(function () {
        var pal = $(this).val();
        var changue = pal.substr(0, 1).toUpperCase() + pal.substr(1);
        $(this).val(changue);
    }).keypress(function (e) {
        if (e.which >= 48 && e.which <= 57) {
            return false;
        }
    });  //Para solo letras;
    $('#id_descripcion_producto').keyup(function () {
        var pal = $(this).val();
        var changue = pal.substr(0, 1).toUpperCase() + pal.substr(1);
        $(this).val(changue);
    });  //Para solo letras;





    $('#id_categoria_producto')
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
                url: '/categoria/nuevo',
                data: function (params) {
                    return {
                        term: params.term,
                        'action': 'search'
                    };
                },
                processResults: function (data) {
                    return {
                        results: data,
                    };
                },
            },
            placeholder: 'Busca una Categoria',
            minimumInputLength: 1,
        });

    $('#id_presentacion')
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
                url: '/presentacion/nuevo',
                data: function (params) {
                    return {
                        term: params.term,
                        'action': 'search'
                    };
                },
                processResults: function (data) {
                    return {
                        results: data,
                    };
                },
            },
            placeholder: 'Busca una Presentacion',
            minimumInputLength: 1,
        });

    $('#id_new_cat').on('click', function () {
        $('#modal-categoria').modal('show');
    });
    $('#id_new_pres').on('click', function () {
        $('#modal-presentacion').modal('show');
    });


    $('#form_cat').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', 'add');
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                '/categoria/nuevo', 'Esta seguro que desea guardar esta categoria?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar esta categoria!', 'far fa-smile-wink', function () {
                        $('#modal-categoria').modal('hide');
                        var newOption = new Option(response.categoria['nombre'], response.categoria['id'], false, true);
                        $('#id_categoria_producto').append(newOption).trigger('change');
                    });

                });
        }
    });
    $('#form_pres').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', 'add');
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                '/presentacion/nuevo', 'Esta seguro que desea guardar esta presentacion?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar esta presentacion!', 'far fa-smile-wink', function () {
                        $('#modal-presentacion').modal('hide');
                        var newOption = new Option(response.presentacion['full'], response.presentacion['id'], false, true);
                        $('#id_presentacion').append(newOption).trigger('change');
                    });
                });
        }
    });

    //enviar formulario de nuevo producto
    $('#form_producto').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', $('#action').val());
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                window.location.pathname, 'Esta seguro que desea guardar este producto?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar este producto!', 'far fa-smile-wink', function () {
                        window.location.href = '/producto/lista'
                    });
                });
        }
    });
});


