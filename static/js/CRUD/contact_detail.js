$(function () {
    $('.detail-leave').click(function (e) {
        let leaveID = $(this).attr('leave-id');
        window.location.href = '/leave/detail/' + leaveID + '/';
    });

    $('button.contact-edit-button').click(function (e) {
        let elem = $(this);
        let contactID = elem.attr('contact-id');
        let contacteditForm = $('#contact-edit-form-' + contactID);
        const fields = ['name', 'eng_name', 'phone', 'work_phone', 'email', 'career', 'location', 'onco_A'];
        $.post('/user/contact/edit/' + contactID + '/',
            contacteditForm.serialize(),
            function (data, status, xhr) {
                let code = data.code
                if (code === 'error') {
                    for (let i in fields) {
                        let key = fields[i];
                        let labelElement = contacteditForm.find('label[for=' + key + ']');
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
                    window.location.href = '/user/list/';
                }
            })
    });
});