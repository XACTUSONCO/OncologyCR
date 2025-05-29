var csrftoken = $("[name=csrfmiddlewaretoken]").val();

$(function () {
    $('#waitinglist-remove-button').click(function (e) {
        let waitinglistID = $(this).attr('waitinglist-id');
        let deleteWaitingList = confirm("정말 삭제하시겠습니까?");
        if (deleteWaitingList) {
            window.location.href = '/research/waitinglist/' + waitinglistID + '/delete/';
        }
    });

    $('#waitinglist-edit-button').click(function (e) {
        e.preventDefault();
        let waitinglistID = $(this).attr('waitinglist-id');
        let waitinglistEditForm = $('#waitinglist-edit-form');
        const fields = ['register_number', 'name', 'doctor', 'sex', 'age', 'curr_status'];
        // $('#formResults').text($('#myForm').serialize());
        $.post('/research/waitinglist/' + waitinglistID + '/edit/',
            waitinglistEditForm.serialize(),
            function (data, status, xhr) {
                let code = data.code
                if (code === 'error') {
                    for (let i in fields) {
                        let key = fields[i];
                        let labelElement = waitinglistEditForm.find('label[for=' + key + ']');
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
                } else if (code === 'success') {
                    window.location.href = '/research/waitinglist/' + waitinglistID + '/';
                }
            })
    });
});