let token = null;

document.addEventListener('DOMContentLoaded', function() {  // The same as window.onload()
  const registrationForm = document.getElementById('login-form');
  registrationForm.addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the default form submission as we will handle it manually with JavaScript
    const formData = new FormData(registrationForm);  // Create a FormData object from the form - gather all the data from inputs
    fetch('/login', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        if (data.success) {
          alert('Login successful!');
          // token = data.token; // Store the token
        } else {
          alert('Login failed: ' + data.message);
        }
      })
      .catch(error => console.error('Error:', error));
  });
});

// Next requests - should include the token in the headers
// fetch(..., token