$(function () {
    $('#pre-initiation-remove-button').click(function (e) {
        let elem = $(this);
        let preinitiationID = elem.attr('pre-initiation-id');
        let deletePreinitiation = confirm("삭제하시겠습니까?");
        if (deletePreinitiation) {
            window.location.href = '/research/pre_initiation/' + preinitiationID + '/delete/';
        }
    });

    $('#add-SIT-setup-button').click(function (e) {
        e.preventDefault();
        let preinitiationID = $(this).attr('pre-initiation-id');
        let setupAddForm = $('.setup-add-form');
        const fields = ['feasibility', 'PSV', 'budgeting_from', 'budgeting_to', 'IRB_new_review', 'IRB_qualified_permission', 'IRB_finalization', 'contract'];
        $.post('/research/pre_initiation/SIT/' + preinitiationID + '/add_setup/',
            setupAddForm.serialize(),
            function (data, status, xhr) {
                let code = data.code
                if (code === 'error') {
                    for (let i in fields) {
                        let key = fields[i];
                        let labelElement = setupAddForm.find('label[for=' + key + ']');
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
                    window.location.href = '/research/pre_initiation/' + preinitiationID + '/';
                }
            })
    });

    $('button.SIT-setup-edit-button').click(function (e) {
        let elem = $(this);
        let setupID = elem.attr('SIT-setup-id');
        let preinitiationID = elem.attr('pre-initiation-id');
        let setupeditForm = $('#SIT-setup-edit-form-' + setupID);
        const fields = ['feasibility', 'PSV', 'budgeting_from', 'budgeting_to', 'IRB_new_review', 'IRB_qualified_permission', 'IRB_finalization', 'contract'];
        $.post('/research/pre_initiation/SIT/' + setupID + '/edit/',

            setupeditForm.serialize(),
            function (data, status, xhr) {
                let code = data.code
                if (code === 'error') {
                    for (let i in fields) {
                        let key = fields[i];
                        let labelElement = setupeditForm.find('label[for=' + key + ']');
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
                    window.location.href = '/research/pre_initiation/' + preinitiationID + '/';
                }
            })
    });

    $('button.SIT-setup-remove-button').click(function (e) {
        let elem = $(this);
        let setupID = elem.attr('SIT-setup-id');
        let deletesetup = confirm("삭제하시겠습니까?");
        if (deletesetup) {
            window.location.href = '/research/pre_initiation/SIT/' +  setupID + '/delete/';
        }
    });

    $('td.IIT_setup').click(function (e) {
        let elem = $(this);
        let setupID = elem.attr('setup-id');
        let modal = $('#edit_IIT_setup_' + setupID);
        modal.modal();
    });

    $('tr.IIT_setup').click(function (e) {
        let elem = $(this);
        let setupID = elem.attr('setup-id');
        let modal = $('#edit_IIT_setup_' + setupID);
        modal.modal();
    });

    $('#add-IIT-setup-button').click(function (e) {
        e.preventDefault();
        let preinitiationID = $(this).attr('pre-initiation-id');
        let setupAddForm = $('.setup-add-form');
        const fields = ['preperation', 'mfds', 'irb', 'crms', 'multicenter', 'etc', 'from_date', 'to_date', 'memo'];
        $.post('/research/pre_initiation/IIT/' + preinitiationID + '/add_setup/',
            setupAddForm.serialize(),
            function (data, status, xhr) {
                let code = data.code
                if (code === 'error') {
                    for (let i in fields) {
                        let key = fields[i];
                        let labelElement = setupAddForm.find('label[for=' + key + ']');
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
                    window.location.href = '/research/pre_initiation/' + preinitiationID + '/';
                }
            })
    });

    $('button.IIT-setup-edit-button').click(function (e) {
        let elem = $(this);
        let setupID = elem.attr('IIT-setup-id');
        let preinitiationID = elem.attr('pre-initiation-id');
        let setupeditForm = $('#IIT-setup-edit-form-' + setupID);
        const fields = ['preperation', 'mfds', 'irb', 'crms', 'multicenter', 'etc', 'from_date', 'to_date', 'memo'];
        $.post('/research/pre_initiation/IIT/' + setupID + '/edit/',
            setupeditForm.serialize(),
            function (data, status, xhr) {
                let code = data.code
                if (code === 'error') {
                    for (let i in fields) {
                        let key = fields[i];
                        let labelElement = setupeditForm.find('label[for=' + key + ']');
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
                    window.location.href = '/research/pre_initiation/' + preinitiationID + '/';
                }
            })
    });

    $('button.IIT-setup-remove-button').click(function (e) {
        let elem = $(this);
        let setupID = elem.attr('IIT-setup-id');
        let deletesetup = confirm("삭제하시겠습니까?");
        if (deletesetup) {
            window.location.href = '/research/pre_initiation/IIT/' +  setupID + '/delete/';
        }
    });
















    $('tr.pre-initiation').click(function (e) {
        let elem = $(this);
        let preinitiationID = elem.attr('pre-initiation-id');
        let modal = $('#edit_pre_initiation_' + preinitiationID);
        modal.modal();
    });

    $('tr.performance-IIT').click(function (e) {
        let elem = $(this);
        let performanceIITID = elem.attr('performance-IIT-id');
        let modal = $('#edit_performance_IIT_' + performanceIITID);
        modal.modal();
    });

    $('button.performance-IIT-remove-button').click(function (e) {
        let elem = $(this);
        let performanceIITID = elem.attr('performance-IIT-id');
        let deleteperformanceIIT = confirm("정말 삭제하시겠습니까?");
        if (deleteperformanceIIT) {
            window.location.href = '/research/performance_IIT/' + performanceIITID + '/delete/';
        }
    });

    $('#pre-initiation-IIT-remove-button').click(function (e) {
        let elem = $(this);
        let preinitiationID = elem.attr('pre-initiation-IIT-id');
        let deletePreinitiation = confirm("삭제하시겠습니까?");
        if (deletePreinitiation) {
            window.location.href = '/research/pre_initiation_IIT/' + preinitiationID + '/delete/';
        }
    });

    $('.pre_initiation_IIT').click(function (e) {
        let elem = $(this);
        let preinitiationID = elem.attr('pre-initiation-IIT-id');
        window.location.href = '/research/pre_initiation_IIT/' + preinitiationID + '/';
    });

    $('button.pre-initiation-edit-button').click(function (e) {
        let elem = $(this);
        let preinitiationID = elem.attr('pre-initiation-id');
        let preinitiationeditForm = $('#pre-initiation-edit-form-' + preinitiationID);
        const fields = ['team', 'pre_research_name', 'PI', 'crc', 'initiation_date', 'CTC_contract', 'CTC_non_contract_reason', 'memo'];
        $.post('/research/pre_initiation/' + preinitiationID + '/edit/',

            preinitiationeditForm.serialize(),
            function (data, status, xhr) {
                let code = data.code
                if (code === 'error') {
                    for (let i in fields) {
                        let key = fields[i];
                        let labelElement = preinitiationeditForm.find('label[for=' + key + ']');
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
                    window.location.href = '/research/pre_initiation/';
                }
            })
    });

    $('#add-performance-IIT-button').click(function (e) {
        e.preventDefault();
        let preinitiationIITID = $(this).attr('pre-initiation-IIT-id');
        let performanceIITAddForm = $('#performance-IIT-add-form');
        const fields = ['iit_setup', 'from_date', 'to_date'];
        $.post('/research/performance_IIT/' + preinitiationIITID + '/add/',
            performanceIITAddForm.serialize(),
            function (data, status, xhr) {
                let code = data.code
                if (code === 'error') {
                    for (let i in fields) {
                        let key = fields[i];
                        let labelElement = performanceIITAddForm.find('label[for=' + key + ']');
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
                    window.location.href = '/research/pre_initiation_IIT/' + preinitiationIITID + '/';
                }
            })
    });
    $('button.performance-IIT-edit-button').click(function (e) {
        let elem = $(this);
        let performanceIITID = elem.attr('performance-IIT-id');
        let performanceIITeditForm = $('#performance-IIT-edit-form-' + performanceIITID);
        let preinitiationIITID = elem.attr('pre-initiation-IIT-id');
        const fields = ['iit_setup', 'from_date', 'to_date'];
        $.post('/research/performance_IIT/' + performanceIITID + '/edit/',

            performanceIITeditForm.serialize(),
            function (data, status, xhr) {
                let code = data.code
                if (code === 'error') {
                    for (let i in fields) {
                        let key = fields[i];
                        let labelElement = performanceIITeditForm.find('label[for=' + key + ']');
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
                    window.location.href = '/research/pre_initiation_IIT/' + preinitiationIITID + '/';
                }
            })
    });
});