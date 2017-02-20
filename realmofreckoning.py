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
#
# sys is for exiting the program
# vtemu is a VT100 emulator for Windows which colorizes text
import sys, vtemu, time, random


# Global variables
##
start_time = time.time() # set starting time

#defines the input prompt
prompt = '=---> '

#sets the initial input value to 'nowhere' (should be n, s, e, w, h, t, i, q, or h, as currently implemented in the keydown() method of the Character class)
go = 'nowhere'

#tells the program whether to display the new player narrative introducing the game and the start scene
# TO-DO:  Get rid of this.  Create an Intro class to print the opening narrative text once and call it at the beginning before the first call to narrative()
_newplayer = True

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
		self.create_char()
		# create starting location on world map
		# TO-DO:  need to instantiate each of the spiders while creating the location
		_starting_l = Location([0,0], True, True, [['spider',2], ['ant',1]])
		print _starting_l
		# this line starts the loop which gets user input for interacting with the environment
		self.narrative(player.get_coords())

	def create_char(self):
		global player
		""" prompts user to answer questions in order to create their character """
		# 
		# print "Welcome to Realm of Reckoning.  Please answer the following questions to create your character:"
		# 			
		# print "1.  What is your character's gender?"
		# sex = raw_input("?")
		# if sex not in ["m", "male", "f", "female"]:
			# print "Please enter male or female."
		# 			
		# print "2.  What is your character's name?"
		# name = raw_input("?")
		# 
		# player = Character(sex, name, 10, 5, 3, 0, [], [0,0])
		# print "Ok, here's some information about your character: ", player
		# self, ch_type, sex, name, copper, inv, coords
		player = Player('Player', 'male', 'Shaun', 0, [], [0,0])

	@classmethod
	def add_location(cls, coords, mon, loot, **monster_types_and_quantities):
		""" adds a location to the map """
		l = Location(coords, mon, loot, **monster_types_and_quantitiesmtaq)
		locations[l.name] = l

	@classmethod
	def coords_to_name(cls, coords):
		""" creates a name to be used as a key for looking up instances of Location in locations """
		name = str(coords[0]) + str(coords[1])
		return name

	@classmethod
	def check_location_existence(cls, coords):
		""" Check for the existence of a Location object and create it if it doesn't exist yet.  This is called when moving to a different location on the map """
		name = Map.coords_to_name(coords)

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
			string = coords_to_name(current_location_coords)
			return locations[string]
		except NameError:
			print "Location does not exist."
		else:
			return

	def teleport(self, coords):
		#loc = self.retrieve_Location(coords)
		player.set_coords(coords)
		self.narrative(player.get_coords())

	def narrative(self, area):
		""" Handles delivery of narrative text based on location as well as any choices available in any given location """
		global player, narratives

		key = tuple(area)

		narratives = {(0,0): ["\n     You are standing in the same field in which you first awoke\nwithout any memory of how you got here.  Which way?\n"],
					  (-1,0): ["\nAs you proceed west, you come upon signs of a battle, \nincluding two bodies lying face-down at the edge of a wood\n near the field in which you awoke.  There are no signs of\n life.  Do you approach the bodies? (y/n)", self.encounter],
					  (0,1): ["\n     You walk for some time to finally arrive at an old, \napparently abandoned fortress which has crumbled with time.  \nThere is nothing here but ruin.  As you approach an outcrop of rock, you realize there is a narrow passage leading down into the ground, perhaps an old cellar entrance.  Do you enter? (y/n)", self.encounter],
					  (0,2): ["\n     As you head north around the abandoned and crumbling\nfortress you see a valley spread out before you.  In the\ndistance to the north is a village with wafts of smoke being\ncarried off by the breeze trailing over the scene like\nthe twisted tails of many kites.  To the west gently\nsloping foothills transition into distant blue mountains\nand to the east, a vast forest conspires to block out all \nsurface detail."]}

		if player._newplayer == True:
			print "\n     You awaken to the distant sound of commotion to your west.  \nYou open your eyes and realize you are in a vulnerable spot\n in an open field.  You look west toward the direction of\n the distant sounds and hear that it is now quiet.  To your \nnorth in the distance is a fortress.  To your east is a \nforest and to your south is a riverbank with \aa boat tied at a pier.  \n\nWhich direction do you go? (Press 'h' for help)"
			player._newplayer = False

		elif key in narratives:
			print narratives[key][0]
			if len(narratives[key]) > 1:  # if there are events associated with this area, execute them
				for i in range(1,len(narratives[key])):
					temp_list = area[:]
					temp_list.append(i)
					ch_key = temp_list
					narratives[key][i](ch_key)

 		else:
			prRed("Under construction.  Returning to the beginning.")
			self.teleport([0,0])
	
		# get user input
		user_input = raw_input(prompt)
		# get rid of any capitalized typing by the user
		user_input.lower()

		# call keydown method of player instance of Character class to handle user input
		self.keydown(user_input)

	def next_choice(self, choice_key):
		""" increments choice_key's 3rd number to proceed a deeper level in the branching choices for any location """
		# cast choice_key back as a list so that it can be modified.  I'm pretty sure others would frown on this approach but it works and I have no idea of how else to create this functionality
		choice_key[2] += 1
		self.encounter(choice_key)

	def encounter(self, choice_key):
		# a third number has been added to the tuple key to represent level of depth (decision/choice 1: outcome, decision/choice 2/outcome, etc.)  The Value of each of these keys goes in the form:  ['user-input choice', print narrative, command(s) to execute]
		
		# prompt user for input in respose to encounter
		input = raw_input(prompt).lower()

		# cast choice_key as a tuple so it can be used as a dictionary key
		t_choice_key = tuple(choice_key)

		outcomes = { (-1,0,1): {'y': ["\nAs you approach one of the bodies closely, you realize\n that he is feigning death when he rolls quickly and \nsinks a blade into your neck.  Your life fades slowly.", player.die], 'n': ["\nWell, daylight's a-wasting.  Where to now?"]}, 
					 (0,1,1):	{'y': ["\nYou steel yourself and proceed down the cracked and disintegrating steps only to find a locked wooden door.  Do you attempt to force the lock? (y/n)", self.next_choice], 'n': ["\nWhere to now?"]},
					 (0,1,2):   {'y': ["\nYou put all your force into it as you drive your shoulder into the door.  It gives way in a sudden explosion of splinters, dust and debris.  It's too dark to proceed safely without a lantern."], 'n': ["\nWhere to now?"]} }

		if t_choice_key in outcomes and input in ['y', 'yes', 'n', 'no']:
			print outcomes[t_choice_key][input][0]
			if len(outcomes[t_choice_key][input]) > 1:
				for i in range (1,len(outcomes[t_choice_key][input])):
					if outcomes[t_choice_key][input][i] == self.next_choice:
						outcomes[t_choice_key][input][i](choice_key)
					else:
						outcomes[t_choice_key][input][i]()
		else:
			# for k in outcomes[choice_key]:
				# print "Please type "
				# for i in outcomes[choice_key]:
					# print "",outcomes[choice_key].key()
			print "Please type 'y(es)'' or 'n(o)'."
			self.encounter(choice_key)

	def keydown(self, user_input):
		""" Handles user input """

		# dictionary of possible user inputs with matching names of methods to call for each
		inputs = {"n": player.move, "s": player.move, "e": player.move, "w": player.move, "q": player.quit_game, "h": player.help_menu, "i": player.inv_list, "a": player.attack, "c": player.attrib_list, "x": player.search_area, "t": player.check_time}	

		if user_input in inputs:
			if user_input in ["n", "s", "e", "w"]:
				inputs[user_input](user_input)  # call the function that matches the key pressed by the user, passing the parameter if it is a direction of travel
			else:  # otherwise don't pass a parameter
				inputs[user_input]()
		if user_input not in inputs:
			print "Please type 'h' for help."
		self.narrative(player.get_coords())


class Location(object):
	""" This class defines all of the attributes to be stored for each location object
		initializes attributes for:
		location 			point containing x and y coordinates
		name 				used to create the key for the dictionary storing each object
		bool_monsters_present 	tracks whether monsters are in the present location
		monster_types_and_quantities  a list of lists in the form: [[string, num], [string, num]], representing the types and quantities of each type of monster present in a map location.  Only assigned if bool_monsters_present is True.
		loot_present 		keeps track of whether loot is in the present location 
							(either having been dropped or spawned initially) """	
	def __init__(self, current_location_coords, bool_monsters_present, loot_present, monster_types_and_quantities):
		global current_location, locations, x, y, loot

		self.coords = current_location_coords
		self.x = current_location_coords[0]
		self.y = current_location_coords[1]		
		self.bool_monsters_present = bool_monsters_present		
		self.loot_present = loot_present
		self.name = str(self.x) + str(self.y)	
		self.monsters_at_location = []
		current_location = self
		locations[self.name] = self

		if self.bool_monsters_present is True:
			self.mtaq_list = monster_types_and_quantities
			# TEST:
			print self.mtaq_list[0][1]

			for x in range(len(self.mtaq_list)-1):
				range_shy = self.mtaq_list[x][1]
				print range_shy
				for quantity in range(1, (range_shy)):
					print self.mtaq_list[x][quantity]
					mon_name = self.mtaq_list[x][0] + str(quantity)
					mon_name = NPC(self.mtaq_list[x][0])
					self.monsters_at_location.append(mon_name)
			print self.monsters_at_location

		# check for existence of loot entry in dictionary before assigning loot listed there to this instance's loot list
		if self.name in loot:
			self.loot = loot[self.name]
		else:
			self.loot = []

	def __str__(self):
		return "Current player location " + str(self.name) + " is at " + str(self.coords) + "\nMonsters present? " + str(self.bool_monsters_present) + "\nLocation contains the following monsters: " + str(self.mtaq_list) + "\nLoot present? " + str(self.loot_present)

	def get_coords(self):
		""" returns a list coordinate pair denoting location's position on map """
		return [self.x, self.y]

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y


class Character(object):
	""" Represents the player with methods for inventory management, searching areas, generating narrative, moving and dying. """
	# dictionary of Character stats as: 'type': ['class name', hitpoints, stamina, magicpoints, copper, [inv], [location]]
	global ch_types

	ch_types = {'Player': ['Player', 10, 10, 10, 0, [], [0,0]],
			 'spider': ['NPC', 3, None, None, 0, ['poison sac'], []],
			 'ant': ['NPC', 1, None, None, 0, [], []],
			 'bear': ['NPC', 15, None, None, 0, ['bear pelt'], []]}

	def __init__(self, ch_type):
		self.ch_type = ch_type # will be either 'player' or 'NPC'
		self.stats_setup(ch_type)
		self._max_inv_size = 5
		self.coords = [0,0]

	def stats_setup(self, ch_type):
		global ch_types

		if self.ch_type in ch_types:
			self.hp = ch_types[self.ch_type][1]
			self.max_hp = self.hp
			self.stamina = ch_types[self.ch_type][2]
			self.max_stam = self.stamina
			self.mp = ch_types[self.ch_type][3]
			self.max_mp = self.mp
			self.copper = ch_types[self.ch_type][4]
		else:
			print "ERROR:  Attempting to create unknown NPC Character type."

	def __str__(self):
		return "\nAttributes for " + str(self.ch_type) +":" + "\nName: " + self.name + "\nhit points: " + str(self.hp) + "/" + str(self.max_hp) + "\nstamina: " + str(self.stamina) + "/" + str(self.max_stam) + "\nmagic points: " + str(self.mp) + "/" + str(self.max_mp) + "\ncopper: " + str(self.copper) + "\ninventory items: " + str(self.inventory) + "\nLocation: " + str(self.get_coords())

	def set_coords(self, coords):
		""" sets the player's coordinates on the map """
		self.coords[0] = coords[0]
		self.coords[1] = coords[1]

	def get_coord(self, element):
		""" returns the player's specified coordinate on the map """
		return self.coords[element]

	def get_coords(self):
		""" returns the player's coordinates on the map """
		return self.coords

	def get_location(self):
		global locations

		location_key = Map.coords_to_name(self.get_coords())
		if location_key in locations:
			location = locations[location_key]
			return location
		else:
			print location_key + " not found."

	# methods for movement around the map and user input
	#
	def move(self, direction):
		# pair all options with an action in a dictionary
		directions = { "n": [self.get_coord(0),(self.get_coord(1)+1)], "s": [self.get_coord(0),(self.get_coord(1)-1)], "e": [(self.get_coord(0)+1),self.get_coord(1)], "w": [(self.get_coord(0)-1), self.get_coord(1)] }
		# execute directional movement by updating player's coords
		if direction in directions:
			self.set_coords(directions[direction])
		# check for the existence of the Location to which the player has moved 
		Map.check_location_existence(self.get_coords())

	def quit_game(self):
		prRed("Are you sure you want to exit? (y/n)")
		choice = raw_input(prompt)
		if choice.lower() in {'y', 'Y', 'yes', 'Yes', 'YES'}:
			self.die()
		elif choice.lower() in {'n', 'no'}:
			print "Let's get back to it then."

	def help_menu(self):
		prBlue("\nHelp:\nn move north\ns move south\ne move east\nw move west\nx search \nt check the time\ni check your inventory\na attributes\nq quit\nh help\n")

	def inv_list(self):
		""" Lists all the items in the player's inventory
		"""
		print "\nInventory: \n" 
		prGreen(self.inventory)

	def attrib_list(self):
		# if self is 'Player':
			# self.get_player_stats()
		# else:
		print self

	def search_area(self):
		""" Searches area upon player pressing 'x' to find and collect loot.  You really should try the goat's milk. """
		# retrieve Location object for current location to check boolean variable for presence of loot at the location
		global loot_list, current_location
		# cast list representing player's x/y coordinates as a tuple for comparison to loot_list dictionary's keys
		area = tuple(self.get_coords())

		lp = current_location.loot_present

		# define a dictionary which contains a tuple representing each map location's coordinates, paired with a list containing (1) a print statement description of the area and (2+) any accompanying commands required to add items to the player's inventory
		loot_list = {(0,0): ["After searching the area you find a bit of rope useful for tinder and a strangely-chilled glass of goat's milk.", "tinder", "goat milk"],
					 (0,1): ["Upon looking around the ruins, you find very little of use, all having been picked clean long ago by scavengers.  You did however manage to find a bit of flint near an old campfire.", "flint"], 
					 (0,2): ["You stumble upon a rusty blade.", "rusty blade"],
					 (-1,0): ["While searching the area, you begin to rifle through the pockets of the two bodies.  On the first, you find a notebook.  The second appears to still be alive so you don't approach him just yet.", "notebook"]}

		if lp == True:	# if loot is present in the area
			if area in loot_list:  # if the area has items contained in the loot list (redundant)
				print loot_list[area][0]	# print the first element of the value list
				for i in range(1, len(loot_list[area])):
					self.inv_add(loot_list[area][i])	# execute the command(s) contained in the second element of the value list, adding said items to player's inventory
			else:
				prYellow("You found nothing useful here.")	
	
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
		""" Removes an item from the player's inventory (and adds it to the location).  Called from inv_prmpt_remove() function """
		## TO-DO: pop item instead, adding it to the list of items in the current Location object
		self.inventory.remove(item)

	def check_time(self):
		""" handles keeping track of in-game time, which is planned to affect interactions in the game """
		pass

	def attack(self):
		""" TO-DO:  add a parameter called initiative which is a to_hit and hp_value modifier based on whether the target sees the attacker coming or is taken off-guard """
		area = self.get_location()

		if area.bool_monsters_present is False:
			print "While we applaud your fervor, there's nothing to attack here."
			return
		else:
			# target of attack becomes first monster retrieved from monster_types_and_quantities list
			target_name = area.mtaq_list[0][0]

			# retrieve instance object with given target_name
			target_object = Map.get self.get_location

			print "Attacking target: " + target

		ra = self.roll_attack()

		print "You attack the " + target
		
		if ra[0] >= 5:
			prGreen("You hit the " + target + "for" + str(ra[1]) + "hp.")
			target.sub_hp(ra[1])
		if target.is_alive:
			print target.ch_type + "retaliates."
			self.roll_attack()
			if ra[0] >= 5:
				prRed(target.ch_type + "hits you for" + str(ra[1]) + "hp.")
			else:
				prRed(target.ch_type + "misses!")

	def roll_attack(self):
		""" a helper method for attack() method, returns a list of two elements:  [to_hit, hp_value] """
		to_hit = random.randint(0,9)
		hp_value = random.randint(0,3)

		return [to_hit, hp_value]

	def sub_hp(self, amt):
		self.hp -= amt
		if self.hp <= 0:
			self.die()
			target_is_alive = False 

	def add_hp(self,amt):
		self.hp += amt
		if self.hp > self.max_hp:
			self.hp = self.max_hp

	def die(self):
		"""	this function kills characters (player or NPC) """
		if self.ch_type is 'Player':
			message = prRed("\nGame Over.\n")
			sys.exit(message)
		else:
			message = "You have defeated the " + self.ch_type + "."

class Player(Character):
	def __init__(self, ch_type, sex, name, copper, inv, coords):
		super(Player, self).__init__(ch_type)
	 	self._sex = sex
	 	self.name = name
	 	self._newplayer = True

	def get_player_stats(self):
		return "\n" + self.ch_type + " attributes for " + str(self.name) + "\ngender: " + str(self._sex) + "\nhit points: " + str(self.hp) + "/" + str(self.max_hp) + "\nstamina: " + str(self.stamina) + "/" + str(self.max_stam) + "\nmagic points: " + str(self.mp) + "/" + str(self.max_mp) + "\ncopper: " + str(self.copper) + "\ninventory items: " + str(self.inventory) + "\nNew player? " + str(self._newplayer) + "\nMax # inventory items: " + str(self._max_inv_size) + "\nLocation: " + str(self.get_coords())

class NPC(Character):
	def __init__(self, ch_type):
		super(NPC, self).__init__(ch_type)
		self.stats_setup(ch_type)

	def npc_stats():
		return "\n" + self.ch_type + " attributes: " + "\nhit points: " + str(self.hp) + "/" + str(self.max_hp) + "\nstamina: " + str(self.stamina) + "/" + str(self.max_stam) + "\nmagic points: " + str(self.mp) + "/" + str(self.max_mp) + "\ncopper: " + str(self.copper) + "\ninventory items: " + str(self.inventory) + "\nMax # inventory items: " + str(self._max_inv_size) + "\nLocation: " + str(self.get_coords())
		

# Game Loop
##
# this line sets up the map and its first location, the player's starting point and calls narrative to start the game loop
world = Map()
