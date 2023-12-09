chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.action === 'extractSubreddit') {
      let subredditName = window.location.pathname.split('/')[2];
      sendToServer(subredditName);
    }
  });
  
  function sendToServer(subredditName) {
    // Replace the URL below with your backend server URL
    // console.log(subredditName);
    let backendUrl ="http://127.0.0.1:8000/text"; 
    
    // // Make a POST request to the backend server
    fetch(backendUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ subreddit: subredditName }),
    })
      .then(response => response.json())
      .then(data => {
        alert('Server Response: ' + JSON.stringify(data));
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Error connecting to the server.');
      });
  }
  