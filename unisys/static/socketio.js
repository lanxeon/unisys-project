
//for appending message to the textbox
window.appendMessage = (messageClass, messageSender, messageContent) => {
    var div = document.createElement("div");
    div.setAttribute("class", "msgContainer");
    var span = document.createElement("span");
    span.setAttribute("class", messageClass);
    span.innerHTML = "<b>"+messageSender+" :</b> "+messageContent;
    div.appendChild(span);

    $('#messages').append(div);
    div.style.height = span.clientHeight+"px";
    //scrollSmoothToBottom("messages");
};


//for scrolling smoothly on appending message
window.scrollSmoothToBottom = (id) => {
    var div = document.getElementById(id);
    $('#' + id).animate({ scrollTop: div.scrollHeight - div.clientHeight }, 500);
};


//Conversion of base64 string to BLOB object. Copied off stack overflow
window.b64toBlob = (b64Data, contentType='', sliceSize=512) => {
    const byteCharacters = atob(b64Data);
    const byteArrays = [];
    
    for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
        const slice = byteCharacters.slice(offset, offset + sliceSize);
    
        const byteNumbers = new Array(slice.length);
        for (let i = 0; i < slice.length; i++) {
        byteNumbers[i] = slice.charCodeAt(i);
        }
    
        const byteArray = new Uint8Array(byteNumbers);
        byteArrays.push(byteArray);
    }
    
    const blob = new Blob(byteArrays, {type: contentType});
    return blob;
};


//For loading up image
window.appendImage = (filedata, messageClass) => {
    //making a new XHR for getting the specified image
    var request = new XMLHttpRequest();
    request.open('GET', filedata, true);
    request.responseType = 'blob';

    request.onload = function() {
        const data = request.response;

        //blob url conversion
        const url = URL.createObjectURL(data);

        //adding image to div
        var div = document.createElement("div");
        div.setAttribute("class", "msgContainer");
        var img = document.createElement("img");
        img.setAttribute("class", messageClass);
        img.src = url;
        div.appendChild(img);

        //adding dummy span for ::before pseudoelement
        var span = document.createElement("span");
        span.setAttribute("class", "localTextEmpty");
        div.appendChild(span);

        var w,h;

        //need to add onload inorder to get image width and height
        img.onload = () => {
            w = img.width;
            h = img.height;
            div.style.height = img.clientHeight+"px";
        }
        $('#messages').append(div);
    };
    request.send();
};



$(document).ready(function() {
  
   window.socket = io(); //default namespace
   window.socket_private = io.connect('/private');
   window.localUser;
   window.remoteUser;
   window.room;
   window.roomID;
   window.ttsServer = window.location.origin+'/tts'; 
   window.socket_video = io.connect('/video'); //socketIO namespace for webrtc video chat


    //script for autplaying audio element on first load
    window.audioStart = function(msgno) {
        let audioElement = document.getElementById('id'+msgno);
        audioElement.play();
    }


    //for finding the remoteUser once form is submitted
    remoteUser = $("#topRecvContent").text();
    console.log("the remote user is: "+remoteUser);

    //private sockets

    //Response from user side on 'connect' event
    socket_private.on('user logged in', (usn)=>{
        console.log('user with username '+usn+' has connected on client side');
        localUser = usn;
        if( typeof remoteUser !== 'undefined' && remoteUser !== '')
        {
            socket_private.emit('create or join room', {'localUser': localUser, 'remoteUser': remoteUser});
            console.log("emmitting the create or join room event");
        }
    });


    
    //On joining room after querying DB and stuff
    socket_private.on('joined room', (id,roomVal) => {
        room = roomVal;
        roomID = id;
        console.log('room name is: '+room);
    });



    //On receiving a text message
    socket_private.on('new private message', function(msg, sender) {
        if(sender != localUser || localUser == remoteUser)
        {
            appendMessage("remoteText", sender, msg);
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


    //On receiving an image
    socket_private.on('image file', (payload) => {
        if(payload.sender != localUser || localUser == remoteUser)
        {
            const file = payload.file;
            const fileName = payload.fileName;
            //console.log(fileName);

            //extract the pure base 64 sting and contentType
            const fileDecoded = file.slice(file.indexOf(",")+1,file.length);
            const contentType = file.slice(file.indexOf("image/"),file.indexOf(";")+1);

            const blob = b64toBlob(fileDecoded, contentType); //Convert base 64 to blob array
            const fileForUrlConversion = new File([blob], fileName, {type: contentType}); //Convert blob into file object

            //File url conversion
            const url = URL.createObjectURL(fileForUrlConversion);

            //adding image to div
            var div = document.createElement("div");
            div.setAttribute("class", "msgContainer");
            var img = document.createElement("img");
            img.setAttribute("class", "remoteImg");
            img.src = url;
            div.appendChild(img);

            //adding dummy span for ::before pseudoelement
            var span = document.createElement("span");
            span.setAttribute("class", "remoteTextEmpty");
            //span.innerHTML = "<b>"+messageSender+" :</b> "+messageContent;
            div.appendChild(span);

            var w,h;

            //need to add onload inorder to get image width and height
            img.onload = () => {
                w = img.width;
                h = img.height;
                div.style.height = img.clientHeight+"px";
            }
            $('#messages').append(div);
        }
    });

    

    //On clicking send button to send a text message
    $('#sendbutton').on('click', function() {
        var message_to_send = $('#myMessage').val();
        
        //make sure there is content in the textarea before sending
        if(message_to_send.trim() == "")
            alert("You need to enter a message first, " + localUser + "!");
        else
        {
            appendMessage("localText", localUser, message_to_send);
            scrollSmoothToBottom("messages");

            const message = {
                                'receiver' : remoteUser, 
                                'message' : message_to_send, 
                                'sender' : localUser, 
                                'room': room , 
                                'roomID': roomID
                            };

            socket_private.emit('private message', message);
            console.log('message sent to: '+remoteUser);
            $('#myMessage').val('');
        }
    });



    //When file is attached
    $('#attachment').on('change', function(e){
        const data = e.originalEvent.target.files[0];
        console.log(data);
        console.log("MIME Type: " + data.type);
        console.log("Image size is: " + (data.size/1000) + "kb");
        if(data.type.includes("image/"))
            sendImage(data)     
    });

    
    //For sending image
    function sendImage(data){
        var reader = new FileReader();
        reader.onload = function(evt){
            
            //Payload being sent to the server
            const msg = {};
            msg.sender = localUser;
            msg.receiver = remoteUser;
            msg.room = room;
            msg.roomID = roomID;
            msg.file = evt.target.result;
            msg.fileName = data.name;
            
            //blob url conversion
            const url = URL.createObjectURL(data);

            //adding image to div
            var div = document.createElement("div");
            div.setAttribute("class", "msgContainer");
            var img = document.createElement("img");
            img.setAttribute("class", "localImg");
            img.src = url;
            div.appendChild(img);

            //adding dummy span for ::before pseudoelement
            var span = document.createElement("span");
            span.setAttribute("class", "localTextEmpty");
            //span.innerHTML = "<b>"+messageSender+" :</b> "+messageContent;
            div.appendChild(span);

            var w,h;

            //need to add onload inorder to get image width and height
            img.onload = () => {
                w = img.width;
                h = img.height;
                div.style.height = img.clientHeight+"px";
            }
            $('#messages').append(div);
            
            //emit the event
            socket_private.emit('image file', msg);
        };
        //reader.readAsDataURL(data);
        reader.readAsDataURL(data);
    }
});     