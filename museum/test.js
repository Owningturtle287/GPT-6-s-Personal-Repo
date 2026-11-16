"use strict";
const assert = require("node:assert/strict");
const { makeMuseum, endingFor, responseFor, seededRandom } = require("./app.js");
let checked = 0;
for (let seed = 0; seed < 100; seed++) {
  const rooms = makeMuseum(seed);
  assert.equal(rooms.length, 3);
  assert.deepEqual(rooms, makeMuseum(seed), "same seed should reproduce the same rooms");
  assert.equal(new Set(rooms.map(e => e.name)).size, 3, "room names must be unique");
  assert.equal(new Set(rooms.map(e => e.origin)).size, 3, "origins must be unique");
  assert.equal(new Set(rooms.map(e => e.warning)).size, 3, "warnings must be unique");
  assert.equal(new Set(rooms.map(e => e.note)).size, 3, "notes must be unique");
  for (const room of rooms) {
    for (const action of ["watch", "touch", "ask"]) {
      assert.ok(responseFor(action, room).includes(room.name));
      checked++;
    }
  }
}
assert.equal(endingFor(["watch", "watch", "touch"]).title, "The Keeper of Small Details");
assert.equal(endingFor(["touch", "touch", "ask"]).title, "The Key Without a Lock");
assert.equal(endingFor(["ask", "watch", "ask"]).title, "The Question That Stayed");
assert.equal(endingFor(["watch", "touch", "ask"]).title, "The Unfinished Room");
const rng1 = seededRandom(42);
const rng2 = seededRandom(42);
for (let i = 0; i < 30; i++) assert.equal(rng1(), rng2());
console.log("Passed: 100 deterministic museum catalogs, " + checked + " scenes, 4 endings.");
