'use strict';


//Get camera video
const constraints = {
    audio: false,
    video: {
        width: {min: 640, ideal:1280, max: 1920},
        height: {min: 480, ideal:720, max: 1080}
    }
};

navigator.mediaDevices.getUserMedia(constraints)
    .then(stream => {
        document.getElementById("localVideo").srcObject = stream;
        console.log("Got local user video");
    })
    .catch(err => {
        console.log('navigator.getUserMedia error: ', err);
        // console.log("Gonna play default video then");
        // const vid = document.getElementById("localVideo");
        // vid.muted = true;
        // vid.loop = true;
        // vid.src = window.location.origin+"/static/images/static.mp4";  
    });

    // const vid = document.getElementById;
    // if(vid.src === undefined){
    //     vid.muted = true;
    //     vid.loop = true;
    //     vid.src = window.location.origin+"/static/images/static.mp4";
    // };


//variables required for webrtc
var isChannelReady = false;
var isInitiator = false;
var isStarted = false;
var localStream;
var pc;
var remoteStream;
var turnReady;

var pcConfig = {
'iceServers': [{
    'urls': 'stun:stun.l.google.com:19302'
}]
};

// Set up audio and video regardless of what devices are present.
var sdpConstraints = {
    offerToReceiveAudio: true,
    offerToReceiveVideo: true
};



