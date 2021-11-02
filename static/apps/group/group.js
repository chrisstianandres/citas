var permisos = {
    items: {
        nombre: '',
        detalle: []
    },
    add: function (data) {
        var array = {
                'modelo': data.modelo,
                'tipo': data.tipo
            };
        this.items.detalle.push(array);
    },
    remove: function (data) {
         $.each(this.items.detalle, function (key, value) {
             if (value.tipo===data.tipo && value.modelo===data.modelo){
                 permisos.items.detalle.splice(key);
             }
         });
    }

};
$(document).ready(function () {
    var action = $('#action').val();
    $('#id_permissions').select2({
        theme: 'classic',
        languaje: 'es',
        placeholder: 'Buscar permiso para agregar...',
        inimumResultsForSearch: 20
    });
    validador();
$("#form").validate({
    rules: {
        name: {
            required: true,
            maxlength: 25,
            minlength: 3,
            lettersonly: true
        }
    },
    messages: {
        name: {
            required: "Este campo es requerido",
            maxlength: "Maximo 25 caracteres",
            minlength: "Minimi 3 caracteres",
        }
    },
});

$('.check_add').click(function () {
    let modelo = $(this).attr('idp');
    let info = {'tipo': 'add', 'modelo': modelo};
    if ($(this).prop('checked')){
        permisos.add(info);
    } else {
        permisos.remove(info);
    }

});
$('.check_view').click(function () {
    let modelo = $(this).attr('idp');
    let info = {'tipo': 'view', 'modelo': modelo};
    if ($(this).prop('checked')){
        permisos.add(info);
    } else {
        permisos.remove(info);
    }

});
$('.check_edit').click(function () {
    let modelo = $(this).attr('idp');
    let info = {'tipo': 'change', 'modelo': modelo};
    if ($(this).prop('checked')){
        permisos.add(info);
    } else {
        permisos.remove(info);
    }

});
$('.check_delete').click(function () {
    let modelo = $(this).attr('idp');
    let info = {'tipo': 'delete', 'modelo': modelo};
    if ($(this).prop('checked')){
        permisos.add(info);
    } else {
        permisos.remove(info);
    }

});

$("#form").on('submit', function (e) {
    e.preventDefault();
    console.log(permisos.items);
    var isvalid = $(this).valid();
    if (isvalid) {
        permisos.items.nombre = $('#id_name').val();
        let data = {'action': action, 'permisos': JSON.stringify(permisos.items)};
        save_with_ajax('Alerta!', window.location.pathname, 'Esta seguro que desea guardar este grupo?',
            data, function (e) {
            window.location.href = '/persona/groups'
        })
    }

})

});
