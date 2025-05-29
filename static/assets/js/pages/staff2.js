$(document).ready(function() {
    var table = $('#usage-detail-table').DataTable({
        'info': false,
        'bLengthChange': false,
        'ordering': false,
    } );

    $('#table-filter').on('change', function(){
       table.search(this.value).draw();
    });
}());