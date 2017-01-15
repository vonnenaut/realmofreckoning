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
# --Location should call Point and Point has at least one method that logically should belong to Location --  rethink these two 
#      classes and consider whether Point should be a superclass of Location.
# --Get rid of 'newplayer' and just implement the starting narrative when calling narrative() for the first time because
#	it's silly to have to keep track of whether the user is a newplayer or not for such a small reason
# --Consider ways to reduce or eliminate all global variables (encapsulate into classes?)
# --Add more text narrative of areas to explore
# --add item persistence on the ground when items are dropped
# --Implement item usage (health potion, equipping weapons, etc.)
# --Implement health, stamina, magic meters
# --Implement battle system
# --Consider whether to modify this with Python libraries, for fun.
# Something like RenPy could introduce visuals, but might require a lot of 
# studying to use and would require hand-made graphics.  Look into other options for visuals kids these days demand.
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
#  ==========  End documentation  ==========
###

# imports
##
#
# sys is for exiting the program
# vtemu is a VT100 emulator for Windows which colorizes text

import sys, vtemu


# The following is formatting for adding color to text for more visual variety and ease of reading
# (may consider looking into Python Curses for similar functionality) If I create an Intro or 
# Initialization function to eliminate newplayer, this is a good candidate for other code to move 
# into the initialization function.
#


# special definitions for colorized text
##
# if the terminal is Linux or Cygwin, use the following codes
if sys.platform in ['linux2', 'cygwin']:
	def prRed(prt): print("\033[91m {}\033[00m" .format(prt))
	def prGreen(prt): print("\033[92m {}\033[00m" .format(prt))
	def prYellow(prt): print("\033[93m {}\033[00m" .format(prt))
	def prLightPurple(prt): print("\033[94m {}\033[00m" .format(prt))
	def prPurple(prt): print("\033[95m {}\033[00m" .format(prt))
	def prBlue(prt): print("\033[96m {}\033[00m" .format(prt))
	def prLightGray(prt): print("\033[97m {}\033[00m" .format(prt))
	def prBlack(prt): print("\033[98m {}\033[00m" .format(prt))

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

if sys.platform == 'win32':	
	def prRed(prt): print("\x1b[1;31m {}\x1b[00m" .format(prt))
	def prGreen(prt): print("\x1b[2;32m {}\x1b[00m" .format(prt))
	def prYellow(prt): print("\x1b[1;33m {}\x1b[00m" .format(prt))
	def prBlue(prt): print("\x1b[1;34m {}\x1b[00m" .format(prt))
	def prPurple(prt): print("\x1b[1;35m {}\x1b[00m" .format(prt))
	def prCyan(prt): print("\x1b[1;36m {}\x1b[00m" .format(prt))
	def prWhite(prt): print("\x1b[1;37m {}\x1b[00m" .format(prt)) 


# Global variables
##
# stores x and y grid location for player's location on the map
x = 0
y = 0

#defines the input prompt
prompt = '=---> '

#sets the initial input value to 'nowhere' (should be n, s, e, w, h, t, i, q, or h, as currently implemented in the move() function)
# Seems like there should be a purpose for calling it nowhere...  should I try to test and catch this somehow?  Haven't seen it cause any problems... yet.
go = 'nowhere'

#tells the program whether to display the new player narrative introducing the game and the start scene
# TO-DO:  Get rid of this.  Create an Intro class to print the opening narrative text once and call it at the beginning before the first call to narrative()
newplayer = True

# a list to keep track of items in player's inventory
inventory = []

# a list to hold all Location objects
locations = {}


# Classes
##

### TO_DO:  Consider making this a superclass of Location, just for fun.
class Point(object):
	"""
	a simple class which defines x and y values for each location on the map
and provides a method for printing the coordinates (for testing)
and returning a name based on converting and concatenating the x-y coordinates
of the current object.  This will be used to name each object uniquely as it
is created during the game.
	"""
	def __init__(self, x, y):
		"""
		initialize a point object with passed x and y coordinates
		"""
		self.x = x
		self.y = y
	
	def move_north(self):
		"""
			add one to the y value, i.e., move north
		"""
		self.y += 1
		check_location_existence(self)
	
	def move_east(self):
		"""
		add one to the x value, i.e., move east
		"""
		self.x += 1
		check_location_existence(self)
	
	def move_south(self):
		"""
			subtract one from the y value, i.e., move south
		"""
		self.y -= 1
		check_location_existence(self)
	
	def move_west(self):
		"""
			subtract one from the x value, i.e., move west
		"""
		self.x -= 1
		check_location_existence(self)
	
	def get_coords(self):
		return [x, y]
	
	def return_object_name(self):
		"""
			Return a unique string made up of the x and y coordinates
			to be used for naming each Location object as it is created and
			for retrieval.
		"""
		return str(self.x) + str(self.y)
	
	def set_coords(self, x, y):
		"""
			Set the location.  This is only being used while the game is being built,
			to account for stepping into a location that hasn't been written yet.
		"""
		self.x = x
		self.y = y


class Location(object):
	""" This class defines all of the attributes to be stored for each location object
		initializes each location object with attributes for:
		location (point containing x and y coordinates)
		name which is used to create the key for the dictionary storing each object
		monsters_present which tracks whether monsters are in the present location
		loot_present which keeps track of whether loot is in the present location 
		(either having been dropped or spawned initially)
	"""	
	def __init__(self, current_location_coords, monsters_present, loot_present):
		self.location = current_location_coords
		self.coords = current_location_coords.get_coords()
		self.monsters_present = monsters_present
		# TO-DO: add the ability to drop items and have them persist
		# but currently loot is handled directly by search so that
		# functionality should be moved here or shared by search and Location
		self.loot_present = loot_present
		self.name = str(self.location.x) + str(self.location.y)
		locations[self.name] = self


# Functions (TO_DO:  which probably belong inside classes)
##

### TO_DO:  move the two following location functions inside the Location class
def check_location_existence(self):
	"""
		Check for the existence of a Location object and create it if it doesn't exist yet
	"""
	current_obj = self.return_object_name()
	if current_obj in locations:
		return
	else:
		current_obj = Location(current_location_coords, False, True)

def retrieve_Location(current_location_coords):
	""" attempts to return an object with a name based on the current location coordinates
		if the object name doesn't exist, throws NameError exception
	"""
	try:
		string = current_location_coords.return_object_name()
		return locations[string]
	except NameError:
		print "Location does not exist."
	else:
		return

### TO_DO:  consider moving this into Location class
def narrative(newplayer):
	""" Handles delivery of narrative text based on location as well as any choices available in any given location
	"""
	global current_location_coords


	if newplayer == True:
		print "\nYou awaken to the distant sound of commotion to your west.  You\n open your eyes and realize you are in a vulnerable spot\n in an open field.  You look west toward the direction of\n the distant sounds and hear that it is now quiet.  \nTo your north in the distance is a fortress.  To your \neast is a forest and to your south is a riverbank\n with a boat tied at a pier.  \nWhich direction do you go? (enter: 'n', 's', 'e' or 'w')"
		newplayer = False

	elif current_location_coords.x == 0 and current_location_coords.y == 0:
		print "\nYou are standing in the same field in which you first awoke without\n any memory of how you got here.  Which way?\n"
	
	elif current_location_coords.x == -1 and current_location_coords.y == 0:
		print "\nAs you proceed west, you come upon signs of a battle, \nincluding two bodies lying face-down at the edge of a wood\n near the field in which you awoke.  There are no signs of\n life.  Do you approach the bodies? (y/n)"		
		choice = raw_input(prompt)
		if choice in {'yes', 'y', 'Y', 'Yes', 'YES', 'YEs', 'YeS', 'yeS'}:
			print "\nAs you approach one of the bodies closely, you realize\n that he is feigning death when he rolls quickly and \nsinks a blade into your neck.  Your life fades slowly."
			die()
		elif choice in {'no', 'n', 'N', 'NO', 'nO'}:
			print "\nWell, daylight's a-wasting.  Where to now?"
		else:
			print "Please type y or n."

	elif current_location_coords.x == 0 and current_location_coords.y == 1:
		print "\nYou walk for some time to finally arrive at an old, \napparently abandoned fortress which is crumbled with time.  \nThere is nothing here but ruins.  Which direction do you go\n from here?"	
	
	elif current_location_coords.x == 0 and current_location_coords.y == 2:
		print "\nAs you head north around the abandoned and crumbling \nfortress you see a valley spread out before you.  In the \ndistance to the north is a village with wafts of smoke being \ncarried off by the breeze trailing over the scene \nlike the twisted tails of many kites.  To the west gently\n sloping foothills transition into distant blue\n mountains and to the east, a vast forest conspires to block out\n all surface detail."
	
	else:
		prRed("Under construction.  Returning to the beginning.  Pick a different direction next time.")
		current_location_coords.set_coords(0, 0)
		narrative(newplayer)

	go = raw_input(prompt)
	move(go, current_location_coords, newplayer)
	
### TO_DO:  If implementing a player class, consider moving this into it.
def move(go, current_location_coords, newplayer):
	""" Handles keeping track of player location based on which direction they head and their current location
		arguments:
		go:  				user input ('n', 's', 'e', 'w', etc.)
		current_location_coords: 	an instance of the Point class which specifies the user's current location with (x, y)
		newplayer:			a boolean which keeps track of whether the player is just starting the game.

	"""

	if go in {'n', 'north', 'North'}:
		current_location_coords.move_north()

	elif go in {'s', 'south', 'South'}:
		current_location_coords.move_south()

	elif go in {'e', 'east', 'East'}:
		current_location_coords.move_east()

	elif go in {'w', 'west', 'West'}:
		current_location_coords.move_west()

	elif go in {'q', 'quit', 'Quit'}:
		prRed("Are you sure you want to exit? (y/n)")
		choice = raw_input(prompt)
		if choice in {'y', 'Y', 'yes', 'Yes', 'YES'}:
			die()
		elif choice in {'n', 'N', 'No', 'NO'}:
			print "Let's get back to it then."
			narrative(newplayer)
			return
		else:
			print "Please type yes or no."

	elif go in {'h', 'H', 'help', 'Help', 'HELP', 'HALP', 'halp'}:
		prBlue("\nHelp:\nn move north\ns move south\ne move east\nw move west\nx search \nt check the time\ni check your inventory\nq quit\nh help\n")
		narrative(newplayer)

	elif go in {'i', 'inventory', 'I', 'Inventory', 'INVENTORY'}:
		inv_list()
		narrative(newplayer)

	elif go in {'x', 'search'}:
		search_area(current_location_coords)
		narrative(newplayer)

	else:
		print "Please type 'n', 's', 'e' or 'w'."
	
	narrative(newplayer)

### TO_DO:  Create an Inventory Class (and a player class while you're at it, as Inventory's superclass) and
# move all of these inv_ functions inside it.
def inv_list():
	""" Lists all the items in the player's inventory
	"""
	print "\nInventory: \n" 
	prGreen(inventory)
	return

def inv_add(item):
	""" Adds an item to the player's inventory, asking if they wish to drop an item if the inventory is full.
	"""
	if len(inventory) < 5:
		inventory.append(item)
		prGreen("\n %s added to inventory." % (item))
	else:
		print "Inventory full.  Drop an item? (y/n)"
		choice = raw_input(prompt)
		if choice in {'y', 'yes', 'Y', 'Yes', 'YES'}:
			inv_prmpt_remove()
			inv_add(item)
		else:
			print "Dropped %s on the ground." % (item)

def inv_prmpt_remove():
	""" Prompts player to pick an item to remove from the inventory
	"""
	print "\nWhich item do you wish to remove?\n"
	prGreen(inventory)
	print "\n"
	choice = raw_input(prompt)
	if choice in inventory:
		inv_remove(choice)
		prGreen("%s dropped on the ground." % (choice))
	else:
		print "Item: %s not found.  Please type the name of the item you wish to remove." % (choice)
		choice = raw_input(prompt)
	return

# TO-DO:  add a feature which places the dropped item at the current grid location to be able to
# pick it up later.
# removes an item from the inventory
#
def inv_remove(item):
	""" Removes an item from the player's inventory.  Called from inv_prmpt_remove() function
	"""
	inventory.remove(item)

### TO_DO:  Consider moving this into Location class
def search_area(current_location_coords):
	""" Searches area upon player pressing 'x' to find and collect loot.  You really should try the goat's milk.
	"""
	# retrieve Location object for current location to check 
	# boolean variable for presence of loot at the location
	curr_coord_name = current_location_coords.return_object_name()
	object_name = retrieve_Location(current_location_coords)
	loot_present = object_name.loot_present

	if curr_coord_name == '00' and loot_present == True:
		print "After searching the area you find a bit of rope useful for tinder and a strangely-chilled glass of goat's milk."
		inv_add("tinder")
		inv_add("goat milk")		
	elif curr_coord_name == '01' and loot_present == True:
		print "Upon looking around the ruins, you find very little of use, all having been picked clean long ago by scavengers.  You did however manage to find a bit of flint near an old campfire."
		inv_add("flint")
	elif curr_coord_name == '02' and loot_present == True:
		print "You stumble upon a rusty blade."
		inv_add("rusty blade")
	else:
		prYellow("You found nothing useful here.")

	object_name.loot_present = False
	return

### TO_DO:  If implementing a Player class, move this into it.
def die():
	"""
		this function ends the program
	"""
	message = prRed("\nGame Over.\n")
	sys.exit(message)


# Game Loop
##
# this line sets up the first location, the player's starting point
current_location_coords = Point(0, 0)
location = Location(current_location_coords, False, True)

# initialize colorama text-colorization
# init()

# this line starts the loop which gets user input for interacting with the environment
narrative(newplayer)
