$(document).ready(function () {
    validador();
    $("#form").validate({
        rules: {
            nombre: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
            descripcion: {
                required: true,
                minlength: 5,
                maxlength: 50
            }
        },
        messages: {
            nombre: {
                required: "Por favor ingresa el nombre de la categoria",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios",
                maxlength: "La descripcion debe tener maximo 50 caracteres",
            },
            descripcion: {
                required: "Por favor ingresa una descripcion",
                minlength: "Ingresa al menos 5 letras",
                maxlength: "La descripcion debe tener maximo 50 caracteres",
            },
        },
    });
    $("#form_cat").validate({
        rules: {
            nombre: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
            descripcion: {
                required: true,
                minlength: 5,
                maxlength: 50
            }
        },
        messages: {
            nombre: {
                required: "Porfavor ingresa el nombre de la categoria",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios",
                maxlength: "La descripcion debe tener maximo 50 caracteres",
            },
            descripcion: {
                required: "Porfavor ingresa una descripcion",
                minlength: "Ingresa al menos 5 letras",
                maxlength: "La descripcion debe tener maximo 50 caracteres",
            },
        },
    });

    $('#id_nombre_categoria').keyup(function (e) {
            var changue = titleCase($(this).val());
            $(this).val(changue);
        }).keypress(function (e) {
        if (e.which >= 48 && e.which <= 57) {
            return false;
        }
    });  //Para solo letras;
    $('#id_descripcion_categoria').keyup(function (e) {
            var changue = titleCase($(this).val());
            $(this).val(changue);
        });


    //enviar formulario de nuevo cliente
    $('#form').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', $('#action').val());
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                window.location.pathname, 'Esta seguro que desea guardar esta categoria?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar esta categoria!', 'far fa-smile-wink', function () {
                         window.location.href = '/categoria/lista'
                    });
                });
        }
    });

});
