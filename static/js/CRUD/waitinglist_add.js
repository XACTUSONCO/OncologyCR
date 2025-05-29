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
                restInputs.prop('disabled', true);
            } else {
                restInputs.prop('disabled', false);
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
            restInputs.prop('disabled', true);
        }
    }


    let naOrElseInput = $('.na-or-else-input');

    for (let i = 0; i < naOrElseInput.length; i++) {
        let _naOrElseInput = $(naOrElseInput[i]);
        let inputs = _naOrElseInput.find('input');
        let firstInput = $(inputs[0]);
        let restInputs = $(inputs.not(firstInput));

        firstInput.click(function () {
            if ($(this).is(':checked')) {
                restInputs.prop('value', '');
                restInputs.prop('disabled', true);
            } else {
                restInputs.prop('disabled', false);
            }
        });
    }

    // initialize
    for (let i = 0; i < naOrElseInput.length; i++) {
        let _naOrElseInput = $(naOrElseInput[i]);
        let inputs = _naOrElseInput.find('input')
        let firstInput = $(inputs[0]);
        let restInputs = $(inputs.not(firstInput));

        if (firstInput.is(':checked')) {
            restInputs.prop('disabled', true);
        }
    }
});