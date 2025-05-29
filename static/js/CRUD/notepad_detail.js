$(function () {
    $('#notepad-remove-button').click(function (e) {
        let notepadID = $(this).attr('notepad-id');
        let deleteNotepad = confirm("정말 삭제하시겠습니까?");
        if (deleteNotepad) {
            window.location.href = '/dataroom/notepad/delete/' + notepadID + '/';
        }
    });
    $('#notepad-edit-button').click(function (e) {
        e.preventDefault();
        let researchID = $(this).attr('research-id');
        let notepadEditForm = $('#notepad-edit-form');
        const fields = ['notepad'];
        // $('#formResults').text($('#myForm').serialize());
        $.post('/dataroom/notepad/edit/' + researchID + '/',
            notepadEditForm.serialize(),
            function (data, status, xhr) {
                let code = data.code
                if (code === 'error') {
                    for (let i in fields) {
                        let key = fields[i];
                        let labelElement = notepadEditForm.find('label[for=' + key + ']');
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
                    window.location.href = '/dataroom/det/' + researchID + '/';
                }
            })
    });
});