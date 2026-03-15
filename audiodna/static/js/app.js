/* AudioDNA — Vanilla JS Frontend  |  Profile + YouTube edition */
const API = '';

const state = {
  songs: [], genres: [], moods: [], countries: [],
  likedSongs: [], playlists: [], filters: {},
  plCounter: 0, pendingSong: null, expandedPl: null,
  profile: null,
  regColor: '#a855f7',
  editColor: '#a855f7',
};

// ── INIT ──────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
  await loadSongs();
  setupLogin();
  setupRegister();
  setupSearch();
  setupProfileEditForm();
  document.getElementById('btn-logout').addEventListener('click', doLogout);
  document.getElementById('btn-clear-filters').addEventListener('click', clearFilters);
  document.getElementById('btn-create-playlist').addEventListener('click', showCreateForm);
  document.getElementById('new-playlist-name').addEventListener('keydown', ev => {
    if (ev.key === 'Enter') confirmCreatePlaylist();
    if (ev.key === 'Escape') cancelCreatePlaylist();
  });
  document.getElementById('modal-new-name').addEventListener('keydown', ev => {
    if (ev.key === 'Enter') modalCreatePlaylist();
    if (ev.key === 'Escape') closePlaylistModal();
  });
  document.getElementById('playlist-modal').addEventListener('click', ev => {
    if (ev.target === document.getElementById('playlist-modal')) closePlaylistModal();
  });
  document.getElementById('profile-modal').addEventListener('click', ev => {
    if (ev.target === document.getElementById('profile-modal')) closeProfileModal();
  });
});

async function loadSongs() {
  const res = await fetch(`${API}/api/songs`);
  const d = await res.json();
  state.songs = d.songs; state.genres = d.genres;
  state.moods = d.moods; state.countries = d.countries;
  renderFilters();
  renderAllSongs();
  document.getElementById('all-count').textContent = `(${state.songs.length})`;
}

// ── AUTH TABS ─────────────────────────────────────────────────
function switchTab(tab) {
  document.getElementById('tab-signin').classList.toggle('active', tab==='signin');
  document.getElementById('tab-register').classList.toggle('active', tab==='register');
  document.getElementById('login-form').classList.toggle('hidden', tab!=='signin');
  document.getElementById('register-form').classList.toggle('hidden', tab!=='register');
}

// ── LOGIN ─────────────────────────────────────────────────────
function setupLogin() {
  document.getElementById('login-form').addEventListener('submit', async ev => {
    ev.preventDefault();
    const email    = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const errEl    = document.getElementById('login-error');
    errEl.classList.add('hidden');
    try {
      const res = await fetch(`${API}/api/login`, {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({email, password}),
      });
      const d = await res.json();
      if (d.success) { applyProfile(d.profile); showDash(); }
      else { errEl.textContent = d.error || 'Invalid credentials'; errEl.classList.remove('hidden'); }
    } catch { applyProfile(null); showDash(); }
  });
}

// ── REGISTER ──────────────────────────────────────────────────
function setupRegister() {
  document.getElementById('register-form').addEventListener('submit', async ev => {
    ev.preventDefault();
    const errEl = document.getElementById('reg-error');
    errEl.classList.add('hidden');
    const payload = {
      name:          document.getElementById('reg-name').value.trim(),
      email:         document.getElementById('reg-email').value.trim(),
      password:      document.getElementById('reg-password').value,
      bio:           document.getElementById('reg-bio').value.trim(),
      location:      document.getElementById('reg-location').value.trim(),
      fav_genre:     document.getElementById('reg-genre').value,
      fav_mood:      document.getElementById('reg-mood').value,
      avatar_color:  state.regColor,
    };
    if (!payload.name || !payload.email || !payload.password) {
      errEl.textContent = 'Name, email and password are required'; errEl.classList.remove('hidden'); return;
    }
    try {
      const res = await fetch(`${API}/api/register`, {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify(payload),
      });
      const d = await res.json();
      if (d.success) { applyProfile(d.profile); showDash(); }
      else { errEl.textContent = d.error || 'Registration failed'; errEl.classList.remove('hidden'); }
    } catch (err) { errEl.textContent = 'Server error. Try again.'; errEl.classList.remove('hidden'); }
  });
}

function pickColor(el) {
  document.querySelectorAll('#reg-color-swatches .swatch').forEach(s => s.classList.remove('active'));
  el.classList.add('active');
  state.regColor = el.dataset.color;
}

function pickEditColor(el) {
  document.querySelectorAll('#edit-color-swatches .swatch').forEach(s => s.classList.remove('active'));
  el.classList.add('active');
  state.editColor = el.dataset.color;
}

// ── APPLY PROFILE ─────────────────────────────────────────────
function applyProfile(profile) {
  state.profile = profile;
  if (!profile) return;
  // topbar avatar
  const initials = profile.name ? profile.name.split(' ').map(w=>w[0]).join('').slice(0,2).toUpperCase() : '?';
  const avatarBtn = document.getElementById('btn-profile');
  const avatarSpan = document.getElementById('avatar-initials');
  avatarSpan.textContent = initials;
  avatarBtn.style.background = profile.avatar_color || '#a855f7';
  // Restore liked songs & playlists from profile
  if (profile.liked_songs && profile.liked_songs.length) {
    state.likedSongs = profile.liked_songs.filter(ls => state.songs.find(s=>s.id===ls.id));
    renderLiked();
  }
  if (profile.playlists && profile.playlists.length) {
    state.playlists = profile.playlists;
    state.plCounter = state.playlists.length;
    renderPlaylists();
  }
}

function showDash() {
  document.getElementById('login-screen').classList.add('hidden');
  document.getElementById('dashboard').classList.remove('hidden');
}

async function doLogout() {
  // auto-save before logout
  await saveUserData(true);
  await fetch(`${API}/api/logout`, {method:'POST'}).catch(()=>{});
  state.profile = null; state.likedSongs = []; state.playlists = []; state.filters = {};
  document.getElementById('login-screen').classList.remove('hidden');
  document.getElementById('dashboard').classList.add('hidden');
}

// ── PROFILE MODAL ─────────────────────────────────────────────
function openProfileModal() {
  const p = state.profile;
  if (!p) return;
  const initials = p.name ? p.name.split(' ').map(w=>w[0]).join('').slice(0,2).toUpperCase() : '?';
  document.getElementById('profile-avatar-big').textContent = initials;
  document.getElementById('profile-avatar-big').style.background = p.avatar_color || '#a855f7';
  document.getElementById('profile-display-name').textContent = p.name || '';
  document.getElementById('profile-display-email').textContent = p.email || '';
  document.getElementById('profile-display-bio').textContent = p.bio ? `"${p.bio}"` : (p.location ? `📍 ${p.location}` : '');
  // Stats
  document.getElementById('stat-liked').textContent = state.likedSongs.length;
  document.getElementById('stat-playlists').textContent = state.playlists.length;
  document.getElementById('stat-songs').textContent = state.playlists.reduce((a,pl)=>a+pl.songs.length,0);
  // Fill edit form
  document.getElementById('edit-name').value = p.name || '';
  document.getElementById('edit-location').value = p.location || '';
  document.getElementById('edit-bio').value = p.bio || '';
  document.getElementById('edit-genre').value = p.fav_genre || '';
  document.getElementById('edit-mood').value = p.fav_mood || '';
  document.getElementById('edit-cur-pw').value = '';
  document.getElementById('edit-new-pw').value = '';
  document.getElementById('edit-confirm-pw').value = '';
  state.editColor = p.avatar_color || '#a855f7';
  // Mark active color swatch
  document.querySelectorAll('#edit-color-swatches .swatch').forEach(s => {
    s.classList.toggle('active', s.dataset.color === state.editColor);
  });
  document.getElementById('profile-edit-error').classList.add('hidden');
  document.getElementById('profile-edit-success').classList.add('hidden');
  document.getElementById('profile-modal').classList.remove('hidden');
}

function closeProfileModal() {
  document.getElementById('profile-modal').classList.add('hidden');
}

function setupProfileEditForm() {
  document.getElementById('profile-edit-form').addEventListener('submit', async ev => {
    ev.preventDefault();
    const errEl = document.getElementById('profile-edit-error');
    const sucEl = document.getElementById('profile-edit-success');
    errEl.classList.add('hidden'); sucEl.classList.add('hidden');
    const newPw   = document.getElementById('edit-new-pw').value;
    const confPw  = document.getElementById('edit-confirm-pw').value;
    const curPw   = document.getElementById('edit-cur-pw').value;
    if (newPw && newPw !== confPw) {
      errEl.textContent = 'New passwords do not match'; errEl.classList.remove('hidden'); return;
    }
    const payload = {
      name:         document.getElementById('edit-name').value.trim(),
      location:     document.getElementById('edit-location').value.trim(),
      bio:          document.getElementById('edit-bio').value.trim(),
      fav_genre:    document.getElementById('edit-genre').value,
      fav_mood:     document.getElementById('edit-mood').value,
      avatar_color: state.editColor,
    };
    if (newPw && curPw) { payload.current_password = curPw; payload.new_password = newPw; }
    try {
      const res = await fetch(`${API}/api/profile`, {
        method: 'PUT', headers: {'Content-Type':'application/json'},
        body: JSON.stringify(payload),
      });
      const d = await res.json();
      if (d.success) {
        applyProfile(d.profile);
        sucEl.textContent = '✓ Profile saved successfully!'; sucEl.classList.remove('hidden');
        // refresh display
        openProfileModal();
      } else {
        errEl.textContent = d.error || 'Save failed'; errEl.classList.remove('hidden');
      }
    } catch { errEl.textContent = 'Server error'; errEl.classList.remove('hidden'); }
  });
}

async function saveUserData(silent = false) {
  if (!state.profile) return;
  const payload = {
    liked_songs: state.likedSongs.map(s => ({id:s.id,title:s.title,artist:s.artist,cover:s.cover,youtube_link:s.youtube_link})),
    playlists: state.playlists.map(pl => ({
      id: pl.id, name: pl.name,
      songs: pl.songs.map(s => ({id:s.id,title:s.title,artist:s.artist,cover:s.cover,youtube_link:s.youtube_link}))
    })),
  };
  try {
    const res = await fetch(`${API}/api/profile/data`, {
      method: 'PUT', headers: {'Content-Type':'application/json'},
      body: JSON.stringify(payload),
    });
    const d = await res.json();
    if (!silent && d.success) {
      const sucEl = document.getElementById('profile-edit-success');
      sucEl.textContent = '✓ Library synced — liked songs & playlists saved!';
      sucEl.classList.remove('hidden');
      setTimeout(() => sucEl.classList.add('hidden'), 3000);
    }
  } catch {}
}

// ── YOUTUBE PLAY ──────────────────────────────────────────────
function playOnYouTube(ytLink) { window.open(ytLink, '_blank', 'noopener'); }

// ── SEARCH ────────────────────────────────────────────────────
function setupSearch() {
  const input = document.getElementById('search-input');
  const dd = document.getElementById('search-dropdown');
  let t;
  input.addEventListener('input', () => {
    clearTimeout(t);
    const q = input.value.trim();
    if (!q) { dd.classList.add('hidden'); return; }
    t = setTimeout(async () => {
      const res = await fetch(`${API}/api/search?q=${encodeURIComponent(q)}`);
      const d = await res.json();
      renderSearchDrop(d.results);
    }, 200);
  });
  document.addEventListener('mousedown', ev => {
    if (!document.getElementById('search-wrap').contains(ev.target)) dd.classList.add('hidden');
  });
}

function renderSearchDrop(songs) {
  const dd = document.getElementById('search-dropdown');
  if (!songs.length) { dd.classList.add('hidden'); return; }
  dd.innerHTML = songs.map(s => rowHTML(s, true)).join('');
  dd.classList.remove('hidden');
  if (songs[0]) triggerSimilar(songs[0].id);
}

// ── FILTERS ───────────────────────────────────────────────────
function renderFilters() {
  renderChips('chips-genre', state.genres, 'genre');
  renderChips('chips-mood', state.moods, 'mood');
  renderChips('chips-country', state.countries, 'country');
}
function renderChips(id, items, key) {
  document.getElementById(id).innerHTML = items.map(v =>
    `<button class="chip ${state.filters[key]===v?'active':''}" onclick="toggleFilter('${key}','${e(v)}')">${e(v)}</button>`
  ).join('');
}
async function toggleFilter(key, val) {
  if (state.filters[key]===val) { delete state.filters[key]; if(key==='country') delete state.filters['artist']; }
  else { state.filters[key]=val; if(key==='country') delete state.filters['artist']; }
  if (state.filters.country) {
    const res = await fetch(`${API}/api/artists-by-country/${encodeURIComponent(state.filters.country)}`);
    const d = await res.json();
    document.getElementById('artist-filter-group').style.display = d.artists.length ? '' : 'none';
    renderChips('chips-artist', d.artists, 'artist');
  } else { document.getElementById('artist-filter-group').style.display = 'none'; }
  renderChips('chips-genre', state.genres, 'genre');
  renderChips('chips-mood', state.moods, 'mood');
  renderChips('chips-country', state.countries, 'country');
  const hasF = Object.keys(state.filters).length > 0;
  document.getElementById('btn-clear-filters').classList.toggle('hidden', !hasF);
  if (hasF) {
    const res = await fetch(`${API}/api/recommend?${new URLSearchParams(state.filters)}`);
    renderRecommended((await res.json()).recommendations);
  } else {
    document.getElementById('recommended-grid').classList.add('hidden');
    document.getElementById('recommended-empty').classList.remove('hidden');
  }
}
function clearFilters() {
  state.filters = {};
  renderFilters();
  document.getElementById('artist-filter-group').style.display = 'none';
  document.getElementById('btn-clear-filters').classList.add('hidden');
  document.getElementById('recommended-grid').classList.add('hidden');
  document.getElementById('recommended-empty').classList.remove('hidden');
}

// ── RECOMMENDED ───────────────────────────────────────────────
function renderRecommended(songs) {
  const grid = document.getElementById('recommended-grid');
  const empty = document.getElementById('recommended-empty');
  if (!songs.length) { grid.classList.add('hidden'); empty.classList.remove('hidden'); return; }
  grid.innerHTML = songs.map((s,i) => `
    <div class="song-card" style="animation-delay:${i*.05}s">
      <div class="cover-wrap"><img src="${s.cover}" alt="${e(s.title)}" loading="lazy"/><div class="cover-overlay"></div></div>
      <div class="card-title">${e(s.title)}</div>
      <div class="card-artist">${e(s.artist)}</div>
      <div class="card-tags"><span class="tag-pill">${e(s.genre)}</span><span class="tag-pill">${e(s.mood)}</span></div>
      <div class="card-actions">
        <button class="card-btn play" onclick="playOnYouTube('${s.youtube_link}')">▶ YT</button>
        <button class="card-btn ${isLiked(s.id)?'liked':''}" id="lc-${s.id}" onclick="toggleLike('${s.id}')">${isLiked(s.id)?'♥':'♡'}</button>
        <button class="card-btn ${isInPl(s.id)?'added':''}" id="ac-${s.id}" onclick="openModal('${s.id}')">${isInPl(s.id)?'✓':'+'}</button>
      </div>
    </div>`).join('');
  grid.classList.remove('hidden'); empty.classList.add('hidden');
}

// ── SIMILAR ───────────────────────────────────────────────────
async function triggerSimilar(songId) {
  const [r1, r2] = await Promise.all([
    fetch(`${API}/api/similar/${songId}`),
    fetch(`${API}/api/mood-vector/${songId}`),
  ]);
  renderSimilar((await r1.json()).similar);
  renderAIPanel((await r2.json()).features);
}
function renderSimilar(songs) {
  const sec = document.getElementById('section-similar');
  const scroll = document.getElementById('similar-scroll');
  if (!songs.length) { sec.style.display='none'; return; }
  scroll.innerHTML = songs.map((s,i) => `
    <div class="song-card" style="animation-delay:${i*.04}s">
      <div class="cover-wrap"><img src="${s.cover}" alt="${e(s.title)}" loading="lazy"/><div class="cover-overlay"></div></div>
      <div class="card-title">${e(s.title)}</div>
      <div class="card-artist">${e(s.artist)}</div>
      <div class="card-tags"><span class="tag-pill">${e(s.genre)}</span></div>
      ${s.similarity_score!==undefined?`<div class="similarity-bar"><div class="similarity-fill" style="width:${Math.round(s.similarity_score*100)}%"></div></div>`:''}
      <div class="card-actions">
        <button class="card-btn play" onclick="playOnYouTube('${s.youtube_link}')">▶ YT</button>
        <button class="card-btn ${isLiked(s.id)?'liked':''}" id="ls-${s.id}" onclick="toggleLike('${s.id}')">${isLiked(s.id)?'♥':'♡'}</button>
        <button class="card-btn ${isInPl(s.id)?'added':''}" id="as-${s.id}" onclick="openModal('${s.id}')">${isInPl(s.id)?'✓':'+'}</button>
      </div>
    </div>`).join('');
  sec.style.display = '';
}
function renderAIPanel(features) {
  if (!features) return;
  const bars = [{name:'Energy',key:'energy',max:1},{name:'Dance',key:'danceability',max:1},{name:'Valence',key:'valence',max:1},{name:'Tempo',key:'tempo',max:200}];
  document.getElementById('ai-panel-content').innerHTML = `<div class="feature-bar">${bars.map(b=>{
    const v=features[b.key]||0,pct=Math.round((v/b.max)*100),disp=b.key==='tempo'?Math.round(v):(v*100).toFixed(0)+'%';
    return `<div class="feature-row"><span class="feature-name">${b.name}</span><div class="feature-track"><div class="feature-fill" style="width:${pct}%"></div></div><span class="feature-val">${disp}</span></div>`;
  }).join('')}</div>`;
  document.getElementById('ai-panel').style.display = '';
}

// ── ALL SONGS ─────────────────────────────────────────────────
function renderAllSongs() {
  document.getElementById('all-songs-list').innerHTML = state.songs.map(s => rowHTML(s, false)).join('');
}
function rowHTML(s, inDrop) {
  return `
    <div class="song-row-item" onclick="${inDrop?`triggerSimilar('${s.id}')`:''}" style="${inDrop?'cursor:pointer':''}">
      <img src="${s.cover}" alt="${e(s.title)}" loading="lazy"/>
      <div class="song-row-info">
        <div class="r-title">${e(s.title)}</div>
        <div class="r-artist">${e(s.artist)}</div>
      </div>
      ${!inDrop?`<div class="song-row-tags"><span class="tag-pill">${e(s.genre)}</span><span class="tag-pill">${e(s.mood)}</span></div>`:''}
      <div class="song-row-actions">
        <button class="row-btn yt" onclick="playOnYouTube('${s.youtube_link}');event.stopPropagation()" title="Play on YouTube">▶</button>
        <button class="row-btn ${isLiked(s.id)?'liked':''}" id="lr-${s.id}" onclick="toggleLike('${s.id}');event.stopPropagation()">${isLiked(s.id)?'♥':'♡'}</button>
        <button class="row-btn ${isInPl(s.id)?'added':''}" id="ar-${s.id}" onclick="openModal('${s.id}');event.stopPropagation()">${isInPl(s.id)?'✓':'+'}</button>
        <button class="row-btn" onclick="triggerSimilar('${s.id}');event.stopPropagation()" title="Find similar">≈</button>
      </div>
    </div>`;
}

// ── LIKE ──────────────────────────────────────────────────────
function toggleLike(id) {
  const song = state.songs.find(s=>s.id===id);
  if (!song) return;
  const idx = state.likedSongs.findIndex(s=>s.id===id);
  if (idx>=0) state.likedSongs.splice(idx,1); else state.likedSongs.unshift(song);
  triggerSimilar(id);
  refreshLikeBtns(id);
  renderLiked();
}
function isLiked(id) { return state.likedSongs.some(s=>s.id===id); }
function refreshLikeBtns(id) {
  const liked = isLiked(id);
  ['lc-','ls-','lr-'].forEach(p => {
    const el = document.getElementById(p+id);
    if (el) { el.textContent=liked?'♥':'♡'; el.classList.toggle('liked',liked); }
  });
}
function renderLiked() {
  document.getElementById('liked-count').textContent = state.likedSongs.length;
  const list = document.getElementById('liked-list');
  if (!state.likedSongs.length) { list.innerHTML='<p class="empty-sidebar">No liked songs yet</p>'; return; }
  list.innerHTML = state.likedSongs.map(s=>`
    <div class="sidebar-song-row">
      <img src="${s.cover}" alt="${e(s.title)}"/>
      <div class="sidebar-song-info">
        <div class="s-title">${e(s.title)}</div>
        <div class="s-artist">${e(s.artist)}</div>
      </div>
      <span style="color:#ec4899;font-size:10px">♥</span>
    </div>`).join('');
}

// ── PLAYLISTS ─────────────────────────────────────────────────
function showCreateForm() {
  document.getElementById('btn-create-playlist').classList.add('hidden');
  document.getElementById('create-playlist-form').classList.remove('hidden');
  document.getElementById('new-playlist-name').focus();
}
function confirmCreatePlaylist() {
  const name = document.getElementById('new-playlist-name').value.trim();
  if (name) createPlaylist(name);
  cancelCreatePlaylist();
}
function cancelCreatePlaylist() {
  document.getElementById('new-playlist-name').value='';
  document.getElementById('create-playlist-form').classList.add('hidden');
  document.getElementById('btn-create-playlist').classList.remove('hidden');
}
function createPlaylist(name) {
  const id = `pl-${++state.plCounter}-${Date.now()}`;
  state.playlists.push({id, name, songs:[]}); renderPlaylists(); return id;
}
function renamePlaylist(id) {
  const pl = state.playlists.find(p=>p.id===id);
  const n = prompt('Rename playlist:', pl?.name);
  if (n?.trim()) { pl.name=n.trim(); renderPlaylists(); }
}
function deletePlaylist(id) {
  state.playlists = state.playlists.filter(p=>p.id!==id); renderPlaylists();
}
function addToPlaylist(plId, songId) {
  const pl = state.playlists.find(p=>p.id===plId);
  const song = state.songs.find(s=>s.id===songId);
  if (!pl||!song||pl.songs.some(s=>s.id===songId)) return;
  pl.songs.unshift(song); renderPlaylists(); refreshAddBtns(songId);
}
function removeFromPlaylist(plId, songId) {
  const pl = state.playlists.find(p=>p.id===plId);
  if (!pl) return; pl.songs=pl.songs.filter(s=>s.id!==songId);
  renderPlaylists(); refreshAddBtns(songId);
}
function isInPl(id) { return state.playlists.some(p=>p.songs.some(s=>s.id===id)); }
function refreshAddBtns(id) {
  const added = isInPl(id);
  ['ac-','as-','ar-'].forEach(p => {
    const el = document.getElementById(p+id);
    if (el) { el.textContent=added?'✓':'+'; el.classList.toggle('added',added); }
  });
}
function togglePl(id) { state.expandedPl = state.expandedPl===id ? null : id; renderPlaylists(); }
function renderPlaylists() {
  document.getElementById('playlist-count').textContent = state.playlists.length;
  const list = document.getElementById('playlists-list');
  if (!state.playlists.length) { list.innerHTML='<p class="empty-sidebar">No playlists yet</p>'; return; }
  list.innerHTML = state.playlists.map(pl => {
    const exp = state.expandedPl===pl.id;
    return `<div class="playlist-item">
      <div class="playlist-header" onclick="togglePl('${pl.id}')">
        <span class="pl-chevron">${exp?'▼':'▶'}</span>
        <span class="pl-name">${e(pl.name)}</span>
        <span class="pl-count">${pl.songs.length}</span>
        <div class="pl-actions">
          <button class="pl-action-btn" onclick="renamePlaylist('${pl.id}');event.stopPropagation()" title="Rename">✎</button>
          <button class="pl-action-btn del" onclick="deletePlaylist('${pl.id}');event.stopPropagation()" title="Delete">✕</button>
        </div>
      </div>
      ${exp?`<div class="playlist-songs">${!pl.songs.length?'<p class="empty-sidebar">Empty</p>':pl.songs.map(s=>`
        <div class="sidebar-song-row">
          <img src="${s.cover}" alt="${e(s.title)}"/>
          <div class="sidebar-song-info">
            <div class="s-title">${e(s.title)}</div>
            <div class="s-artist">${e(s.artist)}</div>
          </div>
          <button class="del-song" onclick="removeFromPlaylist('${pl.id}','${s.id}')">✕</button>
        </div>`).join('')}</div>`:''}</div>`;
  }).join('');
}

// ── PLAYLIST MODAL ────────────────────────────────────────────
function openModal(songId) {
  state.pendingSong = songId;
  document.getElementById('modal-playlists').innerHTML = !state.playlists.length
    ? '<p style="padding:9px 12px;font-size:11px;color:#555">No playlists yet</p>'
    : state.playlists.map(pl => {
        const already = pl.songs.some(s=>s.id===songId);
        return `<div class="modal-pl-item ${already?'already':''}" onclick="${already?'':` pickPl('${pl.id}')`}">
          <span>${e(pl.name)}</span>${already?'<span style="color:#a855f7;font-size:11px">✓</span>':''}
        </div>`;
      }).join('');
  document.getElementById('modal-new-name').value='';
  document.getElementById('playlist-modal').classList.remove('hidden');
}
function pickPl(plId) { if(state.pendingSong) addToPlaylist(plId, state.pendingSong); closePlaylistModal(); }
function closePlaylistModal() { document.getElementById('playlist-modal').classList.add('hidden'); state.pendingSong=null; }
function modalCreatePlaylist() {
  const name = document.getElementById('modal-new-name').value.trim();
  if (name && state.pendingSong) { const id=createPlaylist(name); addToPlaylist(id, state.pendingSong); closePlaylistModal(); }
}

// ── UTILS ─────────────────────────────────────────────────────
function e(str) { return String(str||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

Object.assign(window, {
  switchTab, pickColor, pickEditColor, openProfileModal, closeProfileModal, saveUserData,
  toggleFilter, clearFilters, triggerSimilar, toggleLike, playOnYouTube,
  openModal, pickPl, closePlaylistModal, modalCreatePlaylist,
  confirmCreatePlaylist, cancelCreatePlaylist,
  renamePlaylist, deletePlaylist, removeFromPlaylist, togglePl,
});
