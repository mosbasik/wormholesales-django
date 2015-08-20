

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
    console.log(id)

    $('#'+id).children('.price-display').fadeOut(function(){
        $('#'+id).children('.price-textbox').fadeIn()
    });
    
})

$('.glyphicon-floppy-disk').click(function(e){
    e.preventDefault();

    var id = $(this).parents('.table-cell').attr('id')
    console.log(id)
    var price = $('#'+id).children('.price-textbox').children('input').attr('value')
    // $('#'+id).children('.price-display').html()

    $('#'+id).children('.price-textbox').fadeOut(function(){
        $('#'+id).children('.price-display').fadeIn()
    });
    
})
