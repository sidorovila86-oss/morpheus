/* =========================================================
   DREAM ALBUM + MORPHEUS' SHOP (cosmetics only, no effect on play)
   Album entries: guest-guest meetings (combos), guest@place scenes, caught look-alikes, week endings.
   Each NEW entry pays dust; dust buys looks: lamp shade, mug, lamp light, the beam, the dream sky.
   Saved in localStorage 'morpheus.album'. Survives "new week".
   ========================================================= */
const ALB_T = {
  en: {
    album: 'Dream album', shop: "Morpheus' shop", close: 'Close', open: 'Album',
    dust: n => `✧ ${n} dust`,
    meetings: 'Meetings', caught: 'Look-alikes caught', scenes: 'Guests in places', endings: 'Endings of the week',
    unknown: '???', buy: p => `✧ ${p}`, use: 'Use', inUse: '✔',
    hint: 'Every new meeting, scene, ending or caught look-alike gives dust. Dust only buys looks.',
    newEntries: (n, d) => `✦ New in the dream album: ${n} (+${d} dust)`,
    slots: {lamp: 'Desk lights (several at once)', mug: 'Mug', light: 'Lamp light', hall: 'In the beam', dream: 'Dream sky', tape: 'Cassettes (click the player)', mugOn: 'Mug on the desk', player: 'Cassette player on the desk'},
    items: {lamp: {candle: 'Candle', green: 'Green lamp', red: 'Crimson lamp', navy: 'Navy lamp', rose: 'Rose lamp'},
            mug: {green: 'Sage', coral: 'Coral', blue: 'Blue', lilac: 'Lilac'},
            light: {warm: 'Warm', moon: 'Moonlight', violet: 'Violet', mint: 'Mint'},
            hall: {dust: 'Dust', snow: 'Snow', fire: 'Fireflies', stars: 'Stars'},
            dream: {violet: 'Twilight', sunset: 'Sunset', aurora: 'Aurora', sea: 'Deep sea'},
            tape: {jazz: 'Quiet jazz', lofi: 'Rainy lo-fi', bossa: 'Bossa nova', box: 'Music box', synth: 'Neon synth'},
            mugOn: {yes: 'Keep', no: 'Put away'}, player: {yes: 'Keep', no: 'Put away'}},
  },
  ru: {
    album: 'Альбом снов', shop: 'Лавка Морфея', close: 'Закрыть', open: 'Альбом',
    dust: n => `✧ ${n} пыли`,
    meetings: 'Встречи', caught: 'Раскрытые двойники', scenes: 'Гости и места', endings: 'Концовки недели',
    unknown: '???', buy: p => `✧ ${p}`, use: 'Выбрать', inUse: '✔',
    hint: 'Каждая новая встреча, сцена, концовка или раскрытый двойник приносит пыль сна. За пыль можно купить только украшения.',
    newEntries: (n, d) => `✦ Новое в альбоме снов: ${n} (+${d} пыли)`,
    slots: {lamp: 'Свет на столе (можно несколько сразу)', mug: 'Кружка', light: 'Свет лампы', hall: 'В луче света', dream: 'Небо сна', tape: 'Кассеты (щёлкни по плееру)', mugOn: 'Кружка на столе', player: 'Кассетный плеер на столе'},
    items: {lamp: {candle: 'Свечка', green: 'Зелёная лампа', red: 'Багровая лампа', navy: 'Синяя лампа', rose: 'Розовая лампа'},
            mug: {green: 'Шалфей', coral: 'Коралл', blue: 'Синяя', lilac: 'Сирень'},
            light: {warm: 'Тёплый', moon: 'Лунный', violet: 'Фиолетовый', mint: 'Мятный'},
            hall: {dust: 'Пылинки', snow: 'Снег', fire: 'Светлячки', stars: 'Звёзды'},
            dream: {violet: 'Сумерки', sunset: 'Закат', aurora: 'Сияние', sea: 'Глубина'},
            tape: {jazz: 'Тихий джаз', lofi: 'Лоу-фай и дождь', bossa: 'Босса-нова', box: 'Музыкальная шкатулка', synth: 'Неоновый синт'},
            mugOn: {yes: 'Оставить', no: 'Убрать'}, player: {yes: 'Оставить', no: 'Убрать'}},
  },
  ja: {
    album: '夢のアルバム', shop: 'モルフェウスの店', close: 'とじる', open: 'アルバム',
    dust: n => `✧ 夢のちり ${n}`,
    meetings: '出会い', caught: '見やぶったそっくりさん', scenes: '場所のゲスト', endings: '週のエンディング',
    unknown: '？？？', buy: p => `✧ ${p}`, use: 'つかう', inUse: '✔',
    hint: '新しい出会い・場面・エンディング・見やぶったそっくりさんで夢のちりがもらえる。ちりで買えるのは見た目だけ。',
    newEntries: (n, d) => `✦ 夢のアルバムに新しく ${n}件（ちり +${d}）`,
    slots: {lamp: '机のあかり（いくつでも）', mug: 'マグカップ', light: 'ランプの光', hall: '光の中', dream: '夢の空', tape: 'カセット（プレーヤーをクリック）', mugOn: '机のマグカップ', player: '机のカセットプレーヤー'},
    items: {lamp: {candle: 'ろうそく', green: 'みどりのランプ', red: 'えんじのランプ', navy: 'こんのランプ', rose: 'ばらのランプ'},
            mug: {green: 'セージ', coral: 'コーラル', blue: 'あお', lilac: 'ライラック'},
            light: {warm: 'あたたか', moon: 'つきあかり', violet: 'むらさき', mint: 'ミント'},
            hall: {dust: 'ほこり', snow: 'ゆき', fire: 'ほたる', stars: 'ほし'},
            dream: {violet: 'たそがれ', sunset: 'ゆうやけ', aurora: 'オーロラ', sea: 'しんかい'},
            tape: {jazz: 'しずかなジャズ', lofi: '雨のローファイ', bossa: 'ボサノヴァ', box: 'オルゴール', synth: 'ネオンシンセ'},
            mugOn: {yes: 'おく', no: 'しまう'}, player: {yes: 'おく', no: 'しまう'}},
  },
};

// slot -> option -> price (first option is the free default)
const COS = {
  lamp:  {candle: 0, green: 12, red: 16, navy: 16, rose: 16},
  mug:   {green: 0, coral: 6, blue: 6, lilac: 6},
  light: {warm: 0, moon: 10, violet: 10, mint: 10},
  hall:  {dust: 0, snow: 10, fire: 10, stars: 10},
  dream: {violet: 0, sunset: 12, aurora: 12, sea: 12},
  tape:  {jazz: 0, lofi: 12, bossa: 12, box: 10, synth: 15},
  mugOn: {yes: 0, no: 0},
  player: {yes: 0, no: 0},
};
const ALB_PAY = {c: 3, s: 2, e: 5, d: 3};
// recolours: [target hue in degrees, saturation multiplier] for the green parts of the sprite (null = keep)
const COS_HUE = {
  lamp: {candle: null, green: null, red: [355, 1.15], navy: [222, 1.1], rose: [330, 1.05]},
  mug:  {green: null, coral: [12, 1.7], blue: [210, 1.3], lilac: [275, 1.2]},
};
const COS_LIGHT = {warm: [255, 178, 92], moon: [150, 190, 255], violet: [196, 140, 255], mint: [140, 240, 190]};
const COS_DREAM = {
  violet: ['#1a1726', '#2b2f4a', '#3e3a62', '#5b4f7c', '#7a6896', '#a28fbe', '#c7b3e6'],
  sunset: ['#1e1426', '#3a1e3e', '#5e2a4a', '#8a3a52', '#b85a5a', '#e08a5e', '#f4c07a'],
  aurora: ['#0e1a22', '#123030', '#1a4a44', '#246a54', '#3a8e64', '#6ab88a', '#a8e0b8'],
  sea:    ['#0a1022', '#10203e', '#163058', '#1e4474', '#2a5c90', '#4a7cae', '#7aa4cc'],
};

const ALB = (() => {
  let d = null;
  try { d = JSON.parse(localStorage.getItem('morpheus.album') || 'null') } catch (e) {}
  d = d || {};
  return {c: d.c || [], s: d.s || [], e: d.e || [], d: d.d || [], dust: d.dust || 0, own: d.own || [], cos: d.cos || {}};
})();
let ALB_NEW = [];                       // dust paid for entries found since the last morning
function albSave() { try { localStorage.setItem('morpheus.album', JSON.stringify(ALB)) } catch (e) {} }
const cos = s => ALB.cos[s] || Object.keys(COS[s])[0];
// desk lights are not one choice but a set: the candle and any lamps you own, on the desk at the same time
const deskLights = () => Array.isArray(ALB.cos.lights) ? ALB.cos.lights : [ALB.cos.lamp || 'candle'];
const owns = (s, o) => COS[s][o] === 0 || ALB.own.includes(s + ':' + o);
const AT_ = () => ALB_T[LANG] || ALB_T.en;

function albFind(kind, key) {
  if (ALB[kind].includes(key)) return false;
  ALB[kind].push(key); ALB.dust += ALB_PAY[kind]; ALB_NEW.push(ALB_PAY[kind]); albSave();
  return true;
}
function albNewLine() {
  if (!ALB_NEW.length) return '';
  const t = AT_().newEntries(ALB_NEW.length, ALB_NEW.reduce((a, b) => a + b, 0)); ALB_NEW = [];
  return `<p class="res alb">${t}</p>`;
}

/* ---------- recolouring helpers ---------- */
function rgb2hsl(r, g, b) {
  r /= 255; g /= 255; b /= 255; const mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2;
  if (mx === mn) return [0, 0, l];
  const d = mx - mn, s = l > .5 ? d / (2 - mx - mn) : d / (mx + mn);
  const h = mx === r ? (g - b) / d + (g < b ? 6 : 0) : mx === g ? (b - r) / d + 2 : (r - g) / d + 4;
  return [h * 60, s, l];
}
function hsl2rgb(h, s, l) {
  const k = n => (n + h / 30) % 12, a = s * Math.min(l, 1 - l);
  const f = n => l - a * Math.max(-1, Math.min(k(n) - 3, 9 - k(n), 1));
  return [Math.round(f(0) * 255), Math.round(f(8) * 255), Math.round(f(4) * 255)];
}
function cosTint(c, w, h, slot, opt) {
  const t = COS_HUE[slot][opt || cos(slot)]; if (!t) return; const [hue, sm] = t;
  const id = c.getImageData(0, 0, w, h), d = id.data;
  for (let i = 0; i < d.length; i += 4) {
    if (!d[i + 3]) continue;
    const r = d[i], g = d[i + 1], b = d[i + 2];
    if (!(g > r + 6 && g >= b - 4)) continue;          // only the green parts
    const [H, S, L] = rgb2hsl(r, g, b), o = hsl2rgb((hue + (H - 130) * 0.3 + 720) % 360, Math.min(1, S * sm), L);
    d[i] = o[0]; d[i + 1] = o[1]; d[i + 2] = o[2];
  }
  c.putImageData(id, 0, 0);
}
function applyCos() {
  Object.values(LIGHTS).forEach(l => l.rebuild()); mug.rebuild(); deskShow(); relight();
  if (mus && mus.id !== cos('tape')) musicPlay(cos('tape'));          // swap the tape while it plays
  player?.rebuild();
}

/* ---------- the album / shop overlay ---------- */
let albTab = 'album';
function albHTML() {
  const A = AT_(), sec = (title, keys, kind, text) => {
    const got = keys.filter(k => ALB[kind].includes(k)).length;
    const miss = keys.length - got;
    return `<h3>${title} <span class="small">${got}/${keys.length}</span></h3>` +
      keys.filter(k => ALB[kind].includes(k)).map(k => `<p class="ae">✦ ${text(k)}</p>`).join('') +
      (miss ? `<p class="ae un">${'<span class="aslot">?</span>'.repeat(miss)}</p>` : '');
  };
  const ends = WEEK[LANG].ui.endings;
  return sec(A.meetings, Object.keys(COMBOS), 'c', k => COMBOS[k].t) +
         sec(A.scenes, Object.keys(SCENE_AT), 's', k => SCENE_AT[k]) +
         sec(A.caught, ['fakemom', 'faketeacher', 'fakedog', 'fakeboss'], 'd', k => STR[LANG].v[k].caught) +
         sec(A.endings, ends.map((_, i) => String(i)), 'e', k => ends[+k]);
}
function shopHTML() {
  const A = AT_();
  return `<p class="small">${A.hint}</p>` + Object.keys(COS).map(s =>
    `<h3>${A.slots[s]}</h3><div class="srow">` + Object.keys(COS[s]).map(o => {
      const on = s === 'lamp' ? deskLights().includes(o) : cos(s) === o, have = owns(s, o), can = have || ALB.dust >= COS[s][o];
      const lab = on ? A.inUse : have ? A.use : A.buy(COS[s][o]);
      return `<span class="sit${on ? ' on' : ''}${can ? '' : ' no'}" data-s="${s}" data-o="${o}">${A.items[s][o]} <b>${lab}</b></span>`;
    }).join('') + '</div>').join('');
}
function albRender() {
  const A = AT_();
  $('apaper').innerHTML = `<div class="atabs"><span class="atab${albTab === 'album' ? ' on' : ''}" data-t="album">${A.album}</span>` +
    `<span class="atab${albTab === 'shop' ? ' on' : ''}" data-t="shop">${A.shop}</span><span class="adust">${A.dust(ALB.dust)}</span></div>` +
    `<div class="abody">${albTab === 'album' ? albHTML() : shopHTML()}</div>`;
  $('aclose').textContent = A.close;
}
function albOpen(e) { e?.stopPropagation(); initAudio(); albRender(); $('album').classList.add('on'); sfx.page() }
function albInit() {                    // called by the main script once the DOM helpers exist
 $('t_album').onclick = albOpen; $('malb').onclick = albOpen;
 $('album').addEventListener('click', e => {
  const t = e.target.closest('.atab'), it = e.target.closest('.sit');
  if (e.target.id === 'aclose' || e.target.classList.contains('dim')) { $('album').classList.remove('on'); sfx.drop(); return }
  if (t) { albTab = t.dataset.t; albRender(); sfx.page(); return }
  if (it) {
    const s = it.dataset.s, o = it.dataset.o;
    const have0 = owns(s, o);
    if (!owns(s, o)) { if (ALB.dust < COS[s][o]) { sfx.bad?.(); return } ALB.dust -= COS[s][o]; ALB.own.push(s + ':' + o); sfx.good?.() }
    else sfx.click();
    if (s === 'lamp') { const L = deskLights().slice(), i = L.indexOf(o); if (i >= 0 && have0) L.splice(i, 1); else if (i < 0) L.push(o); ALB.cos.lights = L }
    else ALB.cos[s] = o;
    albSave(); applyCos(); albRender();
  }
 });
}
