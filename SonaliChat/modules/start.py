import asyncio
import random

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.enums import ChatType

from config import STICKER, FSUB, IMG, LOGGER_GROUP_ID, BOT_USERNAME
from SonaliChat import app
from SonaliChat.database import add_user, add_chat, get_fsub, chatsdb
from SonaliChat.modules.helpers import STBUTTON, START, HELP_READ, HELP_ABOUT, ABOUT_BUTTON

FSUB = str(FSUB).lower() == "true"


@app.on_message(filters.command(["start", "aistart"]) & ~filters.bot)
async def start(client, m: Message):

    if FSUB and not await get_fsub(client, m):
        return

    if m.chat.type == ChatType.PRIVATE:
        user_id = m.from_user.id
        await add_user(user_id, m.from_user.username or None)

        # Send random sticker
        if STICKER and isinstance(STICKER, list):
            try:
                sticker_to_send = random.choice(STICKER)
                umm = await m.reply_sticker(sticker=sticker_to_send)
                await asyncio.sleep(1)
                await umm.delete()
            except Exception:
                pass

        # LOGGER_GROUP_ID
        log_msg = (
            f"**✦ ηєᴡ ᴜsєʀ sᴛᴧʀᴛєᴅ ᴛʜє ʙσᴛ**\n\n"
            f"**➻ ᴜsєʀ :** [{m.from_user.first_name}](tg://user?id={user_id})\n"
            f"**➻ ɪᴅ :** `{user_id}`"
        )
        try:
            await client.send_message(LOGGER_GROUP_ID, log_msg)
        except Exception:
            pass

        try:
            accha = await m.reply_text(text="**ꜱᴛᴧʀᴛɪηɢ....🥀**")
            await asyncio.sleep(1)
            await accha.edit("**ᴘɪηɢ ᴘσηɢ...🍫**")
            await asyncio.sleep(0.5)
            await accha.edit("**ꜱᴛᴧʀᴛєᴅ.....😱**")
            await asyncio.sleep(0.5)
            await accha.delete()
        except Exception:
            pass

        # Send random photo
        try:
            if IMG and isinstance(IMG, list):
                await m.reply_photo(
                    photo=random.choice(IMG),
                    caption=START,
                    reply_markup=InlineKeyboardMarkup(STBUTTON),
                )
        except Exception:
            pass


# Bot added to group
@app.on_message(filters.new_chat_members)
async def on_new_chat_members(client: Client, message: Message):
    if (await client.get_me()).id in [user.id for user in message.new_chat_members]:
        chat_id = message.chat.id
        chat_title = message.chat.title
        added_by = message.from_user.mention if message.from_user else "Unknown User"
        chatusername = f"@{message.chat.username}" if message.chat.username else "Private Chat"

        # Try to get invite link
        try:
            invite_link = await client.export_chat_invite_link(chat_id)
        except Exception:
            invite_link = "Not Available"

        # Add chat to DB
        await add_chat(chat_id, chat_title)

        # Send welcome photo
        try:
            if IMG and isinstance(IMG, list):
                await message.reply_photo(
                    photo=random.choice(IMG),
                    caption=START,
                    reply_markup=InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton(
                                "ᴧᴅᴅ ϻє ʙᴧʙʏ",
                                url=f"https://t.me/{BOT_USERNAME}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users"
                            ),
                            InlineKeyboardButton("ᴊσɪη sᴜᴘᴘσʀᴛ", url="https://t.me/purvi_support")
                        ]
                    ])
                )
        except Exception:
            pass

        # Log group added
        log_msg = (
            f"<b>✦ ʙᴏᴛ #ᴀᴅᴅᴇᴅ ɪɴ ᴀ ɢʀᴏᴜᴘ</b>\n\n"
            f"**⚘ ɢʀᴏᴜᴘ ɴᴀᴍᴇ :** {chat_title}\n"
            f"**⚘ ɢʀᴏᴜᴘ ɪᴅ :** {chat_id}\n"
            f"**⚘ ᴜsᴇʀɴᴀᴍᴇ :** {chatusername}\n"
            f"**⚘ ɢʀᴏᴜᴘ ʟɪɴᴋ : [ᴛᴀᴘ ʜᴇʀᴇ]({invite_link})**\n"
            f"**⚘ ᴀᴅᴅᴇᴅ ʙʏ :** {added_by}"
        )
        try:
            await app.send_photo(
                LOGGER_GROUP_ID,
                photo=random.choice(IMG),
                caption=log_msg,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("ɢʀᴏᴜᴘ ʟɪɴᴋ", url=invite_link if invite_link != "Not Available" else "https://t.me/purvi_support")]
                ])
            )
        except Exception:
            pass


@app.on_message(filters.left_chat_member)
async def on_left_chat_member(client: Client, message: Message):
    if (await client.get_me()).id == message.left_chat_member.id:
        chat_id = message.chat.id
        chat_title = message.chat.title
        remove_by = message.from_user.mention if message.from_user else "Unknown User"

        # Remove from DB
        await chatsdb.delete_one({"chat_id": chat_id})

        # Log left
        left_msg = (
            f"<b>✦ ʙᴏᴛ #ʟᴇғᴛ ᴀ ɢʀᴏᴜᴘ</b>\n\n"
            f"**⚘ ɢʀᴏᴜᴘ ɴᴀᴍᴇ :** {chat_title}\n"
            f"**⚘ ɢʀᴏᴜᴘ ɪᴅ :** {chat_id}\n"
            f"**⚘ ʀᴇᴍᴏᴠᴇᴅ ʙʏ :** {remove_by}"
        )
        try:
            await app.send_photo(
                LOGGER_GROUP_ID,
                photo=random.choice(IMG),
                caption=left_msg,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        "sᴇᴇ ɢʀᴏᴜᴘ",
                        url=f"https://t.me/{message.chat.username}" if message.chat.username else "https://t.me/purvi_support"
                    )]
                ])
            )
        except Exception:
            pass


# Help command
@app.on_message(filters.command("help"))
async def help_command(client, message):
    try:
        if IMG and isinstance(IMG, list):
            await message.reply_photo(
                photo=random.choice(IMG),
                caption=HELP_READ,
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            "ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ",
                            url=f"https://t.me/{client.me.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users"
                        ),
                        InlineKeyboardButton("ᴊᴏɪɴ sᴜᴘᴘᴏʀᴛ", url="https://t.me/purvi_support")
                    ]
                ])
            )
    except Exception:
        pass


# Callback Queries
@app.on_callback_query(filters.regex('help'))
async def help_button(client, callback_query):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ", callback_data="back"),
            InlineKeyboardButton("ᴊᴏɪɴ sᴜᴘᴘᴏʀᴛ", url="https://t.me/purvi_support")
        ]
    ])
    await callback_query.answer()
    await callback_query.message.edit_text(HELP_READ, reply_markup=keyboard)


@app.on_callback_query(filters.regex('back'))
async def back_to_menu(client, callback_query):
    await callback_query.message.edit_text(text=START, reply_markup=InlineKeyboardMarkup(STBUTTON))


@app.on_callback_query(filters.regex('ABOUT'))
async def about_section(client, callback_query):
    await callback_query.answer()
    await callback_query.message.edit_text(HELP_ABOUT, reply_markup=InlineKeyboardMarkup(ABOUT_BUTTON))


@app.on_callback_query(filters.regex('HELP_BACK'))
async def help_back(client, callback_query):
    await callback_query.message.edit_text(text=START, reply_markup=InlineKeyboardMarkup(STBUTTON))


# ---------------- AI CHATBOT GROUP HANDLER ---------------- #
@app.on_message(filters.text & filters.group & ~filters.bot)
async def group_chatbot(client, message):
    user_text = message.text
    # Example: Simple echo, replace with AI logic if needed
    reply_text = f"🤖 You said: {user_text}"
    await message.reply_text(reply_text)
