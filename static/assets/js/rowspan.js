/* rowspan table */
/* function findBlocks(theTable) {
    if ($(theTable).data('hasblockrows') == null) {
        console.log('findBlocks'); // to prove we only run this once

        // we will loop through the rows but skip the ones not in a block
        var rows = $(theTable).find('tr');
        for (var i = 0; i < rows.length;) {
            var firstRow = rows[i];
            // find max rowspan in this row - this represents the size of the block
            var maxRowspan = 1;
            $(firstRow).find('td').each(function () {
                var attr = parseInt($(this).attr('rowspan') || '1', 10)
                if (attr > maxRowspan) maxRowspan = attr;
            });
            // set to the index in rows we want to go up to
            maxRowspan += i;
            // build up an array and store with each row in this block
            // this is still memory-efficient, as we are just storing a pointer to the same array
            // ... which is also nice becuase we can build the array up in the same loop
            var blockRows = [];
            for (; i < maxRowspan; i++) {
                $(rows[i]).data('blockrows', blockRows);
                blockRows.push(rows[i]);
            }
            // i is now the start of the next block
        }
        // set data against table so we know it has been inited (for if we call it in the hover event)
        $(theTable).data('hasblockrows', 1);
    }
}

$("td").hover(function () {
    $el = $(this);
    //findBlocks($el.closest('table')); // you can call it here or onload as below
    $.each($el.parent().data('blockrows'), function () {
        $(this).find('td').addClass('hover');
    });
}, function () {
    $el = $(this);
    $.each($el.parent().data('blockrows'), function () {
        $(this).find('td').removeClass('hover');
    });
});

findBlocks($('table'));
*/

/* function findRows(cell) {
    // find the first row
    var firstRow;
    // cheat and only check if first column has a rowspan
    if($el.parent().has('td:first[rowspan]').length > 0){
        // handle top row
        firstRow = $el.parent();
    } else {
        firstRow = $el.parent()
        .prevAll('tr:has(td:first[rowspan]):first');
    }
    
    // find max rowspan
    var maxRowspan = 1;
    firstRow.find('td').each(function(){
        var attr = parseInt($(this).attr('rowspan')||'1', 10)
        if(attr > maxRowspan)
            maxRowspan = attr;
    });
    
    return {firstRow: firstRow, maxRowspan: maxRowspan};
}

$("td").hover(function() {

    $el = $(this);
    var rowDetails = findRows($el);

    var row = rowDetails.firstRow;
    for(var i = 0; i < rowDetails.maxRowspan; ++i) {
        row.find('td').addClass('hover');
        row = row.next();
    }
}, function() { 
    $el = $(this);
    var rowDetails = findRows($el);

    var row = rowDetails.firstRow;
    for(var i = 0; i < rowDetails.maxRowspan; ++i) {
        row.find('td').removeClass('hover');
        row = row.next();
    }
});*/
