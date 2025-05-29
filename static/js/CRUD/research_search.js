$(function () {
    let createAssignPatientForm = function () {

        // Hide all popovers...
        let assignPatientLinks = $('.assign-patient');
        assignPatientLinks.not(this).popover('hide');

        // Create elements
        let element = $(this);
        let container = $('<div class="col-12 pr-0"></div>');

        let containerID = $('<div class="form-group row col-12 pr-0 mr-0"></div>');
        let patientID = $('<label class="col-3 col-form-label mb-0">ID: </label>');
        let _patientIDInput = $('<div class="col-9">' +
            '<input type="text" class="form-control col-sm-12" name="patient_id"\n' +
            '                         placeholder="(환자 ID)"\n' +
            '>' +
            '</div>');

        let containerName = $('<div class="form-group row col-12 pr-0 mb-0"></div>');
        let patientName = $('<label class="col-3 col-form-label mb-0">Name: </label>');
        let _patientNameInput = $('<div class="col-9">' +
            '<input type="text" class="form-control col-sm-12" name="patient_name"\n' +
            '                         placeholder="(환자 이름)"\n' +
            '>' +
            '</div>');

        let submitContainer = $('<div class="form-group pr-3 mb-0" style="text-align: right;">' +
            '                <button type="button" class="cancel btn btn-secondary">Cancel</button>' +
            '                <button type="button" class="submit btn btn-success">Add</button>\n' +
            '              </div>');

        containerID.append(patientID).append(_patientIDInput);
        containerName.append(patientName).append(_patientNameInput);
        submitContainer.find('button.cancel').click(function() {
            element.popover('hide');
        }
        );

        let researchID = element.attr('research-id');
        let researchIDInput = $('#add-patient-research-id');
        let patientIDInput = $('#add-patient-patient-id');
        let patientNameInput = $('#add-patient-patient-name');
        let formContainer = $('#research-assign-patient');
        submitContainer.find('button.submit').click(function() {
            researchIDInput.val(researchID);
            patientIDInput.val(_patientIDInput.find('input').val())
            patientNameInput.val(_patientNameInput.find('input').val())
            formContainer.attr('action', '/research/' + researchID + '/')
            formContainer.submit();
        });

        container.append(containerID)
            .append(containerName)
            .append(submitContainer);
        return container;
    };

    let assignPatientLinks = $('.assign-patient');

    assignPatientLinks.popover({
        placement: 'right',
        container: $('#research-assign-patient'),
        delay: 0,
        html : true,
        content: createAssignPatientForm
    })
});

$(function () {
    let naOrElse = $('.na-or-else');

    for (let i = 0; i < naOrElse.length; i++) {
        let _naOrElse = $(naOrElse[i]);
        let inputs = _naOrElse.find('input');
        let firstInput = $(inputs[0]);
        let restInputs = $(inputs.not(firstInput));

        firstInput.click(function () {
            if ($(this).is(':checked')) {
                restInputs.prop('checked', false);
            }
        });
        restInputs.click(function () {
            if ($(this).is(':checked')) {
                firstInput.prop('checked', false);
            }
        });
    }

    // initialize
    for (let i = 0; i < naOrElse.length; i++) {
        let _naOrElse = $(naOrElse[i]);
        let inputs = _naOrElse.find('input')
        let firstInput = $(inputs[0]);
        let restInputs = $(inputs.not(firstInput));

        if (firstInput.is(':checked')) {
            restInputs.prop('checked', false);
        }
    }
});