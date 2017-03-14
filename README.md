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
# See Issues: https://github.com/vonnenaut/realmofreckoning/issues

#
#====================================================================
# Fixed Bugs:
#--------------------------------------------------------------------
# See Issues: https://github.com/vonnenaut/realmofreckoning/issues
#
#====================================================================
# To-Do/Ideas:
#-------------------------------------------------------------------
# --Add more text narrative of areas to explore
# --add item persistence on the ground when items are dropped
# --Implement item usage (health potion, equipping weapons, etc.)
# --Implement battle system
# --Consider whether to modify this with Python libraries, for fun.
# --Consider creating a visual version of this game once it has more written content
# --Consider how to create randomly-generated areas with randomly-generated loot (<--  might be a good first step to implement.  See 'Design Patterns:  Elements of Reusable OO Software', p. 105)
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
# Update 1/15/17:  Added support for colorized text in Windows and ability to check OS, supporting colorized text
# for either Linux or Windows systems.  Changed some variable names to be more accurante (current_location --> current_location_coords, etc.)
# Added several TO_DO: notes in the code to begin reorganizing the code in a way that makes more sense and gives me a little practice
# with object-oriented programming.
#
# Update 1/24/17:  I've gotten rid of the Point class and moved all of its functionality into the Location class.  I'm having a bit of trouble translating some of the variables and feel I might have multiple variables referring to the same thing, i.e., 'location', 'current_obj', 'current_location_coords' etc.  I will keep working to iron out the bugs first and then review the code to reduce redundancy and improve structure.  
#
# Update 1/24/17 P.S. -- I've gotten the program working again with the new oo-structure.  I don't think it reflects a full understanding of oo design but that will come with time and experience.  So far so good.  Time to break things again by restructuring to encapsulate functionality in a more logical way.
#
# Update 2/17/17:  I moved the methods for adding, retrieving and checking the existence of Locations into the Map class from the Location class since it just makes more sense logically.  I also moved the narrative method from the Character class into the Map class.
#
# Update 2/18/17:  I rewrote both the move and search_area methods to simplify moving around the map and adding new content to new areas of the map by switching from if-else statements to dictionaries.  I also rewrote 'move', renaming it 'keydown' and simplifying its code similarly using a dictionary in place of if-else statements.  I am definitely now a fan of dictionaries and learned this usage from Coursera's Fundamentals of Computing (2of7).
# Update 3/7/17:  I am in the process of separating the program into modules named as follows: main.py (file to run in order to start the program), realm.py, location.py and character.py
#
"""
VT100/ANSI Escape sequence reference chart:
0	Reset all attributes
1	Bright
2	Dim
4	Underscore	
5	Blink
7	Reverse
8	Hidden

	Foreground Colours
30	Black
31	Red
32	Green
33	Yellow
34	Blue
35	Magenta
36	Cyan
37	White

	Background Colours
40	Black
41	Red
42	Green
43	Yellow
44	Blue
45	Magenta
46	Cyan
47	White
"""
#  ==========  End documentation  ==========
###
