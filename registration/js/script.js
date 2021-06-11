/**
* this script is for face detetion and screenshoot
* if system detect face front of camera
* then he take a screen shot of an active windows
*/
const video = document.getElementById('video');
const screenEl = document.createElement('video');
screenEl.id = "screen";
screenEl.autoplay = "autoplay";
const screen = screenEl;
const canvas_screen = document.getElementById('canvas');
var face_context = "";

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
 * We are using Tiny Face Detector
 */
async function loadModel() {
    Promise.all([
        // faceapi.nets.tinyFaceDetector.loadFromUri('/' + window.location.pathname.split( '/' )[1] + '/models')
        faceapi.nets.tinyFaceDetector.loadFromUri('/face-detection-based-web/models'),
        faceapi.nets.ssdMobilenetv1.loadFromUri('/face-detection-based-web/models'),
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
    const canvas_video = faceapi.createCanvasFromMedia(video);
    const displaySize = {
        width: video.width,
        height: video.height
    };
    faceapi.matchDimensions(canvas_video, displaySize);
    setInterval(async () => {
        const detections = await faceapi.detectAllFaces(video, new faceapi.SsdMobilenetv1Options());
        const faceImages = await faceapi.extractFaces(video, detections);

        /**
         * count number of face detected in the stream
         */
        nbr_face = detections.length;
        const resizedDetections = faceapi.resizeResults(detections, displaySize);
        canvas_video.width = video.videoWidth;
        canvas_video.height = video.videoHeight;
        faceImages.forEach(function(canvas){
            face_data = canvas.toDataURL('image/jpeg')
        
            for(var i = 0; i < face_pose.length; i++) {
                if (face_pose[i].src === defaut_src || face_pose[i].src === no_face_src) {
                    nbr_face_ok += 1;
                    face_pose[i].src = face_data;
                    break;
                }
            }
            if (nbr_face_ok === 15) {
                var ctx = canvas_video.getContext('2d');
                ctx.drawImage(video, 0, 0);
                face_context = canvas_video.toDataURL('image/jpeg')
                
                if (confirm("All face pose captured successful \n Do you want stop play video ?")) {
                    stopVideo();
                }
            }
        })
    }, 1000);
});
/**
 * this function is to reset a pose face when the first
 * is not done well
 * @param {any} id
 */
function resetFace(id) {
    var face = document.getElementById(id);

    if (face.src != defaut_src) {
        if (confirm("Do you want to delete and recapture again")) {
            face.src = defaut_src;
            nbr_face_ok--;
            streaming();
        }
        else {
            alert("Please click on fach wich you want to delete");
        }
    }
    else {
        console.log(face.id);
    }
}
function requestXHR(first_name, last_name, image_face, face_context) {
    label = first_name + '_' + last_name
    const toSend = {
        label: label.toLowerCase(),
        face: image_face,
        face_context: face_context,
    };
    
    const jsonString = JSON.stringify(toSend);
    // console.log(jsonString);
    
    var xhr = new XMLHttpRequest();
    var add = "http://localhost:5000/face/regisapi";
  
    xhr.open("POST", add);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(jsonString);
    xhr.addEventListener('readystatechange', function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            console.log(xhr.status)
            response = JSON.parse(xhr.responseText);
            console.log(response);
            if (xhr.status != '200'){
                alert('Face saved succeful')
                for (i = 0; i < face_pose.length; i++) {
                    face_pose[i].src = defaut_src;
                }
                nbr_face_ok = 0;
                face_data = null;
                lastName.value = "";
                firstName.value = "";
            }
        }
    });
}
/**
 * 
 */
function uploadData(face) {
    var form = new FormData();
    form.append("face", face);
   
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "ImageController.php");
    // xhr.setRequestHeader("Content-Type", "multipart/form-data");

    xhr.send(form);
    xhr.addEventListener("readystatechange", function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            console.log(xhr.responseText);
            console.log("status request : " + xhr.status);
            alert("Student registration successefull !");

            for (i = 0; i < face_pose.length; i++) {
                face_pose[i].src = defaut_src;
            }
            nbr_face_ok = 0;
            face_data = null;
            lastName.value = "";
            firstName.value = "";
            gender.selectedIndex = 0;
            birthdayDate.value = "";

            schoolName.value = "";
            codeField = "";
            codeClass = "";

            studentId.value = "";
            phoneNumber.value = "";
            email.value = "";
        }
    });
}
cancelBtn.addEventListener("click", function () {

    for (i = 0; i < face_pose.length; i++) {
        face_pose[i].src = defaut_src;
    }
    nbr_face_ok = 0;
    face_data = null;
    lastName.value = "";
    firstName.value = "";
});

saveBtn.addEventListener("click", function () {
    var error = 0;
    if (lastName.value === "" 
        || firstName.value === ""
        || nbr_face_ok < 15) {
        
        if (lastName.value === "") {
            alert("Please check student last name");
        }
        if (firstName.value === "") {
            alert("Please check student first name");
        }
        if (nbr_face_ok < 15 || face_context == "") {
            alert("Please run webcame to complete all face pose as required");
        }
    } 
    else {
        var image_face = '';
        for (i = 0; i < face_pose.length; i++) {
            image_face = image_face + '-----' + face_pose[i].src;
            // uploadData(face_data);
        }
        // console.log('image_face', image_face)
        requestXHR(firstName.value, lastName.value, image_face, face_context);
    }
});