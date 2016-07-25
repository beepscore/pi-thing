$(document).ready(function() {

    // Setup temperature & humidity chart.
    // use jquery get()
    // get first node in the jQuery collection
    var ctx = $('#dht_chart').get(0).getContext('2d');

    var dhtChart = new Chart(ctx).Line({
        labels: [],
        datasets: [
        {
            label: "Temperature (Celsius)",
            fillColor: "rgba(220,220,220,0.2)",
            strokeColor: "rgba(220,220,220,1)",
            pointColor: "rgba(220,220,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
            data: []
        },
        {
            label: "Humidity (%)",
            fillColor: "rgba(151,187,205,0.2)",
            strokeColor: "rgba(151,187,205,1)",
            pointColor: "rgba(151,187,205,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(151,187,205,1)",
            data: []
        }
        ]

    });

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

    function updateTemperatureHumidity(temperature, humidity) {
        console.log('Temperature : ', temperature);
        console.log('Humidity: ', humidity);
        dhtChart.addData([temperature, humidity],
                new Date().toLocaleTimeString());

        // limit history to dataLengthMaximum most recent readings by removing first
        var dataLengthMaximum = 20;
        if (dhtChart.datasets[0].points.length >= dataLengthMaximum) {
            dhtChart.removeData()
        }
    }

    // attempt to connect to server
    var socket = io.connect();

    // register to listen for event 'connect' which fires when client connects
    socket.on('connect', function() {
        console.log('Client connected!');
    });

    socket.on('temperature_humidity_changed', function(event) {
        updateTemperatureHumidity(event.temperature, event.humidity);
    });

    socket.on('switch_changed', function(event) {
        // event has a payload json dictionary with key 'switch'
        // call updateSwitch with value
        updateSwitch(event.switch)
    });

    // Attach button click handlers
    $('#led_on').click(function() {
        console.log('LED on!');
        // send POST request to server.
        // traditional, non WebSocket method
        //$.post('/led/1');

        // use emit to push to server
        // socketio will use WebSocket if available, else fall back to http
        // emit an event with a name and a payload of json object or string
        socket.emit('change_led', 'on');
    });

    $('#led_off').click(function() {
        console.log('LED off!');
        socket.emit('change_led', 'off');
    });

});
