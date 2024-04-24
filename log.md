TODO: convert this to a kanban board or at least make it more like actual markdown.

# Realm of Reckoning
# A Text-based adventure game
# by
# Daniel Ashcom
# GNU GPL v 3.0 but I want my free beer.
# 
#
#
#===================================================================
# Known Bugs:
#--------------------------------------------------------------------
#

#
#====================================================================
# Fixed Bugs:
#--------------------------------------------------------------------
# 
#
#====================================================================
# To-Do:
#-------------------------------------------------------------------
# --Make code more consistent (commenting, etc.) 
# --Get rid of 'newplayer' and just implement the starting narrative when calling narrative() for the first time because
#	it's silly to have to keep track of whether the user is a newplayer or not for such a small reason
# --Consider ways to reduce or eliminate all global variables (encapsulate into classes?)
# --Add more text narrative of areas to explore
# --add item persistence on the ground when items are dropped
# --Implement item usage (health potion, equipping weapons)
# --Implement health, stamina. magic meters
# --Implement battle system
# --Consider whether to modify this with Python libraries, for fun.
# Something like RenPy could introduce visuals, but might require a lot of 
# studying to use and would require hand-made graphics.
#
#====================================================================
# Notes:
#--------------------------------------------------------------------
#Update 11/21/16:  I realized when I tried to keep track of availability of items on each map location that this grid system is 
# not going to work very conveniently for passing the grid location as a name for a dictionary name/value pair serving this purpose.
# Now I realize I should have just used a traditional x,y grid to specify location from the start and I should define 0,0 as the 
# furthest reaches of the map in the SW corner and begin somewhere NE of there (250,250)?  It's really arbitrary unless I want to build
#impassable mountains or some other insurmountable obstacle into the map to the W and S of the starting location.
#
#Update 12/13/16:  I was able to implement a new Location class and an expanded Point class
# which have both been tested successfully as designed.  Now I need to reintegrate them back
# into this, the main program.  I'm going to have to modify narrative to handle to Point object
# and should consider later creating a separate text file to hold narratives.
#
# Update 12/23/16:  I was able to reintegrate the new Location and modified Point classes back into 
# the main program without much difficulty.  There are no known bugs but the game is very simple.
# I am beginning to understand the suggestions to use Python as a prototyping language.  
# It's so smooth and relatively easy to write with compared to Java.  I've cleaned up/standardized the comments
# mostly, though I still need to define each argument and variable in my comments.  I've updated the To-Do list.
#
# Update 1/14/17:  The approach I had to coloring text worked in Linux but not Windows so I added tests for platform type and have imported a new module called vtemu which is a VT100 emulator for Windows which allows colorized text.
# I've replaced any instances of 'locale' with 'location' in order to avoid bizarre python-interpreter-breaking behavior
# which I observed yesterday involving an error related to 'getdefaultlocale' which I can only assume has something to do 
# with naming a test file 'locale.py' which then somehow overrode a standard python file of the same name.
#
# Thoughts 1/16/17:  Rewrite opening of story to be more interesting and include a challenge.  Idea:  start out on a ship, held captive, amnesia; immediate goals being to find out where you are how to escape and start to learn who you are.  Give the player a reason to continue and an interesting/captivating start to the game.  It would be good to implement more look/search content and also to create some sort of simple crafting/item manipulation feature to the game as well as hit-points, conditions, battle system, etc.
#
#  ==========  End documentation  ==========
