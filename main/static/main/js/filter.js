// Style all checkboxes in the filter group like buttons.
$('.filter-group').buttonset()

// Get all order level filter elements on page load and save them into a list.
var order_filters = $('#filter-inputs .filter-group')
                        .not('.static-group .filter-group')
                        .map(function() {
                            return this //$(this).attr('data-name')
                        })

// Get all static group elements on page load and save them into a list
var static_groups = $('#filter-inputs .static-group')
                        .map(function() {
                            return this // $(this).attr('data-name')
                        })

var foo = get_checked_values()


/**
 * Returns an object containing lists of all the data value attributes of the
 * checkboxes that have been checked, keyed by their category names.
 */
function get_checked_values () {

    result = {}

    // Eventual structure of "result":
    //
    // result = {
    //     "normal_class": [],
    //     "shattered_class": [],
    //     "effect": [],
    //     "statics": {
    //         "static-1": {
    //             "class": [],
    //             "life": [],
    //             "mass": [],
    //             "jump": [],
    //         },
    //         "static-2": {
    //             "class": [],
    //             "life": [],
    //             "mass": [],
    //             "jump": [],
    //         },
    //     },
    // }

    // iterate over all order-level filter groups
    order_filters.each(function() {

        // get the filter group name and initialize a blank list for it
        var category = $(this).attr('data-name')
        result[category] = []

        // iterate over all inputs in filter group
        $(this).find('input').each(function () {

            // if the input is checked, push value to result keyed on group
            if ($(this).is(':checked')) {
                var value = $(this).attr('data-value')
                result[category].push(value)
            }
        })
    })

    // in result, initialize blank statics dictionary
    result['statics'] = {}

    // iterate over all static-level groups
    static_groups.each(function() {

        // get the static group name and initialize blank dictionary for it
        var static_name = $(this).attr('data-name')
        result['statics'][static_name] = {}

        // iterate over all static-group-level inputs
        $(this).find('.filter-group').each(function() {

            // get the the filter group name and initialize a blank list for it
            var category = $(this).attr('data-name')
            result['statics'][static_name][category] = []

            // iterate over all inputs in the filter group
            $(this).find('input').each(function() {

                // if the input is checked, push value to result keyed on group
                if ($(this).is(':checked')) {
                    var value = $(this).attr('data-value')
                    result['statics'][static_name][category].push(value)
                }
            })
        })
    })

    // return the filled object
    return result
}


/**
 * When a filter checkbox is changed, sends an updated request to the server.
 */
$('#filter-inputs input').on('change', function() {
    var checked_value_list = get_checked_values()
    $.ajax({
        url: '/sell/filter/',
        method: 'GET',
        data: {
            filters: JSON.stringify(checked_value_list),
        },
        success: function(data) {
            console.log(data)
        },
        error: function() {
            console.log('failure.')
        },
    })
})
