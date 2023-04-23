
//API KEY AIzaSyCfn97T5S11xfMZbr8Bl0nvk5n0FCg50mA
chrome.storage.local.set({ transcript: "" });


const videoElement = document.querySelector("video");

if (!videoElement) {
  alert("Please open a video and try again.");
} else {
  const stream = videoElement.captureStream();
  const audioTrack = stream.getAudioTracks()[0];

  if (!audioTrack) {
    alert("The video does not have an audio track.");
  } else {
    const audioContext = new AudioContext();
    const mixed = mix(audioContext, [new MediaStream([audioTrack])]);
    const recorder = new MediaRecorder(mixed, { mimeType: "audio/webm" });

    const recordedChunks = [];

    const mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm" });
    mediaRecorder.addEventListener("dataavailable", (event) => {
      if (typeof event.data === "undefined") return;

      if (event.data.size > 0) {
        recordedChunks.push(event.data);
      }
    });

    mediaRecorder.addEventListener("stop", async () => {
      const blob = new Blob(recordedChunks, { type: "audio/webm" });

      const formData = new FormData();
      formData.append("audioFile", blob);

      const response = await fetch(
        "https://speech.googleapis.com/v1/speech:recognize?key=AIzaSyCfn97T5S11xfMZbr8Bl0nvk5n0FCg50mA",
        {
          method: "POST",
          body: formData,
        }
      );
      const data = await response.json();

      const transcription = data.results
        .map((result) => result.alternatives[0].transcript)
        .join("\n");
      console.log(transcription);
    });

    mediaRecorder.start();

    socket = new WebSocket("wss://api.deepgram.com/v1/listen?tier=enhanced", [
      "token",
      "147ffa5b29c089bbdddd8c4155b099020ec3b3fb",
    ]);

    recorder.addEventListener("dataavailable", (evt) => {
      if (evt.data.size > 0 && socket.readyState == 1) socket.send(evt.data);
    });

    socket.onopen = () => {
      recorder.start(250);
    };
    socket.onmessage = (msg) => {
      const { transcript } = JSON.parse(msg.data).channel.alternatives[0];
      if (transcript) {
        console.log(transcript);
        chrome.storage.local.get("transcript", (data) => {
          chrome.storage.local.set({
            transcript: (data.transcript += " " + transcript),
          });

          // Throws error when popup is closed, so this swallows the errors with catch.
          chrome.runtime
            .sendMessage({
              message: "transcriptavailable",
            })
            .catch((err) => ({}));
        });
      }
    };
  }
}

function mix(audioContext, streams) {
  const dest = audioContext.createMediaStreamDestination();
  streams.forEach((stream) => {
    const source = audioContext.createMediaStreamSource(stream);
    source.connect(dest);
  });
  return dest.stream;
}
