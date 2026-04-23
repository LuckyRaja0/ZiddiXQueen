import asyncio
import os
import random

from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from pyrogram.errors import (
    ChatAdminRequired,
    ChatWriteForbidden,
    PeerIdInvalid,
    UserNotParticipant,
)
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
SESSION_NAME = os.environ.get("SESSION_NAME", "")
MONGO_URL = os.environ.get("MONGO_URL", "")


if not all([API_ID, API_HASH, SESSION_NAME, MONGO_URL]):
    raise SystemExit(
        "Missing required environment variables: API_ID, API_HASH, "
        "SESSION_NAME, MONGO_URL"
    )


client = Client(
    name="ziddixqueen",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_NAME,
    in_memory=True,
)


mongo_client = MongoClient(MONGO_URL)
chatai = mongo_client["Word"]["WordDb"]
ziddi = mongo_client["ziddiDb"]["ziddi"]


@client.on_message(
    filters.command("repo", prefixes=["/", ".", "?", "-"]) & ~filters.private
)
async def chatbot(client, message):
    await message.delete()
    ziddiai_msg = await message.reply("🤭🤏✌️")
    await asyncio.sleep(1)
    await ziddiai_msg.edit("**ʙᴏʜᴀᴛ ᴛᴀɪᴊ ʜᴏ ʀᴇᴘᴏ ᴄʜᴀʜɪʏᴇ**")
    await asyncio.sleep(1)
    await ziddiai_msg.edit("**ɪ group se jake lelo 💕**")
    await asyncio.sleep(1)
    await ziddiai_msg.edit(
        "[GO FAST TO GET REPO](https://t.me/+g0YcEKl54yU0ZTU9)"
    )
    await asyncio.sleep(2)
    await message.reply_sticker(
        "CAACAgIAAxkBAAEForNjAykaq_efq4Wd-9KZv-nNxJRn3AACIgMAAm2wQgO8x8PfoXC1eCkE"
    )
    await asyncio.sleep(2)
    await message.reply_photo(
        photo="http://telegra.ph/file/8f4e86e223b3051307dce.jpg",
        caption=(
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "💥 A ᴘᴏᴡᴇʀғᴜʟ ᴀɪ ʙᴏᴛ\n"
            "ᴏғ ♻️ 𝐓𝐈𝐌𝐄 𝐏𝐀𝐒𝐒 🏷️ 🔥\n"
            "━━━━━━━━━━━━━━━━━\n"
            "ᴅᴀᴛᴀʙᴀsᴇ ʙᴀᴄᴋᴇɴᴅ ʙᴏᴛ ғᴏʀ ᴛɢ...\n"
            "┏━━━━━━━━━━━━━━━━━┓\n"
            "┣★ ᴄʀᴇᴀᴛᴇʀ [𝐓𝐈𝐌𝐄 𝐏𝐀𝐒𝐒 🏷️](https://t.me/time_pass_back)\n"
            "┣★ ʙᴏᴛ ᴜᴏᴅᴀᴛᴇs [ᴏᴜʀ ᴏᴛʜᴇʀ ʙᴏᴛs](https://t.me/ziddixbot)\n"
            "┣★ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ [ᴄʜᴀᴛ](https://t.me/+pc-wb-d-ZTliNzNl)\n"
            "┗━━━━━━━━━━━━━━━━━┛\n"
            "💞 \n"
            "IF HAVE ANY QUESTION THEN CONTACT » TO » MY » [OWNER] "
            "@TIME_PASS_BACK"
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🌼 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ 💮",
                        url="https://t.me/+pc-wb-d-ZTliNzNl",
                    )
                ]
            ]
        ),
    )


@client.on_message(
    filters.command("alive", prefixes=["/", ".", "?", "-"]) & ~filters.private
)
async def start(client, message):
    await message.reply_text("**Ziddi x Queen is alive**")


async def _pick_reply(word):
    """Return (text, kind) tuple for a reply, or (None, None) if none found."""
    cursor = chatai.find({"word": word})
    candidates = [doc["text"] for doc in cursor]
    if not candidates:
        return None, None
    hey = random.choice(candidates)
    is_text = chatai.find_one({"text": hey})
    kind = is_text.get("check") if is_text else None
    return hey, kind


async def _send_reply(message, hey, kind, prefer_sticker):
    """Send the reply as sticker or text depending on stored kind.

    `prefer_sticker=True` means: if kind is not "text", send as sticker
    (used when the trigger was a sticker).
    `prefer_sticker=False` means: if kind is not "sticker", send as text
    (used when the trigger was text).
    """
    if prefer_sticker:
        if kind == "text":
            await message.reply_text(hey)
        else:
            await message.reply_sticker(hey)
    else:
        if kind == "sticker":
            await message.reply_sticker(hey)
        else:
            await message.reply_text(hey)


@client.on_message(
    filters.text & ~filters.private & ~filters.me & ~filters.bot
)
async def ziddiai(client: Client, message: Message):
    is_ziddi = ziddi.find_one({"chat_id": message.chat.id})

    if not message.reply_to_message:
        if is_ziddi:
            return
        hey, kind = await _pick_reply(message.text)
        if hey is None:
            return
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        await _send_reply(message, hey, kind, prefer_sticker=False)
        return

    me = await client.get_me()
    user_id = me.id
    if message.reply_to_message.from_user and (
        message.reply_to_message.from_user.id == user_id
    ):
        if is_ziddi:
            return
        hey, kind = await _pick_reply(message.text)
        if hey is None:
            return
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        await _send_reply(message, hey, kind, prefer_sticker=False)
        return

    # Learn: someone replied with text to another user's message
    reply = message.reply_to_message
    if reply.text:
        exists = chatai.find_one(
            {"word": reply.text, "text": message.text}
        )
        if not exists:
            chatai.insert_one(
                {"word": reply.text, "text": message.text, "check": "none"}
            )
    elif reply.sticker:
        exists = chatai.find_one(
            {
                "word": reply.sticker.file_unique_id,
                "text": message.text,
            }
        )
        if not exists:
            chatai.insert_one(
                {
                    "word": reply.sticker.file_unique_id,
                    "text": message.text,
                    "check": "text",
                }
            )


@client.on_message(
    filters.sticker & ~filters.private & ~filters.me & ~filters.bot
)
async def ziddistickerai(client: Client, message: Message):
    is_ziddi = ziddi.find_one({"chat_id": message.chat.id})

    if not message.reply_to_message:
        if is_ziddi:
            return
        hey, kind = await _pick_reply(message.sticker.file_unique_id)
        if hey is None:
            return
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        await _send_reply(message, hey, kind, prefer_sticker=True)
        return

    me = await client.get_me()
    user_id = me.id
    if message.reply_to_message.from_user and (
        message.reply_to_message.from_user.id == user_id
    ):
        if is_ziddi:
            return
        hey, kind = await _pick_reply(message.sticker.file_unique_id)
        if hey is None:
            return
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        await _send_reply(message, hey, kind, prefer_sticker=True)
        return

    # Learn: someone replied with a sticker
    reply = message.reply_to_message
    if reply.text:
        exists = chatai.find_one(
            {
                "word": reply.text,
                "id": message.sticker.file_unique_id,
            }
        )
        if not exists:
            chatai.insert_one(
                {
                    "word": reply.text,
                    "text": message.sticker.file_id,
                    "check": "sticker",
                    "id": message.sticker.file_unique_id,
                }
            )
    elif reply.sticker:
        exists = chatai.find_one(
            {
                "word": reply.sticker.file_unique_id,
                "text": message.sticker.file_id,
            }
        )
        if not exists:
            chatai.insert_one(
                {
                    "word": reply.sticker.file_unique_id,
                    "text": message.sticker.file_id,
                    "check": "none",
                }
            )


@client.on_message(
    filters.text & filters.private & ~filters.me & ~filters.bot
)
async def ziddiprivate(client: Client, message: Message):
    if message.reply_to_message:
        me = await client.get_me()
        if not (
            message.reply_to_message.from_user
            and message.reply_to_message.from_user.id == me.id
        ):
            return

    hey, kind = await _pick_reply(message.text)
    if hey is None:
        return
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    await _send_reply(message, hey, kind, prefer_sticker=False)


@client.on_message(
    filters.sticker & filters.private & ~filters.me & ~filters.bot
)
async def ziddiprivatesticker(client: Client, message: Message):
    if message.reply_to_message:
        me = await client.get_me()
        if not (
            message.reply_to_message.from_user
            and message.reply_to_message.from_user.id == me.id
        ):
            return

    hey, kind = await _pick_reply(message.sticker.file_unique_id)
    if hey is None:
        return
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    await _send_reply(message, hey, kind, prefer_sticker=True)


if __name__ == "__main__":
    client.run()
