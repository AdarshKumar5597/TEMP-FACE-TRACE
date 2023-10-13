document.addEventListener("DOMContentLoaded", () => {
    let flag = 0;
    let but = document.getElementById("camera-access");
    let video = document.getElementById("vid");
    let mediaDevices = navigator.mediaDevices;
    let cameraPart = document.querySelector('.web-cam');
    video.muted = true;

    but.addEventListener("click", () => {
        flag = flag + 1;
        console.log(flag);

        if (flag % 2 == 1) {
            cameraPart.style.background = "#E84949"
            cameraPart.style.boxShadow = "10px 10px 30px 0 rgba(0, 0, 0, 1)"
            mediaDevices
                .getUserMedia({
                    video: true,
                    audio: true,
                })
                .then((stream) => {
                    video.srcObject = stream;
                    video.addEventListener("loadedmetadata", () => {
                        video.play();
                    });
                })
                .catch(alert);
        }
        else {
            flag--;
            cameraPart.style.background = ""
            cameraPart.style.boxShadow = ""
            mediaDevices.getUserMedia({ audio: true, video: true })
                .then(stream => {
                    window.localStream = stream;

                    // Stopping tracks and clearing video source.
                    stream.getTracks().forEach((track) => {
                        track.stop();
                    });
                    video.srcObject = null;
                })
                .catch((err) => {
                    console.log(err);
                });
                
        }
    });
});