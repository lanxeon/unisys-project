/*
 * Taken from Chad Hart's "Object detection Web API" article from webrtchacks.com
 * and modified greatly for suiting the audio element creation as well as
 * to support dynamically resizing the canvas for various widths and heights
 * of the video on the webpage 
 */

//Parameters
const s = document.getElementById('objDetect');
const sourceVideo = s.getAttribute("data-source");  //the source video to use
const uploadWidth = s.getAttribute("data-uploadWidth"); //the width of the upload file
const mirror = s.getAttribute("data-mirror") || false; //mirror the boundary boxes
const scoreThreshold = s.getAttribute("data-scoreThreshold") || 0.5;
const apiServer = s.getAttribute("data-apiServer") || window.location.origin + '/image'; //the full TensorFlow Object Detection API server url

//Video element selector
v = document.getElementById(sourceVideo); //local
vr = document.getElementById("remoteVideo"); //remote

//provide width and height of vieo depending on window size
v.width = window.innerWidth * 0.25;
v.height = v.width * 0.5625;

//for remoteVideo as well
vr.width = window.innerWidth * 0.25;
vr.height = vr.width * 0.5625;


//resize video and canvas accordingly
window.addEventListener("resize", ev => {
    let w = window.innerWidth * 0.25;
    console.log(window.innerWidth);
    let h = w * 0.5625;
  
    if (w && h) {
      v.width = w;
      v.height = h;
      vr.width = w;
      vr.height = h;
      drawCanvas.width = v.width;
      drawCanvas.height = v.height;
    }

    resizeMessages();
  }, false);

//for starting events
let isPlaying = false,
    gotMetadata = false;

//Canvas setup

//create a canvas to grab an image for upload
let imageCanvas = document.createElement('canvas');
let imageCtx = imageCanvas.getContext("2d");

//create a canvas for drawing object boundaries
let drawCanvas = document.createElement('canvas');
document.body.appendChild(drawCanvas);
//for canvas
drawCanvas.width = v.width;
drawCanvas.height = v.height;
let drawCtx = drawCanvas.getContext("2d");

//draw boxes and labels on each detected object
function drawBoxes(objects) {

    //clear the previous drawings
    drawCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);
    console.log('in drawboxes()');

    //filter out objects that contain a class_name and then draw boxes and labels on each
    objects.filter(object => object.class_name).forEach(object => {

        
        let x = object.x * drawCanvas.width;
        let y = object.y * drawCanvas.height;
        let width = (object.width * drawCanvas.width) - x;
        let height = (object.height * drawCanvas.height) - y;
        console.log(object.sentence_generated+object.generated_sentence);


        if(object.sentence_generated == "true")
        {
            console.log('entered condition')
            $('#myMessage').val(object.generated_sentence);
        }

        //flip the x axis if local video is mirrored
        if (mirror) {
            x = drawCanvas.width - (x + width)
        }

        drawCtx.fillText(object.class_name + " - " + Math.round(object.score * 100) + "%", x + 5, y + 20);
        drawCtx.strokeRect(x, y, width, height);

    });
}

//Add file blob to a form and post
function postFile(file) {

    let auto = "false";
    //get the autocorrect checkbox
    autoCorrect = document.getElementById('autoCorrect');
    if(autoCorrect.checked == true)
        auto = "true";

    //Set options as form data
    let formdata = new FormData();
    formdata.append("image", file);
    formdata.append("threshold", scoreThreshold);
    formdata.append("autoCorrect", auto);

    let xhr = new XMLHttpRequest();
    xhr.open('POST', apiServer, true);
    xhr.onload = function () {
        if (this.status === 200) {
            let objects = JSON.parse(this.response);

            //draw the boxes
            drawBoxes(objects);

            //Save and send the next image
            imageCtx.drawImage(v, 0, 0, v.videoWidth, v.videoHeight, 0, 0, uploadWidth, uploadWidth * (v.videoHeight / v.videoWidth));
            imageCanvas.toBlob(postFile, 'image/jpeg');
        }
        else {
            console.error(xhr);
        }
    };
    xhr.send(formdata);
}

//Start object detection
function startObjectDetection() {

    console.log("starting object detection asdfghjk");

    //Set canvas sizes based on input video
    /*
    drawCanvas.width = v.videoWidth;
    drawCanvas.height = v.videoHeight;
    */

    //trial and error
    drawCanvas.width = v.width;
    drawCanvas.height = v.height;
    

    imageCanvas.width = uploadWidth;
    imageCanvas.height = uploadWidth * (v.videoHeight / v.videoWidth);

    //Some styles for the drawcanvas
    drawCtx.lineWidth = 4;
    drawCtx.strokeStyle = "cyan";
    drawCtx.font = "20px Verdana";
    drawCtx.fillStyle = "cyan";

    //Save and send the first image
    imageCtx.drawImage(v, 0, 0, v.videoWidth, v.videoHeight, 0, 0, uploadWidth, uploadWidth * (v.videoHeight / v.videoWidth));
    imageCanvas.toBlob(postFile, 'image/jpeg');

}

//Starting events

//check if metadata is ready - we need the video size
v.onloadedmetadata = () => {
    console.log("video metadata ready");
    gotMetadata = true;
    if (isPlaying)
        startObjectDetection();
};

//see if the video has started playing
v.onplaying = () => {
    console.log("video playing");
    isPlaying = true;
    if (gotMetadata) {
        startObjectDetection();
    }
};