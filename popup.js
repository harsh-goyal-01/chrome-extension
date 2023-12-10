document.addEventListener('DOMContentLoaded', function () {
    let extractButton = document.getElementById('extractButton');

    let upvoted = -1;
    
    const handleVote = (action) => {
      console.log('clicked');
      const thumbsUp = document.querySelector('.thumbs-up');
      const thumbsDown = document.querySelector('.thumbs-down');

      if (action === 'up') {
        thumbsUp.classList.add('clicked');
        thumbsDown.classList.remove('clicked');
        console.log('User voted thumbs up');
        upvoted = 1;
      } else {
        thumbsDown.classList.add('clicked');
        thumbsUp.classList.remove('clicked');
        console.log('User voted thumbs down');
        upvoted = 0;
      }
    }

    extractButton.addEventListener('click', function () {
      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        let activeTab = tabs[0];
        chrome.tabs.sendMessage(activeTab.id, { action: 'extractSubreddit' });
      });
    });

    let upButton = document.getElementById("up-button");

    upButton.addEventListener("click", function () {
      handleVote("up");
    });

    let downButton = document.getElementById("down-button");

    downButton.addEventListener("click", function () {
      handleVote("down");
    });

  });
  