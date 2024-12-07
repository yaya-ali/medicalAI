/*! clinic earning.js | Adminuiux 2023-2024 */

"use strict";

document.addEventListener("DOMContentLoaded", function () {

    /* chart js areachart summary  */
    window.randomScalingFactor = function () {
        return Math.round(Math.random() * 20);
    }

    /* patient summary chart */
    var areachart2 = document.getElementById('earningbyday').getContext('2d');
    var gradient2 = areachart2.createLinearGradient(0, 0, 0, 280);
    gradient2.addColorStop(0, 'rgba(88, 64, 239, 0.5)');
    gradient2.addColorStop(1, 'rgba(88, 64, 239, 0)');
    var gradient1 = areachart2.createLinearGradient(0, 0, 0, 280);
    gradient1.addColorStop(0, 'rgba(145, 195, 0, 0.85)');
    gradient1.addColorStop(1, 'rgba(176, 197, 0, 0)');
    var myareachartCofig2 = {
        type: 'line',
        data: {
            labels: ['1/9', '2/9', '3/9', '4/9', '5/9', '6/9', '7/9', '8/9', '9/9', '10/9'],
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
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                ],
                radius: 0,
                backgroundColor: gradient2,
                borderColor: '#5840ef',
                borderWidth: 1,
                fill: true,
            },
            {
                label: 'earning of Votes',
                data: [
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                    randomScalingFactor(),
                ],
                radius: 0,
                backgroundColor: gradient1,
                borderColor: '#91C300',
                borderWidth: 1,
                fill: true,
            }]
        },
        options: {
            maintainAspectRatio: false,
            barThickness: 16,
            borderRadius: 2,
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

    /* semi doughnut chart js */
    var semidoughnutchart = document.getElementById('semidoughnutchart').getContext('2d');
    var semidata = {
        labels: ['Daily Vages', 'Cancelled Bookings', 'Oxygen', 'Manpower', 'Medical Facilities'],
        datasets: [
            {
                label: 'Expense categories',
                data: [40, 35, 15, 25, 20],
                backgroundColor: ['#6faa00', '#ffc107', '#fd7e14', '#5840ef', '#becede'],
                borderWidth: 0,
            }
        ]
    };
    var mysemidoughnutchartCofig = {
        type: 'doughnut',
        data: semidata,
        options: {
            circumference: 180,
            rotation: -90,
            responsive: true,
            cutout: 80,
            tooltips: {
                position: 'nearest',
                yAlign: 'bottom'
            },
            plugins: {
                legend: {
                    display: false,
                    position: 'top',
                },
                title: {
                    display: false,
                    text: 'Chart.js Doughnut Chart'
                }
            },
            layout: {
                padding: 0,
            },
        },
    };
    var mysemidoughnutchart = new Chart(semidoughnutchart, mysemidoughnutchartCofig);

})