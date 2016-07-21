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

var data = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
        {
            label: "My First dataset",
            fill: false,
            lineTension: 0.1,
            backgroundColor: "rgba(75,192,192,0.4)",
            borderColor: "rgba(75,192,192,1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            data: [65, 59, 80, 81, 56, 55, 40],
            spanGaps: false,
        }
    ]
};

var options = {
    scales: {
        xAxes: [{
            type: 'linear',
            position: 'bottom'
        }]
    }
};

// use jquery get()
var ctx = $("#dht_chart").get(0).getContext("2d");
// get first node in the jQuey collection
var dhtChart = Chart.Line(ctx, {
    data: data,
    options: options
});

// Setup server sent event endpoint for /switch
// https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events

// When javascript source file is not in python template, I think can't use flask url_for
//var thingSource = new EventSource("{{ url_for('thing') }}");
// use url literal
var thingSource = new EventSource("/thing");

function updateSwitch(switchValue) {
    if (switchValue === 0) {
        // find element with id switch_value, set text
        $('#switch_value').text('Off');
        $('#switch_value').toggleClass('label-danger', false);
        $('#switch_value').toggleClass('label-default', true);
    } else if (switchValue === 1) {
        $('#switch_value').text('On');
        $('#switch_value').toggleClass('label-danger', true);
        $('#switch_value').toggleClass('label-default', false);
    }
}

function updateThing(thingState) {
    // thingState.switch is syntactic sugar for thingState['switch']
    updateSwitch(thingState.switch);
    console.log('Temperature : ', thingState.temperature);
    console.log('Humidity: ', thingState.humidity);
}

// configure server sent event receiver
thingSource.onmessage = function(thingEvent) {
    // event data shows on web page but at first I couldn't see it in console log
    // Chrome / View / Developer / Developer tools / console log didn't work
    // Chrome / View / Developer / JavaScript console works
    // now either one works! May be because filter default was not "all"
    // http://stackoverflow.com/questions/18760213/chrome-console-log-console-debug-are-not-working
    // console.log(thingEvent.data);
    jsonObject = $.parseJSON(thingEvent.data)
    updateThing(jsonObject);
}
