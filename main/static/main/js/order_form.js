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
                $('#id_system').parent().removeClass('has-error').addClass('has-success')
                $('#system-details').show()
                $('#id_wormhole_class').html(data.class)
                $('#id_wormhole_effect').html(data.effect.name)

                var static_html = ''
                for (var i = 0; i < data.statics.length; i++) {
                    if (i !== 0) {static_html += ', '}
                    static_html += data.statics[i].abbrev + ' (' + data.statics[i].name + ')'
                }

                $('#id_wormhole_statics').html(static_html)
            },
            error: function() {
                $('#id_system').parent().removeClass('has-success').addClass('has-error')
                $('#system-details').hide()
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
