var time_out
$('#id_system').on('input', function() {
    clearTimeout(time_out)
    time_out = setTimeout(autofill_wh_data, 500)
})


function autofill_wh_data() {
    var input_j_code = $('#id_system').val()
    var j_code_validator = new RegExp('^J[0-9]{6}$')

    if (j_code_validator.test(input_j_code)) {
        $.ajax({
            url: '/order-form/autofill/' + input_j_code + '/',
            method: 'GET',
            success: function(data) {
                $('#id_wormhole_class').val(data.wormhole_class.name)
                $('#id_wormhole_effect').val(data.wormhole_effect.name)
                $('#id_system').parent().removeClass('has-error').addClass('has-success')
            },
            error: function() {
                $('#id_wormhole_class').val('Error')
                $('#id_wormhole_effect').val('Error')
                $('#id_system').parent().removeClass('has-success').addClass('has-error')
            }
        })
    }
}


/**
 * Manages the number formatting of the price field
 */
$('#id_price').autoNumeric('init', {
    aSep: ',',
    aDec: '.',
    aSign: '',
})
