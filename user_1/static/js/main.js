// Add JavaScript for form validation and submission
const form = document.querySelector('form');
form.addEventListener('submit', (event) => {
  event.preventDefault();
  const username = document.querySelector('#username').value;
  const password = document.querySelector('#password').value;
  if (username === '' || password === '') {
    alert('Please enter a username and password');
  } else {
    // Submit the form
    form.submit();
  }
});
// Script for modified alert box 
function geeks(msg, gfg) {
  var confirmBox = $("#containerr");
   
  /* Trace message to display */
  confirmBox.find(".message").text(msg);
   
  /* Calling function */
  confirmBox.find(".yes").unbind().click(function()
  {
  confirmBox.hide();
  });
  confirmBox.find(".yes").click(gfg);
  confirmBox.show();
}