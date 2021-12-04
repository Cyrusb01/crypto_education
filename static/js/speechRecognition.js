let microphones = []
let _currentInput;

if ("webkitSpeechRecognition" in window) {

  // define speech recognition
  let speechRecognition = new webkitSpeechRecognition();
  speechRecognition.continuous = true;
  speechRecognition.interimResults = true;
  speechRecognition.lang = "en";

  // Microphone factory function
  let Microphone = () => {
    let _transcript = "";
    let _listening = false;

    speechRecognition.onresult = (event) => {
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) { 
          const words = (event.results[i][0].transcript).toUpperCase();
          _transcript += words;
          _currentInput.value = _transcript;
        }
      }
    };

    function start() {
      speechRecognition.start();
      _listening = true; 
    }

    function end() {
      if (_listening) {
        speechRecognition.stop(); 
      }
      _transcript = "";
      _listening = false;
    }

    function isListening() {
      return _listening;
    }

    return {start, end, isListening};
  };

  // add mic icons to text elements
  const inputParas = document.querySelectorAll('.listen');
  let microphone = Microphone();

  inputParas.forEach(para => {
    let inputElement = para.querySelector('input');
    let micIcon = document.createElement('span');

    micIcon.innerHTML = '<i class="bi bi-mic-fill"></i>';
    micIcon.style.cursor = 'pointer';
    micIcon.style.opacity = '30%';
    micIcon.style.userSelect = 'none';
    micIcon.classList = ['mic'];

    micIcon.addEventListener('click', () => {
      if (microphone.isListening()) {
        // ending mic
        micIcon.style.opacity = '30%';
        microphone.end();
      } else {
        // starting mic
        _currentInput = inputElement;
        inputElement.value = "";
        micIcon.style.opacity = '100%';
        microphone.start();
      }
    });

    para.appendChild(micIcon);
  });
  
}