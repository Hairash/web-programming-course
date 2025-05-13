const GAME_STATES = {
  LOBBY: 'lobby',
  PLAYING: 'playing',
};
let gameState = GAME_STATES.LOBBY;

window.onload = function () {
  document.getElementById('start-game').addEventListener('click', function () {
    socket.emit('start_game');  // Send message to server to start the game
  });
}

function startGame(data) {
  document.getElementById('lobby').style.display = 'none';
  document.getElementById('game').style.display = 'block'; // Show the game
  const actionsEl = document.getElementById('actions');
  data.actions.forEach(action => {
    button = document.createElement('button');
    button.className = "focus:outline-none text-white bg-gray-700 hover:bg-gray-800 focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-gray-600 dark:hover:bg-gray-700 dark:focus:ring-gray-800"
    button.textContent = action;
    button.addEventListener('click', function () {
      socket.emit('action', action);  // Send action to server
    });
    actionsEl.appendChild(button);
  });
}

function outputPlayersInLobby(data) {
  console.log(data);
  const lobbyPlayersEl = document.getElementById('lobby-players');
  lobbyPlayersEl.innerHTML = ''; // Clear the list before updating
  data.forEach(player => {
    const li = document.createElement('li');
    li.textContent = player;
    lobbyPlayersEl.appendChild(li);
  });
}

function processGameState(data) {
  document.getElementById('table').textContent = data.sticks;
  document.getElementById('current-player').textContent = data.current_player;
  // TODO: Process the game state
}


// ---- Start client ----
const socket = io();  // Initialize WebSocket connection

// Event listeners for socket events - these are the events that the server will emit, and here we handle them
socket.on('players', (data) => {
  console.log('Players:', data);
  outputPlayersInLobby(data);
});

socket.on('current_user', (data) => {
  console.log('Current user:', data);
  document.getElementById('player-name').textContent = data;
})

socket.on('game_started', (data) => {
  console.log('Game started:', data);
  gameState = GAME_STATES.PLAYING;
  startGame(data);
});

socket.on('game_state', (data) => {
  console.log('Game state:', data);
  processGameState(data);
});
