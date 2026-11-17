"use strict";

// Keep all audio controls usable without JavaScript; enhance comparison only.
const players = [...document.querySelectorAll("audio")];
const status = document.getElementById("playback-status");
for (const player of players) {
  player.addEventListener("play", () => {
    for (const other of players) {
      if (other !== player) other.pause();
    }
    status.textContent = `Playing: ${player.dataset.method} · sample ${player.dataset.sample}`;
  });
  player.addEventListener("ended", () => {
    if (players.every(other => other.paused)) status.textContent = "Playback finished.";
  });
  player.addEventListener("pause", () => {
    if (!player.ended && players.every(other => other.paused)) status.textContent = "Playback paused.";
  });
  player.addEventListener("error", () => {
    status.textContent = "This audio could not be loaded. Please reload the page or try another browser.";
  });
}
