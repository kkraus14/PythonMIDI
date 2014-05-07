PythonMIDI
==========
Dependencies, Installation, and Usage

This application is coded entirely in python, and uses python version 2.7.  Python 2.7 can be downloaded from http://python.org/download/.  The three main dependencies for this application are Tkinter, pygame, and midi.  Tkinter is included within the python installer so there aren’t any additional steps or downloads to using it.  The pygame installer can be downloaded from http://www.pygame.org/download.shtml.  The midi library used has a more complicated install than normal.  First, you must download and extract the zip from here https://github.com/vishnubob/python-midi/archive/master.zip.  Once extracted, you need to open a command prompt on the extracted directory (either cd to it or shift + right click within the directory and click open command window here) and run “python setup.py install”.

Once the dependencies are installed, the application script can be run from within IDLE (default python windows IDE).  For some reason, running the script through the command prompt causes a PortMIDI error that was unable to be resolved.  Upon running the script it will ask for a track number (this is to allow for different tracks in multiple track midi files to be played), enter 1 and hit enter.  It will then ask for the beats per minute desired, feel free to change this number as you wish so you can observe the music and piano at a faster or slower pace.  To close the program exit the piano gui window.

This application has only been tested within Windows, so it is unsure if it will work correctly within a Unix environment.  For best results, please use a Windows environment.
