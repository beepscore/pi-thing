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
// var switchSource = new EventSource("\switch");
// use flask url_for to get endpoint for function
var switchSource = new EventSource("{{ url_for( 'switch') }}");

switchSource.onmessage = function(switchEvent) {
  console.log(switchEvent.data);
}
