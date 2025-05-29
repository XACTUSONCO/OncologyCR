(function ($) {
    'use strict';
    $(function () {
        $('.upload-name').on('click', function () {
            var file = $(this).parent().parent().parent().find('.upload-hidden');
            file.trigger('click');
        });

        $('.upload-hidden').on('change', function () {
            var output =$(this).parent().parent().find('.file-list')[0];

            var s = '<ul>';
            for (var i = 0; i < this.files.length; ++i) {
                s += '<li>' + this.files.item(i).name + '</li>';
            }
            s += '</ul>';
            output.innerHTML = s;
        });
    });
})(jQuery);
