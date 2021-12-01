let speech = new SpeechSynthesisUtterance();
const synth = window.speechSynthesis;
const say = (text) => {
  synth.cancel();
  speech.lang = "en";
  speech.text = text;
  synth.speak(speech);
}

document.querySelectorAll('.speak').forEach(para => {
    let speaker = document.createElement('span');
    const text = para.textContent;
    speaker.classList = ['speaker'];
    speaker.style.cursor = "pointer";
    speaker.innerHTML = '&#128264';
    speaker.addEventListener('click', () => say(text));
    para.appendChild(speaker);
});

window.onbeforeunload = () => synth.cancel();