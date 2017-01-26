# Realm of Reckoning
# A Text-based adventure game
# by
# Daniel Ashcom
# GNU GPL v 3.0 but I want my free beer.
# 

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

#defines the input prompt
prompt = '=---> '

#sets the initial input value to 'nowhere' (should be n, s, e, w, h, t, i, q, or h, as currently implemented in the move() function)
# Seems like there should be a purpose for calling it nowhere...  should I try to test and catch this somehow?  Haven't seen it cause any problems... yet.
go = 'nowhere'

#tells the program whether to display the new player narrative introducing the game and the start scene
# TO-DO:  Get rid of this.  Create an Intro class to print the opening narrative text once and call it at the beginning before the first call to narrative()
newplayer = True

inventory = []  # a list to keep track of items in player's inventory

current_location = None  # a temporary reference to the player's current location object

locations = {}  # a dictionary of map location objects, named as a string derived from location's coordinates

player = None		# variable to be used for player instance of Character class; instantiated in world instance of Map class



# Classes
##
class Map(object):
	# globals
	##
	global locations, current_location, player

	# methods
	##
	def __init__(self):
		self.locations = locations
		# create player instance of character class
		player = Character('male', 'Bob', 10, 5, 3, 0, [])
		print player
		# create starting location on world map
		starting_l = Location([0,0], False, True)
		# add starting location to dictionary containing all locations
		locations[starting_l.name] = starting_l
		self.current_location = starting_l
		# this line starts the loop which gets user input for interacting with the environment
		player.narrative()


# TO-DO: add the ability to drop items and have them persist
		# but currently loot is handled directly by search so that
		# functionality should be moved here or shared by search and Location
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
		global current_location, locations

		self.coords = current_location_coords
		self.x = current_location_coords[0]
		self.y = current_location_coords[1]		
		self.monsters_present = monsters_present		
		self.loot_present = loot_present
		self.name = str(self.x) + str(self.y)	
		current_location = self

	def __str__(self):
		return "Current player location " + str(self.name) + " is at " + str(self.coords) + ", monsters present? " + str(self.monsters_present) + " Loot present? " + str(self.loot_present)

	def get_coords(self):
		""" returns a list coordinate pair denoting location's position on map """
		return [self.x, self.y]

	def set_coords(self, x, y):
		"""
			Set the location.
		"""
		self.x = x
		self.y = y
	
	def return_object_name(self):
		"""
			Return a unique string made up of the x and y coordinates
			to be used for naming each Location object as it is created and
			for retrieval.
		"""
		return str(self.x) + str(self.y)

	def get_curr_location(self):
		""" returns the player's current location object """
		return self.current_location

	def add_location(self, coords, mon, loot):
		""" adds a location to the map """
		l = Location(coords, mon, loot)
		locations[l.name] = l

	def check_location_existence(self):
			""" Check for the existence of a Location object and create it if it doesn't exist yet.
			This is called when moving to a different location on the map """
			name = self.return_object_name()

			if name in locations:
				current_location = locations[name]
				return
			else:
				coords = (self.x, self.y)
				new_location = self.add_location(coords, False, True)
				locations[name] = new_location

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

	# Location class's methods for movement around the map
	##
	def move_north(self):
		"""	add one to the y value, i.e., move north """
		self.y += 1
		self.check_location_existence()
	
	def move_east(self):
		""" add one to the x value, i.e., move east """
		self.x += 1
		self.check_location_existence()
	
	def move_south(self):
		""" subtract one from the y value, i.e., move south """
		self.y -= 1
		self.check_location_existence()
	
	def move_west(self):
		""" subtract one from the x value, i.e., move west """
		self.x -= 1
		self.check_location_existence()		


# this class represents the player
class Character(object):
	def __init__(self, sex, name, hp, stam, mp, gld, inv):
		self.sex = sex
		self.name = name
		self.hp = hp
		self.stamina = stam
		self.mp = mp
		self.gold = gld
		self.inventory =  inv

	def __str__(self):
		return "Player attributes for " + str(self.name) + ": sex: " + str(self.sex) + " hit points: " + str(self.hp) + " stamina: " + str(self.stamina) + " magic points: " + str(self.mp) + " gold: " + str(self.gold) + " inventory items: " + str(self.inventory)

	def narrative(self):
		""" Handles delivery of narrative text based on location as well as any choices available in any given location """
		global current_location, player, newplayer
	
		if newplayer == True:
			print "\nYou awaken to the distant sound of commotion to your west.  You\n open your eyes and realize you are in a vulnerable spot\n in an open field.  You look west toward the direction of\n the distant sounds and hear that it is now quiet.  \nTo your north in the distance is a fortress.  To your \neast is a forest and to your south is a riverbank\n with a boat tied at a pier.  \nWhich direction do you go? (enter: 'n', 's', 'e' or 'w')"
			newplayer = False
	
		elif current_location.x == 0 and current_location.y == 0:
			print "\nYou are standing in the same field in which you first awoke without\n 	any memory of how you got here.  Which way?\n"
	
		elif current_location.x == -1 and current_location.y == 0:
			print "\nAs you proceed west, you come upon signs of a battle, \nincluding two bodies lying face-down at the edge of a wood\n near the field in which you awoke.  There are no signs of\n life.  Do you approach the bodies? (y/n)"			
			choice = raw_input(prompt)

			if choice in {'yes', 'y', 'Y', 'Yes', 'YES', 'YEs', 'YeS', 'yeS'}:
				print "\nAs you approach one of the bodies closely, you realize\n that he is feigning death when he rolls quickly and \nsinks a blade into your 	neck.  Your life fades slowly."
				die()

			elif choice in {'no', 'n', 'N', 'NO', 'nO'}:
				print "\nWell, daylight's a-wasting.  Where to now?"

			else:
				print "Please type y or n."
	
		elif current_location.x == 0 and current_location.y == 1:
			print "\nYou walk for some time to finally arrive at an old, \napparently abandoned fortress which is crumbled with time.  \nThere is nothing here 	but ruins.  Which direction do you go\n from here?"	
	
		elif current_location.x == 0 and current_location.y == 2:
			print "\nAs you head north around the abandoned and crumbling \nfortress you see a valley spread out before you.  In the \ndistance to the north is a village with wafts of smoke being \ncarried off by the breeze trailing over the scene \nlike the twisted tails of many kites.  To the west gently\n sloping foothills transition into distant blue\n mountains and to the 	east, a vast forest conspires to block out\n all surface detail."
	
		else:
			prRed("Under construction.  Returning to the beginning.  Pick a different 	direction next time.")
			current_location.set_coords(0, 0)
			self.narrative()
	
		# get user input
		go = raw_input(prompt)

		# call move method of player instance of Character class to handle user input
		self.move(go)

	def move(self, input):
		""" Handles keeping track of player location based on which direction they head and their 	current location arguments	go user input ('n', 's', 'e', 'w', etc.)
		current_location a reference to the instance of the Location class for the 	player's current location on the map newplayer a boolean which keeps track of whether the player is just starting the game.	"""
		global current_location, newplayer	
		
		curr_loc = current_location
	
		if input in {'n', 'north', 'North'}:
			curr_loc.move_north()
		elif input in {'s', 'south', 'South'}:
			curr_loc.move_south()
	
		elif input in {'e', 'east', 'East'}:
			curr_loc.move_east()
		elif input in {'w', 'west', 'West'}:
			curr_loc.move_west()
	
		elif input in {'q', 'quit', 'Quit'}:
			prRed("Are you sure you want to exit? (y/n)")
			choice = raw_input(prompt)
			if choice in {'y', 'Y', 'yes', 'Yes', 'YES'}:
				die()
			elif choice in {'n', 'N', 'No', 'NO'}:
				print "Let's get back to it then."
				
			else:
				print "Please type yes or no."
	
		elif input in {'h', 'H', 'help', 'Help', 'HELP', 'HALP', 'halp'}:
			prBlue("\nHelp:\nn move north\ns move south\ne move east\nw move west\nx search \nt check the time\ni check your inventory\nq quit\nh help\n")
				
		elif input in {'i', 'inventory', 'I', 'Inventory', 'INVENTORY'}:
			inv_list()
				
		elif input in {'x', 'search'}:
			search_area(curr_loc)
				
		else:
			print "Please type 'n', 's', 'e' or 'w'."
		
		self.narrative()


### TO_DO:  Create an Inventory Class and/or add to the Character class and place inventory functions there.
def inv_list():
	""" Lists all the items in the player's inventory
	"""
	print "\nInventory: \n" 
	prGreen(inventory)
	
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
def search_area(curr_loc_coords):
	""" Searches area upon player pressing 'x' to find and collect loot.  You really should try the goat's milk.
	"""
	# retrieve Location object for current location to check 
	# boolean variable for presence of loot at the location
	global current_location
	lp = current_location.loot_present

	if current_location.coords[0] == 0 and current_location.coords[1] == 0 and lp == True:
		print "After searching the area you find a bit of rope useful for tinder and a strangely-chilled glass of goat's milk."
		inv_add("tinder")
		inv_add("goat milk")		
	elif current_location.coords[0] == 0 and current_location.coords[1] == 1 and lp == True:
		print "Upon looking around the ruins, you find very little of use, all having been picked clean long ago by scavengers.  You did however manage to find a bit of flint near an old campfire."
		inv_add("flint")
	elif current_location.coords[0] == 0 and current_location.coords[1] == 2 and lp == True:
		print "You stumble upon a rusty blade."
		inv_add("rusty blade")
	else:
		prYellow("You found nothing useful here.")

	current_location.loot_present = False
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
# this line sets up the map and its first location, the player's starting point and calls narrative to start the game loop
world = Map()
