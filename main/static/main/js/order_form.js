var time_out
$('#id_j_code').on('input', function() {
    clearTimeout(time_out)
    time_out = setTimeout(autofill_wh_data, 500)
})


function autofill_wh_data() {
    var input_j_code = $('#id_j_code').val()
    var j_code_validator = new RegExp('^J[0-9]{6}$')

    if (j_code_validator.test(input_j_code)) {
        $.ajax({
            url: '/order-form/autofill/' + input_j_code + '/',
            method: 'GET',
            success: function(data) {
                $('#id_wormhole_class').val(data.wormhole_class.name)
                $('#id_wormhole_effect').val(data.wormhole_effect.name)
            },
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
