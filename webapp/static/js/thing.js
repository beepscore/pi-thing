$(document).ready(function() {

    // Attach button click handlers
    $('#led_on').click(function() {
        console.log('LED on!');
        $.post('/led/1');
    });

    $('#led_off').click(function() {
        console.log('LED off!');
        $.post('/led/0');
    });
});

// Setup server sent event endpoint for /switch
// https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events

// var switchSource = new EventSource("/switch");
// use flask url_for to get endpoint for function
var switchSource = new EventSource("{{ url_for( 'switch') }}");

switchSource.onmessage = function(switchEvent) {
    // event data shows on web page but at first I couldn't see it in console log
    // Chrome / View / Developer / Developer tools / console log didn't work
    // Chrome / View / Developer / JavaScript console works
    // now either one works! May be because filter default was not "all"
    // http://stackoverflow.com/questions/18760213/chrome-console-log-console-debug-are-not-working
    console.log(switchEvent.data);
}
