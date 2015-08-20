

$('.dropdown-menu').on('click', function (e) {
e.stopPropagation() 
})



$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});

$('#show-filter-inputs').click(function(e){
    e.preventDefault();

    $('#filter-cover').fadeOut(function(){
        $('#filter-inputs').fadeIn()
    });
    
})

$('#hide-filter-inputs').click(function(e){
    e.preventDefault();

    $('#filter-inputs').fadeOut(function(){
        $('#filter-cover').fadeIn()
    });
    
})

$('.glyphicon-pencil').click(function(e){
    e.preventDefault();

    var id = $(this).parents('.table-cell').attr('id')

    $('#'+id).children('.glyphicon-pencil').fadeOut()
    $('#'+id).children('.price-display').fadeOut(function(){
        $('#'+id).children('.price-textbox').fadeIn()
    });
    
})

$('.glyphicon-floppy-disk').click(function(e){
    e.preventDefault();

    var id = $(this).parents('.table-cell').attr('id')
    console.log(id)
    var new_price = $('#'+id).children('.price-textbox').children('input').val()
    // var new_price = $('#'+id).children('')
    $('#'+id).children('.price-display').attr('data-original-title', new_price)
    $('#'+id).children('.price-display').text(new_price)

    $('#'+id).children('.price-textbox').fadeOut(function(){
        $('#'+id).children('.price-display').fadeIn()
        $('#'+id).children('.glyphicon-pencil').fadeIn()
    });
    
})
