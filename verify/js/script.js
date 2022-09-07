/**
* this script is for face detetion and screenshoot
* if system detect face front of camera
* then he take a screen shot of an active windows
*/
const video = document.getElementById('video');
const predictName = document.getElementById('predictName')
const screenEl = document.createElement('video');
screenEl.id = "screen";
screenEl.autoplay = "autoplay";
const screen = screenEl;
const image_face = document.getElementById('face1');

var face_pose = document.getElementsByClassName("face");
var defaut_src = window.location.href + "images/default_user.png";
var no_face_src = window.location.href + "images/no_face.png";

var nbr_face_ok = 0;
var display_surface = "";
var nbr_face = 0;

var webcam_is = false;
var screen_is = false;

var face_data = null;
/**
 * form data
 * */
var lastName = document.getElementById("lastName");
var firstName = document.getElementById("firstName");
var stateOne = "";
var stateTwo = false;
/**
 * option buttun
 * @capture @save @cancel
 * */
var captureBtn = document.getElementById("capture");
var saveBtn = document.getElementById("register");
var cancelBtn = document.getElementById("cancel");

const constraints = {
    video: true
};

/**
 * loading a model for face detection
 */
async function loadModel() {
    Promise.all([
        // faceapi.nets.tinyFaceDetector.loadFromUri('/' + window.location.pathname.split( '/' )[1] + '/models')
        faceapi.nets.tinyFaceDetector.loadFromUri('/face-detection-based-web/models'),
        faceapi.nets.ssdMobilenetv1.loadFromUri('/face-detection-based-web/models'),
        faceapi.nets.faceExpressionNet.loadFromUri('/face-detection-based-web/models'),
    ]).then(startVideo)
}
/**
 * start video stream from web webcame
*/
function startVideo() {
    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia(constraints).
            then(handleSuccess).catch(handleError);
    }
}
/*
 * this function is to stop playing 
 * stream from webcom
 * */
function stopVideo() {
    var stream = video.srcObject;
    var tracks = stream.getTracks();

    for (var i = 0; i < tracks.length; i++) {
        var track = tracks[i];
        track.stop();
    }
    video.srcObject = null;
    webcam_is = false;
    this.innerHTML = "Share webcam";
}
/**
 * when use click on start capture buttuon 
 * or on video frame this function check
 * if the streaming is playing or not
 * and open it or stop it
 * */
function streaming() {
    if (!webcam_is) {
        loadModel();
        webcam_is = true;
    }
    else {
        var stream = video.srcObject;
        var tracks = stream.getTracks();

        for (var i = 0; i < tracks.length; i++) {
            var track = tracks[i];
            track.stop();
        }
        video.srcObject = null;
        webcam_is = false;
        this.innerHTML = "Start capture";
    }
}
function test(){
    console.log("Test okay")
}
function handleSuccess(stream) {
    video.srcObject = stream;
    btn_webcame.innerHTML = "Stop capture";
    webcam_is = true;
}
function handleError(error) {
    console.log("Please give access to your Webcam to enjoy this course !");
}

captureBtn.addEventListener("click", function (event) {
    event.preventDefault();
    /**
     * check if the webcam is open or not
     * and change the status of webcam_is
     */
    streaming();
});
video.addEventListener("mouseenter", () => {
    video.style.cursor = "pointer";
    video.title = "Click here to play webcam for face capture";
});

video.addEventListener("click", () => {
    streaming();
});
video.addEventListener('play', () => {
    setInterval(async () => {
        const detections = await faceapi.detectAllFaces(video, new faceapi.SsdMobilenetv1Options()) //.withFaceExpressions();
        const faceImages = await faceapi.extractFaces(video, detections);
        //count number of face detected in the stream
        nbr_face = detections.length;

        if (nbr_face > 0) {
            const canvas_canvas = document.getElementById('canvas');
            const dims = faceapi.matchDimensions(canvas_canvas, video, true)
            
            const resizedResult = faceapi.resizeResults(detections, dims)
            const minConfidence = 0.05
            faceapi.draw.drawDetections(canvas_canvas, resizedResult)
            // faceapi.draw.drawFaceExpressions(canvas, resizedResult, minConfidence)
            faceImages.forEach(function(canvas){
                face_data = canvas.toDataURL('image/jpeg')
                /**
                 * 
                 */
                console.log(stateOne, stateTwo)
                if(stateOne == ""){
                    requestXHR(face_data);
                    console.log("test okay")   
                }
            })
        }
    }, 10);
});

function requestXHR(face_data) {
    stateOne = 'pending'
    const toSend = {
        face: face_data
    };
    const jsonString = JSON.stringify(toSend);
    
    var xhr = new XMLHttpRequest();
    var add = "http://localhost:5000/face/predapi";
  
    xhr.open("POST", add);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(jsonString);
    xhr.addEventListener('readystatechange', function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            console.log(xhr.status)
            response = JSON.parse(xhr.responseText);
            console.log(response);
            predict_name = response['predict_name'].split("_");
            face_context = response['face_context'];
            if (xhr.status != '200'){
                stateOne = ''
                stateTwo = true
                face_data = null;
                lastName = predict_name[0];
                firstName = predict_name[1];
                last = lastName.charAt(0).toUpperCase() + lastName.slice(1)
                first = firstName.charAt(0).toUpperCase() + firstName.slice(1)
                var predict_div = document.createElement('div');
                predict_div.id = lastName + "_" + firstName
                predict_div.style.padding = '5px';
                predict_div.style.border = '1px solid #f2f2f2';
                predict_div.style.textAlign = 'left'

                var predict = document.createElement('span');
                predict.style.display = 'inline-block';
                predict.style.padding = '5px';
                predict.innerHTML = last + " " + first;

                var context = document.createElement('img');

                context.src = face_context;
                context.width = "120";
                context.height = "100";
                
                predict_div.appendChild(context);
                predict_div.appendChild(predict)
                var old_pred = predictName.getElementsByTagName('div');
                if(old_pred.length > 0){
                    for(var i = 0; i < old_pred.length; i++){
                        if(old_pred[i].id == predict_div.id){
                            predictName.replaceChild(predict_div, old_pred[i])
                            break;
                        }else{
                            predictName.appendChild(predict_div)
                        }
                    }
                }else{
                    predictName.appendChild(predict_div)
                }
            }
        }
    });
}