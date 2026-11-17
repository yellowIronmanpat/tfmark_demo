"use strict";
// Behavioral checks without launching or controlling a browser.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const source = fs.readFileSync(path.join(__dirname, "../assets/js/player.js"), "utf8");

class AudioDouble {
  constructor(index) {
    this.dataset = { method: `Method ${index}`, sample: "01" };
    this.paused = true;
    this.ended = false;
    this.events = {};
    this.sourceEvents = {};
  }
  addEventListener(name, callback) { this.events[name] = callback; }
  querySelectorAll() { return [{ addEventListener: (name, callback) => { this.sourceEvents[name] = callback; } }]; }
  play() { this.paused = false; this.ended = false; this.events.play(); }
  pause() {
    if (!this.paused) { this.paused = true; this.events.pause(); }
  }
  finish() { this.paused = true; this.ended = true; this.events.ended(); }
}

function prepare(withStatus = true) {
  const players = Array.from({ length: 30 }, (_, i) => new AudioDouble(i));
  const status = withStatus ? { textContent: "" } : null;
  vm.runInNewContext(source, {
    document: { querySelectorAll: () => players, getElementById: () => status }
  });
  return { players, status };
}

const { players, status } = prepare();
for (const player of players) {
  player.play();
  assert.equal(players.filter(p => !p.paused).length, 1, "Only one sample may play");
  assert.ok(status.textContent.includes(player.dataset.method), "Announce the active sample");
}
players.at(-1).pause();
assert.equal(status.textContent, "Playback paused.");
players[0].play();
players[0].finish();
assert.equal(status.textContent, "Playback finished.");
players[1].events.error();
assert.ok(status.textContent.includes("Method 1"));
players[2].sourceEvents.error();
assert.ok(status.textContent.includes("Method 2") && status.textContent.includes("WAV link"));
const noStatus = prepare(false);
assert.doesNotThrow(() => { noStatus.players[0].play(); noStatus.players[1].play(); noStatus.players[1].sourceEvents.error(); });
console.log("PASS: 30-player exclusivity, pause/end announcements, audio/source failures, and missing-status resilience.");
