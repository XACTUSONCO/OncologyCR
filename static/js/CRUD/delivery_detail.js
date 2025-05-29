$(function () {
    $('.delivery').click(function (e) {
        let elem = $(this)
        let deliveryID = elem.attr('delivery-id');
        let modal = $('#edit_delivery_' + deliveryID);
        modal.modal();
    });

    $('button.delivery-remove-button').click(function (e) {
        let elem = $(this);
        let deliveryID = elem.attr('delivery-id');
        let deleteDelivery = confirm("삭제하시겠습니까?");
        if (deleteDelivery) {
            window.location.href = '/miscellaneous/94/' + deliveryID + '/delete_delivery/';
        }
    });

    $('button.delivery-edit-button').click(function (e) {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const optionRadios = urlParams.get('optionRadios');

        let elem = $(this);
        let deliveryID = elem.attr('delivery-id');
        let deliveryeditForm = $('#delivery-edit-form-' + deliveryID);
        const fields = ['visit_date', 'assignment', 'crc', 'scheduled_time', 'comment'];
        $.post('/miscellaneous/94/' + deliveryID + '/edit_delivery/',

            deliveryeditForm.serialize(),
            function (data, status, xhr) {
                let code = data.code
                if (code === 'error') {
                    for (let i in fields) {
                        let key = fields[i];
                        let labelElement = deliveryeditForm.find('label[for=' + key + ']');
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
                        window.location.href = '/research/94/';
                    }
            })
    });

    $('button.addcheck').on('click',function () {
        $checkbox = $('.Checked');

        var chkArray = [];
        var updateTechnician = confirm("업데이트하시겠습니까?");
        chkArray = $.map($checkbox, function(el){
            if(el.checked) { return el.id };
        });

        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();

        $.ajax({
                type:'post',
                url: '/miscellaneous/94/update_check/',
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

    $('button.deletecheck').on('click',function () {
        $checkbox = $('.Checked');

        var chkArray = [];
        var updateTechnician = confirm("삭제하시겠습니까?");
        chkArray = $.map($checkbox, function(el){
            if(el.checked) { return el.id };
        });

        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();

        $.ajax({
                type:'post',
                url: '/miscellaneous/94/delete_check/',
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

    $('button.updatechecked').on('click',function () {
        $checkbox = $('.Checked');

        var chkArray = [];
        var updatechecked = confirm("업데이트하시겠습니까?");
        chkArray = $.map($checkbox, function(el){
            if(el.checked) { return el.id };
        });

        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();

        $.ajax({
                type:'post',
                url: '/miscellaneous/94/update_checked/',
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

    $('button.deletechecked').on('click',function () {
        $checkbox = $('.Checked');

        var chkArray = [];
        var deletechecked = confirm("삭제하시겠습니까?");
        chkArray = $.map($checkbox, function(el){
            if(el.checked) { return el.id };
        });

        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();

        $.ajax({
                type:'post',
                url: '/miscellaneous/94/delete_checked/',
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
});