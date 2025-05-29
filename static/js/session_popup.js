// Check if the session has expired
if ({{ session_expired|yesno:"True,False" }}) {
  // Check if this is the first time accessing the login page
  if (window.sessionStorage.getItem('firstLogin') !== 'true') {
    // Open a pop-up window for login
    window.open('/login/', '_blank', 'width=400,height=300');
  } else {
    // Set the sessionStorage flag to indicate subsequent visits to the login page
    window.sessionStorage.setItem('firstLogin', 'false');
  }
}