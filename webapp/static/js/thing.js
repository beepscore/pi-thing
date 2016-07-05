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

// When javascript source file is not in python template, I think can't use flask url_for
//var switchSource = new EventSource("{{ url_for( 'switch') }}");
// use url literal
var switchSource = new EventSource("/switch");

function updateSwitch(switchValue) {
    if (switchValue === '0') {
        $('#switch_value').text('Off');
    } else if (switchValue === '1') {
        $('#switch_value').text('On');
    }
}

switchSource.onmessage = function(switchEvent) {
    // event data shows on web page but at first I couldn't see it in console log
    // Chrome / View / Developer / Developer tools / console log didn't work
    // Chrome / View / Developer / JavaScript console works
    // now either one works! May be because filter default was not "all"
    // http://stackoverflow.com/questions/18760213/chrome-console-log-console-debug-are-not-working
    // console.log(switchEvent.data);
    // find html element with id switch_value and set text
    updateSwitch(switchEvent.data);
}
