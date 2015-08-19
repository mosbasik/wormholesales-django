/**
 * Style all checkboxes in the filter group like buttons.
 */
$('.filter-group').buttonset()


/**
 * Get all of the filter categories on page load and save them into a list.
 */
var filter_category_names = $('#filter-inputs .filter-group').map(function() {
    return $(this).attr('data-name')
}).get()

console.log(filter_category_names)


/**
 * Returns an object containing lists of all the data value attributes of the
 * checkboxes that have been checked, keyed by their category names.
 */
function get_checked_values () {

    // create result object with empty category entries
    var result = {}
    for (var i=0; i<filter_category_names.length; i++) {
        result[filter_category_names[i]] = []
    }

    // populate result object lists with checked boxes
    var inputs = $('#filter-inputs input')
    for (var i=0; i<inputs.length; i++) {
        if ($(inputs[i]).is(':checked')) {
            var category = $(inputs[i]).parent().attr('data-name')
            var value = $(inputs[i]).attr('data-value')
            result[category].push(value)
        }
    }

    // return the filled object
    return result
}


/**
 * When a filter checkbox is changed, sends an updated request to the server.
 */
$('#filter-inputs input').on('change', function() {
    var checked_value_list = get_checked_values()
    console.log(checked_value_list)
    console.log(JSON.stringify(checked_value_list))
    $.ajax({
        url: '/sell/filter/',
        method: 'GET',
        contentType: 'application/json',
        // dataType: 'json',
        data: checked_value_list,
        // data: JSON.stringify(checked_value_list),
        success: function() {
            console.log('success!')
        },
        error: function() {
            console.log('failure.')
        },
    })
})