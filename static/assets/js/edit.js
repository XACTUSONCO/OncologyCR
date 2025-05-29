//달력 (무조건 하단에 배치해야함)
$(function() {
	$('#end_brief, #result_brief, #storage_date, .datepickerStyle, #ICFdate, #scrfail, #nextvisit').datepicker({
		autoclose : true,	//사용자가 날짜를 클릭하면 자동 캘린더가 닫히는 옵션
		templates : {
			leftArrow: '&laquo;',
			rightArrow: '&raquo;'
		}, //다음달 이전달로 넘어가는 화살표 모양 커스텀 마이징 
		todayHighlight : true,
		toggleActive : true,	//이미 선택된 날짜 선택하면 기본값 : false 인 경우 그대로 유지 true 인 경우 날짜 삭제
	});
	$('#dosingdate, #photodate').datepicker({
		autoclose : true,	//사용자가 날짜를 클릭하면 자동 캘린더가 닫히는 옵션
		templates : {
			leftArrow: '&laquo;',
			rightArrow: '&raquo;'
		}, //다음달 이전달로 넘어가는 화살표 모양 커스텀 마이징
		todayHighlight : true,
		toggleActive : true,	//이미 선택된 날짜 선택하면 기본값 : false 인 경우 그대로 유지 true 인 경우 날짜 삭제
		endDate: 'today'
	});


	$(".timepickerStyle").datetimepicker({ 
		format: "Y-m-d H:i",
	});
});//ready end

$(document).ready(function() {
	// -------------------------------------------------------------
	// 파일 업로드
	// -------------------------------------------------------------
	var fileTarget = $('.filebox .upload-hidden');

	fileTarget.on('change', function(){
		if(window.FileReader){
			var filename = $(this)[0].files[0].name;
		} else {
			var filename = $(this).val().split('/').pop().split('\\').pop();
		}

		$(this).siblings('.upload-name').val(filename);
	});

})

function checkInputNo(obj){
	if($(obj).is(":checked")){
		$("#phase1").attr('disabled', true);
		$("#phase2").attr('disabled', true);
		$("#phase3").attr('disabled', true);

		$("#phase1").prop("checked", false);
		$("#phase2").prop("checked", false);
		$("#phase3").prop("checked", false);
	}else{
		$("#phase1").attr('disabled', false);
		$("#phase2").attr('disabled', false);
		$("#phase3").attr('disabled', false);
	}
}

/* 높이 추가
$(window).on('load',function(){
	var wHeight = $( window ).height();
	var ptHeight = $( "#page-topbar" ).height();
	var footerH = $( ".footer" ).height();
	var ptbH = $( ".page-title-box" ).height();
	var tableFixedThead = $("table.fixed-table thead").height();
	var tbodyH = wHeight - (ptHeight+footerH+ptbH+tableFixedThead);
	$("table.fixed-table tbody").height(tbodyH - 150);	
});
 */
