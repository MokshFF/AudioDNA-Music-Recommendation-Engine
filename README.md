# 🎵 AudioDNA — Music Discovery Engine

> AI-powered music discovery with KNN recommendations, user profiles, and YouTube playback.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat&logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![HTML CSS JS](https://img.shields.io/badge/Frontend-HTML%20%2B%20CSS%20%2B%20JS-E34F26?style=flat&logo=html5&logoColor=white)
![YouTube](https://img.shields.io/badge/Playback-YouTube-FF0000?style=flat&logo=youtube&logoColor=white)

---

## ✨ Features

### 🤖 AI / ML
- **KNN Cosine Similarity** — finds similar songs using K-Nearest Neighbors across 8 audio features (energy, danceability, valence, tempo + encoded genre/mood/country/artist)
- **Content-Based Filtering** — weighted multi-feature ML recommendations (genre 3×, mood 2.5×, artist 2×, country 1×)
- **Live AI Mood Analysis Panel** — real-time audio feature vector display with animated progress bars

### 🎵 Music
- **310 famous songs** — Indian (Arijit Singh, Shreya Ghoshal, AR Rahman, Badshah, Atif Aslam, Kishore Kumar, Lata Mangeshkar, Neha Kakkar…) + English (The Weeknd, Ed Sheeran, Taylor Swift, Adele, Drake, Eminem, BTS, BLACKPINK, Coldplay, Queen, Michael Jackson, Bruno Mars…)
- Genres: Pop, Rock, Hip Hop, R&B, EDM, Jazz, Classical, Sufi, Bhangra, Reggaeton, Indie, Afrobeat
- **YouTube playback** — every Play button opens the song directly on YouTube

### 👤 User Profiles
- **Register** with name, bio, location, favourite genre & mood, custom avatar color
- **Login** automatically restores your full library (liked songs + playlists)
- **Edit profile** — update name, bio, location, avatar color, change password
- **Sync Library** — saves your liked songs & playlists to your account on the server
- All profiles stored in `profiles.json` — no database required

### 📋 Library Management
- ❤️ Like / unlike songs → auto-triggers KNN similar song discovery
- 📁 Create, rename, delete playlists
- ➕ Add / remove songs from any playlist
- Left sidebar shows all playlists (expandable) and liked songs

### 🔍 Search & Filters
- Live search across all 310 songs (by title or artist)
- Filter by Genre, Mood, Country, Artist
- Filters chain together for precise AI recommendations

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/AudioDNA.git
cd AudioDNA
```

### 2. Install dependencies
```bash
pip install flask scikit-learn numpy
```

### 3. Run the server
```bash
python app.py
```

### 4. Open in your browser
```
http://localhost:5000
```

> Create an account on the login page — your profile, liked songs, and playlists save automatically.

---

## 📁 Project Structure
```
AudioDNA/
├── app.py                  ← Flask backend + scikit-learn ML engine
├── requirements.txt        ← Python dependencies
├── profiles.json           ← User profiles (auto-created on first register)
├── templates/
│   └── index.html          ← Full Single Page App (login/register + dashboard)
└── static/
    ├── css/
    │   └── style.css       ← Dark glassmorphism UI (Syne + DM Sans fonts)
    └── js/
        └── app.js          ← Vanilla JavaScript frontend
```

---

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/songs` | All 310 songs + genres, moods, countries |
| `GET` | `/api/similar/:id` | KNN similar songs with similarity scores |
| `GET` | `/api/recommend` | ML filtered recommendations (`?genre=&mood=&country=&artist=`) |
| `GET` | `/api/mood-vector/:id` | Audio feature vector for a song |
| `GET` | `/api/search?q=` | Live search by title or artist |
| `GET` | `/api/artists-by-country/:country` | All artists for a country |
| `POST` | `/api/register` | Create new user profile |
| `POST` | `/api/login` | Login + restore saved library |
| `POST` | `/api/logout` | Logout |
| `GET` | `/api/profile` | Get current user's profile |
| `PUT` | `/api/profile` | Update profile info / change password |
| `PUT` | `/api/profile/data` | Sync liked songs + playlists to server |

---

## 🧠 ML Architecture

### KNN Cosine Similarity (Similar Songs)
```
Feature vector per song (8 dimensions):
  genre_encoded  × 3.0
  mood_encoded   × 2.5
  country_enc    × 1.0
  artist_encoded × 2.0
  energy         × 2.0
  danceability   × 1.5
  valence        × 1.5
  tempo / 200    × 1.0

Model: sklearn NearestNeighbors(metric='cosine', n_neighbors=10)
Output: top-8 similar songs with similarity score 0.0 → 1.0
```

### Content-Based Filtering (Recommendations)
```
Weighted scoring per active filter:
  genre match   → +3.0 points
  mood match    → +2.5 points
  artist match  → +2.0 points
  country match → +1.0 point

Output: top-8 songs sorted by total score
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10+, Flask 3.0 |
| ML / AI | scikit-learn (KNN, LabelEncoder), NumPy |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| UI Design | Dark Glassmorphism, Syne + DM Sans (Google Fonts) |
| Playback | YouTube (auto-generated search URL) |
| User Storage | JSON file (`profiles.json`) |

---

## 🎨 UI Preview

- 🌑 **Dark glassmorphism** design with animated gradient orbs
- 🎛️ Three-panel layout — Playlists sidebar · Song grid · Filter sidebar  
- 📊 AI mood analysis bar charts per song
- 🔴 Red YouTube badges on every play button
- 👤 Animated avatar button with your initials + chosen color

---

## 📄 License

MIT License — free to use, modify and distribute.

---

**Made with ❤️ + AI by Moksh**
```

---

## ⭐ Topics / Tags
*(Add these in the GitHub repo Settings → Topics for better discoverability)*
```
python  flask  machine-learning  music  scikit-learn  knn  recommendation-system  html  css  javascript  youtube  bollywood  ai  music-discovery
