/*! component-fullcalendar.js | Adminuiux 2023-2024 */

"use strict";

document.addEventListener("DOMContentLoaded", function () {
    /* calendar view */
    var currentday = new Date();
    var thismonth = ("0" + (currentday.getMonth() + 1)).slice(-2);
    var thisyear = currentday.getFullYear();
    var thisday = ("0" + currentday.getDate()).slice(-2);

    var calendarEl = document.getElementById('calendar');
    var calendar = new Calendar(calendarEl, {
        plugins: [dayGridPlugin, timeGridPlugin, listPlugin],
        initialView: 'dayGridMonth',
        height: 'auto',
        // customButtons: {
        //     myCustomButton: {
        //         text: 'Create Appointment',
        //         click: function () {
        //             alert('clicked the custom button!');
        //         }
        //     }
        // },
        headerToolbar: {
            // left: 'prev,next myCustomButton',
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: [
            {
                title: 'All Day Event',
                className: 'bg-success-subtle',
                start: thisyear + '-' + thismonth + '-01',
                description: 'Lecture'
            },
            {
                title: 'Long Event',
                className: 'bg-success-subtle',
                start: thisyear + '-' + thismonth + '-07',
                end: thisyear + '-' + thismonth + '-10'
            },
            {
                groupId: 999,
                className: 'bg-theme-1-space text-white',
                title: '<span class="position-absolute top-0 end-0 badge bg-success p-1 m-1"><small>Paid</small></span ><p class="mb-0 small fw-medium">16:00 am</p><div class="row gx-2"><div  class="col-auto"><img src="assets/img/modern-ai-image/user-4.jpg" class="avatar avatar-20 rounded-circle" alt=""> <img src="https://i.pravatar.cc/300" class="avatar avatar-20 rounded-circle" alt=""></div> <div class="col">Will Johnson</div></div><p class="mb-0 opacity-75 small text-truncated" >High fever and cough</p>',
                start: thisyear + '-' + thismonth + '-09T16:00:00'
            },
            {
                groupId: 999,
                title: 'Repeating Event',
                className: 'bg-cyan-subtle',
                start: thisyear + '-' + thismonth + '-16T16:00:00'
            },
            {
                title: '<p class="mb-0 small fw-medium">09:00 am - 12:00 pm </p><div class="row gx-2"><div  class="col-auto"><i class="bi bi-microsoft-teams"></i></div><div class="col">Evolution of era</div></div><p class="mb-0 opacity-75 small text-truncated" >Conference</p>',
                className: 'bg-yellow-subtle',
                start: thisyear + '-' + thismonth + '-11',
                end: thisyear + '-' + thismonth + '-13'
            },
            {
                title: 'Meeting',
                className: 'bg-orange-subtle',
                start: thisyear + '-' + thismonth + '-12T10:30:00',
                end: thisyear + '-' + thismonth + '-10T12:30:00'
            },
            {
                title: 'Lunch',
                className: 'bg-purple-subtle',
                start: thisyear + '-' + thismonth + '-' + thisday + 'T04:00:00'
            },
            {
                title: '<p class="mb-0 small fw-medium">10:30 am, 2hr</p><div class="row gx-2"><div  class="col-auto"><i class="bi bi-buildings"></i></div><div class="col">Evolution of era</div></div><p class="mb-0 opacity-75 small text-truncated" >Meeting</p>',
                className: 'bg-orange-subtle',
                start: thisyear + '-' + thismonth + '-' + thisday + 'T10:30:00'
            },
            {
                title: 'Happy Hour',
                className: 'bg-green-subtle',
                start: thisyear + '-' + thismonth + '-' + thisday + 'T12:30:00'
            },
            {
                title: '<p class="mb-0 small fw-medium">16:00 am</p><div class="row gx-2"><div  class="col-auto"><img src="assets/img/modern-ai-image/user-6.jpg" class="avatar avatar-20 rounded-circle" alt=""> </div> <div class="col">Will Johnson</div></div><p class="mb-0 opacity-75 small text-truncated" >High fever and cough</p>',
                className: 'bg-info-subtle',
                start: thisyear + '-' + thismonth + '-10T20:00:00'
            },
            {
                title: '<span class="position-absolute top-0 end-0 badge bg-danger p-1 m-1"><small>Unpaid</small></span ><p class="mb-0 small fw-medium">7:00 am</p><div class="row gx-2"><div  class="col-auto"><img src="assets/img/modern-ai-image/user-7.jpg" class="avatar avatar-20 rounded-circle" alt=""> </div> <div class="col">Rickie Birthday</div></div><p class="mb-0 opacity-75 small text-truncated" >Birthday Celebration</p>',
                className: 'bg-theme-1-space text-white',
                start: thisyear + '-' + thismonth + '-' + thisday + 'T07:00:00'
            },
            {
                title: 'Click for Google',
                className: 'bg-primary-subtle',
                url: 'http://google.com/',
                start: thisyear + '-' + thismonth + '-28'
            }
        ],
        eventContent: function (info) {
            return {
                html: info.event.title
            };
        }
    });
    calendar.render();

});