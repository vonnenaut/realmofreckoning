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
# --Implement health, stamina, usage of items, battle system
# --Consider whether to modify this with Python libraries.
# Something like RenPy could introduce visuals, but might require a lot of 
# studying to use and would require hand-made graphics.
#
#
#====================================================================
# Notes:
#--------------------------------------------------------------------
# The location of the player is tracked on a grid created by a numbering system which originates at the starting point (1000), 
# where numbers increase by one going north, assuming a max north number of 1099 and are prepended by a two-digit number 
# for each column to the left of the 1000 point and the same for East but negative numbers, all relative to the starting 
# point.  Heading due west would produce location numbers starting from 10000 to , 2000, 3000, 4000, etc.  Heading East from 
# 1000 to -1000, -200, -3000, etc.
#
#Update 11/21/16:  I realized when I tried to keep track of availability of items on each map location that this grid system is 
# not going to work very conveniently for passing the grid location as a name for a dictionary name/value pair serving this purpose.
# Now I realize I should have just used a traditional x,y grid to specify location from the start and I should define 0,0 as the 
# furthest reaches of the map in the SW corner and begin somewhere NE of there (250,250?  It's really arbitrary unless I want to build
#impassable mountains or some other insurmountable obstacle into the map to the W and S of the starting location.
#
# these variables are initialized as follows:
#
#sets the starting location on the map grid, but this is too simplistic and causes problems and so must be converted to 
#an x,y dictionary set with non-negative coordinates...  or should it implement a point?
#With a dictionary, we could possibly store x, y, and also whether items have been collected.  However,
# my concern is whether it will require too much manual programming to create this potentially massive
# dictionary set for the game and wonder if there is a way to create a function which will populate these 
# values on the fly, as the player enters each new square of the map.
#
#
#
#Update 12/13/16:  I was able to implement a new Locale class and an expanded Ppoint class
# which have both been tested successfully as designed.  Now I need to reintegrate them back
# into this, the main program.  I'm going to have to modify narrative to handle to Point object
# and should consider later creating a separate text file to hold narratives.
#
#
#  ==========  End documentation  ==========


# sys is for exiting the program
import sys

# formatting for adding color to text for more visual variety and ease of reading
# (may consider looking into Python Curses for similar functionality)
#
def prRed(prt): print("\033[91m {}\033[00m" .format(prt))
def prGreen(prt): print("\033[92m {}\033[00m" .format(prt))
def prYellow(prt): print("\033[93m {}\033[00m" .format(prt))
def prLightPurple(prt): print("\033[94m {}\033[00m" .format(prt))
def prPurple(prt): print("\033[95m {}\033[00m" .format(prt))
def prCyan(prt): print("\033[96m {}\033[00m" .format(prt))
def prLightGray(prt): print("\033[97m {}\033[00m" .format(prt))
def prBlack(prt): print("\033[98m {}\033[00m" .format(prt))

#defines the input prompt
prompt = '=---> '

# stores x and y grid location for player's location on the map
x = 0
y = 0

#sets the initial input value to 'nowhere' (should be n, s, e, w, h, t, i, q, or h, as currently implemented in the move() function)
go = 'nowhere'

#tells the program whether to display the new player narrative introducing the game and the start scene
newplayer = True

# a list to keep track of items in player's inventory
inventory = []

# keep track of whether a player has searched the area yet using a dictionary whose 
# key is the current player location and whose value is # a boolean representing 
# whether or not there is anything in the area to pick up
#cur_collected = {}
# replaced by class Locale and its loot_present attribute

# a list to hold all Locale objects
# TO-DO:  figure out how to make the key or index be represented by a pair of numbers (point, i.e., x,y)
# A tuple might work for this purpose
locations = {}

# a simple class which defines x and y values for each location on the map
# and provides a method for printing the coordinates (for testing)
# and returning a name based on converting and concatenating the x-y coordinates
# of the current object.  This will be used to name each object uniquely as it
# is created during the game.
#
class Point(object):

	# initialize a point object with passed x and y coordinates
	def __init__(self, x, y):
		self.x = x
		self.y = y

	# add one to the y value, i.e.,
	# move north
	def move_north(self):
		self.y += 1
		check_locale_existence(self)

	# add one to the x value, i.e.,
	# move east
	def move_east(self):
		self.x += 1
		check_locale_existence(self)

	# subtract one from the y value, i.e.,
	# move south
	def move_south(self):
		self.y -= 1
		check_locale_existence(self)

	# subtract one from the x value, i.e.,
	# move west
	def move_west(self):
		self.x -= 1
		check_locale_existence(self)

	# return a human-readable set of coordinates
	# for testing purposes
	def return_coords(self):
		return "(" + str(self.x) + ", " + str(self.y) +")"

	# return a unique string made up of the x and y coordinates
	# to be used for naming each Locale object as it is created and
	# for retrieval
	def return_object_name(self):
		return str(self.x) + str(self.y)

	def set_location(self, x, y):
		self.x = x
		self.y = y

# check for the existence of a Locale object
# and create it if it doesn't exist yet
def check_locale_existence(self):
	current_obj = self.return_object_name()
	if current_obj in locations:
		return
	else:
		current_obj = Locale(current_location, False, True)


class Locale(object):
	""" This class defines all of the attributes to be stored for each location object
	"""

	# initializes each locale object with attributes for:
	# location (point containing x and y coordinates)
	# name which is used to create the key for the dictionary storing each object
	# monsters_present which tracks whether monsters are in the present location
	# loot_present which keeps track of whether loot is in the present location 
	# (either having been dropped or spawned initially)
	
	def __init__(self, current_location, monsters_present, loot_present):
		self.location = current_location
		self.name = str(self.location.x) + str(self.location.y)
		self.monsters_present = monsters_present
		# TO-DO: add the ability to drop items and have them persist
		# but currently loot is handled directly by search so that
		# functionality should be moved here or shared by search and Locale
		self.loot_present = loot_present
		locations[self.name] = self


def retrieve_Locale(current_location):
	""" attempts to return an object with a name based on the current location coordinates
		if the object name doesn't exist, throws NameError exception
	"""
	try:
		string = current_location.return_object_name()
		return locations[string]
	except NameError:
		print "Location does not exist."
	else:
		return


def narrative(current_location, newplayer):
	""" Handles delivery of narrative text based on location as well as any choices available in any given location
	"""
	curr_coord_name = current_location.return_object_name()

	if newplayer == True:
		print "\nYou awaken to the distant sound of commotion to your west.  You\n open your eyes and realize you are in a vulnerable spot\n in an open field.  You look west toward the direction of\n the distant sounds and hear that it is now quiet.  \nTo your north in the distance is a fortress.  To your \neast is a forest and to your south is a riverbank\n with a boat tied at a pier.  \nWhich direction do you go? (enter: 'n', 's', 'e' or 'w')"
		newplayer = False

	elif curr_coord_name == '00':
		print "\nYou are standing in the same field in which you first awoke without\n any memory of how you got here.  Which way?\n"
	
	elif curr_coord_name == '-10':
		print "\nAs you proceed west, you come upon signs of a battle, \nincluding two bodies lying face-down at the edge of a wood\n near the field in which you awoke.  There are no signs of\n life.  Do you approach the bodies? (y/n)"		
		choice = raw_input(prompt)
		if choice in {'yes', 'y', 'Y', 'Yes', 'YES', 'YEs', 'YeS', 'yeS'}:
			print "\nAs you approach one of the bodies closely, you realize\n that he is feigning death when he rolls quickly and \nsinks a blade into your neck.  Your life fades slowly."
			die()
		elif choice in {'no', 'n', 'N', 'NO', 'nO'}:
			print "\nWell, daylight's a-wasting.  Where to now?"
		else:
			print "Please type y or n."

	elif curr_coord_name == '01':
		print "\nYou walk for some time to finally arrive at an old, \napparently abandoned fortress which is crumbled with time.  \nThere is nothing here but ruins.  Which direction do you go\n from here?"	
	
	elif curr_coord_name == '02':
		print "\nAs you head north around the abandoned and crumbling \nfortress you see a valley spread out before you.  In the \ndistance to the north is a village with wafts of smoke being \ncarried off by the breeze trailing over the scene \nlike the twisted tails of many kites.  To the west gently\n sloping foothills transition into distant blue\n mountains and to the east, a vast forest conspires to block out\n all surface detail."
	
	else:
		prRed("Under construction.  Returning to the beginning.  Pick a different direction next time.")
		current_location.set_location(0, 0)
		narrative(current_location, newplayer)

	go = raw_input(prompt)
	move(go, current_location, newplayer)
	
# this function takes the current location and modifies it appropriately based on the user directional input (n, s, e, w)
#
def move(go, current_location, newplayer):
	""" Handles keeping track of player location based on which direction they head and their current location
	"""

	if go in {'n', 'north', 'North'}:
		current_location.move_north()

	elif go in {'s', 'south', 'South'}:
		current_location.move_south()

	elif go in {'e', 'east', 'East'}:
		current_location.move_east()

	elif go in {'w', 'west', 'West'}:
		current_location.move_west()

	elif go in {'q', 'quit', 'Quit'}:
		prRed("Are you sure you want to exit? (y/n)")
		choice = raw_input(prompt)
		if choice in {'y', 'Y', 'yes', 'Yes', 'YES'}:
			die()
		elif choice in {'n', 'N', 'No', 'NO'}:
			print "Let's get back to it then."
			narrative(current_location, newplayer)
			return
		else:
			print "Please type yes or no."

	elif go in {'h', 'H', 'help', 'Help', 'HELP', 'HALP', 'halp'}:
		prCyan("\nHelp:\nn move north\ns move south\ne move east\nw move west\nx search \nt check the time\ni check your inventory\nq quit\nh help\n")
		narrative(current_location, newplayer)

	elif go in {'i', 'inventory', 'I', 'Inventory', 'INVENTORY'}:
		inv_list()
		narrative(current_location, newplayer)

	elif go in {'x', 'search'}:
		search_area(current_location)
		narrative(current_location, newplayer)

	else:
		print "Please type 'n', 's', 'e' or 'w'."
	
	narrative(current_location, newplayer)


# print a list of all items contained in the player's inventory
#
def inv_list():
	""" Lists all the items in the player's inventory
	"""
	print "\nInventory: \n" 
	prGreen(inventory)
	return

# add an item to the inventory if the inventory isn't full, otherwise prompt user to drop something and if they decline, dropping the new item on the ground
#
def inv_add(item):
	""" Adds an item to the player's inventory, asking if they wish to drop an item if the inventory is full.
	"""
	if len(inventory) < 3:
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



# prompts user to view a list of inventory items and pick one to remove
#
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


def search_area(current_location):
	""" Searches area upon player pressing 'x' to find and collect loot.  You really should try the goat's milk.
	"""
	# retrieve Locale object for current location to check 
	# boolean variable for presence of loot at the location
	curr_coord_name = current_location.return_object_name()
	object_name = retrieve_Locale(current_location)
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

# this function ends the program
#
def die():
	sys.exit("\nGame Over.\n")


# variables
#

# stores objects/instances of the Locale class, i.e., each actual location on the map grid
locations = {}

# this line sets up the first location, the player's starting point
current_location = Point(0, 0)
location = Locale(current_location, False, True)

# this line starts the loop which gets user input for interacting with the environment
narrative(current_location, newplayer)