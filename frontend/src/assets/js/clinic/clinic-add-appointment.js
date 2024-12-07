/*! clinic-add-appointment.js | Adminuiux 2023-2024 */

"use strict";

document.addEventListener("DOMContentLoaded", function () {
    /* swiper carousel */
    const swiper2 = new Swiper('.swiperautononav', {
        slidesPerView: "auto",
        spaceBetween: '16px',
        autoplay: false,
    });

    /* birth date select  */
    $('#dobdate').daterangepicker({
        "singleDatePicker": true,
        "minYear": 1924,
        "autoApply": true,
        "opens": "center",
        "buttonClasses": "btn",
        "drops": "down",
        "locale": {
            "format": 'DD/MM/YYYY'
        },
        "applyButtonClasses": "btn-theme",
        "cancelClass": "btn-light"
    }, function (start, end, label) {
        //console.log('New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')');
    });

    /* inline calendar */
    $('#inlinewrap1').daterangepicker({
        "singleDatePicker": true,
        "minYear": 2023,
        "autoApply": true,
        "linkedCalendars": false,
        "alwaysShowCalendars": true,
        "parentEl": ".inlinewrap1",
        "endDate": "25/03/2024",
        "opens": "center",
        "buttonClasses": "btn",
        "drops": "up",
        "locale": {
            "format": 'DD/MM/YYYY'
        },
        "applyButtonClasses": "btn-theme",
        "cancelClass": "btn-light"
    }, function (start, end, label) {
        //console.log('New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')');
    });

    /* inline calendar activate  */
    if ($('#inlinewrap1').length > 0) {
        $('#inlinewrap1').click();
    }

});