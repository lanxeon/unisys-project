$(document).ready(function() {

    //socketio.emit('user joined', user.usn, namespace = '/private')
    var socket = io();
    var socket_private = io.connect('/private');

    //regular sockets
    socket.on('connect', function() {
        socket.send('User has connected!');
        console.log("NIGggggzzz");
    });
    
    socket.on('message', function(msg) {
        $("#messages").append('<li>'+msg+'</li>');
        console.log('Received message');
    });

    $('#sendbutton').on('click', function() {
        socket.send($('#myMessage').val());
        $('#myMessage').val('');
    });
    
    
    //private sockets
    socket_private.on('connect', (usn) =>{
        emit('user joined', usn, namespace = '/private');
    });

});