# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

import os
import io
import re
import html
import telebot
import requests
import database 
import threading

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

from flask import Flask, send_file, request
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageDraw, ImageFont,ImageFilter, ImageOps

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
POSTER_GROUP_URL = os.environ.get("POSTER_GROUP_URL", "https://t.me/+VXY_za8DNjQzYmVl")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

database.init_db()
session = requests.Session()
SEARCH_CACHE = {}
IMDB_SEARCH_CACHE = {}
CACHE_DIR = "poster_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
OWNER_ID = 7284759394 #replace your Telegram ID 

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

# Custom Image URLs
START_IMAGE_URL = "https://telegra.ph/file/2ab528ba65c23832cdcf6-4ff26f1b433ef961eb.jpg"
ABOUT_IMAGE_URL = "https://graph.org/file/283e03b08d8306b8d85af-8436c3be9697b2374c.jpg"
FSUB_IMAGE_URL  = "https://graph.org/file/faf795187aa693e1024a4-746b376c8dcc889d4f.jpg"

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@app.route('/')
def home():
    return "Mohammed Poster Bot is Running 24/7! Enjoy 🎊"

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@app.route('/poster/<item_id>')
def serve_poster(item_id):
    """Flask route to reliably serve the cached poster image file (landscape or portrait)."""
    poster_type = request.args.get('type', 'landscape')

    filename = f"{item_id}_portrait.jpg" if poster_type == 'portrait' else f"{item_id}.jpg"
    file_path = os.path.join(CACHE_DIR, filename)

    if os.path.exists(file_path):
        return send_file(file_path, mimetype='image/jpeg')

    fallback_path = os.path.join(CACHE_DIR, f"{item_id}.jpg")
    if os.path.exists(fallback_path):
        return send_file(fallback_path, mimetype='image/jpeg')

    return "poster not found or expired.", 404

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def is_user_member(user_id):
    channels = database.get_fsub_channels()
    if not channels:
        return True
    for channel in channels:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception:
            pass
    return True

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def send_fsub_prompt(chat_id):
    channels = database.get_fsub_channels()
    markup = telebot.types.InlineKeyboardMarkup()
    for channel in channels:
        channel_name = channel.replace("@", "")
        markup.add(telebot.types.InlineKeyboardButton(text=f"• Jᴏɪɴ {channel} •", url=f"https://t.me/{channel_name}"))

    markup.add(telebot.types.InlineKeyboardButton(text="• ᴄʜᴇᴄᴋ sᴜʙsᴄʀɪᴘᴛɪᴏɴ •", callback_data="check_fsub"))

    fsub_text = (
        " <b>ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ</b>\n\n"
        "<b>›› ‼️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ᴛᴏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ, sᴜʙsᴄʀɪʙᴇ ɴᴏw...</b>\n"
        "<b>ᴀғᴛᴇʀ Jᴏɪɴɪɴɢ, ᴄʟɪᴄᴋ <i>ᴄʜᴇᴄᴋ sᴜʙsᴄʀɪᴘᴛɪᴏɴ</i> ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.</b>"
    )
    try:
        bot.send_photo(chat_id, FSUB_IMAGE_URL, caption=fsub_text, parse_mode="HTML", reply_markup=markup)
    except Exception:
        bot.send_message(chat_id, fsub_text, parse_mode="HTML", reply_markup=markup)

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@bot.message_handler(commands=['help'])
def help_command(message):
    user_id = message.from_user.id
    database.add_user(user_id, message.from_user.first_name or "user")

    if database.is_banned(user_id):
        return

    if not is_user_member(user_id):
        send_fsub_prompt(message.chat.id)
        return

    help_text = (
        "<b>📖 <u>How To Search & Use Aero Poster Bot</u></b>\n\n"
        "<b>1️⃣ Direct Title Search:</b>\n"
        "Just send any title to get poster images.\n"
        "<i>Example:</i> <code>Doomsday</code>\n\n"
        "<b>2️⃣ Title + Year Search:</b>\n"
        "Narrow down to a specific release year.\n"
        "<i>Example:</i> <code>Doomsday 2026</code>\n\n"
        "<b>3️⃣ TV Series / Season Search:</b>\n"
        "Specify the season number for TV shows.\n"
        "<i>Example:</i> <code>The Mentalist S01</code> or <code>Stranger Things Season 2</code>\n\n"
        "<b>4️⃣ Language & Regional Search:</b>\n"
        "Add a language tag anywhere in your query to filter regional movies/dramas.\n"
        "<i>Example:</i> <code>Crush Kdrama</code>, <code>Crush 2024 Chi</code>, or <code>Doomsday English</code>\n\n"
        "<b>🌐 <u>Supported Language Keywords:</u></b>\n"
        "• <b>Korean:</b> <code>kdrama</code>, <code>k-drama</code>, <code>korean</code>, <code>kr</code>\n"
        "• <b>Chinese:</b> <code>chi</code>, <code>cdrama</code>, <code>chinese</code>, <code>mandarin</code>, <code>zh</code>\n"
        "• <b>Japanese:</b> <code>jdrama</code>, <code>j-drama</code>, <code>japanese</code>, <code>jap</code>, <code>anime</code>, <code>ja</code>\n"
        "• <b>Indian:</b> <code>hindi</code>, <code>tamil</code>, <code>telugu</code>, <code>malayalam</code>, <code>kannada</code>, <code>bengali</code>, <code>marathi</code>, <code>punjabi</code>\n"
        "• <b>Global:</b> <code>english</code>, <code>spanish</code>, <code>french</code>, <code>german</code>, <code>italian</code>, <code>russian</code>, <code>portuguese</code>, <code>turkish</code>, <code>arabic</code>, <code>thai</code>\n\n"
        "<b>🎬 <u>IMDb Info Lookup:</u></b>\n"
        "Use <code>/imdb [Title]</code> to get detailed metadata cards and ratings."
    )

    markup = InlineKeyboardMarkup(row_width=2)
    dev_btn = InlineKeyboardButton(text="• ᴅᴇᴠᴇʟᴏᴘᴇʀ •", url="https://t.me/Mr_Mohammed_29")
    support_btn = InlineKeyboardButton(text="• sᴜᴘᴘᴏʀᴛ •", url="https://t.me/Coders_Grp")
    close_btn = InlineKeyboardButton(text="• ᴄʟᴏsᴇ •", callback_data="imdb_close")

    markup.row(dev_btn, support_btn)
    markup.row(close_btn)

    try:
        bot.send_message(message.chat.id, help_text, parse_mode="HTML", reply_markup=markup)
    except Exception as e:
        print(f"Error sending help message: {e}")

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "user"
    database.add_user(user_id, first_name)

    if database.is_banned(user_id):
        bot.reply_to(message, " <b>you are banned from using this bot.</b>", parse_mode="HTML")
        return

    if not is_user_member(user_id):
        send_fsub_prompt(message.chat.id)
        return

    welcome_text = (
        "👋 <b>Wᴇʟᴄᴏᴍᴇ Tᴏ Uɴɪᴠᴇʀsᴀʟ Pᴏsᴛᴇʀ Bᴏᴛ</b>\n\n"
        "<b>𝗌𝖾𝗇𝖽 𝗆𝖾 𝖺𝗇𝗒 𝗍𝗂𝗍𝗅𝖾 (𝗆𝗈𝗏𝗂𝖾𝗌, 𝗌𝖾𝗋𝗂𝖾𝗌, 𝖺𝗇𝗂𝗆𝖾, 𝗄-𝖽𝗋𝖺𝗆𝖺𝗌, 𝖾𝗍𝖼.), "
        "𝖺𝗇𝖽 𝗂 𝗐𝗂𝗅𝗅 𝗀𝖾𝗇𝖾𝗋𝖺𝗍𝖾 𝗍𝗁𝖾 𝗉𝗈𝗌𝗍𝖾𝗋 𝗅𝖺𝗒𝗈𝗎𝗍 𝖿𝗈𝗋 𝗒𝗈𝗎</b>\n\n"
        "<b>Pᴏᴡᴇʀᴇᴅ Bʏ : <a href=\"https://t.me/Aero_Unity\">Aᴇʀᴏ Uɴɪᴛʏ</a></b>"
    )

    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    about_btn = telebot.types.InlineKeyboardButton(text="• Aʙᴏᴜᴛ •", callback_data="btn_about")
    updates_btn = telebot.types.InlineKeyboardButton(text="• Uᴘᴅᴀᴛᴇs •", url="https://t.me/Aero_Unity")
    owner_btn = telebot.types.InlineKeyboardButton(text="• Oᴡɴᴇʀ •", url="https://t.me/Mr_Mohammed_29")

    markup.row(about_btn, updates_btn)
    markup.row(owner_btn)

    try:
        bot.send_photo(message.chat.id, START_IMAGE_URL, caption=welcome_text, parse_mode="HTML", reply_markup=markup)
    except Exception:
        bot.send_message(message.chat.id, welcome_text, parse_mode="HTML", reply_markup=markup)

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@bot.message_handler(commands=['pmsearch'])
def toggle_pm_search(message):
    user_id = message.from_user.id

    if user_id != OWNER_ID:
        bot.reply_to(message, " <b>ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ: ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ sᴇɴᴘᴀɪ</b>", parse_mode="HTML")
        return

    args = message.text.strip().split()
    if len(args) > 1:
        action = args[1].lower()
        if action in ['on', 'enable', 'true', '1']:
            database.set_global_pm_search(True)
            bot.reply_to(message, "✅ <b>pm search enabled for users!</b>", parse_mode="HTML")
        elif action in ['off', 'disable', 'false', '0']:
            database.set_global_pm_search(False)
            bot.reply_to(message, "🔒 <b>pm search disabled for users!</b>", parse_mode="HTML")
        else:
            bot.reply_to(message, "⚠️ usage: <code>/pmsearch on</code> or <code>/pmsearch off</code>", parse_mode="HTML")
    else:
        status = database.get_global_pm_search()
        status_str = "🟢 <b>on</b>" if status else "🔴 <b>off</b>"
        bot.reply_to(message, f" <b>PM Sᴇᴀʀᴄʜ Sᴛᴀᴛᴜs:</b> {status_str}", parse_mode="HTML")

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@bot.callback_query_handler(func=lambda call: True)
def handle_all_callbacks(call):
    user_id = call.from_user.id
    
    if database.is_banned(user_id):
        bot.answer_callback_query(call.id, " you are banned from using this bot.", show_alert=True)
        return
    
    if call.data.startswith("p_") or call.data == "noop":
        if call.data == "noop":
            bot.answer_callback_query(call.id)
            return
        
        parts = call.data.split("_")
        search_id = parts[1]
        index = int(parts[2])

        photo_url, caption, markup = build_poster_page(search_id, index)
        if photo_url:
            try:
                bot.edit_message_media(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    media=telebot.types.InputMediaPhoto(photo_url, caption=caption, parse_mode="HTML"),
                    reply_markup=markup
                )
            except Exception as e:
                print(f"Pagination edit error: {e}")
                
        bot.answer_callback_query(call.id)
        return
        
    if call.data.startswith("imdb_select_") or call.data == "imdb_close":
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass

        if call.data == "imdb_close":
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception:
                pass
            return

        parts = call.data.split("_")
        if len(parts) < 4:
            return
            
        search_id = parts[2]
        item_idx = int(parts[3])

        search_items = IMDB_SEARCH_CACHE.get(search_id)
        if not search_items or item_idx >= len(search_items):
            try:
                bot.answer_callback_query(call.id, "Session expired, please search again.", show_alert=True)
            except Exception:
                pass
            return

        selected_item = search_items[item_idx]
        item_id = selected_item.get("id")
        media_type = selected_item.get("media_type", "movie")

        endpoint = "movie" if media_type == "movie" else "tv"
        details_url = f"https://api.themoviedb.org/3/{endpoint}/{item_id}?api_key={TMDB_API_KEY}&append_to_response=external_ids"
        
        try:
            det_res = session.get(details_url, timeout=5)
            if det_res.status_code == 200:
                details = det_res.json()
                
                title = details.get("title") or details.get("name") or "Unknown"
                release_date = details.get("release_date") or details.get("first_air_date") or ""
                year = release_date.split("-")[0] if release_date else "N/A"
                rating = details.get("vote_average", "N/A")
                if rating != "N/A":
                    rating = f"{round(rating, 1)} / 10"

                rel_info = release_date if release_date else "N/A"
                genres = [f"#{g['name'].replace(' ', '')}" for g in details.get("genres", [])]
                genre_str = ", ".join(genres) if genres else "N/A"

                spoken_langs = [f"#{l.get('english_name', l.get('name')).replace(' ', '')}" for l in details.get("spoken_languages", [])]
                lang_str = ", ".join(spoken_langs) if spoken_langs else "N/A"

                countries = [f"#{c.get('name').replace(' ', '_')}" for c in details.get("production_countries", [])]
                country_str = ", ".join(countries) if countries else "N/A"

                overview = details.get("overview", "No storyline available.")

                external_ids = details.get("external_ids", {})
                imdb_id = external_ids.get("imdb_id")
                imdb_link = f"https://www.imdb.com/title/{imdb_id}" if imdb_id else "https://www.imdb.com"

                poster_path = details.get("poster_path") or details.get("backdrop_path")
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

                caption_lines = [
                    f"• 🎬 <b>{html.escape(title)}</b> [{year}]",
                    f"• ⭐ <b>IMDb Rating:</b> {rating}",
                    f"• 📅 <b>Release Info:</b> {rel_info}",
                    f"• 🎭 <b>Genre:</b> {genre_str}",
                    f"• 🌐 <b>Language:</b> {lang_str}",
                    f"• 🏳️ <b>Country of Origin:</b> {country_str}\n",
                    f"• 📖 <b>Storyline:</b>\n<i>{html.escape(overview)}</i>"
                ]
                caption_text = "\n".join(caption_lines)

                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton(text="• ɪᴍᴅʙ ɪᴍᴀɢᴇ •", url=imdb_link))

                try:
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                except Exception:
                    pass

                if poster_url:
                    bot.send_photo(
                        chat_id=call.message.chat.id,
                        photo=poster_url,
                        caption=caption_text,
                        parse_mode="HTML",
                        reply_markup=markup
                    )
                else:
                    bot.send_message(
                        chat_id=call.message.chat.id,
                        text=caption_text,
                        parse_mode="HTML",
                        reply_markup=markup
                    )
        except Exception as e:
            print(f"IMDb details error: {e}")
        return

    if call.data == "cancel_session":
        try:
            bot.answer_callback_query(call.id, "Session cancelled.")
        except Exception:
            pass
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        return

    if call.data.startswith("media_card_"):
        parts = call.data.split("_")
        search_id = parts[2]
        target_index = int(parts[3])

        data = SEARCH_CACHE.get(search_id)
        if not data:
            try:
                bot.answer_callback_query(call.id, "Session expired, please search again.", show_alert=True)
            except Exception:
                pass
            return

        artworks = data["artworks"]
        posters = data["posters"]
        total_pages = len(artworks)
        current_index = target_index % total_pages

        caption_text = (
            f"<b>{html.escape(data['title'])}</b> ❞\n\n"
            f"» <b>Type:</b> {data.get('type', 'Manhwa')}\n"
            f"» <b>Average Rating:</b> {data['rating']}\n"
            f"» <b>Status:</b> {data['status']}\n"
            f"» <b>Chapters:</b> {data['chapters']}\n"
            f"» <b>Genres:</b> {html.escape(data['genres'])}\n\n"
            f"▶ <u><b>SYNOPSIS</b></u>\n"
            f"<b>➔</b> <i>{html.escape(data['synopsis'][:400])}...</i> ❞"
        )

        try:
            img_bytes = session.get(artworks[current_index], timeout=5).content
            p_bytes_list = []
            for p_url in posters[:2]:
                try:
                    p_bytes_list.append(session.get(p_url, timeout=4).content)
                except Exception:
                    p_bytes_list.append(img_bytes)

            genres_list = [g.strip() for g in data["genres"].split(",")]
            card_io = generate_custom_media_card(
                img_bytes, p_bytes_list, data["title"], genres_list,
                data["synopsis"], logo_url=data["logo_url"], branding="Manga Aero"
            )

            markup = InlineKeyboardMarkup()
            prev_idx = (current_index - 1) % total_pages
            next_idx = (current_index + 1) % total_pages

            markup.row(
                InlineKeyboardButton(text="◀ ᴘʀᴇᴠ •", callback_data=f"media_card_{search_id}_{prev_idx}"),
                InlineKeyboardButton(text=f"{current_index+1:02d}/{total_pages:02d}", callback_data="noop"),
                InlineKeyboardButton(text="• ɴᴇxᴛ ▶", callback_data=f"media_card_{search_id}_{next_idx}")
            )
            markup.row(InlineKeyboardButton(text="• ᴄᴀɴᴄᴇʟ •", callback_data="cancel_session"))

            bot.edit_message_media(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                media=telebot.types.InputMediaPhoto(card_io, caption=caption_text, parse_mode="HTML"),
                reply_markup=markup
            )
        except Exception as e:
            print(f"Media card update error: {e}")

        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        return

    if call.data == "check_fsub":
        if is_user_member(user_id):
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception:
                pass
            
            welcome_text = (
                "✅ <b>VᴇʀɪғɪᴄᴀᴛɪᴏN Sᴜᴄᴄᴇssғᴜʟ</b>\n\n"
                "<b>Wᴇʟᴄᴏᴍᴇ Bᴀᴄᴋ 𝗌𝖾𝗇𝖽 𝗆𝖾 𝖺𝗇𝗒 𝗍𝗂𝗍𝗅𝖾 (𝗆𝗈𝗏𝗂𝖾𝗌, 𝗌𝖾𝗋𝗂𝖾𝗌, 𝖺𝗇𝗂𝗆𝖾, 𝗄-𝖽𝗋𝖺𝗆𝖺𝗌, 𝖾𝗍𝖼.), "
                "to 𝗀𝖾𝗇𝖾𝗋𝖺𝗍𝖾 𝗍𝗁𝖾 𝗉𝗈𝗌𝗍𝖾𝗋 𝗅𝖺𝗒𝗈𝗎𝗍 𝖿𝗈𝗋 𝗒𝗈𝗎</b>"
            )
            markup = telebot.types.InlineKeyboardMarkup(row_width=2)
            about_btn = telebot.types.InlineKeyboardButton(text="• Aʙᴏᴜᴛ •", callback_data="btn_about")
            updates_btn = telebot.types.InlineKeyboardButton(text="• Uᴘᴅᴀᴛᴇs •", url="https://t.me/Aero_Unity")
            owner_btn = telebot.types.InlineKeyboardButton(text="• Oᴡɴᴇʀ •", url="https://t.me/Mr_Mohammed_29")
            markup.row(about_btn, updates_btn)
            markup.row(owner_btn)
            
            bot.send_photo(call.message.chat.id, START_IMAGE_URL, caption=welcome_text, parse_mode="HTML", reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, "›› ‼️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ᴛᴏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs", show_alert=True)
            
    elif call.data == "btn_about":
        about_text = (
            "⍟───[ <b>ᴍʏ ᴅᴇᴛᴀɪʟꜱ</b> ]───⍟\n\n"
            "‣ <b>ᴍʏ ɴᴀᴍᴇ : <a href=\"https://t.me/Aero_Poster_bot\">ᴀᴇʀᴏ ᴘᴏsᴛᴇʀ ʙᴏᴛ</a></b>\n"
            "‣ <b>ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href=\"https://t.me/Mr_Mohammed_29\"><b>ᴍᴏʜᴀᴍᴍᴇᴅ</b></a></b>\n"
            "‣ <b>ʟɪʙʀᴀʀʏ : ᴘʏʀᴏɢʀᴀᴍ / ᴛᴇʟᴇʙᴏᴛ</b>\n"
            "‣ <b>ʟᴀɴɢᴜᴀɢᴇ : <a href=\"https://www.python.org/download/releases/3.0/\">ᴘʏᴛʜᴏɴ 𝟹</a></b>\n"
            "‣ <b>ʙᴏᴛ sᴇʀᴠᴇʀ : <a href=\"https://t.me/Aero_Unity\"><b>ᴀᴇʀᴏ ᴜɴɪᴛʏ</b></a></b>\n"
            "‣ <b>ʙᴜɪʟᴅ sᴛᴀᴛᴜs : ᴠ3.0 [sᴛᴀʙʟᴇ] </b>"
        )
        markup = telebot.types.InlineKeyboardMarkup()
        home_btn = telebot.types.InlineKeyboardButton(text="• Hᴏᴍᴇ •", callback_data="btn_home")
        markup.add(home_btn)
        try:
            bot.edit_message_media(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                media=telebot.types.InputMediaPhoto(ABOUT_IMAGE_URL, caption=about_text, parse_mode="HTML"),
                reply_markup=markup
            )
        except Exception:
            try:
                bot.edit_message_caption(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    caption=about_text,
                    parse_mode="HTML",
                    reply_markup=markup
                )
            except Exception:
                bot.send_photo(call.message.chat.id, ABOUT_IMAGE_URL, caption=about_text, parse_mode="HTML", reply_markup=markup)

    elif call.data == "btn_home":
        welcome_text = (
            "👋 <b>Wᴇʟᴄᴏᴍᴇ Tᴏ Uɴɪᴠᴇʀsᴀʟ Pᴏsᴛᴇʀ Bᴏᴛ!</b>\n\n"
            "<b>𝗌𝖾𝗇𝖽 𝗆𝖾 𝖺𝗇𝗒 𝗍𝗂𝗍𝗅𝖾 (𝗆𝗈𝗏𝗂𝖾𝗌, 𝗌𝖾𝗋𝗂𝖾𝗌, 𝖺𝗇𝗂𝗆𝖾, 𝗄-𝖽𝗋𝖺𝗆𝖺𝗌, 𝖾𝗍𝖼.), "
            "𝖺𝗇𝖽 𝗂 𝗐𝗂𝗅𝗅 𝗀𝖾𝗇𝖾𝗋𝖺𝗍𝖾 𝗍𝗁𝖾 𝗉𝗈𝗌𝗍𝖾𝗋 𝗅𝖺𝗒𝗈𝗎𝗍 𝖿𝗈𝗋 𝗒𝗈𝗎!</b>"
        )
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        about_btn = telebot.types.InlineKeyboardButton(text="• Aʙᴏᴜᴛ •", callback_data="btn_about")
        updates_btn = telebot.types.InlineKeyboardButton(text="• Uᴘᴅᴀᴛᴇs •", url="https://t.me/Aero_Unity")
        owner_btn = telebot.types.InlineKeyboardButton(text="• Oᴡɴᴇʀ •", url="https://t.me/Mr_Mohammed_29")
        markup.row(about_btn, updates_btn)
        markup.row(owner_btn)
        
        try:
            bot.edit_message_media(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                media=telebot.types.InputMediaPhoto(START_IMAGE_URL, caption=welcome_text, parse_mode="HTML"),
                reply_markup=markup
            )
        except Exception:
            try:
                bot.edit_message_caption(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    caption=welcome_text,
                    parse_mode="HTML",
                    reply_markup=markup
                )
            except Exception:
                bot.send_photo(call.message.chat.id, START_IMAGE_URL, caption=welcome_text, parse_mode="HTML", reply_markup=markup)
                
    bot.answer_callback_query(call.id)

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@bot.message_handler(commands=['stats'])
def bot_stats(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "<b>ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ: ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ sᴇɴᴘᴀɪ </b>", parse_mode="HTML")
        return

    users = database.get_all_users()
    total_users = len(users)

    user_list_str = ""
    for idx, (uid, fname) in enumerate(users[:25], 1):
        safe_fname = html.escape(fname or "user")
        user_list_str += f"{idx}. {safe_fname} (<code>{uid}</code>)\n"

    if total_users > 25:
        user_list_str += f"\n<i>...and {total_users - 25} more users.</i>"

    stats_msg = (
        f"📊 <b>𝖡𝗈𝗍 𝖲𝗍𝖺𝗍𝗂𝗌𝗍𝗂𝖼𝗌:</b>\n\n"
        f"<b>ᴛᴏᴛᴀʟ ᴜsᴇʀs:</b> <code>{total_users}</code>\n\n"
        f"<b>ᴜsᴇʀs ʟɪsᴛs:</b>\n{user_list_str if user_list_str else 'no users yet.'}"
    )
    bot.reply_to(message, stats_msg, parse_mode="HTML")

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, " <b>ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ: ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ sᴇɴᴘᴀɪ</b>", parse_mode="HTML")
        return
    args = message.text.split()
    if len(args) > 1:
        try:
            target_id = int(args[1].strip())
            database.ban_user(target_id)
            bot.reply_to(message, f"✅ sᴜᴄᴄᴇssꜰᴜʟʟʏ ʙᴀɴɴᴇᴅ ᴀ ᴜsᴇʀ ɪᴅ : <code>{target_id}</code>", parse_mode="HTML")
        except ValueError:
            bot.reply_to(message, "‼️ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ ɪᴅ", parse_mode="HTML")
    else:
        bot.reply_to(message, " <code>/ban user_id</code>", parse_mode="HTML")

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@bot.message_handler(commands=['unban'])
def unban_user(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, " <b>ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ: ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ sᴇɴᴘᴀɪ</b>", parse_mode="HTML")
        return
    args = message.text.split()
    if len(args) > 1:
        try:
            target_id = int(args[1].strip())
            database.unban_user(target_id)
            bot.reply_to(message, f"✅ sᴜᴄᴄᴇssꜰᴜʟʟʏ ᴜɴʙᴀɴɴᴇᴅ ᴜsᴇʀ ɪᴅ : <code>{target_id}</code>", parse_mode="HTML")
        except ValueError:
            bot.reply_to(message, "‼️ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ ɪᴅ.", parse_mode="HTML")
    else:
        bot.reply_to(message, "<code>/unban user_id</code>", parse_mode="HTML")

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@bot.message_handler(commands=['banlist'])
def list_banned_users(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, " <b>ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ: ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ sᴇɴᴘᴀɪ</b>", parse_mode="HTML")
        return
    banned_ids = database.get_banned_users()
    if banned_ids:
        banned_str = "\n".join([f"• <code>{uid}</code> •" for uid in banned_ids])
        bot.reply_to(message, f"🚫 <b>ʙᴀɴɴᴇᴅ ᴜsᴇʀs ʟɪsᴛ:</b>\n\n{banned_str}", parse_mode="HTML")
    else:
        bot.reply_to(message, "‼️ ɴᴏ ʙᴀɴɴᴇᴅ ᴜsᴇʀs ꜰᴏᴜɴᴅ.", parse_mode="HTML")

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@bot.message_handler(commands=['addforcesub'])
def add_force_sub(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, " <b>ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ: ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ sᴇɴᴘᴀɪ </b>", parse_mode="HTML")
        return
    args = message.text.split()
    if len(args) > 1:
        channel = args[1].strip()
        current_channels = database.get_fsub_channels()
        if channel not in current_channels:
            database.add_fsub_channel(channel)
            bot.reply_to(message, f"<b>✅ sᴜᴄᴄᴇssꜰᴜʟʟʏ ᴀᴅᴅᴇᴅ <code>{channel}</code> ᴛᴏ ꜰᴏʀᴄᴇ sᴜʙsᴄʀɪᴘᴛɪᴏɴ ʟɪsᴛ.</b>", parse_mode="HTML")
        else:
            bot.reply_to(message, f"‼️ ᴄʜᴀɴɴᴇʟ <code>{channel}</code> ɪs ᴀʟʀᴇᴀᴅʏ ɪɴ ᴛʜᴇ ʟɪsᴛ.", parse_mode="HTML")
    else:
        bot.reply_to(message, "<code>/addforcesub @channelusername</code>", parse_mode="HTML")

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@bot.message_handler(commands=['removeforce'])
def remove_force_sub(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, " <b>ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ: ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ sᴇɴᴘᴀɪ</b>", parse_mode="HTML")
        return
    args = message.text.split()
    if len(args) > 1:
        channel = args[1].strip()
        current_channels = database.get_fsub_channels()
        if channel in current_channels:
            database.remove_fsub_channel(channel)
            bot.reply_to(message, f"<b>✅️ sᴜᴄᴄᴇssꜰᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ <code>{channel}</code> ꜰʀᴏᴍ ꜰᴏʀᴄᴇ sᴜʙsᴄʀɪᴘᴛɪᴏɴ ʟɪsᴛ</b>", parse_mode="HTML")
        else:
            bot.reply_to(message, f"‼️ ᴄʜᴀɴɴᴇʟ<code>{channel}</code> ɴᴏᴛ ꜰᴏᴜɴᴅ ɪɴ ʟɪsᴛ.", parse_mode="HTML")
    else:
        bot.reply_to(message, " <code>/removeforce @channelusername</code>", parse_mode="HTML")

@bot.message_handler(commands=['fsublist'])
def list_force_sub(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, " <b>ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ: ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ sᴇɴᴘᴀɪ </b>", parse_mode="HTML")
        return
    channels = database.get_fsub_channels()
    if channels:
        channels_str = "\n".join([f"• <code>{ch}</code> •" for ch in channels])
        bot.reply_to(message, f" <b>ꜰᴏʀᴄᴇ sᴜʙsᴄʀɪᴘᴛɪᴏN ᴄʜᴀɴɴᴇʟs ʟɪsᴛ:</b>\n\n{channels_str}", parse_mode="HTML")
    else:
        bot.reply_to(message, "‼️<b>ɴᴏ sᴜʙsᴄʀɪᴘᴛɪᴏɴ ᴄʜᴀɴɴᴇʟs ᴀʀᴇ ᴄᴜʀʀᴇɴᴛʟʏ sᴇᴛ.</b>", parse_mode="HTML")

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@bot.message_handler(commands=['broadcast'])
def broadcast_message_handler(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "<b> ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ sᴇɴᴘᴀɪ</b>", parse_mode="HTML")
        return

    if not message.reply_to_message:
        bot.reply_to(message, "⚠️ Please <b>reply to a message</b> to broadcast it.", parse_mode="HTML")
        return

    reply_msg = message.reply_to_message
    users = database.get_all_users()

    success = 0
    failed = 0

    status_msg = bot.reply_to(message, "🚀 <b>Broadcast started...</b> Please wait.", parse_mode="HTML")

    for uid, _ in users:
        try:

            bot.copy_message(chat_id=uid, from_chat_id=message.chat.id, message_id=reply_msg.message_id, reply_markup=reply_msg.reply_markup)
            success += 1
        except Exception as e:
            print(f"Broadcast failed for {uid}: {e}")
            failed += 1

    bot.edit_message_text(
        f"✅ <b>Broadcast Completed!</b>\n\n"
        f"• <b>Successful:</b> {success}\n"
        f"• <b>Failed:</b> {failed}",
        message.chat.id,
        status_msg.message_id,
        parse_mode="HTML"
    )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@bot.message_handler(commands=['broadcastpin'])
def broadcast_pin_handler(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "<b>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ sᴇɴᴘᴀɪ</b>", parse_mode="HTML")
        return

    if not message.reply_to_message:
        bot.reply_to(message, "⚠️ Please <b>reply to a message</b> to broadcast and pin it.", parse_mode="HTML")
        return

    reply_msg = message.reply_to_message
    users = database.get_all_users()

    success = 0
    failed = 0

    status_msg = bot.reply_to(message, " <b>Broadcast & Pin started...</b> Please wait.", parse_mode="HTML")

    for uid, _ in users:
        try:
            sent_msg = bot.copy_message(chat_id=uid, from_chat_id=message.chat.id, message_id=reply_msg.message_id, reply_markup=reply_msg.reply_markup)
            bot.pin_chat_message(chat_id=uid, message_id=sent_msg.message_id)
            success += 1
        except Exception as e:
            print(f"Broadcast Pin failed for {uid}: {e}")
            failed += 1

    bot.edit_message_text(
        f"✅ <b>Broadcast & Pin Completed!</b>\n\n"
        f"• <b>Successful:</b> {success}\n"
        f"• <b>Failed:</b> {failed}",
        message.chat.id,
        status_msg.message_id,
        parse_mode="HTML"
    )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@bot.message_handler(commands=['broadcastunpin'])
def broadcast_unpin_handler(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "<b>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ sᴇɴᴘᴀɪ</b>", parse_mode="HTML")
        return

    if not message.reply_to_message:
        bot.reply_to(message, "⚠️ Please <b>reply to a message</b> to broadcast, pin, and unpin it.", parse_mode="HTML")
        return

    reply_msg = message.reply_to_message
    users = database.get_all_users()

    success = 0
    failed = 0

    status_msg = bot.reply_to(message, "🚀 <b>Broadcast & Unpin started... Please wait.</b>", parse_mode="HTML")

    for uid, _ in users:
        try:
            sent_msg = bot.copy_message(chat_id=uid, from_chat_id=message.chat.id, message_id=reply_msg.message_id, reply_markup=reply_msg.reply_markup)
            bot.pin_chat_message(chat_id=uid, message_id=sent_msg.message_id)
            bot.unpin_chat_message(chat_id=uid, message_id=sent_msg.message_id)
            success += 1
        except Exception as e:
            print(f"Broadcast Unpin failed for {uid}: {e}")
            failed += 1

    bot.edit_message_text(
        f"✅ <b>Broadcast & Unpin Completed!</b>\n\n"
        f"• <b>Successful:</b> {success}\n"
        f"• <b>Failed:</b> {failed}",
        message.chat.id,
        status_msg.message_id,
        parse_mode="HTML"
    )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def get_tmdb_logo_url(item_id, media_type):
    endpoint = "movie" if media_type == "movie" else "tv"
    url = f"https://api.themoviedb.org/3/{endpoint}/{item_id}/images?api_key={TMDB_API_KEY}"
    try:
        res = session.get(url, timeout=4).json()
        logos = res.get("logos", [])
        if logos:
            en_logos = [l for l in logos if l.get("iso_639_1") == "en"]
            selected_logo = en_logos[0] if en_logos else logos[0]
            return f"https://image.tmdb.org/t/p/original{selected_logo['file_path']}"
    except Exception:
        pass
    return None

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def add_title_overlay(image_bytes, title_text="", logo_url=None, position="center"):
    orig_img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    target_width, target_height = 1280, 720

    if orig_img.width / orig_img.height < 1.33:
        bg = orig_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        bg = bg.filter(ImageFilter.GaussianBlur(15))
        portrait = orig_img.copy()
        portrait.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
        bg.paste(portrait, ((target_width - portrait.width) // 2, (target_height - portrait.height) // 2), portrait if portrait.mode == 'RGBA' else None)
        image = bg
    else:
        image = orig_img.resize((target_width, target_height), Image.Resampling.LANCZOS)

    if logo_url:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            logo_res = session.get(logo_url, headers=headers, timeout=5)
            if logo_res.status_code == 200:
                logo_img = Image.open(io.BytesIO(logo_res.content)).convert("RGBA")
                max_logo_w = int(target_width * 0.55)
                max_logo_h = int(target_height * 0.35)

                w_percent = (max_logo_w / float(logo_img.size[0]))
                h_size = int(float(logo_img.size[1]) * float(w_percent))

                if h_size > max_logo_h:
                    h_percent = (max_logo_h / float(logo_img.size[1]))
                    max_logo_w = int(float(logo_img.size[0]) * float(h_percent))
                    h_size = max_logo_h

                logo_img = logo_img.resize((max_logo_w, h_size), Image.Resampling.LANCZOS)
                logo_w, logo_h = logo_img.size

                margin_x = int(target_width * 0.08)
                margin_y = int(target_height * 0.08)

                pos = position.lower()
                if pos == "left":
                    x, y = margin_x, (target_height - logo_h) // 2
                elif pos == "right":
                    x, y = target_width - logo_w - margin_x, (target_height - logo_h) // 2
                elif pos in ["up", "top"]:
                    x, y = (target_width - logo_w) // 2, margin_y
                elif pos in ["down", "bottom"]:
                    x, y = (target_width - logo_w) // 2, target_height - logo_h - margin_y
                else:
                    x, y = (target_width - logo_w) // 2, (target_height - logo_h) // 2

                image.paste(logo_img, (x, y), mask=logo_img)
        except Exception as e:
            print(f"Error applying logo overlay: {e}")

    output = io.BytesIO()
    image.convert("RGB").save(output, format="JPEG", quality=95)
    output.seek(0)
    return output

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def generate_custom_media_card(poster_bytes, portrait_bytes_list, title, genres, synopsis, logo_url=None, branding="Manga Aero"):
    target_w, target_h = 1280, 720
    
    canvas = Image.new("RGBA", (target_w, target_h), (18, 16, 16, 255))
    
    try:
        raw_art = Image.open(io.BytesIO(poster_bytes)).convert("RGBA")
        art_right = ImageOps.fit(raw_art, (680, target_h), method=Image.Resampling.LANCZOS)
        canvas.paste(art_right, (600, 0))
    except Exception as e:
        print(f"Error processing artwork: {e}")
        raw_art = None
        
    if raw_art:
        bg_blur = raw_art.resize((600, target_h), Image.Resampling.LANCZOS)
        bg_blur = bg_blur.filter(ImageFilter.GaussianBlur(25))
        # Dark overlay tint over the blurred image
        dark_tint = Image.new("RGBA", (600, target_h), (25, 20, 18, 210))
        bg_blur.paste(dark_tint, (0, 0), dark_tint)
        canvas.paste(bg_blur, (0, 0))
    else:
        left_panel = Image.new("RGBA", (600, target_h), (28, 24, 22, 255))
        canvas.paste(left_panel, (0, 0))

    draw = ImageDraw.Draw(canvas)

    # 4. Top Header Branding
    draw.text((40, 25), branding, fill=(255, 255, 255))
    draw.text((170, 30), "CRUISE THROUGH INFINITE CHAPTERS", fill=(180, 180, 180))

    thumb_coords = [(40, 75), (40, 210)]
    for idx, p_bytes in enumerate(portrait_bytes_list[:2]):
        try:
            th_img = Image.open(io.BytesIO(p_bytes)).convert("RGBA")
            th_img = ImageOps.fit(th_img, (100, 120), method=Image.Resampling.LANCZOS)
            tx, ty = thumb_coords[idx]
            canvas.paste(th_img, (tx, ty))
            draw.rectangle([tx, ty, tx + 100, ty + 120], outline=(240, 240, 240), width=2)
        except Exception:
            pass
            
    syn_box_x1, syn_box_y1, syn_box_x2, syn_box_y2 = 155, 75, 570, 340
    draw.rounded_rectangle([syn_box_x1, syn_box_y1, syn_box_x2, syn_box_y2], radius=12, fill=(35, 30, 28, 200), outline=(65, 55, 50), width=1)    
    box_center_x = (syn_box_x1 + syn_box_x2) // 2
    syn_title = "SYNOPSIS  »»»"
    draw.text((box_center_x - (len(syn_title) * 3.5), 88), syn_title, fill=(255, 255, 255))

    words = synopsis.split()
    lines, curr_line = [], ""
    for w in words:
        if len(curr_line + " " + w) < 30:
            curr_line += " " + w
        else:
            lines.append(curr_line.strip())
            curr_line = w
    if curr_line:
        lines.append(curr_line.strip())

    y_pos = 120
    for line in lines[:5]:
        line_w = len(line) * 6.5
        lx = box_center_x - (line_w / 2)
        draw.text((lx, y_pos), line, fill=(215, 215, 215))
        y_pos += 20

    sub_tag = f"»»» {branding}"
    draw.text((box_center_x - (len(sub_tag) * 3.5), y_pos + 8), sub_tag, fill=(180, 180, 180))
    title_box_x1, title_box_y1, title_box_x2, title_box_y2 = 40, 360, 570, 670
    draw.rounded_rectangle([title_box_x1, title_box_y1, title_box_x2, title_box_y2], radius=15, fill=(18, 24, 32, 235), outline=(45, 58, 72), width=1) 
    clean_title = title.upper()[:24]
    bottom_center_x = (title_box_x1 + title_box_x2) // 2
    title_x = bottom_center_x - (len(clean_title) * 4.5)
    draw.text((title_x, 380), clean_title, fill=(255, 255, 255))

    gx, gy = 60, 440
    for g in genres[:6]:
        tag_text = g.upper()[:12]
        draw.rounded_rectangle([gx, gy, gx + 125, gy + 32], radius=16, outline=(120, 135, 150), width=1)
        draw.text((gx + 16, gy + 8), tag_text, fill=(210, 220, 235))
        gx += 140
        if gx > 460:
            gx = 60
            gy += 45

    draw.text((bottom_center_x - (len(branding) * 3.5), 625), branding.upper(), fill=(140, 140, 140))

    if logo_url:
        try:
            logo_res = session.get(logo_url, timeout=5)
            if logo_res.status_code == 200:
                logo_img = Image.open(io.BytesIO(logo_res.content)).convert("RGBA")
                logo_img.thumbnail((450, 180), Image.Resampling.LANCZOS)
                lx = 600 + (680 - logo_img.width) // 2
                ly = target_h - logo_img.height - 40
                canvas.paste(logo_img, (lx, ly), mask=logo_img)
        except Exception as e:
            print(f"Error drawing logo overlay: {e}")
            
    output = io.BytesIO()
    canvas.convert("RGB").save(output, format="JPEG", quality=95, subsampling=0)
    output.seek(0)
    return output
    
# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def build_poster_page(search_id, index=0):
    cache = SEARCH_CACHE.get(search_id)
    if not cache:
        return None, None, None

    results = cache["results"]
    total = len(results)
    index = max(0, min(index, total - 1))
    item = results[index]

    title = item.get("title") or item.get("name") or "unknown title"
    item_id = str(item.get("id"))
    media_type = item.get("media_type", "movie")
    season_number = cache.get("season_number")

    release_date = item.get("release_date") or item.get("first_air_date") or ""
    year = release_date.split("-")[0] if release_date else "n/a"

    endpoint = "movie" if media_type == "movie" else "tv"
    details_url = f"https://api.themoviedb.org/3/{endpoint}/{item_id}?api_key={TMDB_API_KEY}"
    languages_list = []
    genre_list = []

    try:
        det_res = session.get(details_url, timeout=4)
        if det_res.status_code == 200:
            det_data = det_res.json()

            for g in det_data.get("genres", []):
                genre_name = g.get("name")
                if genre_name:
                    genre_list.append(genre_name)

            spoken = det_data.get("spoken_languages", [])
            for lang in spoken:
                name = lang.get("english_name") or lang.get("name")
                if name:
                    languages_list.append(name)
    except Exception:
        pass

    genres = ", ".join(genre_list) if genre_list else "Action, Adventure"

    if not languages_list:
        languages_list = [item.get("original_language", "en").upper()]

    language_str = ", ".join(languages_list)

    backdrop_path = item.get("backdrop_path")
    poster_path = item.get("poster_path")

    if season_number and media_type == "tv":
        title = f"{title} season {season_number}"

    backdrop_url_original = f"https://image.tmdb.org/t/p/original{backdrop_path}" if backdrop_path else f"https://image.tmdb.org/t/p/original{poster_path}"
    poster_url_original = f"https://image.tmdb.org/t/p/original{poster_path}" if poster_path else backdrop_url_original

    logo_url = get_tmdb_logo_url(item_id, media_type)

    img_response = session.get(backdrop_url_original, timeout=8)
    if img_response.status_code == 200:
        img_obj = Image.open(io.BytesIO(img_response.content))
        img_width, img_height = img_obj.size
        resolution_str = f"{img_width}x{img_height}"

        cache_key = f"{item_id}_s{season_number}_idx{index}" if season_number else f"{item_id}_idx{index}"

        positions_list = ["center", "left", "right", "up", "down"]
        assigned_position = positions_list[index % len(positions_list)]

        processed_image_io = add_title_overlay(img_response.content, title, logo_url, position=assigned_position)
        landscape_file_path = os.path.join(CACHE_DIR, f"{cache_key}.jpg")
        with open(landscape_file_path, "wb") as f:
            f.write(processed_image_io.getvalue())

        portrait_file_path = os.path.join(CACHE_DIR, f"{cache_key}_portrait.jpg")
        try:
            port_res = session.get(poster_url_original, timeout=8)
            if port_res.status_code == 200:
                p_img = Image.open(io.BytesIO(port_res.content)).convert("RGB")
                if p_img.width > p_img.height:
                    p_img = p_img.resize((800, 1200), Image.Resampling.LANCZOS)

                portrait_io = io.BytesIO()
                p_img.save(portrait_io, format="JPEG", quality=95)
                with open(portrait_file_path, "wb") as f:
                    f.write(portrait_io.getvalue())
            else:
                with open(portrait_file_path, "wb") as f:
                    f.write(processed_image_io.getvalue())
        except Exception:
            with open(portrait_file_path, "wb") as f:
                f.write(processed_image_io.getvalue())

        app_url = os.environ.get("RENDER_EXTERNAL_URL") or request.host_url.rstrip('/')
        landscape_url = f"{app_url}/poster/{cache_key}"
        portrait_url = f"{app_url}/poster/{cache_key}?type=portrait"

        safe_title = html.escape(title)

        caption_lines = [
            f"• <b>Tɪᴛʟᴇ : {safe_title} ({year})</b>",
            f"• <b>Gᴇɴʀᴇ : {genres}</b>",
            f"• <b>Lᴀɴɢᴜᴀɢᴇ : {language_str}</b>",
            f"• <b>Rᴇsᴏʟᴜᴛɪᴏɴs : {resolution_str}</b>",
            f"• <b>Lɪɴᴋ :</b> <a href=\"{landscape_url}\"><b>Dɪʀᴇᴄᴛ Lɪɴᴋ</b></a>",
            f"• <b>Pᴏʀᴛʀᴀɪᴛ :</b> <a href=\"{portrait_url}\"><b>Cʟɪᴄᴋ Hᴇʀᴇ</b></a>\n",
            f"<b>›› Pᴏᴡᴇʀᴇᴅ Bʏ : <a href=\"https://t.me/Aero_Unity\">Aᴇʀᴏ Uɴɪᴛʏ</a></b>"
        ]

        caption = "\n".join(caption_lines)

        markup = telebot.types.InlineKeyboardMarkup()

        first_btn = telebot.types.InlineKeyboardButton(text="<<", callback_data=f"p_{search_id}_0")
        prev_idx = max(0, index - 1)
        prev_btn = telebot.types.InlineKeyboardButton(text="<", callback_data=f"p_{search_id}_{prev_idx}")
        count_btn = telebot.types.InlineKeyboardButton(text=f"{index+1}/{total}", callback_data="noop")
        next_idx = min(total - 1, index + 1)
        next_btn = telebot.types.InlineKeyboardButton(text=">", callback_data=f"p_{search_id}_{next_idx}")
        last_btn = telebot.types.InlineKeyboardButton(text=">>", callback_data=f"p_{search_id}_{total-1}")

        markup.row(first_btn, prev_btn, count_btn, next_btn, last_btn)

        aero_button = telebot.types.InlineKeyboardButton(text="• ᴀᴇʀᴏ ᴜɴɪᴛʏ •", url="https://t.me/Aero_Unity")
        open_image_button = telebot.types.InlineKeyboardButton(text="• ᴏᴘᴇɴ ɪᴍᴀɢᴇ •", url=landscape_url)
        markup.row(aero_button, open_image_button)

        return backdrop_url_original, caption, markup

    return None, None, None

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@bot.message_handler(func=lambda message: not message.text.strip().startswith("/"))
def search_poster(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "user"
    database.add_user(user_id, first_name)

    if database.is_banned(user_id):
        return

    if not is_user_member(user_id):
        send_fsub_prompt(message.chat.id)
        return

    if message.chat.type == "private" and user_id != OWNER_ID:
        pm_enabled = database.get_global_pm_search()
        if not pm_enabled:
            access_denied_text = (
                "🔒 <b>ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ</b>\n\n"
                "<b>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀ ᴀᴜᴛʜᴏʀɪsᴇᴅ ᴜsᴇʀ.\n\n"
                "ᴘʟᴇᴀsᴇ ᴜsᴇ ᴛʜɪs ʙᴏᴛ ɪɴ ᴏᴜʀ ᴘᴏsᴛᴇʀ ɢʀᴏᴜᴘ.</b>"
            )
            markup = telebot.types.InlineKeyboardMarkup()
            group_btn = telebot.types.InlineKeyboardButton(text="• ᴊᴏɪɴ ᴘᴏsᴛᴇʀ ɢʀᴏᴜᴘ •", url=POSTER_GROUP_URL)
            markup.add(group_btn)
            bot.reply_to(message, access_denied_text, parse_mode="HTML", reply_markup=markup)
            return

    raw_query = message.text.strip()
    if raw_query.startswith("/p "):
        raw_query = raw_query[3:].strip()
    elif raw_query.startswith("/poster "):
        raw_query = raw_query[8:].strip()

    # Comprehensive Language Map
    LANG_MAP = {
        # East Asian / Dramas
        r'(?i)\b(?:kdrama|k-drama|korean|kr)\b': 'ko',
        r'(?i)\b(?:chi|cdrama|chinese|mandarin|zh)\b': 'zh',
        r'(?i)\b(?:jdrama|j-drama|japanese|jap|anime|ja)\b': 'ja',
        r'(?i)\b(?:thai|th)\b': 'th',

        # Indian Languages
        r'(?i)\b(?:hindi|hin|hi)\b': 'hi',
        r'(?i)\b(?:tamil|tam|ta)\b': 'ta',
        r'(?i)\b(?:telugu|tel|te)\b': 'te',
        r'(?i)\b(?:malayalam|mal|ml)\b': 'ml',
        r'(?i)\b(?:kannada|kan|kn)\b': 'kn',
        r'(?i)\b(?:bengali|ben|bn)\b': 'bn',
        r'(?i)\b(?:marathi|mar|mr)\b': 'mr',
        r'(?i)\b(?:punjabi|pun|pa)\b': 'pa',

        # European Languages
        r'(?i)\b(?:spanish|spa|es)\b': 'es',
        r'(?i)\b(?:french|fre|fr)\b': 'fr',
        r'(?i)\b(?:german|ger|de)\b': 'de',
        r'(?i)\b(?:italian|ita|it)\b': 'it',
        r'(?i)\b(?:russian|rus|ru)\b': 'ru',
        r'(?i)\b(?:portuguese|por|pt)\b': 'pt',
        r'(?i)\b(?:turkish|tur|tr)\b': 'tr',

        # Middle Eastern & English
        r'(?i)\b(?:arabic|ara|ar)\b': 'ar',
        r'(?i)\b(?:persian|farsi|fa)\b': 'fa',
        r'(?i)\b(?:indonesian|indo|id)\b': 'id',
        r'(?i)\b(?:english|eng|en)\b': 'en',
    }

    lang_filter = None
    clean_query = raw_query

    for pattern, code in LANG_MAP.items():
        if re.search(pattern, clean_query):
            lang_filter = code
            clean_query = re.sub(pattern, '', clean_query).strip()
            break

    search_year = None
    year_match = re.search(r'\b(19\d\d|20\d\d)\b', clean_query)
    if year_match:
        search_year = year_match.group(1)
        clean_query = re.sub(r'\b(19\d\d|20\d\d)\b', '', clean_query).strip()

    season_number = None
    season_match = re.search(r'(?i)\b(?:s|season)\s*0*(\d+)\b', clean_query)
    if season_match:
        season_number = int(season_match.group(1))
        clean_query = re.sub(r'(?i)\b(?:s|season)\s*0*\d+\b', '', clean_query).strip()

    status_msg = bot.reply_to(message, f"<b><i>searching <code>{html.escape(raw_query)}</code>...</i></b>", parse_mode="HTML")

    if not TMDB_API_KEY:
        bot.edit_message_text("⚠️ <b>𝖾𝗋𝗋𝗈𝗋:</b> <code>tmdb_api_key</code> 𝗂𝗌 𝗆𝗂𝗌𝗌𝗂𝗇𝗀!.", message.chat.id, status_msg.message_id, parse_mode="HTML")
        return

    year_param = f"&primary_release_year={search_year}" if search_year else ""
    first_air_year_param = f"&first_air_date_year={search_year}" if search_year else ""
    lang_param = f"&with_original_language={lang_filter}" if lang_filter else ""
    results = []

    try:

        if season_number or lang_filter in ["ko", "zh", "ja"]:
            tv_url = f"https://api.themoviedb.org/3/search/tv?api_key={TMDB_API_KEY}&query={requests.utils.quote(clean_query)}{first_air_year_param}{lang_param}"
            tv_res = session.get(tv_url, timeout=5)
            if tv_res.status_code == 200:
                results = tv_res.json().get("results", [])
                for r in results:
                    r["media_type"] = "tv"

        if not results:
            movie_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={requests.utils.quote(clean_query)}{year_param}{lang_param}"
            res = session.get(movie_url, timeout=5)
            if res.status_code == 200:
                results = res.json().get("results", [])
                for r in results:
                    r["media_type"] = "movie"

            if not results and (year_param or lang_param):
                fallback_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={requests.utils.quote(clean_query)}"
                fallback_res = session.get(fallback_url, timeout=5)
                if fallback_res.status_code == 200:
                    results = fallback_res.json().get("results", [])
                    for r in results:
                        r["media_type"] = "movie"

            if not results:
                tv_url = f"https://api.themoviedb.org/3/search/tv?api_key={TMDB_API_KEY}&query={requests.utils.quote(clean_query)}{first_air_year_param}{lang_param}"
                tv_res = session.get(tv_url, timeout=5)
                if tv_res.status_code == 200:
                    results = tv_res.json().get("results", [])
                    for r in results:
                        r["media_type"] = "tv"

        if lang_filter and results:
            strict_filtered = [i for i in results if i.get("original_language") == lang_filter]
            if strict_filtered:
                results = strict_filtered

        if results:
            valid_items = [i for i in results if i.get("backdrop_path") or i.get("poster_path")]
            if not valid_items:
                bot.edit_message_text("‼️ ɪᴍᴀɢᴇ ʙᴀɴɴᴇʀ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ꜰᴏʀ ᴛʜɪs ᴛɪᴛʟᴇ.", message.chat.id, status_msg.message_id)
                return

            target_item = valid_items[0]
            item_id = str(target_item.get("id"))
            media_type = target_item.get("media_type", "movie")

            images_list = []
            img_endpoint = "tv" if (media_type == "tv" or season_number) else "movie"

            if season_number and media_type == "tv":
                images_url = f"https://api.themoviedb.org/3/tv/{item_id}/season/{season_number}/images?api_key={TMDB_API_KEY}"
            else:
                images_url = f"https://api.themoviedb.org/3/{img_endpoint}/{item_id}/images?api_key={TMDB_API_KEY}"

            try:
                img_res = session.get(images_url, timeout=5)
                if img_res.status_code == 200:
                    img_data = img_res.json()
                    backdrops = img_data.get("backdrops", [])
                    posters = img_data.get("posters", [])

                    for b in backdrops:
                        if b.get("file_path"):
                            images_list.append({
                                **target_item,
                                "backdrop_path": b.get("file_path")
                            })
                    if not images_list:
                        for p in posters:
                            if p.get("file_path"):
                                images_list.append({
                                    **target_item,
                                    "backdrop_path": p.get("file_path")
                                })
            except Exception:
                pass

            if not images_list:
                images_list = [target_item]

            search_id = str(message.message_id)
            SEARCH_CACHE[search_id] = {
                "results": images_list,
                "season_number": season_number
            }

            photo_url, caption, markup = build_poster_page(search_id, index=0)

            try:
                bot.delete_message(message.chat.id, status_msg.message_id)
            except Exception:
                pass

            if photo_url:
                bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo_url,
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=markup
                )
            else:
                bot.send_message(message.chat.id, "❌ failed to generate poster.")
        else:
            bot.edit_message_text("ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴘᴇʟʟɪɴɢ.", message.chat.id, status_msg.message_id)

    except Exception as e:
        try:
            bot.edit_message_text(f"⚠️ ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ: {html.escape(str(e))}", message.chat.id, status_msg.message_id, parse_mode="HTML")
        except Exception:
            pass

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@bot.message_handler(commands=['imdb'])
def imdb_command(message):
    args = message.text.split(maxsplit=1)

    if len(args) == 1:
        bot.reply_to(
            message,
            "<b>Usage:</b> <code>/imdb [Movie Name] or [IMDb URL]</code>",
            parse_mode="HTML"
        )
        return

    query = args[1].strip()
    status_msg = bot.reply_to(message, "<b><i>Searching TMDb...</i></b>", parse_mode="HTML")

    search_url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={requests.utils.quote(query)}"

    try:
        res = session.get(search_url, timeout=5)
        if res.status_code != 200:
            bot.edit_message_text("⚠️ <i>Failed to fetch results from TMDb.</i>", message.chat.id, status_msg.message_id, parse_mode="HTML")
            return

        data = res.json()
        results = data.get("results", [])

        valid_results = [item for item in results if item.get("title") or item.get("name")]

        if not valid_results:
            bot.edit_message_text("‼️ <b>No titles found for your search!</b>", message.chat.id, status_msg.message_id, parse_mode="HTML")
            return

        search_id = str(message.message_id)
        IMDB_SEARCH_CACHE[search_id] = valid_results[:10]

        markup = InlineKeyboardMarkup()
        for idx, item in enumerate(IMDB_SEARCH_CACHE[search_id]):
            title = item.get("title") or item.get("name")
            release_date = item.get("release_date") or item.get("first_air_date") or ""
            year = release_date.split("-")[0] if release_date else "N/A"

            button_text = f"{title} ({year})"
            callback_data = f"imdb_select_{search_id}_{idx}"
            markup.add(InlineKeyboardButton(text=button_text, callback_data=callback_data))

        markup.add(InlineKeyboardButton(text="• Cʟᴏsᴇ •", callback_data="imdb_close"))

        bot.delete_message(message.chat.id, status_msg.message_id)
        bot.send_message(
            chat_id=message.chat.id,
            text="<b>Select The Correct Title From Below Results :</b>",
            parse_mode="HTML",
            reply_markup=markup
        )

    except Exception as e:
        bot.edit_message_text(f"⚠️ <b>An error occurred:</b> <code>{html.escape(str(e))}</code>", message.chat.id, status_msg.message_id, parse_mode="HTML")

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@bot.message_handler(commands=['jhs', 'posters'])
def movie_poster_handler(message):
    query = message.text.replace("/jhs", "").replace("/posters", "").strip()

    if not query:
        bot.reply_to(
            message, 
            "<b>Usage:</b> /jhs [Search Query]\n<i>Example:</i> /jhs Iron man", 
            parse_mode="HTML"
        )
        return

    search_url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={requests.utils.quote(query)}"
    response = requests.get(search_url).json()
    results = response.get("results", [])

    if not results:
        bot.reply_to(message, f"‼️ Nᴏ Rᴇsᴜʟᴛs Fᴏᴜɴᴅ Fᴏʀ ʏᴏᴜʀ <b>{query}</b>", parse_mode="HTML")
        return

    item = results[0]
    media_type = item.get("media_type", "movie")
    item_id = str(item.get("id"))
    title = item.get("title") or item.get("name") or "Unknown Title"

    backdrop_path = item.get("backdrop_path")
    poster_path = item.get("poster_path")

    if not backdrop_path and not poster_path:
        bot.reply_to(message, f"⚠️ Found <b>{title}</b>, but no image banners are available.", parse_mode="HTML")
        return

    genres_list = []
    endpoint = "movie" if media_type == "movie" else "tv"
    details_url = f"https://api.themoviedb.org/3/{endpoint}/{item_id}?api_key={TMDB_API_KEY}"
    try:
        det_res = session.get(details_url, timeout=4)
        if det_res.status_code == 200:
            det_data = det_res.json()
            for g in det_data.get("genres", []):
                if g.get("name"):
                    genres_list.append(g.get("name"))
    except Exception:
        pass

    genres = ", ".join(genres_list) if genres_list else "Action, Adventure"

    raw_backdrop_url = f"https://image.tmdb.org/t/p/original{backdrop_path}" if backdrop_path else f"https://image.tmdb.org/t/p/original{poster_path}"
    poster_url_original = f"https://image.tmdb.org/t/p/original{poster_path}" if poster_path else raw_backdrop_url
    logo_url = get_tmdb_logo_url(item_id, media_type)

    positions_list = ["center", "left", "right", "up", "down"]
    assigned_position = positions_list[int(item_id) % len(positions_list)]

    cache_key = f"{item_id}_jhs"
    landscape_file_path = os.path.join(CACHE_DIR, f"{cache_key}.jpg")
    portrait_file_path = os.path.join(CACHE_DIR, f"{cache_key}_portrait.jpg")

    try:
        img_response = session.get(raw_backdrop_url, timeout=8)
        if img_response.status_code == 200:
            # Generate and save overlay banner (with TMDb logo and dynamic position)
            processed_io = add_title_overlay(img_response.content, title, logo_url, position=assigned_position)
            with open(landscape_file_path, "wb") as f:
                f.write(processed_io.getvalue())

        port_res = session.get(poster_url_original, timeout=8)
        if port_res.status_code == 200:
            with open(portrait_file_path, "wb") as f:
                f.write(port_res.content)
    except Exception as e:
        print(f"Error caching images: {e}")

    app_url = os.environ.get("RENDER_EXTERNAL_URL") or request.host_url.rstrip('/')
    banner_url = f"{app_url}/poster/{cache_key}"
    portrait_url = f"{app_url}/poster/{cache_key}?type=portrait"

    languages = item.get("original_language", "en").upper()

    caption = (
        f"• 🎬 <b>Tɪᴛʟᴇ : {html.escape(title)}</b>\n"
        f"• 🏛️ <b>Tʏᴘᴇ : </b> {media_type.upper()}\n"
        f"• 🎭 <b>Gᴇɴʀᴇ : </b> {genres}\n"
        f"• 🌐 <b>Lᴀɴɢᴜᴀɢᴇ :</b> {languages}\n\n"
        f"• 🖼️ <b>Bᴀɴɴᴇʀ :</b> <a href='{banner_url}'>Lɪɴᴋ</a>\n"
        f"• 🖼️ <b>Pᴏsᴛᴇʀ :</b> <a href='{portrait_url}'>Lɪɴᴋ</a>"
    )

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("• Bᴀɴɴᴇʀ •", url=banner_url),
        InlineKeyboardButton("• Pᴏsᴛᴇʀ •", url=portrait_url)
    )

    try:

        if os.path.exists(landscape_file_path):
            with open(landscape_file_path, 'rb') as photo:
                bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=markup
                )
        else:
            bot.send_photo(
                chat_id=message.chat.id,
                photo=banner_url,
                caption=caption,
                parse_mode="HTML",
                reply_markup=markup
            )
    except Exception as e:
        bot.reply_to(message, f"❌ Error sending poster: {e}", parse_mode="HTML")

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@bot.message_handler(commands=['manga'])
def manga_command_handler(message):
    query = message.text.replace("/manga", "").strip()
    if not query:
        bot.reply_to(message, "<b>Usage:</b> <code>/manga [title]</code>", parse_mode="HTML")
        return

    status_msg = bot.reply_to(message, "⚙️ <b>ɢᴇɴᴇʀᴀᴛɪɴɢ ᴩᴏsᴛᴇʀ, ᴡᴀɪᴛ a sec...</b>", parse_mode="HTML")
        
    search_url = f"https://api.themoviedb.org/3/search/tv?api_key={TMDB_API_KEY}&query={requests.utils.quote(query)}"
    res = session.get(search_url, timeout=5).json()
    results = res.get("results", [])

    if not results:
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={requests.utils.quote(query)}"
        res = session.get(search_url, timeout=5).json()
        results = res.get("results", [])

    if not results:
        bot.reply_to(message, f"‼️ No results found for <b>{html.escape(query)}</b>", parse_mode="HTML")
        return

    item = results[0]
    item_id = str(item.get("id"))
    media_type = item.get("media_type", "tv")
    title = item.get("name") or item.get("title") or query
    endpoint = "tv" if media_type == "tv" else "movie"
    details_url = f"https://api.themoviedb.org/3/{endpoint}/{item_id}?api_key={TMDB_API_KEY}&append_to_response=images"
    det_res = session.get(details_url, timeout=5).json()
    orig_lang = det_res.get("original_language", "ja").lower()
    adult = det_res.get("adult", False)
    genres_list = [g["name"] for g in det_res.get("genres", [])]

    if adult or any(g.lower() in ["erotica", "hentai", "ecchi"] for g in genres_list):
        detected_type = "Pornhwa" if orig_lang == "ko" else "Hentai"
    elif orig_lang == "ko":
        detected_type = "Manhwa"
    elif orig_lang == "zh":
        detected_type = "Manhua"
    elif orig_lang == "ja":
        detected_type = "Manga"
    else:
        detected_type = "Manga" if media_type == "tv" else "Comic"

    vote_avg = det_res.get("vote_average", 0)
    rating_pct = f"{int(vote_avg * 10)}%" if vote_avg else "84%"
    genres_str = ", ".join(genres_list) if genres_list else "Action, Fantasy"
    status_str = det_res.get("status", "Releasing")
    episodes = det_res.get("number_of_episodes")
    chapters_str = f"{episodes}+" if episodes else "120+"
    images = det_res.get("images", {})
    artworks = [f"https://image.tmdb.org/t/p/original{i['file_path']}" for i in images.get("backdrops", [])[:8]]
    posters = [f"https://image.tmdb.org/t/p/w500{i['file_path']}" for i in images.get("posters", [])[:2]]

    if not artworks:
        path = item.get("backdrop_path") or item.get("poster_path")
        artworks = [f"https://image.tmdb.org/t/p/original{path}"] if path else ["https://graph.org/file/faf795187aa693e1024a4-746b376c8dcc889d4f.jpg"]

    if not posters:
        posters = [artworks[0], artworks[0]]

    logo_url = get_tmdb_logo_url(item_id, endpoint)
    synopsis = det_res.get("overview") or item.get("overview") or "No synopsis available."

    search_id = str(message.message_id)
    SEARCH_CACHE[search_id] = {
        "title": title,
        "type": detected_type,
        "genres": genres_str,
        "rating": rating_pct,
        "status": status_str,
        "chapters": chapters_str,
        "synopsis": synopsis,
        "artworks": artworks,
        "posters": posters,
        "logo_url": logo_url
    }

    current_index = 0
    total_pages = len(artworks)

    caption_text = (
        f"<b>{html.escape(title)}</b> ❞\n\n"
        f"» <b>Type:</b> {detected_type}\n"
        f"» <b>Average Rating:</b> {rating_pct}\n"
        f"» <b>Status:</b> {status_str}\n"
        f"» <b>Chapters:</b> {chapters_str}\n"
        f"» <b>Genres:</b> {html.escape(genres_str)}\n\n"
        f"▶ <u><b>SYNOPSIS</b></u>\n"
        f"<b>➔</b> <i>{html.escape(synopsis[:400])}...</i> ❞"
    )

    try:
        img_bytes = session.get(artworks[current_index], timeout=5).content
        p_bytes_list = []
        for p_url in posters[:2]:
            try:
                p_bytes_list.append(session.get(p_url, timeout=4).content)
            except Exception:
                p_bytes_list.append(img_bytes)

        card_io = generate_custom_media_card(
            img_bytes, p_bytes_list, title, genres_list if isinstance(genres_list, list) else ["Action", "Fantasy"],
            synopsis, logo_url=logo_url, branding="Manga Aero"
        )

        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton(text="◀ ᴘʀᴇᴠ •", callback_data=f"media_card_{search_id}_{current_index-1}"),
            InlineKeyboardButton(text=f"01/{total_pages:02d}", callback_data="noop"),
            InlineKeyboardButton(text="• ɴᴇxᴛ ▶", callback_data=f"media_card_{search_id}_{current_index+1}")
        )
        markup.row(InlineKeyboardButton(text="• ᴄᴀɴᴄᴇʟ•", callback_data="cancel_session"))

        try:
            bot.delete_message(message.chat.id, status_msg.message_id)
        except Exception:
            pass

        bot.send_photo(
            chat_id=message.chat.id,
            photo=card_io,
            caption=caption_text,
            parse_mode="HTML",
            reply_markup=markup
        )
    except Exception as e:
        bot.reply_to(message, f"❌ Error generating manga result: {e}", parse_mode="HTML")

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    try:
        bot.remove_webhook()
    except Exception:
        pass

    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    app.run(host="0.0.0.0", port=port)

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #