$(function () {
    $('#add-SAE-button').click(function (e) {
        e.preventDefault();
        let researchID = $(this).attr('research-id');
        let SAEAddForm = $('#SAE-add-form');
        const fields = ['assignment', 'start_date', 'term'];
        $.post('/research/SAE/add/',
            SAEAddForm.serialize(),
            function (data, status, xhr) {
            let code = data.code
                if (code === 'error') {
                    for (let i in fields) {
                        let key = fields[i];
                        let labelElement = SAEAddForm.find('label[for=' + key + ']');
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
                    window.location.href = '/research/SAE/' + researchID + '/';
                }
            })

    });



    $('button.SAE-remove-button').click(function (e) {
        let elem = $(this);
        let saeID = elem.attr('SAE-id');
        let deleteSAE = confirm("정말 삭제하시겠습니까?");
        if (deleteSAE) {
            window.location.href = '/research/SAE/' + saeID + '/delete/';
        }
    });

    $('button.SAE-edit-button').click(function (e) {
        let elem = $(this);
        let saeID = elem.attr('SAE-id');
        let researchID = elem.attr('research-id');
        let SAEeditForm = $('#SAE-edit-form-' + saeID);
        const fields = ['assignment', 'start_date', 'term'];
        $.post('/research/SAE/' + saeID + '/edit/',
            SAEeditForm.serialize(),
            function (data, status, xhr) {
                let code = data.code
                if (code === 'error') {
                    for (let i in fields) {
                        let key = fields[i];
                        let labelElement = SAEeditForm.find('label[for=' + key + ']');
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
                } else {
                    window.location.href = '/research/SAE/' + researchID + '/';
                }
            })
    });
});


