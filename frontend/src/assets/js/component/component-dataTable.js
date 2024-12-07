/*! component-dataTable.js | Adminuiux 2023-2024 */
"use strict";

document.addEventListener("DOMContentLoaded", function () {
    /* responsive last visible table cell */
    lastvisibletd();

});

document.addEventListener("window.resize", function () {
    alert()
    var table = $('#datatable').DataTable();
    table.columns.adjust().draw();
    lastvisibletd();
});


/* responsive last visible table cell after cell hides*/
function lastvisibletd() {
    $('.table tbody tr td').removeClass('lastvisible');
    $('.table tbody tr').each(function () {
        var thisis = $(this);
        thisis.find('td:visible:last').addClass('lastvisible');
    })
}
