from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

from pyrogram.errors.exceptions import bad_request_400
from pyrogram.errors import (
    FloodWait,
    SessionPasswordNeeded,
    PhoneCodeInvalid,
    PhoneCodeExpired
)

from sessionMaker import (
    sessionCli,
    LOG_CHANNEL
)

async def pyroCreateSession(api_id: int, api_hash: str):
    return Client(":memory:", api_id=int(api_id), api_hash=str(api_hash)) 

@sessionCli.on_callback_query(filters.create(lambda _, __, query: 'sele_pyrogram' in query.data))
async def pyroGen(sessionCli, callback_data):
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
    if str(PHONE.text).startswith('+'):
        
        # Creating userClient 
        try:
            userClient = await pyroCreateSession(int(API_ID.text), str(API_HASH.text))
        except Exception as e:
            await API_HASH.reply(f'**SOMETHING WENT WRONG**:\n`{e}`')
            return
        
        try:
            await userClient.connect()
        except ConnectionError:
            await userClient.disconnect()
            await userClient.connect()
        
        try:
            sent_code = await userClient.send_code(PHONE.text)
        except FloodWait as e:
            await sessionCli.send_message(
                chat_id=user_id,
                text=(
                    f"**I CANNOT CREATE SESSION FOR YOU.\n**BECAUSE YOU HAVE A FLOODWAIT OF :** `{e.x} SECONDS`"
                )
            )
            return
        
        except bad_request_400 as e:
            await sessionCli.send_message(
                chat_id=user_id,
                text=(
                    f'`{e}`'
                )
            )
            return
        
        ASK_CODE = await sessionCli.ask(
            chat_id=user_id,
            text=(
                '**SEND ME YOUR VERIFICATION CODE.**\n\n**FORMAT : 1-2-3-4-5** ✅ \n**FORMAT : 12345** 🚫\n**FORMAT : 12345** 🚫'
            )
        )

        try:
            await userClient.sign_in(
                phone_number=PHONE.text,
                phone_code_hash=sent_code.phone_code_hash,
                phone_code=ASK_CODE.text.replace('-', '')
            )
        except SessionPasswordNeeded:
            PASSWARD = await sessionCli.ask(
                chat_id=user_id,
                text=(
                "**THE ENTERED TELEGRAM NUMBER IS PROTECTED WITH TWO-STEP VERIFICATION. PLEASE ENTER YOUR TWO-STEP VERIFICATION PASSWORD**"
                )
            )

            try:
                await userClient.check_password(PASSWARD.text)
            except Exception as e:
                await sessionCli.send_message(
                    chat_id=user_id,
                    text=(
                        f'**SOMETHING WENT WRONG** :\n`{e}`'
                    )
                )
                return

        except PhoneCodeInvalid:
            await sessionCli.send_message(
                chat_id=user_id,
                text=(
                    "**THE CODE YOU SENT SEEMS INVALID, TRY AGAIN.**"
                )
            )
            return
        
        except PhoneCodeExpired:
            await sessionCli.send_message(
                chat_id=user_id,
                text=(
                    '**THE CODE YOU SENT SEEMS EXPIRED. TRY AGAIN.**'
                )
            )
            return

        session_string = await userClient.export_session_string()
        await sessionCli.send_message(
            chat_id=user_id,
            text=(
                f'**YOUR STRING SESSION HAS BEEN SUCCESSFULLY CREATED**\n**TYPE : — PYROGRAM**\n\n**HERE :-** ⤵️\n\n`{session_string}`\n\n**BOT BY :-** @hilmay619'
            )
        )

        await sessionCli.send_message(
            chat_id=LOG_CHANNEL,
            text=(
                f'{callback_data.from_user.mention} ( `{callback_data.from_user.id}` ) created new session.'
            )
        )
    
    else:
        try:
            botClient = await pyroCreateSession(api_id=int(API_ID.text), api_hash=str(API_HASH.text))
        except Exception as e:
            await sessionCli.send_message(
                chat_id=user_id,
                text=(
                    f'**SOMETHING WENT WRONG**:\n`{e}`'
                )
            )
            return
        try:
            await botClient.connect()
        except ConnectionError:
            await botClient.disconnect()
            await botClient.connect()
        
        try:
            await botClient.sign_in_bot(PHONE.text)
        except bad_request_400 as e:
            await sessionCli.send_message(
                chat_id=user_id,
                text=f'`{e}`'
            )
            return
        
        await sessionCli.send_message(
            chat_id=user_id,
            text=(
                f'**YOUR STRING SESSION HAS BEEN SUCCESSFULLY CREATED**\n**TYPE : — PYROGRAM**\n\n**HERE :-** ⤵️\n\n `{(await botClient.export_session_string())}`\n\n**BOT BY :-** @hilmay619'
            )
        )

        await sessionCli.send_message(
            chat_id=LOG_CHANNEL,
            text=(
                f'{callback_data.from_user.mention} ( `{callback_data.from_user.id}` ) created new session.'
            )
        )