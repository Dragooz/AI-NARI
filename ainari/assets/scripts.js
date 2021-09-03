$(document).ready(function() {

    $('#info_table').DataTable({
        "order": [],
        "columnDefs": [{
            "targets"  : 'no-sort',
            "orderable": false,
            "width": "10%", "targets": 2,
          }]
        });

    $('#info_table').addClass('table-border')

});