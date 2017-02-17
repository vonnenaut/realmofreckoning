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
# To-Do/Ideas:
#-------------------------------------------------------------------
# -- Implement a more readable, concise way to handle logic, replacing if-else with dictionaries (I think ... ?) --  See Coursera Fundamentals of Computing 2of7, wk 7b Programming Tips (02:30)
# --Consider ways to reduce or eliminate all global variables (encapsulate into classes?)
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

# imports
##
#
# sys is for exiting the program
# vtemu is a VT100 emulator for Windows which colorizes text
import sys, vtemu


# Global variables
##

#defines the input prompt
prompt = '=---> '

#sets the initial input value to 'nowhere' (should be n, s, e, w, h, t, i, q, or h, as currently implemented in the keydown() method of the Character class)
go = 'nowhere'

#tells the program whether to display the new player narrative introducing the game and the start scene
# TO-DO:  Get rid of this.  Create an Intro class to print the opening narrative text once and call it at the beginning before the first call to narrative()
newplayer = True

inventory = []  # a list to keep track of items in player's inventory

coords = [0,0]  # a list of coordinates for the current player's location on the map

current_location = None  # a temporary reference to the player's current location object

locations = {}  # a dictionary of map location objects, key'd as a string derived from location's coordinates

loot = {}  # a dictionary of loot, key'd with the same string derived from each location's coordinates as the locations dictionary of Location instances

player = None		# variable to be used for player instance of Character class; instantiated in world instance of Map class

world = None

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


# Classes
##
class Map(object):
	""" creates, stores and retrieves locations; presents narratives for each """
	# methods
	##
	def __init__(self):
		global player

		self.locations = locations
		# create player instance of character class
		player = Character('male', 'Bob', 10, 5, 3, 0, [], [0,0])
		# create starting location on world map
		starting_l = Location([0,0], False, True)
		# this line starts the loop which gets user input for interacting with the environment
		self.narrative()

	@classmethod
	def add_location(cls, coords, mon, loot):
		""" adds a location to the map """
		l = Location(coords, mon, loot)
		locations[l.name] = l

	@classmethod
	def coords_to_Name(cls, coords):
		name = str(coords[0]) + str(coords[1])
		return name

	@classmethod
	def check_location_existence(cls, coords):
		""" Check for the existence of a Location object and create it if it doesn't exist yet.  This is called when moving to a different location on the map """
		name = Map.coords_to_Name(coords)

		if name in locations:
			current_location = locations[name]
			return
		else:
			new_location = Map.add_location(coords, False, True)
			locations[name] = new_location
	
	@classmethod
	def retrieve_Location(cls, current_location_coords):
		""" attempts to return an object with a name based on the current location coordinates 	if the object name doesn't exist, throws NameError exception """

		try:
			string = coords_to_Name(current_location_coords)
			return locations[string]
		except NameError:
			print "Location does not exist."
		else:
			return

	@classmethod
	def teleport(cls, coords):
		loc = Map.retrieve_Location(coords)
		player.set_Coords(coords)
		Map.narrative()

	@classmethod
	def narrative(cls):
		""" Handles delivery of narrative text based on location as well as any choices available in any given location """
		global player
			
		if player.newplayer == True:
			print "\n     You awaken to the distant sound of commotion to your west.  \nYou open your eyes and realize you are in a vulnerable spot\n in an open field.  You look west toward the direction of\n the distant sounds and hear that it is now quiet.  \nTo your north in the distance is a fortress.  To your \neast is a forest and to your south is a riverbank\n with a boat tied at a pier.  \nWhich direction do you go? (enter: 'n', 's', 'e' or 'w')"
			player.newplayer = False
	
		elif player.coords == [0,0]:
			print "\n     You are standing in the same field in which you first awoke without\nany memory of how you got here.  Which way?\n"
	
		elif player.coords[0] == -1 and player.coords[1] == 0:
			print "\nAs you proceed west, you come upon signs of a battle, \nincluding two bodies lying face-down at the edge of a wood\n near the field in which you awoke.  There are no signs of\n life.  Do you approach the bodies? (y/n)"			
			choice = raw_input(prompt)

			if choice in {'yes', 'y', 'Y', 'Yes', 'YES', 'YEs', 'YeS', 'yeS'}:
				print "\nAs you approach one of the bodies closely, you realize\n that he is feigning death when he rolls quickly and \nsinks a blade into your neck.  Your life fades slowly."
				self.die()

			elif choice in {'no', 'n', 'N', 'NO', 'nO'}:
				print "\nWell, daylight's a-wasting.  Where to now?"

			else:
				print "Please type y or n."
	
		elif player.coords[0] == 0 and player.coords[1] == 1:
			print "\n     You walk for some time to finally arrive at an old, \napparently abandoned fortress which is crumbled with time.  \nThere is nothing here 	but ruins.  Which direction do you go\n from here?"	
	
		elif player.coords[0] == 0 and player.coords[1] == 2:
			print "\n     As you head north around the abandoned and crumbling\nfortress you see a valley spread out before you.  In the\ndistance to the north is a village with wafts of smoke being\ncarried off by the breeze trailing over the scene like\nthe twisted tails of many kites.  To the west gently\nsloping foothills transition into distant blue mountains\nand to the east, a vast forest conspires to block out all \nsurface detail."
	
		else:
			prRed("Under construction.  Returning to the beginning.  Pick a different 	direction next time.")
			Map.teleport([0,0])
	
		# get user input
		user_input = raw_input(prompt)
		# get rid of any capitalized typing by the user
		user_input.lower()

		# call keydown method of player instance of Character class to handle user input
		player.keydown(user_input)



class Location(object):
	""" This class defines all of the attributes to be stored for each location object
		initializes attributes for:
		location 			point containing x and y coordinates
		name 				used to create the key for the dictionary storing each object
		monsters_present 	tracks whether monsters are in the present location
		loot_present 		keeps track of whether loot is in the present location 
							(either having been dropped or spawned initially) """	
	def __init__(self, current_location_coords, monsters_present, loot_present):
		global current_location, locations, x, y, loot

		self.coords = current_location_coords
		self.x = current_location_coords[0]
		self.y = current_location_coords[1]		
		self.monsters_present = monsters_present		
		self.loot_present = loot_present
		self.name = str(self.x) + str(self.y)	
		current_location = self
		# check for existence of loot entry in dictionary before assigning loot listed there to this instance's loot list
		if self.name in loot:
			self.loot = loot[self.name]
		else:
			self.loot = []

	def __str__(self):
		return "Current player location " + str(self.name) + " is at " + str(self.coords) + ", monsters present? " + str(self.monsters_present) + " Loot present? " + str(self.loot_present)

	def get_coords(self):
		""" returns a list coordinate pair denoting location's position on map """
		return [self.x, self.y]

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y
	
	def return_name(self):
		"""
			Return a unique string made up of the x and y coordinates to be used for naming each Location object as it is created and for retrieval from the dictionary of Location objects.
		"""
		return str(self.x) + str(self.y)


class Character(object):
	""" Represents the player with methods for inventory management, searching areas, generating narrative, moving and dying. """
	global current_location, world

	def __init__(self, sex, name, hp, stam, mp, gld, inv, coords):
		self.sex = sex
		self.name = name
		self.hp = hp
		self.stamina = stam
		self.mp = mp
		self.gold = gld
		self.inventory =  inv
		self.newplayer = True
		self.max_inv_size = 5
		self.coords = [0,0]

	def __str__(self):
		return "\nPlayer attributes for " + str(self.name) + ":\nsex: " + str(self.sex) + "\nhit points: " + str(self.hp) + "\nstamina: " + str(self.stamina) + "\nmagic points: " + str(self.mp) + "\ngold: " + str(self.gold) + "\ninventory items: " + str(self.inventory) + "\nNew player? " + str(self.newplayer) + "\nMax # inventory items: " + str(self.max_inv_size) + "\nLocation: " + str(self.coords)

	def set_Coords(self, coords):
		""" sets the player's coordinates on the map """
		self.coords[0] = coords[0]
		self.coords[1] = coords[1]

	# methods for movement around the map and user input
	def move_north(self):
		"""	add one to the y value, i.e., move north """
		self.coords[1] += 1
		Map.check_location_existence(self.coords)
	
	def move_east(self):
		""" add one to the x value, i.e., move east """
		self.coords[0] += 1
		Map.check_location_existence(self.coords)
	
	def move_south(self):
		""" subtract one from the y value, i.e., move south """
		self.coords[1] -= 1
		Map.check_location_existence(self.coords)
	
	def move_west(self):
		""" subtract one from the x value, i.e., move west """
		self.coords[0] -= 1
		Map.check_location_existence(self.coords)

	def quit_game(self):
		prRed("Are you sure you want to exit? (y/n)")
		choice = raw_input(prompt)
		if choice.lower() in {'y', 'Y', 'yes', 'Yes', 'YES'}:
			self.die()
		elif choice.lower() in {'n', 'no'}:
			print "Let's get back to it then."

	def help_menu():
		prBlue("\nHelp:\nn move north\ns move south\ne move east\nw move west\nx search \nt check # the time\ni check your inventory\na attributes\nq quit\nh help\n")

	def inv_list(self):
		""" Lists all the items in the player's inventory
		"""
		print "\nInventory: \n" 
		prGreen(self.inventory)

	def attrib_list():
		print self

	def search_area(self):
		""" Searches area upon player pressing 'x' to find and collect loot.  You really should try the goat's milk. """
		# retrieve Location object for current location to check boolean variable for presence of loot at the location
		lp = current_location.loot_present
		
		if self.coords == [0,0] and lp == True:
			print "After searching the area you find a bit of rope useful for tinder and a 	strangely-chilled glass of goat's milk."
			self.inv_add("tinder")
			self.inv_add("goat milk")		
		elif self.coords == [0,1] and lp == True:
			print "Upon looking around the ruins, you find very little of use, all having been picked clean long ago by scavengers.  You did however manage to find a bit of flint near an old 	campfire."
			self.inv_add("flint")
		elif self.coords == [0,2] and lp == True:
			print "You stumble upon a rusty blade."
			self.inv_add("rusty blade")
		else:
			prYellow("You found nothing useful here.")
	
		current_location.loot_present = False
		return
	
	
	def inv_add(self, item):
		""" Adds an item to the player's inventory, asking if they wish to drop an item if the inventory is full. """
		if len(self.inventory) < 5:
			self.inventory.append(item)
			prGreen("\n %s added to inventory." % (item))
		else:
			print "Inventory full.  Drop an item? (y/n)"
			choice = raw_input(prompt)
			if choice in {'y', 'yes', 'Y', 'Yes', 'YES'}:
				self.inv_prmpt_remove()
				self.inv_add(item)
			else:
				print "Dropped %s on the ground." % (item)

	def inv_prmpt_remove():
		""" Prompts player to pick an item to remove from the inventory	"""
		print "\nWhich item do you wish to remove?\n"
		prGreen(inventory)
		print "\n"
		choice = raw_input(prompt)
		if choice in inventory:
			self.inv_remove(choice)
			prGreen("%s dropped on the ground." % (choice))
		else:
			print "Item: %s not found.  Please type the name of the item you wish to remove." % (choice)
			choice = raw_input(prompt)
		return

	def inv_remove(self, item):
		""" Removes an item from the player's inventory.  Called from inv_prmpt_remove() function
		"""
		self.inventory.remove(item)
	


	def keydown(self, user_input):
		""" Handles user input """

		# dictionary of possible user inputs with matching names of methods to call for each
		inputs = {"n": self.move_north, "s": self.move_south, "e": self.move_east, "w": self.move_west, "q": self.quit_game, "h": self.help_menu, "i": self.inv_list, "a": self.attrib_list, "x": self.search_area}		

		if user_input in inputs:
			inputs[user_input]()  # call the function that matches the key pressed by the user
		if user_input not in inputs:
			print "Please type 'h' for help."
		Map.narrative()

	def die(self):
		"""	this function ends the program """
		message = prRed("\nGame Over.\n")
		sys.exit(message)


# Game Loop
##
# this line sets up the map and its first location, the player's starting point and calls narrative to start the game loop
world = Map()
