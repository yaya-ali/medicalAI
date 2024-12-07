/*! clinic-view-patient.js | Adminuiux 2023-2024 */

"use strict";

document.addEventListener("DOMContentLoaded", function () {

    window.Dropzone

    /* patient sleep chart */
    window.randomScalingFactor = function () {
        return Math.round(Math.random() * 20);
    }
    var areachart2 = document.getElementById('patientsummary').getContext('2d');
    var myareachartCofig2 = {
        type: 'line',
        data: {
            labels: ['1/8', '2/8', '3/8', '4/8', '5/8', '6/8', '7/8'],
            datasets: [{
                label: '# of Votes',
                data: [
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                ],
                radius: 2,
                backgroundColor: 'rgba(0, 0, 0, 0)',
                borderColor: '#5840ef',
                borderWidth: 3,
                fill: true,
                tension: 0.3,
            }]
        },
        options: {
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false,
                },
            },
            scales: {
                y: {
                    display: false,
                    beginAtZero: true,
                },
                x: {
                    grid: {
                        display: false
                    },
                    display: true,
                    beginAtZero: true,
                }
            }
        }
    }
    var myAreaChart2 = new Chart(areachart2, myareachartCofig2);


    /* Initialize dataTable */
    $('#clientScheduleGrid').DataTable({
        searching: false,
        lengthChange: false,
        autoWidth: false,
        columnDefs: [{ orderable: false, targets: 4 }],
        order: [[0, 'desc']],
        pageLength: 4,
        responsive: true,
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