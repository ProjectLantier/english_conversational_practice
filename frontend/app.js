/**
 * app.js
 * 
 * Handles frontend logic for the English Conversational Practice Application.
 * - Starts/stops audio recording
 * - Sends audio for speech recognition
 * - Processes input and displays system response, grammar/phoneme feedback
 * - Plays TTS audio for responses, except final summaries
 * - Allows user to hear phoneme examples from /get_phoneme_audio endpoint
 */

let mediaRecorder;
let audioChunks = [];
let currentAudio = null;
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const systemResponseEl = document.getElementById('system-response');
const feedbackEl = document.getElementById('feedback');
const userTranscriptEl = document.getElementById('user-transcript');
const loadingEl = document.getElementById('loading'); // Loading indicator element

/**
 * Shows the loading spinner.
 */
function showLoading() {
  loadingEl.style.display = 'block';
}

/**
 * Hides the loading spinner.
 */
function hideLoading() {
  loadingEl.style.display = 'none';
}

async function startRecording() {
  if (currentAudio && !currentAudio.paused) {
    currentAudio.pause();
    currentAudio.currentTime = 0;
  }

  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  audioChunks = [];

  mediaRecorder.ondataavailable = event => {
    audioChunks.push(event.data);
  };

  mediaRecorder.onstop = async () => {
    showLoading(); // Show processing spinner

    try {
      const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
      const formData = new FormData();
      formData.append('audio', audioBlob, 'user_audio.webm');

      // Send audio for speech recognition
      const recognitionRes = await fetch('/recognize_speech', {
        method: 'POST',
        body: formData
      });
      const recognitionData = await recognitionRes.json();
      const userText = recognitionData.transcription;
      userTranscriptEl.textContent = userText;

      // Process input and get response
      const processRes = await fetch('/process_input', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: userText })
      });
      const processData = await processRes.json();
      
      const isSummary = processData.is_summary;

      if (isSummary) {
        // Final summary should go in feedback, not in system response
        feedbackEl.innerHTML = processData.response;
        systemResponseEl.innerHTML = ""; // Clear system response since final summary goes to feedback

        // Do NOT call TTS for summary
      } else {
        // Normal response flow:
        systemResponseEl.innerHTML = processData.response;

        let feedbackHTML = "";
        if (processData.grammar_errors && processData.grammar_errors.length > 0) {
          feedbackHTML += "<h3>Grammar Issues:</h3>";
          processData.grammar_errors.forEach(e => {
            feedbackHTML += `<p>In "${e.original_sentence}", "${e.error_word}" should be "${e.suggestion}". ${e.explanation}</p>`;
          });
        } else {
          feedbackHTML += "<p>No significant grammar issues.</p>";
        }

        if (processData.pronunciation_errors && processData.pronunciation_errors.length > 0) {
          feedbackHTML += "<h3>Pronunciation Issues:</h3>";
          processData.pronunciation_errors.forEach(err => {
            const userPh = err.user_phonemes.join(" ");
            const correctPh = err.correct_phonemes.join(" ");
            const userIpa = err.user_ipa.join(" ");
            const correctIpa = err.correct_ipa.join(" ");

            let mismatchIndex = -1;
            for (let i = 0; i < Math.min(err.user_phonemes.length, err.correct_phonemes.length); i++) {
              if (err.user_phonemes[i] !== err.correct_phonemes[i]) {
                mismatchIndex = i;
                break;
              }
            }

            let correctPhHTML = "";
            for (let i = 0; i < err.correct_phonemes.length; i++) {
              let ph = err.correct_phonemes[i];
              if (i === mismatchIndex) {
                correctPhHTML += `<span style="color:red;">${ph}</span> <button class="btn btn-sm btn-info" onclick="playPhoneme('${ph}')">Hear</button> `;
              } else {
                correctPhHTML += ph + " ";
              }
            }

            // Also show IPA with highlight:
            let correctIpaHTML = "";
            for (let i = 0; i < err.correct_ipa.length; i++) {
              let ph = err.correct_ipa[i];
              if (i === mismatchIndex) {
                correctIpaHTML += `<span style="color:red;">${ph}</span> `;
              } else {
                correctIpaHTML += ph + " ";
              }
            }

            feedbackHTML += `
              <p>
              Word: '${err.word}' mispronounced.<br>
              You said (ARPAbet): [${userPh}]<br>
              You said (IPA): [${userIpa}]<br>
              Try (ARPAbet): [${correctPhHTML}]<br>
              Try (IPA): [${correctIpaHTML}]<br>
              ${err.difference_note}
              </p>
            `;
          });
          if (processData.pronunciation_suggestions && processData.pronunciation_suggestions.length > 0) {
            feedbackHTML += "<p>Suggestions:<br>" + processData.pronunciation_suggestions.join("<br>") + "</p>";
          }
        } else {
          feedbackHTML += "<p>No significant pronunciation issues.</p>";
        }

        feedbackEl.innerHTML = feedbackHTML;

        // Proceed with TTS
        console.log("Response before TTS:", processData.response);
        const audioRes = await fetch('/get_audio_response', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ response_text: processData.response })
        });
        const audioData = await audioRes.json();
        const audioUrl = audioData.audio_url;

        if (currentAudio && !currentAudio.paused) {
          currentAudio.pause();
          currentAudio.currentTime = 0;
        }
        currentAudio = new Audio(audioUrl);
        currentAudio.play();
      }
    } catch (error) {
      console.error("Error during processing:", error);
      // Optionally, display an error message to the user
      feedbackEl.innerHTML = "<p class='text-danger'>An error occurred while processing your input. Please try again.</p>";
    } finally {
      hideLoading(); // Hide processing spinner
    }
  };

  mediaRecorder.start();
  startBtn.disabled = true;
  stopBtn.disabled = false;
}

function stopRecording() {
  mediaRecorder.stop();
  startBtn.disabled = false;
  stopBtn.disabled = true;
}

async function playPhoneme(phoneme) {
  try {
    const res = await fetch('/get_phoneme_audio', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({phoneme: phoneme})
    });
    const data = await res.json();
    const audioUrl = data.audio_url;
    const audio = new Audio(audioUrl);
    audio.play();
  } catch (error) {
    console.error("Error playing phoneme audio:", error);
  }
}

startBtn.addEventListener('click', startRecording);
stopBtn.addEventListener('click', stopRecording);