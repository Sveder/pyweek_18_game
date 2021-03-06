Byte - a Zombie Game
===============

Entry in PyWeek #18  <http://www.pyweek.org/18/>
URL: https://pyweek.org/e/byte/
By: Sveder
License: see LICENSE.txt


Running the Game
----------------

TESTING NOTICE: This is a multiplayer game by nature. To run a server you'll probably need to configure your
NAT (usually a router, for home users) to tunnel the selected port to your specific subnet-network
ip. If you want to test it with me, FEEL FREE to email me at m@sveder.com and we'll work out a time.
You can also test it locally by running the commands below, and opening two instances.

Open a terminal / console and "cd" to the game directory and run:

run_game.exe <network_role> <game_role> <host> <port>

where network role is: y - server
                       n - client
                       
and game roles are: shooter, lighter

Example:
run_game.exe n shooter 0.0.0.0 8080

run_game.exe y lighter 84.108.247.140 8080

LOCAL TESTING COMMANDS:
To test this locally, you can open two consoles and run these two commands each in its own console:

run_game.exe y shooter 0.0.0.0 8080
run_game.exe n lighter 84.108.247.140 8080

You'll get two instance running correctly you can move the mouse from one to the other and experience both terrifying roles :)


How to Play the Game
--------------------

Shooter: Left Click the mouse button to shoot. Right click to reload.
Flashlighter: Move the mouse and try to find the zombie to help your friend.

One player is in control of the flashlight and is the one who can see the zombies coming. He should
use the power of the amazing flashlight to help the other player spot the zombies and kill them, as the
second player controls the shotgun. Work together and defeat the fearsome zombies! You probably can't, but
still keep trying.

"Cheats":
z - spawn zombie


Known Issues
-----------------

The player rectangle is a bit bigger than it seems. It has a shadow but it's not visible.
No actual motivation to play the game. More enemies were planned, but of course time won. 



Credits 
-----------------
Music: "Cylinder Two" and "Cylinder Eight" by Chris Zabriskie from:
http://freemusicarchive.org/music/Chris_Zabriskie/

Sounds:
ambient_zombie_call.ogg- "Zombie Graboid Death Gasp.mp3" by XTDream from:
http://freesound.org/people/XTDream/sounds/97668/

far_away_zombie.ogg - "Zombie 15" by missozzy from:
http://freesound.org/people/missozzy/sounds/169845/

death.ogg - "Monster Sounds � Slow Zombie Death" by scorpion67890 from:
http://freesound.org/people/scorpion67890/sounds/169058/

shot.ogg - "Gun Fire Sound" by GoodSoundForYou from:
http://soundbible.com/1998-Gun-Fire.html

empty_shot.ogg - "Empty Gun Shot" by KlawyKogut from:
http://freesound.org/people/KlawyKogut/sounds/154934/#

reload.ogg - "Gun Sounds : REALoaded � Firearm Reloading 2" by davdud101:
http://freesound.org/people/davdud101/sounds/150500/

zombie sprites - "Zombie RPG sprites" by Curt from:
http://opengameart.org/content/zombie-rpg-sprites
"Curt - cjc83486 http://opengameart.org/content/zombie-rpg-sprites"

AMAZING player sprites - "tmim Heroine - Bleed's Game Art" by bleed from:
http://opengameart.org/content/tmim-heroine-bleeds-game-art
Visit his portfolio: http://remusprites.carbonmade.com/

happy_happy_joy_joy.ogg - (definitely not a) "Suicide note" by 11linda:
http://freesound.org/people/11linda/sounds/181986/

heart.png - "Larger simple heart" by eylvisaker from:
http://opengameart.org/content/larger-simple-heart

skull.png - "Gold Skull" by Cameron 'cron' Fraser from:
http://opengameart.org/content/gold-skull


Development notes 
-----------------

Creating a source distribution with::

   python setup.py sdist

You may also generate Windows executables and OS X applications::

   python setup.py py2exe
   python setup.py py2app

Upload files to PyWeek with::

   python pyweek_upload.py

Upload to the Python Package Index with::

   python setup.py register
   python setup.py sdist upload

