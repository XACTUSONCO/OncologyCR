// Call the dataTables jQuery plugin
$(document).ready(function() {
/*B - Buttons
f - Filtering input
r - Processing display element
t - The table
i - Table information summary
p - Pagination control*/
	var table = $('#staffTable01').DataTable({
        dom: 'Bfrltp',
        buttons: [
            'excel'
        ],
		columnDefs: [ 
			{ orderable: false, targets: [8] }//, { visible: false, targets: [5,12,13] } 
		],
		"ordering": false,
		pageLength: 50,
		//select: true,
		'rowsGroup': [0],
		'columns': [
			{'data': 'team', 'name': 'team' },
			{'data': 'name', 'name': 'name'},
			{'data': 'eng_name', 'name': 'eng_name'},
			{'data': 'phone', 'name': 'phone'},
			{'data': 'work_phone', 'name': 'work_phone'},
			{'data': 'email', 'name': 'email'},
			{'data': 'career', 'name': 'career'},
			{'data': 'location', 'name': 'location'},
			{'data': '', 'name': ''}
		]
    } );
	$('#table-filter').on('change', function(){
       table.search(this.value).draw();   
    });
	$('#table-filter2').on('change', function(){
       table.search(this.value).draw();   
    });
    /*
	$('#staffTable01 tbody').on('click', 'button', function() {
		myrow = table.row( $(this).parents('tr') ).data();
		table.rows( {page: 'current'} ).deselect();
		table.row( $(this) ).select();

		$( 'select#team' ).val(myrow.team );
		$( 'input#name' ).val(myrow.name );
		$( 'input#eng_name' ).val(myrow.eng_name );
		$( 'input#phone' ).val(myrow.phone );
		$( 'input#work_phone' ).val(myrow.work_phone );
		$( 'input#email' ).val(myrow.email );
		$( 'input#career' ).val(myrow.career );
		$( 'select#location' ).val(myrow.location);
		$('#myModal').modal('show');
	  });
	  */


	  	
	// 휴가 유형
	var table2 = $('#holidayTable01').DataTable({
		//"order": [[ 0, 'desc' ]],
        dom: "Bfrltp",
        buttons: [
            'excel'
        ],
		ordering: false
    } );

	//교육자료
	/*
	var table3 = $('#eduTable01').DataTable({
		//"order": [[ 1, 'desc' ]],
        //dom: "frltp",
		//ordering: false
		dom: "frltp",
		ordering: false
    } );
    */
	
	//Certification
	var table4 = $('#certification-table').DataTable({
		"order": [[ 4, 'desc' ]],
        //dom: "frltp",
		//ordering: false
		dom: "frltp",
    } );
		
}());

