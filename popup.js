document.addEventListener('DOMContentLoaded', function () {
    let extractButton = document.getElementById('extractButton');
    
    extractButton.addEventListener('click', function () {
      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        let activeTab = tabs[0];
        chrome.tabs.sendMessage(activeTab.id, { action: 'extractSubreddit' });
      });
    });
  });
  