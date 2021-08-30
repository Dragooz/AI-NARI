$(document).ready(function() {

    $('#info_table').DataTable({
        "order": [],
        "columnDefs": [{
            "targets"  : 'no-sort',
            "orderable": false,
          }]
        });
      // include form to retrieve i guess
    $('.action_taken').click(function(){
      next = $('input[name="next"]').val()
      pard_id = $('input[name="pard_id"]').val()
      action_name = $('input[name="action_name"]').val()

      $.ajax({
        url: $('input[name="url"]').val(), //which url to send data to
        data: {
          'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
          'next': next,
          'pard_id': pard_id,
          'action_name': action_name,
        },
        type: 'post',
        success: function(response){
          if (response.success) {
            success_answer = 'ajax call success. ' + action_name + ' is performed.'
            alert(success_answer);
            window.location=window.location; //reload using this to avoid warning
            // here you update the HTML to change the active to innactive
          }else{
            fail_answer = 'ajax call not success. ' + action_name + ' is not performed.'
            alert("ajax call not success.");
          }
        }
      })
    })

});