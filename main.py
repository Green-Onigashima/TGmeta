#Main file Telegram Bot instgram post bot 
#By @PythonBotz 
import asyncio
from pyrogram import Client, filters
from instagrapi import Client as InstaClient
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton

#env Change This to your varible's
TELEGRAM_API_ID = "5843476"  #here put your api id
TELEGRAM_API_HASH = "8121c753chj5688cc2623d1277338d"  #hash id
TELEGRAM_BOT_TOKEN = "77141832222:AAHJIXxmVB8JSrJXSA_9Jxxxxxxxx" #bot token
INSTAGRAM_USERNAME = "foileds" #instagram username 
INSTAGRAM_PASSWORD = "YOUR PASSWORD" # password the instagram account
AUTHORIZED_USERS_FILE = "authorized_users.txt" # this file save allowed users id to use bot 
CAPTION_FILE = "caption.txt" # this file save caption to use in reels
DEFAULT_LANGUAGE = "en"  # here you can change language (en=english fa=farsi)


insta_client = InstaClient()
insta_client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)


app = Client("my_bot", api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH, bot_token=TELEGRAM_BOT_TOKEN)


main_menu_fa = ReplyKeyboardMarkup(
    [
        [KeyboardButton("📤 ارسال یک Reels")],
        [KeyboardButton("📤 ارسال چند Reels همزمان")]
    ],
    resize_keyboard=True
)

main_menu_en = ReplyKeyboardMarkup(
    [
        [KeyboardButton("📤 Upload a Reels")],
        [KeyboardButton("📤 Upload Multiple Reels")]
    ],
    resize_keyboard=True
)


def save_language(user_id, language):
    try:
        with open("languages.txt", "a") as file:
            file.write(f"{user_id}:{language}\n")
    except Exception as e:
        print(f"Error saving language: {e}")


def get_language(user_id):
    try:
        with open("languages.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                uid, lang = line.strip().split(":")
                if uid == str(user_id):
                    return lang
    except FileNotFoundError:
        return DEFAULT_LANGUAGE
    return DEFAULT_LANGUAGE

userss = ["6076683960", "6450266465"]
def is_authorized(user_id):
    if user_id in userss:
        return False


@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id  # Correct the attribute name to 'id'
    
    # Send unauthorized message
    await message.reply(
        f"⛔ok you are allowed\n\n🆔 Your user ID: {user_id}"
    )

    # Get language after sending the unauthorized message
    language = get_language(user_id)

    if language == "fa":
        await message.reply(
            "👋 به ربات خوش آمدید!\nبرای آپلود یک Reels یا چند Reels همزمان، روی دکمه‌های زیر کلیک کنید.",
            reply_markup=main_menu_fa
        )
    else:
        await message.reply(
            "👋 Welcome to the bot!\nClick on the buttons below to upload a Reels or multiple Reels at once.",
            reply_markup=main_menu_en
        )



@app.on_message(filters.text & filters.regex("^📤 ارسال یک Reels$"))
async def request_single_reels_fa(client, message):
    user_id = message.from_user.id

    await message.reply("🎥 لطفاً فیلم خود را ارسال کنید.")

@app.on_message(filters.text & filters.regex("^📤 Upload a Reels$"))
async def request_single_reels_en(client, message):
    user_id = message.from_user.id
    await message.reply("🎥 Please send your video.")


@app.on_message(filters.text & filters.regex("^📤 ارسال چند Reels همزمان$"))
async def request_multiple_reels_fa(client, message):
    user_id = message.from_user.id

    await message.reply("🎥 لطفاً چند ویدئوی خود را ارسال کنید. ربات به ترتیب و با فاصله 30 ثانیه آنها را آپلود خواهد کرد.")

@app.on_message(filters.text & filters.regex("^📤 Upload Multiple Reels$"))
async def request_multiple_reels_en(client, message):

    await message.reply("🎥 Please send your videos. The bot will upload them one by one with a 30-second gap.")


@app.on_message(filters.video)
async def upload_multiple_reels(client, message):
    user_id = message.from_user.id

    try:
        
        language = get_language(user_id)

        
        video_path = await message.download()

        
        with open(CAPTION_FILE, "r", encoding="utf-8") as file:
            caption = file.read().strip()

        
        insta_client.clip_upload(video_path, caption)

        
        if language == "fa":
            await message.reply("✅ فیلم با موفقیت به عنوان Reels در اینستاگرام پست شد.")
        else:
            await message.reply("✅ The video was successfully uploaded as a Reels on Instagram.")

        
        await asyncio.sleep(30)

    except Exception as e:
        
        if language == "fa":
            await message.reply(f"⚠️ خطا: {e}")
        else:
            await message.reply(f"⚠️ Error: {e}")


app.run()
