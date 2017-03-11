# Realm of Reckoning
# A Text-based adventure game
# by
# Daniel Ashcom
# GNU GPL v 3.0 but I want my free beer.
# 
#====================================================================
# To-Do/Ideas:
#-------------------------------------------------------------------
# -- Continue with implementing more readable, concise ways of handling logic, replacing if-else with dictionaries (I think ... ?) --  See Coursera Fundamentals of Computing 2of7, wk 7b Programming Tips (02:30)
# 
# --Add more text narrative of areas to explore
# --add item persistence on the ground when items are dropped
# --Implement item usage (health potion, equipping weapons, etc.)
# --Implement battle system
# --Consider whether to modify this with Python libraries, for fun.
# --Consider creating a visual version of this game once it has more written content
# --Consider how to create randomly-generated areas with randomly-generated loot (<--  might be a good first step to implement.  See 'Design Patterns:  Elements of Reusable OO Software', p. 105)
#
#  ==========  End documentation  ==========
###

# imports
##
# sys is for exiting the program
# vtemu is a VT100 emulator for Windows which colorizes text
from realm import Realm

# Game Loop
##
# this line sets up the Realm and its first location, the player's starting point
world = Realm()
