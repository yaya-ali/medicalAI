/*! component-toast.js | Adminuiux 2023-2024 */

"use strict";

document.addEventListener("DOMContentLoaded", function () {
    const toastTrigger1 = document.getElementById('liveToast1Btn')
    const toastLiveExample1 = document.getElementById('liveToast1')

    if (toastTrigger1) {
        const toastBootstrap1 = bootstrap.Toast.getOrCreateInstance(toastLiveExample1)
        toastTrigger1.addEventListener('click', () => {
            toastBootstrap1.show()
        })
    }

    const toastTrigger2 = document.getElementById('liveToast2Btn')
    const toastLiveExample2 = document.getElementById('liveToast2')

    if (toastTrigger2) {
        const toastBootstrap2 = bootstrap.Toast.getOrCreateInstance(toastLiveExample2)
        toastTrigger2.addEventListener('click', () => {
            toastBootstrap2.show()
        })
    }
    const toastTrigger3 = document.getElementById('liveToast3Btn')
    const toastLiveExample3 = document.getElementById('liveToast3')

    if (toastTrigger3) {
        const toastBootstrap3 = bootstrap.Toast.getOrCreateInstance(toastLiveExample3)
        toastTrigger3.addEventListener('click', () => {
            toastBootstrap3.show()
        })
    }

});

$(window).on('load', function () {

});