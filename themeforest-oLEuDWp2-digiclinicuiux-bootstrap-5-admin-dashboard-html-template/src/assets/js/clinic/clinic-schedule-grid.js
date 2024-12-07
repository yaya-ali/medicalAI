/*! clinic-schedule-grid.js | Adminuiux 2023-2024 */

"use strict";

document.addEventListener("DOMContentLoaded", function () {

    /* Initialize dataTable */
    $('#clientScheduleGrid').DataTable({
        searching: false,
        lengthChange: false,
        autoWidth: false,
        columnDefs: [{ orderable: false, targets: 4 }],
        order: [[0, 'desc']],
        pageLength: 8,
        responsive: true,
    });

    /* responsive last visible table cell */
    lastvisibletd();

    /* swiper carousel */
    const swiper2 = new Swiper('.swiperautononav', {
        slidesPerView: "auto",
        spaceBetween: '16px',
        autoplay: true,
    });

});

document.addEventListener('resize', function () {
    /* resize */
    var table = $('#clientScheduleGrid').DataTable();
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
