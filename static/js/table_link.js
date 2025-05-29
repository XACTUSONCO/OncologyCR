$(function () {
        let trs = $('table tr.table-link');

        for (let i = 0; i < trs.length; i++) {
            const tr = trs[i];
            const link = tr.getAttribute('data-link');

            const tds = $(tr).find('td');
            for (let j = 0; j < tds.length; j++) {
                const td = tds[j];
                if (!td.hasAttribute('data-link-disabled')) {
                    $(td).click(function (e) {
                        e.preventDefault();
                        window.location = link;
                    });
                }
            }
        }
    }
);