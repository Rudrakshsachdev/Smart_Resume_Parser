// This script handles the dynamic behaviour of the web page, including the score bar animation, mobile menu toggle, theme toggle, and file upload interactions.

document.addEventListener("DOMContentLoaded", () => { 
  const scoreBar = document.getElementById("scoreBar"); // getting the score bar element by its ID

  if (scoreBar) { // checking if the score bar element exists
    const score = parseInt(scoreBar.getAttribute("data-score")) || 0; // parsing the score from the data attribute, defaulting to 0 if not found 

    let barColor;
    if (score >= 80) { 
      barColor = 'var(--secondary-dark)';
    } else if (score >= 50) {
      barColor = '#f59e0b';
    } else {
      barColor = '#ef4444';
    }

    // this timeout is used to ensure the score bar width and color 
    setTimeout(() => {
      scoreBar.style.width = score + "%";
      scoreBar.style.backgroundColor = barColor;
    }, 200); // after a delay of 200 milliseconds

    let current = 0; // initializing the current score to 0
    const interval = setInterval(() => { // setting an interval to update the score bar text
      if (current <= score) { 
        scoreBar.innerText = current + "%";
        current++;
      } else {
        clearInterval(interval);
      }
    }, 20); // updating the score bar text every 20 milliseconds
  }
});

// mobile menu toggle functionality and this part of the code handles the mobile menu toggle and theme toggle functionality
document.getElementById('mobileMenuBtn').addEventListener('click', function () { 
  document.getElementById('mobileMenu').classList.toggle('active'); 
  this.classList.toggle('active');
});

// theme toggle functionality and this part of the code handles the theme toggle functionality
document.getElementById('themeToggle').addEventListener('click', function () {
  document.body.classList.toggle('dark-theme'); // toggling the dark theme class on the body element
  const icon = this.querySelector('i');
  if (document.body.classList.contains('dark-theme')) {
    icon.classList.replace('fa-moon', 'fa-sun'); // changing the icon to the sun when dark theme is active
  } else {
    icon.classList.replace('fa-sun', 'fa-moon'); // changing the icon to the moon when dark theme is inactive
  }
});

// File upload functionality and this part of the code handles the file upload functionality
document.getElementById('resumeUpload').addEventListener('change', function (e) {
  const fileInput = e.target; // getting the file input element
  const fileNameDisplay = document.getElementById('fileName'); // getting the file name display element
  const fileSelectionBox = document.getElementById('fileSelected'); // getting the file selection box element

  if (fileInput.files.length > 0) { 
    fileNameDisplay.textContent = fileInput.files[0].name;
    fileSelectionBox.style.display = 'flex';
  } else {
    fileSelectionBox.style.display = 'none';
  }
});

const fileUploadBox = document.querySelector('.file-upload-box'); // getting the file upload box element
const fileUploadLabel = document.querySelector('.file-upload-label'); // getting the file upload label element

// adding event listeners for drag and drop events to highlight the file upload box
['dragenter', 'dragover'].forEach(eventName => { 
  fileUploadLabel.addEventListener(eventName, highlight, false); // highlighting the box on drag enter and drag over events
});

// adding event listeners for drag leave and drop events to unhighlight the file upload box
['dragleave', 'drop'].forEach(eventName => {
  fileUploadLabel.addEventListener(eventName, unhighlight, false); // unhighlighting the box on drag leave and drop events
});

// this function highlights the file upload box when a file is dragged over it
function highlight(e) {
  e.preventDefault(); // preventing the default behavior of the event
  e.stopPropagation(); // stopping the propagation of the event
  fileUploadBox.classList.add('highlight'); 
}

// this function unhighlights the file upload box when a file is dragged out of it or dropped
function unhighlight(e) {
  e.preventDefault();
  e.stopPropagation();
  fileUploadBox.classList.remove('highlight');
}


// this part of the code handles the OTP verification functionality
document.getElementById('otp-form').addEventListener('submit', function(e) {
  e.preventDefault(); // preventing the page reload

  const otpInput = document.querySelector('input[name="otp"]'); //getting the Otp input element

  if(otpInput.value.length === 6) {
    alert('OTP verified successfully!'); 
  } else {
    alert('Please enter a valid 6-digit OTP.');
  }
});


// this part of the code handles the chat functionality
function toggleChat() {
  const win = document.getElementById('chat-window'); // getting the chat window element
  win.style.display = win.style.display === 'none' ? 'block' : 'none'; //toggling the display of the chat window
}

// this function sends the message to the server and updates the chat log with the response
function sendMessage() {
  const input = document.getElementById('chat-input'); // getting the chat input element
  const log = document.getElementById('chat-log'); // getting the chat log element

  const message = input.value; // getting the message from the input field

  log.innerHTML += `<div <b>You:</b> ${message}</div>`; // appending the message to the chat log
  input.value = ''; // clearing the input field

  // fetching the response from the server
  fetch('/chatbot/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken') // getting the csrf token
    },
    body: JSON.stringify({message: message}), // sending the message as a json object
  })
  .then(response => response.json()) // parsing the response as json
  .then(data => {
    log.innerHTML += `<div><b>Bot:</b> ${data.response}</div>`; // appending the bot's response to the chat log
    log.scrollTop = log.scrollHeight; // scrolling to the bottom of the chat log
  })
  .catch(error => {
    log.innerHTML += `<div><b>Error:</b> ${error.message}</div>`; // appending the error message to the chat log
    console.log('Error:', error); // logging the error to the console
  })
}

// this function retrieves the CSRF token from the cookies
function getCookie(name) {
  let cookieValue = null; // retrieving the cookie value

  // checking if the cookie exists and is not empty
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';'); // splitting the cookies by semicolon

    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim(); // trimming the cookie string

      // checking that if the cookie starts with the name followed by an equal sign
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1)); // decoding the cookie value
        break; // breaking the loop if the cookie is found
      }
    }
  }
  return cookieValue; // returning the cookie value
}