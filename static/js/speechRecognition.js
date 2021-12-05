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
    let micIcon = document.createElement('button');

    let ogplaceholder = "";

    micIcon.innerHTML = '<i class="bi bi-mic-fill"></i>';
    micIcon.style.cursor = 'pointer';
    micIcon.style.marginLeft = '-3px';
    micIcon.style.borderTopLeftRadius = "0px";
    micIcon.style.borderBottomLeftRadius = "0px";
    micIcon.classList.add('btn');
    micIcon.classList.add('btn-danger');
    micIcon.classList.add('mic');

    micIcon.addEventListener('click', function(event) {
      event.preventDefault();
      event.target.blur();
      if (microphone.isListening()) {
        // ending mic
        micIcon.classList.remove("active");
        inputElement.placeholder = ogplaceholder;
        microphone.end();
      } else {
        // starting mic
        _currentInput = inputElement;
        ogplaceholder = inputElement.placeholder;
        inputElement.placeholder = "Recording...";
        inputElement.value = "";
        micIcon.classList.add("active");
        microphone.start();
      }
    });

    para.appendChild(micIcon);
  });
}
  