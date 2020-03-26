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

    function scrollSmoothToBottom (id) {
        var div = document.getElementById(id);
        $('#' + id).animate({
           scrollTop: div.scrollHeight - div.clientHeight
        }, 500);
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


    socket_private.on('joined room', (roomVal) => {
        room = roomVal;
        console.log('room name is: '+room);
    });


    socket_private.on('new private message', function(msg, sender) {
        if(sender != localUser || localUser == remoteUser)
        {
            var div = document.createElement("div");
            div.setAttribute("class", "msgContainer");
            var span = document.createElement("span");
            span.setAttribute("class", "remoteText");
            span.innerHTML = "<b>"+sender+" :</b> "+msg;
            div.appendChild(span);

            $('#messages').append(div);
            div.style.height = span.clientHeight+"px";
            scrollSmoothToBottom("messages");

            ttsCheck = document.getElementById('tts');
            if(ttsCheck.checked == true) {
                let formdata = new FormData();
                formdata.append("recMsg", msg);
                
                let xhr = new XMLHttpRequest();
                xhr.open('POST', ttsServer, true);
                xhr.onload = function() {
                    if(this.status === 200) {
                        let payload = JSON.parse(this.response);
                        url = payload.url;
                        msgno = payload.msgno;

                        audio = document.createElement('div');
                        audio.style.marginTop = "7px";
                        audio.style.marginBottom = "1px";
                        audio.innerHTML = "<audio id = 'id"+msgno+"' src='"+ url + "' controls onloadstart = 'audioStart("+msgno+")' style='position:relative; width:40%; height: 20px; left: 3%;'>";
                        $("#messages").append(audio);
                        scrollSmoothToBottom("messages");
                    }
                    else
                        console.error(xhr);
                }
                xhr.send(formdata);
                console.log('Converting Text-To-Speech');
            }
            
            console.log('Received message');
        }
    });
    

    $('#sendbutton').on('click', function() {
        var message_to_send = $('#myMessage').val();
        
        //make sure there is content in the textarea before sending
        if(message_to_send.trim() == "")
            alert("You need to enter a message first, " + localUser + "!");
        else
        {
            var div = document.createElement("div");
            div.setAttribute("class", "msgContainer");
            var span = document.createElement("span");
            span.setAttribute("class", "localText");
            span.innerHTML = "<b>"+localUser+" :</b> "+message_to_send;
            div.appendChild(span);

            $('#messages').append(div);
            div.style.height = span.clientHeight+"px";
            scrollSmoothToBottom("messages");

            socket_private.emit('private message', {'receiver' : remoteUser, 'message' : message_to_send, 'sender' : localUser, 'room': room });
            console.log('message sent to: '+remoteUser);
            $('#myMessage').val('');
        }
    });
});     