$(function () {

    let naOrElseInput = $('.na-or-else-input');

    for (let i = 0; i < naOrElseInput.length; i++) {
        let _naOrElseInput = $(naOrElseInput[i]);
        let inputs = _naOrElseInput.find('input');
        let firstInput = $(inputs[0]);
        let restInputs = $(inputs.not(firstInput));

        firstInput.click(function () {
            if ($(this).is(':checked')) {
                restInputs.prop('disabled', false);
            } else {
                restInputs.prop('value', '');
                restInputs.prop('disabled', true);
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
            restInputs.prop('disabled', false);
        }
    }
});