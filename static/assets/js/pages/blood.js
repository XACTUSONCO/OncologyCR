// Call the dataTables jQuery plugin
$(document).ready(function() {
/*B - Buttons
f - Filtering input
r - Processing display element
l - lengthMenu
t - The table
i - Table information summary
p - Pagination control*/
	//연구 목록
	var table = $('#bloodTable01').DataTable({
		"order": [[ 1, 'desc' ]],
        dom: "frltp",
        buttons: [
            'excel', 'print'
        ],
		//lengthMenu: [10, 20, 50, 100, 200, 500]
		columnDefs: [ 
			{ orderable: false, targets: [12, 13] }
		],
		'rowsGroup': [0, 1, 2]
    } );
	$('#table-filter').on('change', function(){
       table.search(this.value).draw();   
    });
	$('#table-filter2').on('change', function(){
       table.search(this.value).draw();   
    });
	$('#table-filter3').on('change', function(){
       table.search(this.value).draw();   
    });
	$('#table-filter4').on('change', function(){
       table.search(this.value).draw();   
    });
	$('#table-filter5').on('change', function(){
       table.search(this.value).draw();   
    });
	
}());