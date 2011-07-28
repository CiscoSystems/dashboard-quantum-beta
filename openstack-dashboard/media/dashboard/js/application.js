$(function(){
  $('input#table_search').quicksearch('tr.odd, tr.even');

  // show+hide image details
  $(".details").hide()
  $("td").click(function(e){
    $(this).parent().nextUntil(".even, .odd").fadeToggle("slow");
  })

  $("#user_tenant_list").hide()
  $("#drop_btn").click(function(){
    $("#user_tenant_list").toggle();
  })


  // confirmation on deletion of items
  $(".delete").click(function(e){
    var response = confirm('Are you sure you want to delete the '+$(this).attr('title')+" ?");
    return response;
  })

  $(".reboot").click(function(e){
    var response = confirm('Are you sure you want to reboot the '+$(this).attr('title')+" ?");
    return response;
  })

  $(".disable").click(function(e){
    var response = confirm('Are you sure you want to disable the '+$(this).attr('title')+" ?");
    return response;
  })

  $(".enable").click(function(e){
    var response = confirm('Are you sure you want to enable the '+$(this).attr('title')+" ?");
    return response;
  })
  
  // Convert the rename input into a dialog
  $(".form-rename div.network_rename_div").dialog({
      autoOpen : false,
      modal : true,
      draggable : true,
      resizable: false,
      position: 'center',
      title : 'Enter new network name'
  });

  $(".form-rename .rename").click(function() {
      var id = $(this).attr('id');
      id = id.replace(/^rename_/,'');
      // Show the dialog
      $("div#rename_div_"+id).dialog('open');
      // Return false here to prevent submitting the form
      return false;
  });
 
  $("div.network_rename_div .dialog_rename").click(function() {
      var id = $(this).attr('id');
      // Update name
      $('#new_name_'+id).val($('#change_to_'+id).val());
      // Close dialog
      $("div#rename_div_"+id).dialog('close');
      // Submit original form
      $("form#form_rename_"+id).submit();
  });
   
  // disable multiple submissions when launching a form
  $("form").submit(function() {
      $(this).submit(function() {
          return false;
      });
      return true;
  });
  
})
