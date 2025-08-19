# EasyChessBot
"PVP Chess" system, in a place where no one asked for.<br>
...<br>
<br>
<br>
Just kidding someone did ask for it.<br>
Except, it was myself.<br>

![phito](https://github.com/user-attachments/assets/aea413d5-7320-4354-8024-53c1595df41e)
<br>
# Usage
For the ones that want to test the project, Current build is hosted in my server and accessible in telegram.<br>
Simply add https://t.me/EasyChessBot to a group chat and use one of the commands to start a game session, then ask your friend to join the session and everything should be clear after that.
<br>
<br>
# Installation & Setup
* Step 1: Downloading the project<br>
  * Option 1: Paste `git clone https://github.com/amirgame197/EasyChessBot` to automatically download the files. you may need to install `git`.<br>
  * Option 2: Manually download the project files anywhere you want.<br>
  <br>
* Step 2: Install the required package: Telethon
  * If you dont have the python's async telethon package, you can install it using `pip install telethon`. as simple as that!
  <br>
* Step 3: Configuration
  * Open `config.py`. There are some changes you need to apply.
  * The first line is your telegram bot's token. Paste your token there
  * Second and third lines are your `app_id` and `app_hash`. You need these to setup a proper connection to telegram.
    * You can obtain them from `https://my.telegram.org`: Create an application with any info you like, Copy your app id and hash then paste them to `config.py`.
    * These two things are connected to your telegram account. You must keep them confidential otherwise if they get exposed somewhere then some dude can use them to do nasty stuff and its your account in danger, not his.
  <br>
* Step 4: Activating
  * To run the code, simply run `python EasyChessBot.py` and wait for it to connect. Should take a bit of time in its first boot because its generating session files
  <br>
* Step 5: Enjoy
  * If you can.
  <br>
  <br>
# The Story
Each repository comes with a story. Some of them you dig deep enough, and you find out everything.<br>
But some other, you will never know whats inside their heart..<br>
<br>
This one, everything started since 2023. I've been creating some interesting telegram bots lately, but all the time...<br>
<br>
There was this question in my mind,<br>
What project do i exactly do to make a name for myself. People see me and say "oh wow is This the guy who made <That_Project>? gotta get his sign."<br>
All that fame, money, success... I had to find the key.<br>
I searched through telegram. Holy hell dude, every single idea - It was somehow made its way into telegram bots. Some guy even made a telegram bot that lets you grow your dick and fight other with it? Unbelievable.<br>
So what, i search for days and no interesting project comes up in my mind that has'nt been in telegram before? Oh boy. The same day i was playing some board games with my friends and a chess game took my attention.<br>
Well i have seen @gamee in telegram that had chess, but it came with a catch. it was not "literally in telegram": Whenever you want to play, it opens a web page and the you take the game from there. Telegram was just an API.<br>
I thought okay, telegram does have buttons and a chess game is just a big 8x8 list of buttons. I knew what i was up to.<br>
<br>
I've done some research about how a chess game even works, i didnt know all the rules obviously.<br>
Like one day later, i started crafing. Schematics, planning, style, managers, all these stuff had to be a working combination.<br>
Time passed and everything nearly came together, except only one thing.<br>
<br>
How the hell am i going to create the chess core when i dont know how this game even works??<br>
Believe me, i tried. I tried creating the core myself and every single run was a mess. I just could not get through it. A part of it was because chess is kinda complicated, another part is the fact that well. I had no idea what i was doing.<br>
After my big defeat i found a pretty pupular JS Package called Chess.js - As you can see this package is a chess but in js.<br>
The idea was that you launch a chess in server, controls each side from the clients. Knowing the full plan made the whole progress a lot faster and easier.<br>
<br>
<br>
Finally the project was done and it was time to show it to everyone and wait for them to fall in love with it!!!<br>
To be fair their only reaction was "The hell is this"<br>
I played some sessions with them and i lost all of them.<br>
Additionally someone did fall in love with the bot, but it doesnt really matter. She would fall in love with anything.
<br>
<br>
Then i just came to a conclusion.<br>
<br>
Maybe it was not the best idea i could pull off?<br>
Oh well. Not everything you make should be a masterpiece<br>
<br>
*Looks at the buried projects directory*<br>
I guess there is a lot of them. I'll publish each one, plus a story for the ones like me.<br>
<br>
The ones who will always find a way, but they can never reach their destination.
