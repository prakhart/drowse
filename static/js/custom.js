/* custom js file*/

$(function() {

$(".accordion-custom").accordion({
//whether the first section is expanded or not
firstChildExpand: true,
});
})

$(document).on('click', '.browse', function(){
  var file = $(this).parent().parent().parent().find('.file');
  file.trigger('click');
});
$(document).on('change', '.file', function(){
  $(this).parent().find('.form-control').val($(this).val().replace(/C:\\fakepath\\/i, ''));
});
$('.btn-custom').click(function(){
	$('#goModal2').modal('hide');
	$('#goModal3').modal('show')
});

