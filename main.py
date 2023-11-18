import logging
logger = logging.getLogger(__name__)

import os
from os import getenv
from os import environ
from telegraph import upload_file
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

Bot = Client(
    "Telegraph Uploader Bot",
    bot_token=os.environ.get("BOT_TOKEN", "6320796768:AAGu6C6R991duq6K1LGBiD3Sn1WHPaK_oUU"),
    api_id=int(os.environ.get("API_ID", "11973721")),
    api_hash=os.environ.get("API_HASH", "5264bf4663e9159565603522f58d3c18")
)
BANNED_CHANNELS = list(set(int(x) for x in str(getenv("BANNED_CHANNELS", "-1001296894100")).split()))
DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS/")

START_CAPTION = """ʜᴇʏ {}, 🥀
๏ ᴛʜɪs ɪs {} !

➻ ꜱᴇɴᴅ ᴀɴʏ ʙᴇʟᴏᴡ 5ᴍʙ ᴘʜᴏᴛᴏ/ᴠɪᴅᴇᴏ ᴛᴏ ɢᴇᴛ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ 

──────────────────
๏ ᴛʜᴀɴᴋꜱ ʙʏ 💞 @Privates_RoBot

──────────────────
๏ ⚔️ ᴘᴏᴡᴇʀ ʙʏ @Prime_Rolex"""

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('✨ 𝚄𝙿𝙳𝙰𝚃𝙴𝚂 𝙲𝙷𝙰𝙽𝙽𝙴𝙻', url='https://telegram.me/Privates_RoBot')
        ]
    ]
)

@Bot.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_CAPTION,
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    else:
        await update.message.delete()

@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    # Send the start photo with caption
    await bot.send_photo(
        chat_id=update.chat.id,
        photo="https://graph.org/file/24297757645fd9e66203e.jpg",
        caption=START_CAPTION.format(update.from_user.mention, "TeleGraph Bot"),
        reply_markup=START_BUTTONS
    )

@Bot.on_message(filters.private & filters.media)
async def getmedia(bot, update):
    medianame = DOWNLOAD_LOCATION + str(update.from_user.id)
    try:
        message = await update.reply_text(
            text="`ᴘʀᴏᴄᴇꜱꜱɪɴɢ...`",
            quote=True,
            disable_web_page_preview=True
        )
        await bot.download_media(
            message=update,
            file_name=medianame
        )
        response = upload_file(medianame)
        try:
            os.remove(medianame)
        except:
            pass
    except Exception as error:
        text=f"Error :- <code>{error}</code>"
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton('More Help', callback_data='help')]]
        )
        await message.edit_text(
            text=text,
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
        return
    text=f"**Link :-** `https://telegra.ph{response[0]}`\n\n**Join :-** @Privates_RoBot"
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="ᴏᴘᴇɴ ʟɪɴᴋ 🛡️", url=f"https://telegra.ph{response[0]}"),
                InlineKeyboardButton(text="ꜱʜᴇʀᴇ ʟɪɴᴋ 🗡️", url=f"https://telegram.me/share/url?url=https://telegra.ph{response[0]}")
            ]
        ]
    )
    await message.edit_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

@Bot.on_message(
    filters.channel
    & (
        filters.document
        | filters.video
    ),
    group=4,
)
async def channel_receive_handler(bot, broadcast):
    if int(broadcast.chat.id) in Config.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔥 Uploaded By", url=f'https://telegram.me/Star_Moviess_Tamil')]])
    try:
        await bot.edit_message_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass

Bot.run()
