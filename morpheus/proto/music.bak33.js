/* =========================================================
   CASSETTE PLAYER: a desk item you can put anywhere (even on the glass),
   click = play / stop. Tapes are bought in Morpheus' shop.
   Each tape is a real music file: proto/music/<tape>.mp3 (or .ogg), looped.
   ========================================================= */
const TAPES = {
  jazz:  {col: '#c9a24a', dir: 'jazz', list: ['blue-light', 'jazz-loop', 'jazz-waltz', 'restaurant-cafe', 'cafe-mfcc', 'jazz-bar', 'aurec-jazz', 'smooth-jazz', 'cool-jazz', 'jazz-guitar', 'jazz-trio', 'french-jazz', 'cocktail-jazz', 'night-jazz', 'coffee-jazz', 'dinner-jazz', 'jazz-club', 'jazz-cafe', 'relaxing-jazz', 'vintage-jazz']},
  lofi:  {col: '#8aa0c8'},
  bossa: {col: '#d8805a'},
  box:   {col: '#e8b8d0'},
  synth: {col: '#c060d8'},
};
const MUS_T = {
  en: {empty: t => `The "${t}" tape is blank. Put a file at proto/music/${t}.mp3`},
  ru: {empty: t => `Кассета «${t}» пустая. Нужен файл proto/music/${t}.mp3`},
  ja: {empty: t => `カセット「${t}」はからっぽ。proto/music/${t}.mp3 を入れてね`},
};
let mus = null;                                          // {id, el} for one file, {id, mix} for a folder tape
const MIX_BUF = {};                                      // url -> loudness gain

/* a folder tape = an endless mix: random order (never the same track twice in a row), each loop repeated
   for ~1-2 minutes, 4 s fade-out, a short pause, the next one fades in. Loudness is evened out by RMS. */
async function mixLoad(url) {
  // decoded songs are big (~50 MB each), so only the loudness is remembered, not the audio
  const buf = await AC.decodeAudioData(await (await fetch(url)).arrayBuffer());
  if (!MIX_BUF[url]) {
    let sum = 0, n = 0; for (let c = 0; c < buf.numberOfChannels; c++) { const d = buf.getChannelData(c); for (let i = 0; i < d.length; i += 64) { sum += d[i] * d[i]; n++ } }
    MIX_BUF[url] = Math.min(2.5, .12 / (Math.sqrt(sum / n) || .1));
  }
  return {buf, gain: MIX_BUF[url]};
}
function mixStart(id) {
  const T = TAPES[id], bus = AC.createGain(); bus.gain.value = .9; bus.connect(musicOut);
  const mix = {bus, last: null, src: null, timer: 0, dead: false};
  const next = async () => {
    if (mix.dead) return;
    const pool = T.list.filter(n => n !== mix.last), name = pool[Math.floor(Math.random() * pool.length)]; mix.last = name;
    let tr; try { tr = await mixLoad(`music/${T.dir}/${name}.mp3`) } catch (e) { mix.timer = setTimeout(next, 500); return }
    if (mix.dead) return;
    const s = AC.createBufferSource(), g = AC.createGain(), t = AC.currentTime + .05, len = tr.buf.duration;
    const reps = Math.max(1, Math.round((70 + Math.random() * 50) / len)), dur = reps * len, fade = Math.min(4, len / 2);
    s.buffer = tr.buf; s.loop = true; s.connect(g).connect(bus);
    g.gain.setValueAtTime(.0001, t); g.gain.exponentialRampToValueAtTime(tr.gain, t + 1.5);
    g.gain.setValueAtTime(tr.gain, t + dur - fade); g.gain.exponentialRampToValueAtTime(.0001, t + dur);
    s.start(t); s.stop(t + dur + .1); mix.src = s;
    mix.timer = setTimeout(next, (dur + 1.5 + Math.random() * 2.5) * 1000);    // pause between tracks
  };
  next(); return mix;
}

function musicStop() {
  if (!mus) return;
  if (mus.mix) { const m = mus.mix; m.dead = true; clearTimeout(m.timer); m.bus.gain.setTargetAtTime(.0001, AC.currentTime, .15); setTimeout(() => { try { m.src?.stop() } catch (e) {} m.bus.disconnect() }, 900) }
  else mus.el.pause();
  mus = null; player?.rebuild();
}
function musicPlay(id) {
  initAudio(); musicStop();
  if (TAPES[id].list) { mus = {id, mix: mixStart(id)}; return }
  const el = new Audio(); el.loop = true;
  const tries = [`music/${id}.mp3`, `music/${id}.ogg`]; let k = 0;
  el.onerror = () => {
    if (++k < tries.length) { el.src = tries[k]; el.play().catch(() => {}); return }
    if (mus?.el === el) { mus = null; player?.rebuild(); think((MUS_T[LANG] || MUS_T.en).empty(id)) }
  };
  el.src = tries[0]; mus = {id, el}; applyVolumes(); el.play().catch(() => {});
}

/* ---------- the player itself ---------- */
let player = null;
function drawPlayer(c, it) {
  const R = (x, y, w, h, col) => { c.fillStyle = col; c.fillRect(x, y, w, h) };
  const on = !!mus, tape = TAPES[cos('tape')], ph = on ? Math.floor(performance.now() / 140) % 4 : 0;
  R(1, 3, 38, 22, '#313638'); R(0, 4, 40, 20, '#313638');                     // outline
  R(1, 4, 38, 20, '#2c3a4a'); R(1, 4, 38, 2, '#4a5e74'); R(1, 22, 38, 2, '#1e2834'); R(38, 5, 1, 18, '#1e2834');
  for (let i = 0; i < 4; i++) { const down = on && i === 1; R(5 + i * 6, down ? 2 : 1, 5, down ? 2 : 3, '#313638'); R(6 + i * 6, down ? 2 : 1, 3, down ? 1 : 2, i === 3 ? '#c0404a' : '#9aa6b2') }
  R(4, 7, 25, 13, '#14181e'); R(4, 7, 25, 1, '#0a0c10'); R(4, 19, 25, 1, '#3a4a5e');   // tape window
  R(6, 8, 21, 11, '#cfc6b0'); R(6, 8, 21, 3, tape.col); R(6, 11, 21, 1, '#8a8270');    // the cassette + its label colour
  R(9, 13, 15, 4, '#2a2420');
  for (const cx of [11, 22]) {                                                  // reels turn while playing
    R(cx - 1, 13, 3, 3, '#e8e4dc'); R(cx, 14, 1, 1, '#2a2420');
    const sp = [[0, -1], [1, 0], [0, 1], [-1, 0]][ph]; R(cx + sp[0], 14 + sp[1], 1, 1, '#6a6258');
  }
  for (let y = 8; y < 20; y += 2) for (let x = 31; x < 37; x += 2) R(x, y, 1, 1, '#1a222c');   // speaker grille
  R(32, 20, 2, 2, on ? '#5adc6a' : '#2a3a2a');
}
function playerInit() {
  const el = document.createElement('div'); el.className = 'item'; el.id = 'player';
  const blank = document.createElement('canvas'); blank.width = 40; blank.height = 26;
  el.innerHTML = `<img width="40" height="26" alt="" src="${blank.toDataURL()}">`;
  $('stage').insertBefore(el, $('shade'));
  let pos = {x: 104, y: 96};
  try { pos = JSON.parse(localStorage.getItem('morpheus.player') || 'null') || pos } catch (e) {}
  player = new Item(el, {x: pos.x, y: pos.y, w: 40, h: 26, tiltK: .6, minY: 0, noGlass: true, compose: drawPlayer,
    onClick: () => { if (mus) musicStop(); else musicPlay(cos('tape')); sfx.click(); player.rebuild() },
    onDrop: () => { try { localStorage.setItem('morpheus.player', JSON.stringify({x: Math.round(player.tx), y: Math.round(player.ty)})) } catch (e) {} }});
  setInterval(() => { if (mus && player) player.rebuild() }, 140);           // spin the reels
  deskShow();
}
function deskShow() {                                                         // shop: what stands on the desk
  mug.el.style.display = cos('mugOn') === 'no' ? 'none' : '';
  const cnd = cos('lamp') === 'candle';
  lamp.el.style.display = cnd ? 'none' : ''; candle.el.style.display = cnd ? '' : 'none';
  if (player) { const show = cos('player') !== 'no'; player.el.style.display = show ? '' : 'none'; if (!show) musicStop() }
}
