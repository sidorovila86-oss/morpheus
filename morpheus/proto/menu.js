/* =========================================================
   TITLE MENU + SETTINGS
   Menu: Continue (if a week is in progress) / New game / Dream album / Settings.
   Settings: language, master / music / sound volume, text speed, fullscreen.
   Saved in localStorage 'morpheus.settings'. Esc or the gear opens settings during play.
   ========================================================= */
const MENU_T = {
  en: {cont: n => `Continue · night ${n}`, newGame: 'New game', sure: 'Sure? The week starts over', settings: 'Settings', album: 'Dream album',
       title: 'Settings', lang: 'Language', master: 'Volume', music: 'Music', sfx: 'Sounds', speed: 'Text speed',
       speeds: {slow: 'Slow', normal: 'Normal', fast: 'Fast', instant: 'Instant'}, full: 'Fullscreen', on: 'On', off: 'Off', close: 'Close', menu: 'Main menu'},
  ru: {cont: n => `Продолжить · ночь ${n}`, newGame: 'Новая игра', sure: 'Точно? Неделя начнётся заново', settings: 'Настройки', album: 'Альбом снов',
       title: 'Настройки', lang: 'Язык', master: 'Громкость', music: 'Музыка', sfx: 'Звуки', speed: 'Скорость текста',
       speeds: {slow: 'Медленно', normal: 'Обычно', fast: 'Быстро', instant: 'Сразу'}, full: 'Полный экран', on: 'Вкл', off: 'Выкл', close: 'Закрыть', menu: 'Главное меню'},
  ja: {cont: n => `つづける・第${n}夜`, newGame: 'はじめから', sure: '本当に？一週間が最初からになります', settings: '設定', album: '夢のアルバム',
       title: '設定', lang: '言語', master: '音量', music: '音楽', sfx: '効果音', speed: '文字の速さ',
       speeds: {slow: 'おそい', normal: 'ふつう', fast: 'はやい', instant: 'すぐ'}, full: '全画面', on: 'オン', off: 'オフ', close: 'とじる', menu: 'タイトルへ'},
};
const MT = () => MENU_T[LANG] || MENU_T.en;
const SET = (() => {
  let d = {}; try { d = JSON.parse(localStorage.getItem('morpheus.settings') || '{}') || {} } catch (e) {}
  return {master: d.master ?? 80, music: d.music ?? 70, sfx: d.sfx ?? 80, speed: d.speed || 'normal'};
})();
function setSave() { try { localStorage.setItem('morpheus.settings', JSON.stringify(SET)) } catch (e) {} }
const TS = () => ({slow: 1.8, normal: 1, fast: .45, instant: 0})[SET.speed] ?? 1;    // text speed factor for all typing

/* volumes: sfx -> master gain, tapes -> musicOut, both -> mainOut -> speakers */
let mainOut = null, musicOut = null;
function audioBuses() {                 // called once from initAudio()
  mainOut = AC.createGain(); musicOut = AC.createGain();
  master.disconnect(); master.connect(mainOut); musicOut.connect(mainOut); mainOut.connect(AC.destination);
  applyVolumes();
}
function applyVolumes() {
  const v = k => Math.pow(SET[k] / 100, 1.6);        // ears are logarithmic
  if (AC) { mainOut.gain.value = v('master'); master.gain.value = .5 * v('sfx'); musicOut.gain.value = v('music') }
  if (mus?.el) mus.el.volume = .6 * v('master') * v('music');
}

/* ---------- title menu ---------- */
let sureNew = false;
function startGame() { initAudio(); $('start').classList.remove('on'); $('memo').classList.add('on'); sfx.page() }
function menuLabels() {
  const T = MT();
  $('t_cont').textContent = T.cont(NIGHT); $('t_cont').style.display = NIGHT > 1 ? '' : 'none';
  $('t_new').textContent = sureNew ? T.sure : T.newGame; $('t_new').classList.toggle('warn', sureNew);
  $('t_set').textContent = T.settings; $('t_album').textContent = T.album; $('gear').title = T.settings;
  if ($('settings').classList.contains('on')) setRender();
}

/* ---------- settings ---------- */
function setRender() {
  const T = MT(), seg = (key, opts, cur) => `<div class="seg">` +
    opts.map(([v, lab]) => `<span class="sb${v === cur ? ' on' : ''}" data-k="${key}" data-v="${v}">${lab}</span>`).join('') + `</div>`;
  const slider = k => `<input type="range" min="0" max="100" step="5" value="${SET[k]}" data-k="${k}"><span class="sv">${SET[k]}</span>`;
  const inGame = !$('start').classList.contains('on');
  $('spaper').innerHTML = `<h2>${T.title}</h2>
    <div class="srow2"><span class="sl">${T.lang}</span>${seg('lang', [['en', 'English'], ['ru', 'Русский'], ['ja', '日本語']], LANG)}</div>
    <div class="srow2"><span class="sl">${T.master}</span>${slider('master')}</div>
    <div class="srow2"><span class="sl">${T.music}</span>${slider('music')}</div>
    <div class="srow2"><span class="sl">${T.sfx}</span>${slider('sfx')}</div>
    <div class="srow2"><span class="sl">${T.speed}</span>${seg('speed', Object.entries(T.speeds), SET.speed)}</div>
    <div class="srow2"><span class="sl">${T.full}</span>${seg('full', [['1', T.on], ['0', T.off]], document.fullscreenElement ? '1' : '0')}</div>
    <div class="sbtns">${inGame ? `<span class="btn" id="stomenu">${T.menu}</span>` : ''}<span class="btn" id="sclose">${T.close}</span></div>`;
}
function setOpen() { initAudio(); setRender(); $('settings').classList.add('on'); sfx.page() }
function setClose() { $('settings').classList.remove('on'); sfx.drop() }

function menuInit() {
  $('t_cont').onclick = e => { e.stopPropagation(); startGame() };
  $('t_new').onclick = e => {
    e.stopPropagation();
    if (NIGHT > 1 && !sureNew) { sureNew = true; menuLabels(); sfx.click(); return }
    if (NIGHT > 1) { saveWeek(null); reloadInto(); return }        // wipe the week, go straight to Monday's memo
    startGame();
  };
  $('t_set').onclick = e => { e.stopPropagation(); setOpen() };
  $('gear').onclick = e => { e.stopPropagation(); setOpen() };
  addEventListener('keydown', e => {
    if (e.key !== 'Escape') return;
    if ($('settings').classList.contains('on')) setClose();
    else if (!document.querySelector('.ov.on:not(#start)') || $('start').classList.contains('on')) setOpen();
  });
  const S = $('settings');
  S.addEventListener('input', e => {
    const k = e.target.dataset?.k; if (!k) return;
    SET[k] = +e.target.value; e.target.nextElementSibling.textContent = SET[k]; applyVolumes(); setSave();
  });
  S.addEventListener('change', e => { if (e.target.dataset?.k === 'sfx') sfx.click() });   // a sample of the new sound level
  S.addEventListener('click', e => {
    if (e.target.id === 'sclose' || e.target.classList.contains('dim')) { setClose(); return }
    if (e.target.id === 'stomenu') { location.reload(); return }      // the night restarts from its memo, like any reload
    const b = e.target.closest('.sb'); if (!b) return;
    const k = b.dataset.k, v = b.dataset.v; sfx.click();
    if (k === 'lang') applyLang(v);
    if (k === 'speed') { SET.speed = v; setSave() }
    if (k === 'full') { (v === '1' ? document.documentElement.requestFullscreen?.() : document.fullscreenElement && document.exitFullscreen?.())?.catch?.(() => {}); setTimeout(setRender, 250) }
    setRender();
  });
  document.addEventListener('fullscreenchange', () => { if (S.classList.contains('on')) setRender() });
  menuLabels();
}

