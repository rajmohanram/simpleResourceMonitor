$(function () {
    $('.table').DataTable({
      "paging": true,
      "lengthChange": true,
      "searching": true,
      "ordering": true,
      "info": true,
      "autoWidth": false,
      "responsive": true,
    });

    // get monitoring interval
    $.ajax({
      url: '/srm/get-interval?type=http',
      type: 'GET',
      dataType:'json',
      success: function(response){
          var interval = response['interval'];
          interval_string = interval + ' min';
          $('#interval').html(interval_string);
      }
    });

    // get data to fill the update endpoint form
    $('.update').click(function(){
        var url = $(this).attr('value');
        $.ajax({
          url: url,
          type: 'GET',
          dataType:'json',
          success: function(response){
              var endpoint = response['endpoint'];
              $('#upd-id').attr("value", endpoint[0]);
              $('#upd-endpoint').attr("value", endpoint[1]);
              $('#upd-url').attr("value", endpoint[2]);
          }
        });
    });

    // set the delete endpoint url
    $('.delete').click(function(){
        var url = $(this).attr('value');
        $("#delete-link").attr("href", url);
    });

    // get data to fill the update interval form
    $('#upd-interval').click(function(){
      var interval = $('#interval').html();
      $('#new-interval').attr("value", interval.slice(0,1));
    });
});