import re
import os
import time
import config
import random
import asyncio
import datetime
import subprocess
from telethon import TelegramClient, events, Button, types

client = TelegramClient('easychess', config.app_id, config.app_hash, connection_retries=None, retry_delay=15).start(bot_token=config.token)
ongoing_matches = {}
ongoing_matches_spam_timer = {}

@client.on(events.NewMessage())
async def make_normal_match(event):
    if(event.text.lower() == '/make' or event.text.lower() == '/make@easychessbot'):
        await make_match(event, False)
    if(event.text.lower() == '/makelegacy' or event.text.lower() == '/makelegacy@easychessbot'):
        await make_match(event, True)
    if(event.text.lower() == '/help' or event.text.lower() == '/help@easychessbot' or event.text.lower() == '/start' or event.text.lower() == '/start@easychessbot'):
        await event.reply("""Normal Mode:

‌ ♖︎  ♘︎  ♗︎  ♔︎ ♕︎ ♗︎ ♘︎  ♖︎
‌ ♙︎  ♙︎  ♙︎  ♙︎  ♙︎ ♙︎  ♙︎  ♙︎
⬜⬛⬜⬛⬜⬛⬜⬛
⬛⬜⬛⬜⬛⬜⬛⬜
⬜⬛⬜⬛⬜⬛⬜⬛
⬛⬜⬛⬜⬛⬜⬛⬜
‌ ♟︎‍  ♟︎‍  ♟︎‍  ♟︎‍  ♟︎‍ ♟︎‍  ♟︎‍  ♟︎‍
‌ ♜︎  ♞︎  ♝︎  ♚︎ ♛︎ ♝︎ ♞︎  ♜︎


Legacy Mode:

Ⓡ Ⓝ Ⓑ Ⓚ Ⓠ Ⓑ Ⓝ Ⓡ
Ⓟ Ⓟ Ⓟ Ⓟ Ⓟ Ⓟ Ⓟ Ⓟ
⬜⬛⬜⬛⬜⬛⬜⬛
⬛⬜⬛⬜⬛⬜⬛⬜
⬜⬛⬜⬛⬜⬛⬜⬛
⬛⬜⬛⬜⬛⬜⬛⬜
🅟 🅟 🅟 🅟 🅟 🅟 🅟 🅟
🅡 🅝 🅑 🅚 🅠 🅑 🅝 🅡


You may have problems recognizing Normal Mode's chess pieces if your operating system does not have a emoji for each of them. in this case, consider using Legacy Mode.""")
    
async def make_match(event, legacy):
    user = await event.get_sender()
    name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
    user_tag = f"[{name}](tg://user?id={user.id})"
    created_match = await client.send_message(event.chat_id, f"Player White: {user_tag}\nWaiting for another player to join...", reply_to=event.id)
    if legacy:
        join_button = Button.inline("Join", data=f'join_{event.chat_id}@{created_match.id}[legacy]')
    else:
        join_button = Button.inline("Join", data=f'join_{event.chat_id}@{created_match.id}')
    match_folder = f"matches_history/{event.chat_id}@{created_match.id}"
    os.makedirs(match_folder, exist_ok=True)
    with open(f'{match_folder}/Players', 'a') as file:
        file.write(f"{event.sender_id} ")
    await client.edit_message(event.chat_id, created_match.id, f"Player White: {user_tag}\nWaiting for another player to join...", buttons=join_button)

@client.on(events.CallbackQuery())
async def callback_handler(event):
    print(event.data.decode())
    if 'join_' in str(event.data.decode()):
        match_id = str(event.data.decode()).replace('join_', '').replace('[legacy]', '')
    else:
        match_id = str(event.data.decode()).replace('[legacy]', '').split('_')[1]
    white_user_id = open(f'matches_history/{match_id}/Players').readline().split()[0]
    white_user = await client.get_entity(int(white_user_id))
    white_name = f"{white_user.first_name} {white_user.last_name}" if white_user.last_name else white_user.first_name
    white_user_tag = f"[{white_name}](tg://user?id={white_user.id})"
    second_user_id = event.sender_id
    second_user = await client.get_entity(int(second_user_id))
    second_name = f"{second_user.first_name} {second_user.last_name}" if second_user.last_name else second_user.first_name
    second_user_tag = f"[{second_name}](tg://user?id={second_user.id})"
    players_msg = f"Player White: {white_user_tag}\nPlayer Black: {second_user_tag}"

    if 'join_' in str(event.data.decode()):
        match_message = await client.get_messages(int(match_id.split('@')[0]), ids=int(match_id.split('@')[1]))
        if str(second_user_id) in match_message.text:
            await event.answer("You cannot re/join your own match.")
        else:
            with open(f'matches_history/{match_id}/Players', 'a') as file:
                file.write(f"{second_user_id}")
            await client.edit_message(int(match_id.split('@')[0]), int(match_id.split('@')[1]), f"{players_msg}\n\nPlayer White, pickup your piece:")
            if '[legacy]' in event.data.decode():
                await gameplay(event, match_id, None, True, players_msg)
            else:
                await gameplay(event, match_id, None, False, players_msg)
    else:
        if '[legacy]' in event.data.decode():
            await gameplay(event, match_id, str(event.data.decode()).split('_')[0], True, players_msg)
        else: 
            await gameplay(event, match_id, str(event.data.decode()).split('_')[0], False, players_msg)
async def gameplay(event, match_id, movement_data, legacy, players_msg):
    match_message = await client.get_messages(int(match_id.split('@')[0]), ids=int(match_id.split('@')[1]))
    white_player_id = open(f'matches_history/{match_id}/Players').readline().split()[0]
    black_player_id = open(f'matches_history/{match_id}/Players').readline().split()[1]
    if int(match_id.replace('@', '')) not in ongoing_matches:
        process = await asyncio.create_subprocess_exec('node', 'chess_handler/chess_handler.js', stdout=asyncio.subprocess.PIPE, stdin=asyncio.subprocess.PIPE)
        ongoing_matches[int(match_id.replace('@', ''))] = process
        ongoing_matches_spam_timer[int(match_id.replace('@', ''))] = datetime.datetime.now()
    else:
        process = ongoing_matches[int(match_id.replace('@', ''))]
        if movement_data:
            black_allowed = ['♔︎','♕︎','♖︎','♗︎','♘︎','♙︎','🔳','[♚︎]','[♛︎]','[♜︎]','[♝︎]','[♞︎]','[♟︎‍]','Ⓚ','Ⓠ','Ⓡ','Ⓑ','Ⓝ','Ⓟ','[🅚]','[🅠]','[🅡]','[🅑]','[🅝]','[🅟]']

            white_allowed =  ['♚︎','♛︎','♜︎','♝︎','♞︎','♟︎‍','🔲','[♔︎]','[♕︎]','[♖︎]','[♗︎]','[♘︎]','[♙︎]','🅚','🅠','🅡','🅑','🅝','🅟','[Ⓚ]','[Ⓠ]','[Ⓡ]','[Ⓑ]','[Ⓝ]','[Ⓟ]']
            chosen_piece = await get_piece(client, event.chat_id, match_id, movement_data)
            if (datetime.datetime.now() - ongoing_matches_spam_timer[int(match_id.replace('@', ''))]).total_seconds() > 3:
                if int(event.sender_id) == int(white_player_id) and chosen_piece in white_allowed:
                    process.stdin.write(movement_data.encode('utf-8') + b'\n')
                    await process.stdin.drain()
                
                elif int(event.sender_id) == int(black_player_id) and chosen_piece in black_allowed:
                    process.stdin.write(movement_data.encode('utf-8') + b'\n')
                    await process.stdin.drain()
                elif chosen_piece == '🔘':
                    return
                else:
                    print(chosen_piece)
                    await event.answer("Not your turn!")
                    return
                ongoing_matches_spam_timer[match_id] = datetime.datetime.now()
            else:
                print('spam')
                await event.answer("You must wait 3 seconds.")
    latest_board = ""
    while True:
        #if process.poll() is not None:
        #    del ongoing_matches[int(match_id.replace('@', ''))]
        #    await event.answer("Game Finished.")
        #    break 
        # ^^^^^^^^^^ Hello future me here i have no idea why is this section commented out but im gonna keep it because there must have been a reason for it. i guess.
        output = await process.stdout.readline()
        if output:
            chess, other, legal = separate_data(output.decode('utf-8'))
            print (chess, other, legal)
            if legal:
                for legals in legal:
                    legal_move = legals.split('#')[0]
                    legal_color = legals.split('#')[1]
                    chess = lastest_board.replace(f'{legal_move}:solid', f'{legal_move}:green:{legal_color}').replace(f'{legal_move}:rook:W', f'{legal_move}:rook:GW').replace(f'{legal_move}:pawn:W', f'{legal_move}:pawn:GW').replace(f'{legal_move}:king:W', f'{legal_move}:king:GW').replace(f'{legal_move}:bishop:W', f'{legal_move}:bishop:GW').replace(f'{legal_move}:queen:W', f'{legal_move}:queen:GW').replace(f'{legal_move}:knight:W', f'{legal_move}:knight:GW').replace(f'{legal_move}:rook:B', f'{legal_move}:rook:GB').replace(f'{legal_move}:pawn:B', f'{legal_move}:pawn:GB').replace(f'{legal_move}:king:B', f'{legal_move}:king:GB').replace(f'{legal_move}:bishop:B', f'{legal_move}:bishop:GB').replace(f'{legal_move}:queen:B', f'{legal_move}:queen:GB').replace(f'{legal_move}:knight:B', f'{legal_move}:knight:GB')
                    lastest_board = chess
                    other = other.replace(legal_move, '').replace('~', '').replace('&', '')
                    
            if chess:
                buttons = []
                lastest_board = chess
                if legacy:
                    pieces = chess.replace('rook:B', 'Ⓡ' ).replace('rook:W', '🅡' ).replace('pawn:B', 'Ⓟ' ).replace('pawn:W', '🅟' ).replace('king:B', 'Ⓚ' ).replace('king:W', '🅚' ).replace('bishop:B', 'Ⓑ' ).replace('bishop:W', '🅑' ).replace('queen:B', 'Ⓠ' ).replace('queen:W', '🅠' ).replace('knight:B', 'Ⓝ' ).replace('knight:W', '🅝' ).replace('solid', '🔘' ).replace('green:w', '🔲').replace('green:b', '🔳').replace('rook:GB', '[Ⓡ]' ).replace('rook:GW', '[🅡]' ).replace('pawn:GB', '[Ⓟ]' ).replace('pawn:GW', '[🅟]' ).replace('king:GB', '[Ⓚ]' ).replace('king:GW', '[🅚]' ).replace('bishop:GB', '[Ⓑ]' ).replace('bishop:GW', '[🅑]' ).replace('queen:GB', '[Ⓠ]' ).replace('queen:GW', '[🅠]' ).replace('knight:GB', '[Ⓝ]' ).replace('knight:GW', '[🅝]' ).replace('solid', '🔘' ).replace('green:w', '🔲').replace('green:b', '🔳').split()
                else:
                    pieces = chess.replace('rook:B', '♖︎' ).replace('rook:W', '♜︎' ).replace('pawn:B', '♙︎' ).replace('pawn:W', '♟︎‍' ).replace('king:B', '♔︎' ).replace('king:W', '♚︎' ).replace('bishop:B', '♗︎' ).replace('bishop:W', '♝︎' ).replace('queen:B', '♕︎' ).replace('queen:W', '♛︎' ).replace('knight:B', '♘︎' ).replace('knight:W', '♞︎' ).replace('solid', '🔘' ).replace('green:w', '🔲').replace('green:b', '🔳').replace('rook:GB', '[♖︎]' ).replace('rook:GW', '[♜︎]' ).replace('pawn:GB', '[♙︎]').replace('pawn:GW', '[♟︎‍]' ).replace('king:GB', '[♚︎]' ).replace('king:GW', '[♔︎]' ).replace('bishop:GB', '[♙︎]' ).replace('bishop:GW', '[♝︎]' ).replace('queen:GB', '[♕︎]' ).replace('queen:GW', '[♛︎]' ).replace('knight:GB', '[♘︎]' ).replace('knight:GW', '[♞︎]' ).replace('solid', '🔘' ).replace('green:w', '🔲').replace('green:b', '🔳').split()
                print(pieces)
                for i in range(8):
                    row_buttons = []
                    for j in range(8):
                        piece_info = pieces[i*8 + j]
                        callback, emoji = piece_info.split(':')
                        button = Button.inline(emoji, data=f'{callback}_{match_id}')
                        row_buttons.append(button)
                    buttons.append(row_buttons)
            if other.strip() or chess.strip():
                try:
                    other_msg = other.split('|')[-2]
                except:
                    other_msg = other.split('|')[-1]
                try:
                    await client.edit_message(event.chat_id, match_message.id, f'{players_msg}\n\n{other_msg}', buttons=buttons)
                    append_history(match_id, str(pieces))
                except Exception as e:
                    print (e)

def separate_data(s):
    p = '([a-h][1-8]:\w+(?::[BW])?)'
    c = ' '.join(re.findall(p, s))
    o = re.sub(p, '', s).strip()
    try:
        l = o.split('~')[1].split('&')
    except Exception as e: 
        return c, o, None
    return c, o, l

async def get_piece(client, chat_id, match_id, callback_data):
    message = await client.get_messages(chat_id, ids=int(match_id.split('@')[1]))
    for row in message.buttons:
        for button in row:
            if button.data.decode('utf-8') == f'{callback_data}_{match_id}':
                return button.text
    return None

def append_history(match_id, pieces):
    # Future me here again hi, Dont ask me why dont you use a database or something more ram based and stuff - it was two whoooole years ago, All my new shit is ram based so i can enjoy my ram filling up more quick.
    afile = open(f'matches_history/{match_id}/History', 'a')
    rfile = open(f'matches_history/{match_id}/History', 'r')
    lines = rfile.readlines()
    if not lines or pieces != lines[-1]:
        afile.write(f'\n{pieces}')

try:
    print('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()
finally:
    client.disconnect()