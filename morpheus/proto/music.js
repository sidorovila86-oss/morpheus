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
  en: {empty: t => `The "${t}" tape is blank. Put a file at proto/music/${t}.mp3`, hint: 'A cassette player. Click it to play or stop the music. More tapes in the shop.'},
  ru: {empty: t => `Кассета «${t}» пустая. Нужен файл proto/music/${t}.mp3`, hint: 'Кассетный плеер. Щёлкни — заиграет музыка, ещё раз — стоп. Другие кассеты в лавке.'},
  ja: {empty: t => `カセット「${t}」はからっぽ。proto/music/${t}.mp3 を入れてね`, hint: 'カセットプレーヤー。クリックで音楽をかける／とめる。ほかのカセットは店で。'},
};
let mus = null;
// every night (every page load) the music starts by itself with the first click or key press.
// Stopping the player silences only the current night: the next one starts with music again.
let musWanted = true;
try { localStorage.removeItem('morpheus.music'); sessionStorage.removeItem('morpheus.music') } catch (e) {}
function musPref(on) { musWanted = on }
function musAuto(e) { if (e?.target?.closest?.('#player')) return; if (musWanted && !mus && player && cos('player') !== 'no') musicPlay(cos('tape')) }
addEventListener('pointerdown', musAuto, {once: true, capture: true});
addEventListener('keydown', musAuto, {once: true, capture: true});                                          // {id, el} for one file, {id, mix} for a folder tape
const MIX_BUF = {};                                      // url -> loudness gain

/* a folder tape = an endless mix: random order (never the same track twice in a row), each loop repeated
   for ~1-2 minutes, 4 s fade-out, a short pause, the next one fades in. Loudness is evened out by RMS. */
// the first track is downloaded while the title screen is up, so the music starts the moment the player clicks
const MIX_PRE = {};
function mixPrefetch(id) {
  const T = TAPES[id]; if (!T?.list || MIX_PRE[id]) return;
  const name = T.list[Math.floor(Math.random() * T.list.length)], url = `music/${T.dir}/${name}.mp3`;
  MIX_PRE[id] = {name, url, data: fetch(url).then(r => r.arrayBuffer()).catch(() => null)};
}
async function mixLoad(url) {
  // decoded songs are big (~50 MB each), so only the loudness is remembered, not the audio
  const pre = Object.values(MIX_PRE).find(p => p.url === url && !p.used);
  let data = pre ? await pre.data : null; if (pre) pre.used = true;
  if (!data) data = await (await fetch(url)).arrayBuffer();
  const buf = await AC.decodeAudioData(data);
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
    const pre = MIX_PRE[id] && !MIX_PRE[id].used ? MIX_PRE[id].name : null;
    const pool = T.list.filter(n => n !== mix.last), name = pre || pool[Math.floor(Math.random() * pool.length)]; mix.last = name;
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

function musicStop(slow) {
  if (!mus) return;
  if (mus.mix) { const m = mus.mix, tc = slow ? 1 : .15; m.dead = true; clearTimeout(m.timer); m.bus.gain.setTargetAtTime(.0001, AC.currentTime, tc); setTimeout(() => { try { m.src?.stop() } catch (e) {} m.bus.disconnect() }, tc * 6000) }
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
  const nudge = !on && performance.now() % 2600 < 420;                      // idle: the PLAY key winks, "press me"
  for (let i = 0; i < 4; i++) { const down = on && i === 1; R(5 + i * 6, down ? 2 : 1, 5, down ? 2 : 3, '#313638'); R(6 + i * 6, down ? 2 : 1, 3, down ? 1 : 2, i === 3 ? '#c0404a' : i === 1 && nudge ? '#f4f0c0' : '#9aa6b2') }
  if (nudge) { R(11, 0, 3, 1, '#f4f0c0') }
  R(4, 7, 25, 13, '#14181e'); R(4, 7, 25, 1, '#0a0c10'); R(4, 19, 25, 1, '#3a4a5e');   // tape window
  R(6, 8, 21, 11, '#cfc6b0'); R(6, 8, 21, 3, tape.col); R(6, 11, 21, 1, '#8a8270');    // the cassette + its label colour
  R(9, 13, 15, 4, '#2a2420');
  for (const cx of [11, 22]) {                                                  // reels turn while playing
    R(cx - 1, 13, 3, 3, '#e8e4dc'); R(cx, 14, 1, 1, '#2a2420');
    const sp = [[0, -1], [1, 0], [0, 1], [-1, 0]][ph]; R(cx + sp[0], 14 + sp[1], 1, 1, '#6a6258');
  }
  for (let y = 8; y < 20; y += 2) for (let x = 31; x < 37; x += 2) R(x, y, 1, 1, '#1a222c');   // speaker grille
  R(32, 20, 2, 2, on ? '#5adc6a' : nudge ? '#3a8a46' : '#2a3a2a');
}
function playerInit() {
  const el = document.createElement('div'); el.className = 'item'; el.id = 'player';
  const blank = document.createElement('canvas'); blank.width = 40; blank.height = 26;
  el.innerHTML = `<img width="40" height="26" alt="" src="${blank.toDataURL()}">`;
  $('stage').insertBefore(el, $('shade'));
  let pos = {x: 104, y: 96};
  try { pos = JSON.parse(localStorage.getItem('morpheus.player') || 'null') || pos } catch (e) {}
  player = new Item(el, {x: pos.x, y: pos.y, w: 40, h: 26, tiltK: .6, minY: 0, noGlass: true, compose: drawPlayer,
    onClick: () => { if (mus) { musicStop(); musPref(false) } else { musicPlay(cos('tape')); musPref(true) } sfx.click(); player.rebuild() },
    onEnter: () => think((MUS_T[LANG] || MUS_T.en).hint, true), onLeave: () => thinkRelease(),
    onDrop: () => { try { localStorage.setItem('morpheus.player', JSON.stringify({x: Math.round(player.tx), y: Math.round(player.ty)})) } catch (e) {} }});
  setInterval(() => { if (player && player.el.style.display !== 'none') player.rebuild() }, 140);   // spin the reels / wink the play key
  deskShow();
}
/* little notes float out of the speaker: a stream while it plays, a lone one now and then while it is silent */
const NOTES = [];let noteT = 0;
const NOTE_PX = ['..##', '..#.', '..#.', '###.', '###.'];
function drawNotes(c, now) {
  if (!player || player.el.style.display === 'none' || dreaming) { NOTES.length = 0; return }
  const on = !!mus;
  if (now > noteT) { noteT = now + (on ? 650 + Math.random() * 500 : 3800 + Math.random() * 1500);
    NOTES.push({x: player.x + 31 + Math.random() * 4, y: player.y + 4, ph: Math.random() * 6, t: 0, a: on ? .95 : .55}) }
  const col = TAPES[cos('tape')].col;
  for (let i = NOTES.length - 1; i >= 0; i--) { const n = NOTES[i]; n.t += 1 / 60;
    if (n.t > 1.6) { NOTES.splice(i, 1); continue }
    const x = Math.round(n.x + Math.sin(n.ph + n.t * 4) * 2 + n.t * 3), y = Math.round(n.y - n.t * 16), a = n.a * Math.min(1, n.t * 4, (1.6 - n.t) * 1.5);
    c.globalAlpha = a; NOTE_PX.forEach((r, yy) => [...r].forEach((ch, xx) => { if (ch === '#') { c.fillStyle = col; c.fillRect(x + xx, y + yy, 1, 1) } }));
  }
  c.globalAlpha = 1;
}
function deskShow() {                                                         // shop: what stands on the desk
  mug.el.style.display = cos('mugOn') === 'no' ? 'none' : '';
  lightsShow();
  if (player) { const show = cos('player') !== 'no'; player.el.style.display = show ? '' : 'none'; if (!show) musicStop() }
}

try { mixPrefetch(cos('tape')) } catch (e) {}

/* =========================================================
   DREAM MUSIC: a soft lullaby generated on the fly while Mira's dream plays.
   Slow warm pads (Fmaj7 - Em7 - Dm9 - Cmaj7), a low hum, and a music-box melody of chord tones
   with a long soft echo. The jazz tape fades out when the dream starts; the next night starts the tape again.
   ========================================================= */
let dreamMus = null;
function dreamMusicStart() {
  initAudio(); if (dreamMus) return;
  musicStop(true);
  const now = AC.currentTime, out = AC.createGain();
  out.gain.setValueAtTime(.0001, now); out.gain.exponentialRampToValueAtTime(1.8, now + 4); out.connect(musicOut);
  const dl = AC.createDelay(2), fb = AC.createGain(), lp = AC.createBiquadFilter(), wet = AC.createGain();   // soft echo
  dl.delayTime.value = .46; fb.gain.value = .42; lp.type = 'lowpass'; lp.frequency.value = 1800; wet.gain.value = .45;
  dl.connect(lp); lp.connect(fb); fb.connect(dl); lp.connect(wet); wet.connect(out);
  const padBus = AC.createBiquadFilter(); padBus.type = 'lowpass'; padBus.frequency.value = 900; padBus.Q.value = .3; padBus.connect(out);
  const boxBus = AC.createGain(); boxBus.connect(out); boxBus.connect(dl);
  const hz = m => 440 * 2 ** ((m - 69) / 12);
  const CH = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60, 64], [48, 52, 55, 59]];
  const BAR = 5.2;
  const voice = (type, f, t0, att, len, peak, bus, det = 0) => {
    const o = AC.createOscillator(), g = AC.createGain();
    o.type = type; o.frequency.value = f; o.detune.value = det;
    g.gain.setValueAtTime(.0001, t0); g.gain.exponentialRampToValueAtTime(peak, t0 + att);
    g.gain.exponentialRampToValueAtTime(.0001, t0 + len);
    o.connect(g); g.connect(bus); o.start(t0); o.stop(t0 + len + .1);
  };
  const box = (f, t0, v) => {                               // a music-box note: sine + a quiet bright partial
    voice('sine', f, t0, .008, 2.6, .055 * v, boxBus);
    voice('sine', f * 3, t0, .004, .5, .008 * v, boxBus);
  };
  let bar = 0, t = now + .3, last = 0;
  const sched = () => {
    while (t < AC.currentTime + BAR * 1.5) {
      const ch = CH[bar % CH.length];
      for (const m of ch) { voice('triangle', hz(m - 12), t, 1.8, BAR + 1.6, .03, padBus, -6); voice('triangle', hz(m - 12), t, 2.2, BAR + 1.6, .022, padBus, 7) }
      voice('sine', hz(ch[0] - 24), t, 1.2, BAR + 1, .07, padBus);
      const tones = ch.map(m => m + 12).concat(ch.slice(0, 2).map(m => m + 24));
      for (let k = 0; k < 8; k++) {                          // a slow melody in eighths, never a big leap
        if (k && Math.random() < .42) continue;
        let m = tones[Math.floor(Math.random() * tones.length)];
        if (last && Math.abs(m - last) > 9) m = tones.reduce((a, b) => Math.abs(b - last) < Math.abs(a - last) ? b : a);
        last = m; box(hz(m), t + k * BAR / 8 + Math.random() * .03, k ? .75 + Math.random() * .25 : 1);
      }
      t += BAR; bar++;
    }
  };
  sched(); dreamMus = {out, timer: setInterval(sched, 800)};
}
function dreamMusicStop() {
  if (!dreamMus) return; const d = dreamMus; dreamMus = null; clearInterval(d.timer);
  d.out.gain.setTargetAtTime(.0001, AC.currentTime, .8); setTimeout(() => d.out.disconnect(), 5000);
}
