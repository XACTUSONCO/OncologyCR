$(function () {
    $('.supporting').click(function (e) {
        let elem = $(this)
        let supportingID = elem.attr('supporting-id');
        window.location.href = '/miscellaneous/supporting/' + supportingID + '/edit/';
    });

    $('#supporting-remove-button').click(function (e) {
        let elem = $(this);
        let supportingID = elem.attr('supporting-id');
        let deleteSupporting = confirm("삭제하시겠습니까?");
        if (deleteSupporting) {
            window.location.href = '/miscellaneous/supporting/' + supportingID + '/delete/';
        }
    });

    $('button.supporting-edit-button').click(function (e) {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const optionRadios = urlParams.get('optionRadios');

        let elem = $(this);
        let supportingID = elem.attr('supporting-id');
        let supportingeditForm = $('#supporting-edit-form-' + supportingID);
        const fields = ['lab_date', 'assignment', 'kinds', 'post_hour', 'crc', 'supporting_type', 'comment'];
        $.post('/miscellaneous/supporting/' + supportingID + '/edit/',

            supportingeditForm.serialize(),
            function (data, status, xhr) {
                let code = data.code
                if (code === 'error') {
                    for (let i in fields) {
                        let key = fields[i];
                        let labelElement = supportingeditForm.find('label[for=' + key + ']');
                        let container = labelElement.parent();

                        if (key in data.error) {
                            container.addClass('card-inverse-danger');
                            const msg = data.error[key][0];
                            let text = $('<div class="text-danger small" style="line-height: 1rem;">' + msg + '</div>')
                            labelElement.find('.text-danger').remove();
                            labelElement.append(text);
                        } else {
                            container.removeClass('card-inverse-danger');
                            labelElement.find('.text-danger').remove();
                        }
                    }
                } else if (code === 'success' && optionRadios === 'period') {
                    window.location.href = window.location.href
                    } else {
                        window.location.href = '/miscellaneous/supporting';
                    }
            })
    });

    $('button.addtechnician').on('click',function () {
        $checkbox = $('.Checked');

        var chkArray = [];
        var updateTechnician = confirm("업데이트하시겠습니까?");
        chkArray = $.map($checkbox, function(el){
            if(el.checked) { return el.id };
        });

        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();

        $.ajax({
                type:'post',
                url: '/miscellaneous/supporting/update_technician/',
                headers: {"X-CSRFTOKEN": "{{ csrf_token }}"},
                data:{
                    "chkArray" : chkArray,
                    "csrfmiddlewaretoken": "{{ csrf_token }}",
                },
                success:function(data){
                    console.log(chkArray);
                    location.reload();
                },
                error : function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + xhr.responseText);
                }
       });
    });

    $('button.deletetechnician').on('click',function () {
        $checkbox = $('.Checked');

        var chkArray = [];
        var updateTechnician = confirm("삭제하시겠습니까?");
        chkArray = $.map($checkbox, function(el){
            if(el.checked) { return el.id };
        });

        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();

        $.ajax({
                type:'post',
                url: '/miscellaneous/supporting/delete_technician/',
                headers: {"X-CSRFTOKEN": "{{ csrf_token }}"},
                data:{
                    "chkArray" : chkArray,
                    "csrfmiddlewaretoken": "{{ csrf_token }}",
                },
                success:function(data){
                    console.log(chkArray);
                    location.reload();
                },
                error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText);
                }
       });
    });

    $('button.deleteobjects').on('click',function () {
        $checkbox = $('.Checked');

        var chkArray = [];
        var deleteObjects = confirm("삭제하시겠습니까?");
        chkArray = $.map($checkbox, function(el){
            if(el.checked) { return el.id };
        });

        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();

        $.ajax({
                type:'post',
                url: '/miscellaneous/supporting/delete_objects/',
                headers: {"X-CSRFTOKEN": "{{ csrf_token }}"},
                data:{
                    "chkArray" : chkArray,
                    "csrfmiddlewaretoken": "{{ csrf_token }}",
                },
                success:function(data){
                    console.log(chkArray);
                    location.reload();
                },
                error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText);
                }
       });
    });


    $('.QC').click(function (e) {
        let elem = $(this)
        let QCID = elem.attr('QC-id');
        window.location.href = '/miscellaneous/QC/' + QCID + '/edit/';
    });

    $('#QC-remove-button').click(function (e) {
        let elem = $(this);
        let QCID = elem.attr('QC-id');
        let deleteSQC = confirm("삭제하시겠습니까?");
        if (deleteSQC) {
            window.location.href = '/miscellaneous/QC/' + QCID + '/delete/';
        }
    });
});