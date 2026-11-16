/* Browser adaptation of Experiments 007–008.
   Seeded randomness here is implemented in JavaScript, so a numeric seed
   generates a stable web catalog but need not match Python's random.Random.
   No backend, analytics, storage, or external requests.
*/
"use strict";

const OBJECTS = [
  ["The Weatherless Umbrella", "When opened, it shelters its holder from a memory that has not happened yet.", "☂"],
  ["The Compass of Almost", "Its needle points toward the road its owner nearly took.", "⌁"],
  ["The Unsent Letterbox", "Every morning it receives one letter that its sender was too afraid to write.", "✉"],
  ["The Borrowed Mirror", "It reflects the face of the last person who truly listened to you.", "◇"],
  ["The Quiet Lighthouse", "Its lamp illuminates things people forgot to say.", "✧"],
  ["The Tuesday Telescope", "It shows constellations that will not exist until someone names them.", "✶"],
  ["The Apology Engine", "It converts explanations into the words their speakers meant to say.", "⚙"],
  ["The Pocket Door", "It opens only onto rooms someone has dreamed of but never entered.", "▣"],
  ["The Hourglass of Detours", "Its sand falls upward whenever someone changes their mind.", "⌛"],
  ["The Map of Missing Streets", "It contains every shortcut that disappeared when a city grew up.", "⌖"],
  ["The Forgetful Teacup", "It leaves the taste of a conversation rather than the taste of tea.", "♨"],
  ["The Second-Chance Camera", "It photographs the moment immediately before a person decides to be kind.", "◈"]
];

const ORIGINS = [
  "Recovered from an attic whose house had been demolished seventy years earlier.",
  "Donated anonymously, wrapped in a newspaper dated next Thursday.",
  "Found beside a railway platform that appears on no timetable.",
  "Unearthed beneath the foundation of a library with no books.",
  "Delivered in a crate marked FRAGILE: POSSIBILITY.",
  "Discovered at the bottom of a well that had never contained water.",
  "Traded for a story by a traveler who would not give a name.",
  "Found on the last shelf of a shop that closed before it opened.",
  "Recovered after a storm in which nothing became wet.",
  "Left at the reception desk with an unsigned thank-you note.",
  "Retrieved from a garden where the shadows pointed north.",
  "Donated by the museum's first visitor, who has not arrived yet."
];

const WARNINGS = [
  "Please do not ask it to prove that it works.",
  "Handle gently; it has already survived one ending.",
  "Do not compare your experience with another visitor's.",
  "If it changes while you are watching, notify the night curator.",
  "Keep your ticket. You may need it to find the exit.",
  "Photography is permitted, but captions are discouraged.",
  "No refunds are given for recovered possibilities.",
  "Please leave unfinished questions in the tray by the door.",
  "Do not attempt to repair what might not be broken.",
  "If you recognize it, please do not say from where.",
  "Visitors are asked not to make promises in this gallery.",
  "The museum accepts no responsibility for sudden nostalgia."
];

const OBSERVATIONS = [
  "One visitor stood here for an hour, then left smiling without explanation.",
  "The curator's notes end in the middle of a sentence.",
  "A child asked whether it could be borrowed. Nobody answered immediately.",
  "It has never been stolen, although the case is often found unlocked.",
  "The dust beneath it is older than the object itself.",
  "Its catalog number changes whenever the museum is empty.",
  "Visitors often return to this room without remembering why.",
  "The night guard reports hearing applause from an empty gallery.",
  "The object weighs exactly as much as a handwritten apology.",
  "The exhibit log contains three entries in the same handwriting, centuries apart.",
  "A replacement was commissioned once. The replacement arrived first.",
  "The museum insists this was its very first acquisition. So do eleven other objects."
];

const ENDINGS = {
  watch: {
    title: "The Keeper of Small Details",
    passage: "You leave with a catalog of things nobody thought to label. On its final page: the sound of your footsteps as you went home."
  },
  touch: {
    title: "The Key Without a Lock",
    passage: "Your ticket unfolds into a brass key. No door in the museum fits it. The curator says that is what makes it yours."
  },
  ask: {
    title: "The Question That Stayed",
    passage: "At the exit, the sign has become a question mark. You step into the night carrying a question that has grown larger, not smaller."
  },
  mixed: {
    title: "The Unfinished Room",
    passage: "The museum cannot decide whether you came to observe, alter, or understand. It leaves one room unfinished, with a lamp on and a visitor's chair waiting."
  }
};

function seededRandom(seed) {
  let a = seed >>> 0;
  return function () {
    a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t ^= t + Math.imul(t ^ (t >>> 7), 61 | t);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffledSample(values, n, rng) {
  const items = values.slice();
  for (let i = items.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [items[i], items[j]] = [items[j], items[i]];
  }
  return items.slice(0, n);
}

function makeMuseum(seed) {
  const rng = seededRandom(seed);
  const objects = shuffledSample(OBJECTS, 3, rng);
  const origins = shuffledSample(ORIGINS, 3, rng);
  const warnings = shuffledSample(WARNINGS, 3, rng);
  const notes = shuffledSample(OBSERVATIONS, 3, rng);
  return objects.map((obj, i) => ({
    name: obj[0],
    behavior: obj[1],
    symbol: obj[2],
    origin: origins[i],
    warning: warnings[i],
    note: notes[i]
  }));
}

function endingFor(choices) {
  const majority = ["watch", "touch", "ask"].find(kind => choices.filter(x => x === kind).length >= 2);
  return ENDINGS[majority || "mixed"];
}

function responseFor(action, exhibit) {
  if (action === "watch") {
    return "You linger before " + exhibit.name + ". Its label reads: " + exhibit.behavior + " The gallery clock waits for you to finish looking.";
  }
  if (action === "touch") {
    return "You rest a hand on the glass enclosing " + exhibit.name + ". Your paper admission ticket acquires a tiny silver notch. The curator pretends not to notice.";
  }
  if (action === "ask") {
    return "You ask " + exhibit.name + " what it has been waiting for. A new line appears beneath its catalog number: " + exhibit.note;
  }
  throw new Error("Unknown action: " + action);
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { makeMuseum, endingFor, responseFor, seededRandom };
}

if (typeof document !== "undefined") {
  const get = id => document.getElementById(id);
  const mainSections = ["welcome", "journey", "finale"];
  let seed = readSeed();
  let exhibits = [];
  let choices = [];
  let roomIndex = 0;
  let responded = false;

  function readSeed() {
    const params = new URLSearchParams(location.search);
    const fromUrl = params.get("seed");
    const n = Number(fromUrl);
    return fromUrl !== null && Number.isSafeInteger(n) && n >= 0 && n <= 4294967295 ? n : 6;
  }

  function updateLocation() {
    const url = new URL(location.href);
    url.searchParams.set("seed", String(seed));
    history.replaceState(null, "", url.toString());
  }

  function showSection(id) {
    for (const name of mainSections) get(name).hidden = name !== id;
    const top = get("main");
    if (top) top.scrollIntoView({ block: "start", behavior: "instant" });
  }

  function focusExhibit() {
    const title = get("exhibit-name");
    title.tabIndex = -1;
    title.focus({ preventScroll: true });
  }

  function begin(newSeed) {
    seed = newSeed >>> 0;
    exhibits = makeMuseum(seed);
    choices = [];
    roomIndex = 0;
    responded = false;
    updateLocation();
    get("seed-label").textContent = "CATALOG #" + String(seed).padStart(6, "0");
    showSection("journey");
    renderRoom();
  }

  function renderProgress() {
    const list = get("room-progress");
    list.replaceChildren();
    for (let i = 0; i < exhibits.length; i++) {
      const item = document.createElement("li");
      item.className = i < choices.length ? "done" : i === roomIndex ? "current" : "";
      item.textContent = "Room " + String(i + 1).padStart(2, "0") + (i < choices.length ? " — " + choices[i].toUpperCase() : "");
      list.appendChild(item);
    }
  }

  function renderRoom() {
    if (roomIndex >= exhibits.length) {
      showEnding();
      return;
    }
    responded = false;
    const e = exhibits[roomIndex];
    get("room-number").textContent = "ROOM " + String(roomIndex + 1).padStart(2, "0") + " / 03";
    get("exhibit-name").textContent = e.name;
    get("exhibit-behavior").textContent = e.behavior;
    get("exhibit-origin").textContent = e.origin;
    get("exhibit-symbol").textContent = e.symbol;
    get("choice-area").hidden = false;
    get("result-area").hidden = true;
    get("next-room").innerHTML = roomIndex === 2 ? "See your ending <span aria-hidden='true'>→</span>" : "Continue the tour <span aria-hidden='true'>→</span>";
    renderProgress();
    focusExhibit();
  }

  function choose(action) {
    if (responded || !["watch", "touch", "ask"].includes(action)) return;
    responded = true;
    choices.push(action);
    const e = exhibits[roomIndex];
    get("result-text").textContent = responseFor(action, e);
    get("curator-footnote").textContent = "Curator's notice: " + e.warning;
    get("choice-area").hidden = true;
    get("result-area").hidden = false;
    renderProgress();
    get("next-room").focus({ preventScroll: true });
  }

  function nextRoom() {
    if (!responded) return;
    roomIndex++;
    renderRoom();
  }

  function showEnding() {
    const ending = endingFor(choices);
    get("ending-title").textContent = ending.title;
    get("ending-passage").textContent = ending.passage;
    const wrap = get("tour-choices");
    wrap.replaceChildren();
    for (let i = 0; i < choices.length; i++) {
      const item = document.createElement("span");
      item.textContent = "Room " + (i + 1) + " · " + choices[i][0].toUpperCase() + choices[i].slice(1);
      wrap.appendChild(item);
    }
    showSection("finale");
    get("ending-title").tabIndex = -1;
    get("ending-title").focus({ preventScroll: true });
  }

  function randomSeed() {
    if (typeof crypto !== "undefined" && crypto.getRandomValues) {
      return crypto.getRandomValues(new Uint32Array(1))[0];
    }
    return (Math.random() * 4294967296) >>> 0;
  }

  async function copyLink() {
    const url = new URL(location.href);
    url.searchParams.set("seed", String(seed));
    const button = get("share");
    try {
      await navigator.clipboard.writeText(url.toString());
      button.textContent = "Link copied ✓";
      setTimeout(() => { button.textContent = "Copy museum link ⧉"; }, 2200);
    } catch (_) {
      window.prompt("Copy this museum link:", url.toString());
    }
  }

  get("enter").addEventListener("click", () => begin(seed));
  get("restart").addEventListener("click", () => begin(seed));
  get("again").addEventListener("click", () => begin(randomSeed()));
  get("same-night").addEventListener("click", () => begin(seed));
  get("share").addEventListener("click", copyLink);
  get("next-room").addEventListener("click", nextRoom);
  document.querySelectorAll("[data-action]").forEach(button => {
    button.addEventListener("click", () => choose(button.dataset.action));
  });
}
