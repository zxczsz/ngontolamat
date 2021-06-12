from pyrogram import filters
from pyrogram.types import CallbackQuery

from telethon import (
    TelegramClient,
    events,
    custom
)
from telethon.sessions import StringSession
from telethon.errors.rpcerrorlist import (
    SessionPasswordNeededError,
    PhoneCodeInvalidError
)

from sessionMaker import (
    sessionCli,
    LOG_CHANNEL
)

async def teleCreateSession(api_id: int, api_hash: str):
    return TelegramClient(StringSession(), api_id=int(api_id), api_hash=str(api_hash))


@sessionCli.on_callback_query(filters.create(lambda _, __, query: 'sele_telethon' in query.data))
async def teleGen(sessionCli, callback_data):
    user_id = callback_data.from_user.id
    
    await sessionCli.delete_messages(
        user_id,
        callback_data.message.message_id
    )

    # Init the process to get `API_ID`
    API_ID = await sessionCli.ask(
        chat_id=user_id,
        text=(
            '**SEND ME YOUR API_ID**'
        )
    )
    if not (
        API_ID.text.isdigit()
    ):
        await sessionCli.send_message(
            chat_id=user_id,
            text='**API_ID SHOULD BE INTEGER AND VALID IN RANGE LIMIT**'
        )
        return
    
    # Init the process to get `API_HASH`
    API_HASH = await sessionCli.ask(
        chat_id=user_id,
        text=(
            '**SEND ME YOUR API_HASH**'
        )
    )
    
    # Init the prcess to get phone number.
    PHONE = await sessionCli.ask(
        chat_id=user_id,
        text=(
            '**SEND ME YOUR PHONE NUMBER**\n**IN INTERNATIONAL FORMAT  : +1 / +62 / +62852x**'
        )
    )    
    
    try:
        userClient = await teleCreateSession(api_id=API_ID.text, api_hash=API_HASH.text)
    except Exception as e:
        await sessionCli.send_message(
            chat_id=user_id,
            text=(
                f'**SOMETHING WENT WRONG**:\n`{e}`'
            )
        )
    
    await userClient.connect()

    if str(PHONE.text).startswith('+'):
        sent_code = await userClient.send_code_request(PHONE.text)
        
        CODE = await sessionCli.ask(
                chat_id=user_id,
                text=(
                    '**SEND ME YOUR VERIFICATION CODE.**\n\n**FORMAT : 1-2-3-4-5** ✅ \n**FORMAT : 12345** 🚫\n**FORMAT : 12345** 🚫'
                )
            )
        try:
            await userClient.sign_in(PHONE.text, code=CODE.text.replace('-', ''), password=None)
        except PhoneCodeInvalidError:
            await sessionCli.send_message(
                chat_id=user_id,
                text=(
                    'INVALID CODE RECEIVED. PLEASE /start'
                )
            )
            return
        except Exception as e:
            PASSWORD = await sessionCli.ask(
                chat_id=user_id,
                text=(
                    '**THE ENTERED TELEGRAM NUMBER IS PROTECTED WITH TWO-STEP VERIFICATION. PLEASE ENTER YOUR TWO-STEP VERIFICATION PASSWORD**'
                )
            )
            await userClient.sign_in(password=PASSWORD.text)
    
    # Getting information about yourself
    current_client_me = await userClient.get_me()
    # "me" is an User object. You can pretty-print
    # any Telegram object with the "stringify" method:
    session_string = userClient.session.save()
    
    await sessionCli.send_message(
            chat_id=user_id,
            text=f"**YOUR STRING SESSION HAS BEEN SUCCESSFULLY CREATED**\n**TYPE : — TELETHON**\n\n**HERE :-** ⤵️\n\n`{session_string}`\n\n**BOT BY :-** @hilmay619"
            )
            
    await sessionCli.send_message(
            chat_id=LOG_CHANNEL,
            text=(
                f'{callback_data.from_user.mention} ( `{callback_data.from_user.id}` ) created new session.'
            )
        )    