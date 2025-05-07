const GAME_STATES = {
  LOBBY: 'lobby',
  PLAYING: 'playing',
};
let gameState = GAME_STATES.LOBBY;

window.onload = function() {
  document.getElementById('start-game').addEventListener('click', function() {
    fetch('/start_game', {
      method: 'POST',
    })
      .then(response => response.json())
      .then(data => {
        console.log('Game started successfully');
      })
      .catch(error => console.error('Error:', error));
  });
}

function startGame() {
  document.getElementById('lobby').style.display = 'none';
  document.getElementById('game').style.display = 'block'; // Show the game
  // Here you can redirect to the game page or update the UI
}

function getCurrentUser() {
  fetch('/current_user')
    .then(response => response.json())
    .then(data => {
      const playerName = document.getElementById('player-name');
      playerName.textContent = data.name;
    })
    .catch(error => console.error('Error fetching current user:', error));
}

function outputPlayersInLobby(data) {
  console.log(data);
  const lobbyPlayersEl = document.getElementById('lobby-players');
  lobbyPlayersEl.innerHTML = ''; // Clear the list before updating
  data.players.forEach(player => {
    const li = document.createElement('li');
    li.textContent = player;
    lobbyPlayersEl.appendChild(li);
  });
}


function processGameData(data) {
  document.getElementById('table').textContent = data.sticks;
  document.getElementById('current-player').textContent = data.current_player;
  const actionsEl = document.getElementById('actions');
  actionsEl.innerHTML = ''; // Clear previous actions
  data.actions.forEach(action => {
    button = document.createElement('button');
    button.className = "focus:outline-none text-white bg-gray-700 hover:bg-gray-800 focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-gray-600 dark:hover:bg-gray-700 dark:focus:ring-gray-800"
    button.textContent = action;
    button.addEventListener('click', function() {
      fetch('/action', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action: action }),
      })
        .then(response => response.json())
        .then(data => {
          console.log('Action sent successfully');
        })
        .catch(error => console.error('Error:', error));
    });
    actionsEl.appendChild(button);
  });
}


// ---- Start client ----
getCurrentUser();

setInterval(function() {
  fetch('/game_data')
    .then(response => response.json())
    .then(data => {
      if (gameState === GAME_STATES.LOBBY) {
        outputPlayersInLobby(data);
        if (data.state === GAME_STATES.PLAYING) {
          gameState = GAME_STATES.PLAYING;
          startGame();
        }
      }
      else if (gameState === GAME_STATES.PLAYING) {
        processGameData(data);
      }

    })
    .catch(error => console.error('Error fetching players:', error));
}, 1000);
