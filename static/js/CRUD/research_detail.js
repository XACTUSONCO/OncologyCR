$(function () {
    $('#research-remove-button').click(function (e) {
        let researchID = $(this).attr('research-id')
        let deleteResearch = confirm("정말 삭제하시겠습니까?");
        if (deleteResearch) {
            window.location.href = '/research/' + researchID + '/delete/';
        }
    });

    $('tr.research-waitinglist').click(function (e) {
        let elem = $(this);
        let waitingID = elem.attr('waiting-id');
        let modal = $('#edit_waiting_' + waitingID);
        modal.modal();
    });

    $('button.research-waiting-remove-button').click(function (e) {
        let elem = $(this);
        let waitingID = elem.attr('waiting-id');
        let deleteWaiting = confirm("삭제하시겠습니까?");
        if (deleteWaiting) {
            window.location.href = '/research/waitinglist/research/' + waitingID + '/delete/';
        }
    });

    $('button.research-waiting-edit-button').click(function (e) {
        let elem = $(this);
        let researchID = $(this).attr('research-id')
        let waitingID = elem.attr('waiting-id');
        let waitingeditForm = $('#waiting-edit-form-' + waitingID);
        const fields = ['register_number', 'name', 'doctor', 'age', 'sex', 'curr_status'];
        $.post('/research/waitinglist/research/' + waitingID + '/edit/',
            waitingeditForm.serialize(),
            function (data, status, xhr) {
                let code = data.code
                if (code === 'error') {
                    for (let i in fields) {
                        let key = fields[i];
                        let labelElement = waitingeditForm.find('label[for=' + key + ']');
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
                    window.location.href = '/research/' + researchID + '/';
                }
            })
    });


    $('td.image').click(function (e) {
        let elem = $(this);
        let endstudyID = elem.attr('end-study-id');
        let modal = $('#view_binder_image_' + endstudyID);
        modal.modal();
    });
    $('td.end-research-image').click(function (e) {
        let elem = $(this);
        let endresearchID = elem.attr('end-research-id');
        let modal = $('#view_binder_end_research_image_' + endresearchID);
        modal.modal();
    });

    $('#end-research-remove-button').click(function (e) {
        let endresearchID = $(this).attr('end-research-id')
        let deleteEndresearch = confirm("정말 삭제하시겠습니까?");
        if (deleteEndresearch) {
            window.location.href = '/research/end_study/' + endresearchID + '/delete/';
        }
    });
    $('td.detail-assignment').click(function (e) {
        let assignmentID = $(this).attr('assignment-id');
        window.location.href = '/assignment/' + assignmentID + '/';
    });
    $('button.update-assignment').click(function (e) {
        let waitingID = $(this).attr('waiting-id');
        let researchID = $(this).attr('research-id')
        window.location.href = '/research/' + researchID + '/update_assignment/' + waitingID + '/';
    });
});