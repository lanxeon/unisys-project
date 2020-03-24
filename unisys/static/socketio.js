$(document).ready(function() {
    var socket = io();
    var socket_private = io.connect('/private');
    var localUser;
    var remoteUser;
    var room;
    ttsServer = window.location.origin+'/tts';
    

    //script for autplaying audio element on first load
    window.audioStart = function(msgno) {
        let audioElement = document.getElementById('id'+msgno);
        audioElement.play();
    }

    //for finding the remoteUser once form is submitted
    remoteUser = $("#topRecvContent").text();
    console.log("the remote user is: "+remoteUser);

    //private sockets

    socket_private.on('user logged in', (usn)=>{
        console.log('user with username '+usn+' has connected on client side');
        localUser = usn;
        if( typeof remoteUser !== 'undefined' && remoteUser !== '')
        {
            socket_private.emit('create or join room', {'localUser': localUser, 'remoteUser': remoteUser});
            console.log("emmitting the create or join room event");
        }
    });

    /*
    if( typeof remoteUser !== 'undefined' && remoteUser !== '' && typeof localUser !== 'undefined' && localUser != '')
    {
        socket_private.emit('create or join room', {'localUser': localUser, 'remoteUser': remoteUser});
        console.log("emmitting the create or join room event");
    }
    */

    socket_private.on('joined room', (roomVal) => {
        room = roomVal;
        console.log('room name is: '+room);
    });


    socket_private.on('new private message', function(msg, sender) {
        if(sender != localUser || localUser == remoteUser)
        {
            //$("#messages").append("<span class = 'remoteText'><b>"+sender+" :</b> " +msg+"</span><br>");
            var div = document.createElement("div");
            div.setAttribute("class", "msgContainer");
            var span = document.createElement("span");
            span.setAttribute("class", "remoteText");
            span.innerHTML = "<b>"+sender+" :</b> "+msg;
            div.appendChild(span);
            //div.innerHTML = "<span class = 'remoteText'><b>"+sender+" :</b> "+msg+"</span>";
            $('#messages').append(div);
            div.style.height = span.clientHeight+"px";
            console.log(div.style.height+" "+span.clientHeight);
            //$('#messages').append("<br>");
    
            let formdata = new FormData();
            formdata.append("recMsg", msg);
            
            let xhr = new XMLHttpRequest();
            xhr.open('POST', ttsServer, true);
            xhr.onload = function() {
                if(this.status === 200) {
                    let payload = JSON.parse(this.response);
                    url = payload.url;
                    msgno = payload.msgno;

                    audio = document.createElement('p');
                    audio.innerHTML = "<audio id = 'id"+msgno+"' src='"+ url + "' controls onloadstart = 'audioStart("+msgno+")' style='position:relative; width:40%; height: 20px; left: 3%;'>";
                    $("#messages").append(audio);
                    //$("#messages").append('<br>');
                }
            else
                console.error(xhr);
            }
            xhr.send(formdata);
            
            console.log('Received message');
        }
    });


    
    $('#sendbutton').on('click', function() {
        var message_to_send = $('#myMessage').val();
        var div = document.createElement("div");
        div.setAttribute("class", "msgContainer");
        var span = document.createElement("span");
        span.setAttribute("class", "localText");
        span.innerHTML = "<b>"+localUser+" :</b> "+message_to_send;
        div.appendChild(span);
        //div.innerHTML = "<span class = 'localText'><b>"+localUser+" :</b> "+message_to_send+"</span>";
        $('#messages').append(div);
        div.style.height = span.clientHeight+"px";
        console.log(div.style.height+" "+span.clientHeight);
        //$('#messages').append("<span class = 'localText'><b>"+localUser+" :</b> "+message_to_send+"</span><br>");
        console.log('Currently, the room number is (while sending msg): '+ room);
        socket_private.emit('private message', {'username' : remoteUser, 'message' : message_to_send, 'sender' : localUser, 'room': room });
        console.log('message sent to: '+remoteUser);
        $('#myMessage').val('');
    });
});     