Byte - a Zombie Game
===============

Entry in PyWeek #18  <http://www.pyweek.org/18/>
URL: https://pyweek.org/e/byte/
By: Sveder
License: see LICENSE.txt


Running the Game
----------------

On Windows or Mac OS X, locate the "run_game.pyw" file and double-click it.

Othewise open a terminal / console and "cd" to the game directory and run:

  python run_game.py


How to Play the Game
--------------------



Move the cursor around the screen with the mouse.

Press the left mouse button to fire the ducks.


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

