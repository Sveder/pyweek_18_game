from distutils.core import setup
import py2exe

setup(console=['run_game.py'], options={
          "py2exe": {
              "excludes": ["Numeric"],
              }
          }
      )