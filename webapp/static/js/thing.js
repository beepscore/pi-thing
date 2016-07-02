$(document).ready(function() {
    $('#led_on').click(function() {
        console.log('LED on!');
        $.post('/led/1');
    });
    $('#led_off').click(function() {
        console.log('LED off!');
        $.post('/led/0');
    });
});
