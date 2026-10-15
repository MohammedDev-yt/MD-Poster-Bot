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
import threading
import database

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

from flask import Flask, send_file, request
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
POSTER_GROUP_URL = os.environ.get("POSTER_GROUP_URL", "https://t.me/+VXY_za8DNjQzYmVl") #replace your group link
OWNER_ID = 7284759394 #replace your Telegram ID

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

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
        
    return "poster not found or expired, Contact to Owner [#@Mr_Mohammed_29]", 404

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
                    f"🎬 <b>{html.escape(title)}</b> [{year}]",
                    f"⭐ <b>IMDb Rating:</b> {rating}",
                    f"📅 <b>Release Info:</b> {rel_info}",
                    f"🎭 <b>Genre:</b> {genre_str}",
                    f"🌐 <b>Language:</b> {lang_str}",
                    f"🏳️ <b>Country of Origin:</b> {country_str}\n",
                    f"📖 <b>Storyline:</b>\n<i>{html.escape(overview)}</i>"
                ]
                caption_text = "\n".join(caption_lines)

                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton(text="📺 IMDb Page", url=imdb_link))

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

# --- Admin-Only Commands --- #
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

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

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
            # Correct TeleBot syntax for copying any message type (text, photo, media, etc.)
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

def add_title_overlay(image_bytes, title_text="", logo_url=None):
    orig_img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    target_width, target_height = 1280, 720

    if orig_img.width / orig_img.height < 1.33:
        bg = orig_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        bg = bg.filter(ImageFilter.GaussianBlur(15))
        
        portrait = orig_img.copy()
        portrait.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
        
        x_offset = (target_width - portrait.width) // 2
        y_offset = (target_height - portrait.height) // 2
        bg.paste(portrait, (x_offset, y_offset), portrait if portrait.mode == 'RGBA' else None)
        image = bg
    else:
        image = orig_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    if logo_url:
        try:
            logo_res = session.get(logo_url, timeout=5)
            if logo_res.status_code == 200:
                logo_img = Image.open(io.BytesIO(logo_res.content)).convert("RGBA")
                max_logo_w = int(target_width * 0.6)
                max_logo_h = int(target_height * 0.3)
                logo_img.thumbnail((max_logo_w, max_logo_h), Image.Resampling.LANCZOS)
                logo_w, logo_h = logo_img.size
                x = int((target_width - logo_w) / 2)
                y = int(target_height - logo_h - (target_height * 0.08))
                image.paste(logo_img, (x, y), logo_img)
        except Exception:
            pass

    output = io.BytesIO()
    image.convert("RGB").save(output, format="JPEG", quality=92)
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
    try:
        det_res = session.get(details_url, timeout=4)
        if det_res.status_code == 200:
            det_data = det_res.json()
            spoken = det_data.get("spoken_languages", [])
            for lang in spoken:
                name = lang.get("english_name") or lang.get("name")
                if name:
                    languages_list.append(name)
    except Exception:
        pass

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

        processed_image_io = add_title_overlay(img_response.content, title, logo_url)
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

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

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
            bot.edit_message_text("❌ <b>No titles found for your search!</b>", message.chat.id, status_msg.message_id, parse_mode="HTML")
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

        markup.add(InlineKeyboardButton(text="❌ Close", callback_data="imdb_close"))

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
