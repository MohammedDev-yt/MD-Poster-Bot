
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:050505,50:6A00FF,100:00C8FF&height=180&section=header&text=UNIVERSAL%20POSTER%20BOT&fontSize=35&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Developed%20By%20Mohammed&descAlignY=60&descSize=16" width="100%">
</p>

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=36BCF7F1&width=435&lines=Welcome+To+Universal+Poster+Bot;Your+Ultimate+Poster+Search+Bot;TMDb+Logo-Driven+Poster+System;Bot+is+Made+By+Mohammed)](https://git.io/typing-svg)

<p align="center">
  <a href="https://github.com/MohammedDev-yt/MD-Poster-Bot/stargazers"><img src="https://img.shields.io/github/stars/MohammedDev-yt/MD-Poster-Bot?style=for-the-badge&logo=github&color=f43f8e&logoColor=white" alt="Stars"/></a>
  <a href="https://github.com/MohammedDev-yt/MD-Poster-Bot/network/members"><img src="https://img.shields.io/github/forks/MohammedDev-yt/MD-Poster-Bot?style=for-the-badge&logo=github&color=a855f7&logoColor=white" alt="Forks"/></a>
  <a href="https://github.com/MohammedDev-yt/MD-Poster-Bot/issues"><img src="https://img.shields.io/github/issues/MohammedDev-yt/MD-Poster-Bot?style=for-the-badge&logo=github&color=7c3aed&logoColor=white" alt="Issues"/></a>
  <a href="https://github.com/MohammedDev-yt/MD-Poster-Bot/pulls"><img src="https://img.shields.io/github/issues-pr/MohammedDev-yt/MD-Poster-Bot?style=for-the-badge&logo=github&color=ec4899&logoColor=white" alt="Pull Requests"/></a>
  <a href="https://github.com/MohammedDev-yt/MD-Poster-Bot/commits"><img src="https://img.shields.io/github/last-commit/MohammedDev-yt/MD-Poster-Bot?style=for-the-badge&logo=github&color=6366f1&logoColor=white" alt="Last Commit"/></a>
  <a href="https://github.com/MohammedDev-yt/MD-Poster-Bot/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/MohammedDev-yt/MD-Poster-Bot?style=for-the-badge&logo=mit&color=22c55e&logoColor=white" alt="License"/>
  </a>
  <a href="https://www.python.org/" target="_blank">
    <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11"/>
  </a>
  <a href="https://github.com/eternnoir/pyTelegramBotAPI" target="_blank">
    <img src="https://img.shields.io/badge/Framework-TeleBot-brightgreen?style=for-the-badge&logo=telegram&logoColor=white" alt="TeleBot"/>
  </a>
  <a href="https://www.mongodb.com/" target="_blank">
    <img src="https://img.shields.io/badge/Database-MongoDB-green?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB"/>
  </a>
  <a href="https://www.themoviedb.org/" target="_blank">
    <img src="https://img.shields.io/badge/API-TMDb-blueviolet?style=for-the-badge&logo=themoviedb&logoColor=white" alt="TMDb"/>
  </a>
  <a href="https://t.me/Mr_Mohammed_29" target="_blank">
    <img src="https://img.shields.io/badge/Developer-Mohammed-purple?style=for-the-badge&logo=telegram&logoColor=white" alt="Developer"/>
  </a>
  <a href="https://t.me/Aero_Unity" target="_blank">
    <img src="https://img.shields.io/badge/Updates-Aero_Unity-blueviolet?style=for-the-badge&logo=telegram&logoColor=white" alt="Updates"/>
  </a>
</p>

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

## ✨ Features

- 🎬 **Universal Title Search:** Search movies, TV series, anime, and regional dramas instantly.
- 🖼️ **Logo-Driven Poster Layouts:** Automatically overlays official TMDb title logos on high-resolution landscape banners with clean blurring and padding.
- 📱 **Dual Orientation Links:** Generates both landscape banner links and tall portrait poster preview links.
- 📑 **Interactive Pagination:** Browse multiple backdrop options seamlessly with inline pagination controls (`<< < 1/N > >>`).
- 📊 **Detailed IMDb Lookup:** Fetch rich metadata cards, genres, ratings, and storylines using `/imdb`.
- 🔒 **Force Subscription Support:** Require users to join specific update/support channels before accessing the bot.
- 📢 **Advanced Broadcast System:** Broadcast text, photos, videos, GIFs, stickers, and interactive inline buttons with `/broadcast`, `/broadcastpin`, and `/broadcastunpin`.
- 🗄️ **MongoDB & SQLite Fallback:** Flexible database backend with automatic user tracking on `/start`.
- 🛡️ **Admin & Security Management:** Ban/unban users, configure PM search toggle (`/pmsearch`), and restrict PM queries to authorized groups.
- 🌐 **Persistent Flask Web Server:** Keeps the web service active 24/7 with reliable cached image file serving.

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

## ✨ Commands

### 👤 User & Owner Commands

```text
start - Start the bot & register in database
help - Show detailed search and usage instructions
imdb [Title] - Get detailed metadata card and IMDb ratings
pmsearch - Toggle global PM search mode [Owner only]
broadcast - Broadcast message with buttons to all users [Owner only]
broadcastpin - Broadcast message, pin it, and notify users [Owner only]
broadcastunpin - Broadcast, pin, and unpin message [Owner only]
stats - View total users and stats list [Owner only]
ban - Ban a user ID [Owner only]
unban - Unban a user ID [Owner only]
banlist - View banned users list [Owner only]
addforcesub - Add force subscription channel [Owner only]
removeforce - Remove force subscription channel [Owner only]
fsublist - View force subscription channels [Owner only]
```

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

<details>
<summary><h2> Click Here Development & Deployment</h2></summary>

Welcome to the development documentation of Universal Poster Bot.

📁 Repository Structure
```
MD-Poster-Bot/
│
├── poster_cache/         # Cached landscape and portrait posters
├── database.py           # MongoDB & SQLite database interface
├── bot.py                # Main Telegram bot & Flask server
├── Dockerfile            # Docker container configuration
├── requirements.txt      # Python dependencies
└── render.yml            # Render deployment configuration
```

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

<details>

<summary><b>Click Here To Expand Variables</b></summary>

| Variable        | Description                                |
| --------------- | ------------------------------------------ |
| `BOT_TOKEN`     | Telegram Bot Token from BotFather          |
| `TMDB_API_KEY`  | TMDb API Key for fetching posters and metadata |
| `MONGO_URI`     | MongoDB Connection String                  |
| `POSTER_GROUP_URL`  | Telegram group link for restricted PM searches |
| `RENDER_EXTERNAL_URL` | External app URL for direct image links |
| `PORT`           | Web server port (Default: 5000)  | 

```
#Example Environment Configuration

BOT_TOKEN = YOUR_BOT_TOKEN_HERE
TMDB_API_KEY = YOUR_TMDB_API_KEY_HERE
MONGO_URI = mongodb+srv://username:password@cluster.mongodb.net/
POSTER_GROUP_URL = [https://t.me/+VXY_za8DNjQzYmVl](https://t.me/+VXY_za8DNjQzYmVl)
RENDER_EXTERNAL_URL = Your Deployed App URL
PORT = 5000 or 8080
```
</details>


🚀 <summary><b>DEPLOYMENT GUIDE</summary></b>

1. Deploy on Render
<p align="left">
<a href="https://render.com/">
<img src="https://img.shields.io/badge/🚀%20Deploy%20on%20Render-6A00FF?style=for-the-badge&logo=render">
</a>
</p>

2. Deploy on Koyeb
<p align="left">
<a href="https://app.koyeb.com/">
<img src="https://img.shields.io/badge/🚀%20Deploy%20on%20Koyeb-000000?style=for-the-badge&logo=koyeb&logoColor=white">
</a>
</p>

3. Deploy on Railway
<p align="left">
<a href="https://railway.app/">
<img src="https://img.shields.io/badge/🚀%20Deploy%20on%20Railway-131415?style=for-the-badge&logo=railway&logoColor=white">
</a>
</p>

4. Deploy On Heroku 
<p align="left">
<a href="https://heroku.com/">
<img src="https://img.shields.io/badge/🚀%20Deploy%20on%20Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white">
</a>
</p>

5. Deploy via Docker
<p align="left">
<img src="https://img.shields.io/badge/🚀%20Deploy%20via%20Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white">
</p>

Build and run the container locally or on a server using Docker:

```
#Build docker image
docker build -t universal-poster-bot .
```

```
#Run container with environment variables
docker run -d \
  -e BOT_TOKEN="your_bot_token" \
  -e TMDB_API_KEY="your_tmdb_key" \
  -e MONGO_URI="your_mongo_uri" \
  -p 5000:5000 \
  --name poster-bot universal-poster-bot
```

6. Deploy on VPS / Local Machine
<p align="left">
<img src="https://img.shields.io/badge/🚀%20Deploy%20on%20VPS/Local-00599C?style=for-the-badge&logo=linux&logoColor=white">
</p>

```
#Clone repository
git clone [https://github.com/MohammedDev-yt/MD-Poster-Bot.git](https://github.com/MohammedDev-yt/MD-Poster-Bot.git)
cd MD-Poster-Bot

#Create virtual environment
python3 -m venv venv
source venv/bin/activate

#Install requirements
pip install -r requirements.txt

#Run bot
python bot.py
```
</details>

> [!NOTE]
>  * ⚠️ Never publish your actual BOT_TOKEN or TMDB_API_KEY on GitHub.
>
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

> [!CAUTION]
>  * Never share your BOT_TOKEN.
>  * Keep your TMDB_API_KEY and MONGO_URI private.
>  * Use environment variables for sensitive credentials.
>

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

> [!WARNING]
> DON'T REMOVE MY CREDIT...
>  * Developer: @Mr_Mohammed_29
>  * Updates: @Aero_Unity
>  * Support: @Coders_Grp
>
 
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

⭐ Fork and ⭐ this repo
If you like this bot, give it a ⭐ on GitHub to support the project!
<p align="center">
<b>Made with ❤️ by Mohammed</b>

📩 Contact: <a href="https://t.me/Mr_Mohammed_29">Mohammed</a>
</p>
<p align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:050505,50:6A00FF,100:00C8FF&height=120&section=footer"/>
</p>

