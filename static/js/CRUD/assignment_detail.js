$(function () {
    $('#assignment-remove-button').click(function (e) {
        let assignmentID = $(this).attr('assignment-id');
        let deleteAssignment = confirm("정말 삭제하시겠습니까?");
        if (deleteAssignment) {
            window.location.href = '/assignment/' + assignmentID + '/delete/';
        }
    });
    $('#add-feedback-button').click(function (e) {
        e.preventDefault();
        let assignmentID = $(this).attr('assignment-id');
        let researchID = $(this).attr('assignment-research-id');
        let feedbackAddForm = $('#feedback-add-form');
        let ICFdate = feedbackAddForm.find('input[name=ICF_date]').val();
        const fields = ['response', 'dosing_date', 'next_visit', 'photo_date', 'cycle', 'toxicity', 'tx_dose', 'FU', 'is_accompany', 'EOS'];
        $.post('/assignment/' + assignmentID + '/new_feedback/',
            feedbackAddForm.serialize(),
            function (data, status, xhr) {
                let code = data.code
                if (code === 'error') {
                    for (let i in fields) {
                        let key = fields[i];
                        let labelElement = feedbackAddForm.find('label[for=' + key + ']');
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
                } else if (code === 'success' && researchID == 210 && ICFdate) {
                    alert('HER2 ctDNA 연구 등록 부탁드립니다.');
                    window.location.href = '/assignment/' + assignmentID + '/';
                } else if (code === 'success' && researchID == 27 && ICFdate) {
                    alert('EFFECT 연구 등록 부탁드립니다.');
                    window.location.href = '/assignment/' + assignmentID + '/';
                } else if (code === 'success') {
                    window.location.href = '/assignment/' + assignmentID + '/';
                }
            })
    });
    $('#assignment-edit-button').click(function (e) {
        e.preventDefault();
        let assignmentID = $(this).attr('assignment-id')
        let assignmentEditForm = $('#assigment-edit-form');
        const fields = ['status', 'phase', 'no', 'register_number', 'name', 'sex', 'age', 'dx', 'previous_tx', 'ECOG', 'PI'];
        // $('#formResults').text($('#myForm').serialize());
        $.post('/assignment/' + assignmentID + '/edit/',
            assignmentEditForm.serialize(),
            function (data, status, xhr) {
                let code = data.code
                if (code === 'error') {
                    for (let i in fields) {
                        let key = fields[i];
                        let labelElement = assignmentEditForm.find('label[for=' + key + ']');
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
                    window.location.href = '/assignment/' + assignmentID + '/';
                }
            })
    });

    $('button.feedback').click(function (e) {
        let elem = $(this);
        let feedbackID = elem.attr('feedback-id');
        let modal = $('#edit_feedback_' + feedbackID);
        modal.modal();
    });

    $('button.feedback-remove-button').click(function (e) {
        let elem = $(this);
        let feedbackID = elem.attr('feedback-id');
        // let assignmentID = elem.attr('assignment-id');
        let deleteFeedback = confirm("정말 피드백을 삭제하시겠습니까?");
        if (deleteFeedback) {
            window.location.href = '/feedback/' + feedbackID + '/delete/';
        }
    });

    $('button.feedback-edit-button').click(function (e) {
        let elem = $(this);
        let feedbackID = elem.attr('feedback-id');
        let feedbackeditForm = $('#feedback-edit-form-' + feedbackID);
        let assignmentID = elem.attr('assignment-id');
        const fields = ['response', 'dosing_date', 'next_visit', 'photo_date', 'cycle', 'toxicity', 'tx_dose', 'FU', 'is_accompany', 'EOS'];
        $.post('/feedback/' + feedbackID + '/edit/',

            feedbackeditForm.serialize(),
            function (data, status, xhr) {
                let code = data.code
                if (code === 'error') {
                    for (let i in fields) {
                        let key = fields[i];
                        let labelElement = feedbackeditForm.find('label[for=' + key + ']');
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
                    window.location.href = '/assignment/' + assignmentID + '/';
                }
            })
    });

    $('.datepicker').datepicker({
        format: 'mm/dd/yyyy',
        weekStart: 1,
        autoclose: true,
        todayHighlight: true,
    });
});