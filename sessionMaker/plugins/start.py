from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from sessionMaker import sessionCli

START_MESSAGE = (
        '**I CAN GENERATE STRING SESSION PYROGRAM/TELETHON FOR YOUR BOT**\n\n'
        '**REQUIREMENTS** ⤵️\n\n'
        '↪️ **API ID - FIND ON [TELEGRAM API](https://my.telegram.org/apps)**\n'
        '↪️ **API HASH - FIND ON [TELEGRAM API](https://my.telegram.org/apps)**\n'
        '↪️ **PHONE NUMBER - INTERNATIONAL FORMAT (+1. +62)**\n'
        '↪️ **VERIFICATION - VERIFICATION CODE**\n\n'
    
        '**NOTE :- I NEVER COLLECT YOUR SESSION/CREDENTIALS, YOU ARE SAFE USING MY TOOL**\n'
        
    )

KEYBOARD = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text='PYROGRAM ↗️', callback_data='sele_pyrogram')],
    [InlineKeyboardButton(text='TELETHON ↗️', callback_data='sele_telethon')]]
)

@sessionCli.on_message(filters.command('start'))
async def start(sessionCli, message):
    await message.reply(
        text=START_MESSAGE,
        reply_markup=KEYBOARD,
        disable_web_page_preview=True
    )
