"use strict";

// Keep all audio controls usable without JavaScript; enhance comparison only.
const players = [...document.querySelectorAll("audio")];
const status = document.getElementById("playback-status");
const announce = (message) => { if (status) status.textContent = message; };
for (const player of players) {
  player.addEventListener("play", () => {
    for (const other of players) {
      if (other !== player) other.pause();
    }
    announce(`Playing: ${player.dataset.method} · sample ${player.dataset.sample}`);
  });
  player.addEventListener("ended", () => {
    if (players.every(other => other.paused)) announce("Playback finished.");
  });
  player.addEventListener("pause", () => {
    if (!player.ended && players.every(other => other.paused)) announce("Playback paused.");
  });
  const reportError = () => announce(`Could not load ${player.dataset.method} · sample ${player.dataset.sample}. Try the WAV link below the player or reload the page.`);
  player.addEventListener("error", reportError);
  // A failed <source> request can emit its own non-bubbling error event.
  for (const source of player.querySelectorAll("source")) {
    source.addEventListener("error", reportError);
  }
}
