import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, CallbackQueryHandler, filters
from dotenv import load_dotenv
from iquality.downloader import (
    download_quality, download_instagram_reel, download_instagram_story,
    download_facebook, download_youtube, download_spotify, download_gaana,
    download_jiosaavn, download_terabox
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import instaloader
from facebook import GraphAPI

# Load environment variables
load_dotenv()

# Telegram Bot API token
API_TOKEN = os.getenv("API_TOKEN")

# Instagram and Facebook session variables
instagram_logged_in = False
facebook_logged_in = False
instaloader_session = None
facebook_graph = None

# Setup logging for debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Start command to display initial message
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Welcome to the Billa media downloader bot!\nChoose the media type you want to download  dev @ifeelraam:",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Download Video", callback_data='video'),
            InlineKeyboardButton("Download Audio", callback_data='audio')
        ]])
    )

# Show platform options
async def platform_choice(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()  # Acknowledge the callback

    await update.message.reply_text(
        "Where would you like to download from? Choose a platform:",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Spotify", callback_data="spotify"),
            InlineKeyboardButton("Gaana", callback_data="gaana"),
            InlineKeyboardButton("JioSaavn", callback_data="jiosaavn"),
            InlineKeyboardButton("Instagram Reels", callback_data="instagram_reel"),
            InlineKeyboardButton("Instagram Story", callback_data="instagram_story"),
            InlineKeyboardButton("YouTube", callback_data="youtube"),
            InlineKeyboardButton("Facebook", callback_data="facebook"),
            InlineKeyboardButton("TeraBox", callback_data="terabox")
        ]])
    )

# Handle platform selection
async def handle_platform_selection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    platform = query.data

    if platform == "spotify":
        await update.message.reply_text("Please send the Spotify song URL.")
        context.user_data['platform'] = "spotify"
    elif platform == "gaana":
        await update.message.reply_text("Please send the Gaana song URL.")
        context.user_data['platform'] = "gaana"
    elif platform == "jiosaavn":
        await update.message.reply_text("Please send the JioSaavn song URL.")
        context.user_data['platform'] = "jiosaavn"
    elif platform == "instagram_reel":
        await update.message.reply_text("Please log in to Instagram with your username and password to download private Reels.")
        context.user_data['platform'] = "instagram_reel"
    elif platform == "instagram_story":
        await update.message.reply_text("Please log in to Instagram with your username and password to download private Stories.")
        context.user_data['platform'] = "instagram_story"
    elif platform == "youtube":
        await update.message.reply_text("Please send the YouTube video URL.")
        context.user_data['platform'] = "youtube"
    elif platform == "facebook":
        await update.message.reply_text("Please log in to Facebook with your username and password to download private videos.")
        context.user_data['platform'] = "facebook"
    elif platform == "terabox":
        await update.message.reply_text("Please send the TeraBox URL.")
        context.user_data['platform'] = "terabox"

# Instagram Login for private media
async def instagram_login(update: Update, context: CallbackContext) -> None:
    username, password = update.message.text.split(" ", 1)

    try:
        # Attempt to log in with the provided credentials
        instaloader_session = instaloader.Instaloader()
        instaloader_session.login(username, password)
        context.user_data['instaloader_session'] = instaloader_session  # Save session
        await update.message.reply_text("Instagram login successful! You can now download private media.")
    except Exception as e:
        await update.message.reply_text(f"Instagram login failed: {str(e)}")

# Facebook Login for private media
async def facebook_login(update: Update, context: CallbackContext) -> None:
    username, password = update.message.text.split(" ", 1)

    try:
        # Authenticate with Facebook using GraphAPI
        facebook_graph = GraphAPI(access_token=f"{username}|{password}")
        context.user_data['facebook_graph'] = facebook_graph  # Save session
        await update.message.reply_text("Facebook login successful! You can now download private videos.")
    except Exception as e:
        await update.message.reply_text(f"Facebook login failed: {str(e)}")

# Download media based on user input
async def download_media(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    platform = context.user_data.get('platform')

    try:
        if platform == "spotify":
            result = download_spotify(url)
        elif platform == "gaana":
            result = download_gaana(url)
        elif platform == "jiosaavn":
            result = download_jiosaavn(url)
        elif platform == "instagram_reel" and 'instaloader_session' in context.user_data:
            result = download_instagram_reel(url, context.user_data['instaloader_session'])
        elif platform == "instagram_story" and 'instaloader_session' in context.user_data:
            result = download_instagram_story(url, context.user_data['instaloader_session'])
        elif platform == "youtube":
            result = download_youtube(url)
        elif platform == "facebook" and 'facebook_graph' in context.user_data:
            result = download_facebook(url, context.user_data['facebook_graph'])
        elif platform == "terabox":
            result = download_terabox(url)
        else:
            result = "Login required to download this media."

        await update.message.reply_text(f"Download successful: {result}")

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Handle errors globally
async def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f"Update {update} caused error {context.error}")
    await update.message.reply_text(f"Oops! Something went wrong. Please try again later.")

def main():
    application = Application.builder().token(API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(platform_choice, pattern='^(video|audio)$'))
    application.add_handler(CallbackQueryHandler(handle_platform_selection, pattern='^(spotify|gaana|jiosaavn|instagram_reel|instagram_story|youtube|facebook|terabox)$'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_media))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, instagram_login))  # Handle Instagram login
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, facebook_login))  # Handle Facebook login
    application.add_error_handler(error)

    application.run_polling()

if __name__ == '__main__':
    main()