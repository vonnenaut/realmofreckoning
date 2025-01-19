"""
Realm serves essentially as the game's main engine and logic handler, importing sys for ending the game, 
vtemu for text colorization, location for handling information in each location and character for player
and NPC (including monsters and non-combatants) stats and behaviors.  Realm, in turn, is imported and called by main.py.
"""

# imports
##
import sys, loc_mgr, json, vtemu
from location import Location
from character import Character


# special definitions for colorized text
##

# if the terminal is Windows, use these codes instead
if sys.platform == 'win32':	
	def prRed(prt): print("\x1b[1;31m {}\x1b[00m" .format(prt))
	def prGreen(prt): print("\x1b[2;32m {}\x1b[00m" .format(prt))
	def prYellow(prt): print("\x1b[1;33m {}\x1b[00m" .format(prt))
	def prBlue(prt): print("\x1b[1;34m {}\x1b[00m" .format(prt))
	def prPurple(prt): print("\x1b[1;35m {}\x1b[00m" .format(prt))

# if the terminal is Linux or Cygwin, use the following codes
else:
	def prRed(prt): print("\033[91m {}\033[00m" .format(prt))
	def prGreen(prt): print("\033[92m {}\033[00m" .format(prt))
	def prYellow(prt): print("\033[93m {}\033[00m" .format(prt))
	def prBlue(prt): print("\033[96m {}\033[00m" .format(prt))
	def prPurple(prt): print("\033[95m {}\033[00m" .format(prt))


class Realm(object):
	""" creates, stores and retrieves locations; presents narratives for each """
	# class variables
	##

	#defines the input prompt
	PROMPT = '=---> '

	# methods
	##
	def __init__(self):
		self.locations = {}				# dictionary containing instances of Location class representing each traversible area of the Realm
		starting_coords = [0,0]
		self.add_location(starting_coords)
		# self.create_char()		# create player instance of character class  #TODO: implement player creation process at start of game
		# for testing, comment the above and uncomment below
		self.player = Character('male', 'Rick', 10, 5, 3, 0, [], [0,0], '')

		# open narratives.json and encounters.json to be used for retrieving narrative for each location on grid and navigating specific story encounters at given locations
		with open('narratives.json', 'r') as narratives_file:
			self.narratives_data = json.load(narratives_file)
		with open('encounters.json', 'r') as encounters_file:
			self.encounters_data = json.load(encounters_file)
  
  		# TODO: remove
		# Test
		# print("\nself.narratives_data:\n {}".format(self.narratives_data))
		# print("\nself.narratives_data['0,0']['text']:\n {}".format(self.narratives_data['0,0']['text']))
		# print("\nself.narratives_data['0,0']['actions']:\n {}".format(self.narratives_data['0,0']['actions']))

		# print("\nself.encounters_data:\n {}".format(self.encounters_data)
        # )
		# print("\nself.encounters_data['0,1,1']:\n {}".format(self.encounters_data['0,1,1']["y"]))  
  
		self.narrative(self.player.get_coords())	# this line starts the loop which gets user input for interacting with the environment
  
	def __str__(self):
		pass


	def create_char(self):
		""" prompts user to answer questions in order to create their character """
		print("Welcome to Realm of Reckoning.  Please answer the following questions to create your character:")
		 			
		print("1.  What is your character's gender?")
		sex = input("?")
		if sex in ["m", "male"]:
			sex = "male"
		elif sex in ["f", "female"]:
			sex = "female"
		else:
			print("Please enter male or female.")
			sex = input("?")
					
		print("2.  What is your character's name?")
		name = input("?")
		 
		self.player = Character(sex, name, 10, 5, 3, 0, [], [0,0])
		print("Ok, here's some information about your character: ", self.player)

	def add_location(self, coords):
		""" adds a location to the Realm """
		key = tuple(coords)

		# check for existence of loot to add to this location per LOOT_LIST
		if key in loc_mgr.LOOT_LIST:
			loot = loc_mgr.LOOT_LIST[key]
			loot_present = True
		else:
			loot = []
			loot_present = False

		# check for existence of monsters to add to this location per MONSTER_LIST
		if key in loc_mgr.MONSTER_LIST:
			monster_list = loc_mgr.get_master_monster_list()
			monsters = monster_list[key]
			monsters_present = True
		else:
			monsters = []
			monsters_present = False

		# create new instance of Location and add it to the list of instances, then set it to the player's current location
		new_location = Location(coords, monsters_present, loot_present, monsters, loot)
		self.add_to_locations(new_location)
		self.current_player_location = new_location

	def add_to_locations(self, location):
		""" adds a new Location instance to a dictionary of Location instances """
		self.get_locations_dict()[location.name] = location

	def narrative(self, area):
		""" Handles delivery of narrative text based on location as well as any choices available in any given location """
		key = "{},{}".format(area[0],area[1])

		if self.player.newplayer == True:
			prBlue("\nWelcome to Realm of Reckoning!")
			print("\nYou awaken to the distant sound of commotion to your west.  \nYou open your eyes and realize you are in a vulnerable spot in \nan open field and realize that you carry nothing useful to \nhelp you survive should you run into trouble.  You look west \ntoward the direction of the distant sounds and hear that it \nis now quiet.  To your north in the distance is a fortress.  \nTo your east is a forest and to your south is a riverbank \nwith a boat tied at an old pier.  \n\nWhich direction do you go? (Press 'h' for help)")
			self.player.newplayer = False

		elif key in self.narratives_data:
			text = self.narratives_data[key]['text']
			actions = self.narratives_data[key]['actions']
			print(text)		
   
			if actions != None:  # if there are actions associated with this area, execute them
				for action in actions:
					temp_list = area[:]
					temp_list.append(action)
					choice_key = "{},{},{}".format(temp_list[0], temp_list[1], temp_list[2])
     
					self.encounter(choice_key)
		else: # if we have gone off the map of existing narratives, return to the location from which player attempted to move
			prRed("This location is under construction. Try a different direction.")
			self.move_back(self.player)
			self.narrative(self.player.get_coords())
	
		# get user input
		user_input = input(self.PROMPT)
		# get rid of any capitalized typing by the user
		user_input.lower()

		# call keydown method of player instance of Character class to handle user input
		self.keydown(user_input)


	def next_choice(self, choice_key):
		""" increments choice_key's 3rd number to proceed a deeper level in the branching choices for any location """
		# cast choice_key back as a list so that it can be modified.  I'm pretty sure others would frown on this approach but it works and I have no idea of how else to create this functionality
		choice_key = list(choice_key)
		self.encounter(choice_key)

	def encounter(self, choice_key):
		""" handles interactions for encounters on specific Realm Locations """
		# a third element, a descriptive word or phrase, has been added to the narratives key to make choice_key, and it represents a sort of level of depth (decision/choice 1: outcome, decision/choice 2/outcome, etc.)  The format of each of these choice_keys goes in the string form "x-coordinate,y-coordinate,description", to be used to look up narrative and possible further choices in the file encounters.json, which is imported as the variable encounters_data.
		
		# prompt user for input in respose to encounter
		user_input = input(self.PROMPT).lower()
  
		if choice_key in self.encounters_data and user_input in self.encounters_data[choice_key]:
			print(self.encounters_data[choice_key][user_input][0])
   
			if len(self.encounters_data[choice_key][user_input]) > 1:
				if self.encounters_data[choice_key][user_input][1] == "die":
					self.die()
				else:
					choice_key = "{},{},{}".format(self.player.get_coord(0), self.player.get_coord(1),  self.encounters_data[choice_key][user_input][1])
					self.encounter(choice_key)
		else:
			prRed("Command not recognized.  Please type 'h' for help.")

	def get_locations_dict(self):
		return self.locations

	def check_location_existence(self, coords):
		""" Check for the existence of a Location object and create it if it doesn't exist yet.  This is called when moving to a different location on the Realm """
		name = self.get_location_name(coords)

		if name in self.get_locations_dict():
			return True
		else:
			return False

	def get_location_name(self, coords):
		""" takes Location coordinates as input, returning a string name for a Location """
		name = str(coords[0]) + str(coords[1])
		return name

	def get_location(self, current_location_coords):
		""" attempts to return an object with a name based on the current location coordinates if the object name doesn't exist, throws NameError exception """
		try:
			string = self.get_location_name(current_location_coords)
			# return self.locations[string]
			return self.get_locations_dict()[string]
		except NameError:
			print("Location does not exist.")

	def move(self, char, direction):
		""" taking character instance and user input direction as parameters, handles player movement between Locations """
		# pair all options with an action in a dictionary
  		# TODO: replace with imported movement module, a la
		# "n": [0, 1], "s": [-1, 0], etc.
		directions = { "n": [char.get_coord(0),(char.get_coord(1)+1)],
					   "s": [char.get_coord(0),(char.get_coord(1)-1)],
					   "e": [(char.get_coord(0)+1),char.get_coord(1)],
					   "w": [(char.get_coord(0)-1), char.get_coord(1)] }

		# execute directional movement by updating player's coords
		if direction in directions:
			char.set_move_dir(direction)
			char.set_coords(directions[direction])
			coords = char.get_coords()
		# check for the existence of the Location to which the player has moved 
		if self.check_location_existence(coords):
			self.get_location(coords)
		else:
			self.add_location(coords)
		self.narrative(self.player.get_coords())

	def invert_dir(self, dir):
		""" invert a direction, i.e., n --> s, e --> w """
		inversions = {
						'n': 's',
                		's': 'n',
                  		'e': 'w',
                    	'w': 'e' }

		if dir in inversions:
			return inversions[dir]

	def move_back(self, char):
		""" move player back to the location they came from
  			This is intended to handle under-construction areas """
		last_move_dir = self.player.get_move_dir()

		# pair all options with an action in a dictionary
		directions = { "n": [char.get_coord(0),(char.get_coord(1)+1)],
					   "s": [char.get_coord(0),(char.get_coord(1)-1)],
					   "e": [(char.get_coord(0)+1),char.get_coord(1)],
					   "w": [(char.get_coord(0)-1), char.get_coord(1)] }

		# execute directional movement by updating player's coords
		move_dir = self.invert_dir(last_move_dir)

		if move_dir in directions:
			self.player.set_move_dir(move_dir)
			self.player.set_coords(directions[move_dir])
			coords = self.player.get_coords()
		# check for the existence of the Location to which the player has moved
		if self.check_location_existence(coords):
			self.get_location(coords)
		else:
			self.add_location(coords)
		self.narrative(self.player.get_coords())

	def help_menu(self):
		prBlue("\nHelp:\nn move north\ns move south\ne move east\nw move west\nx search \ni check your inventory\na attributes\nq quit\nh help\n")

	def inv_list(self):
		""" Lists all the items in the player's inventory
		"""
		print("\nInventory: \n")
		prGreen(self.player.get_inventory())

	def inv_add(self, item):
		""" Adds an item to the player's inventory, asking if they wish to drop an item if the inventory is full. """
		if self.player.add_to_inventory(item):
			prGreen("\n %s added to inventory." % (item))
		else:
			print("Inventory full.  Drop an item? (y/n)")
			choice = input(self.PROMPT)
			if choice in {'y', 'yes', 'Y', 'Yes', 'YES'}:
				self.inv_prmpt_remove()
				self.inv_add(item)
			else:
				print("Dropped %s on the ground." % (item))

	def inv_prmpt_remove(self):
		""" Prompts player to pick an item to remove from the inventory	"""
		print("\nWhich item do you wish to remove?\n")
		prGreen(self.player.inventory)
		print("\n")

		choice = input(self.PROMPT)

		if choice in self.player.get_inventory():
			self.inv_remove(choice)
			prGreen("%s dropped on the ground." % (choice))
		else:
			print("Item: %s not found.  Please type the name of the item you wish to remove." % (choice))
			choice = input(self.PROMPT)
		return

	def inv_remove(self, item):
		""" Removes an item from the player's inventory (and adds it to the location).  Called from inv_prmpt_remove() function """
		## TO-DO: pop item instead, adding it to the list of items in the current Location object
		inventory = self.player.get_inventory()
		dropped_item = inventory.pop(inventory.index(item))
		self.current_player_location.add_loot(dropped_item)

	def search_area(self):
		""" Searches area upon player pressing 'x' to find and collect loot.  You really should try the goat's milk. """
		# cast list representing player's x/y coordinates as a tuple for comparison to LOOT_LIST dictionary's keys
		coords = tuple(self.player.get_coords())
		loot_present = self.current_player_location.get_loot_present()
		removal_list = []

		if loot_present:	# if loot is present in the area
			if coords in loc_mgr.LOOT_LIST:  # if the area has items contained in the loot list
				# copy_of_LOOT_LIST = self.LOOT_LIST[coords]
				for i in range(1, len(loc_mgr.LOOT_LIST[coords])):
					self.inv_add(loc_mgr.LOOT_LIST[coords][i])	# execute the command(s) contained in the second element of the value list, adding said items to player's inventory
					removal_list.append(loc_mgr.LOOT_LIST[coords][i])
				self.current_player_location.remove_loot(removal_list)  # removes item from the location
					
		else:
			prYellow("You found nothing useful here.")

	def die(self):
		"""	this function ends the program """
		message = prRed("\nGame Over.\n")
		sys.exit(message)

	def quit_game(self):
		prRed("Are you sure you want to exit? (y/n)")
		choice = input(self.PROMPT)

		if choice.lower() in {'y', 'Y', 'yes', 'Yes', 'YES'}:
			self.die()
		elif choice.lower() in {'n', 'no'}:
			print("Let's get back to it then.")

	def keydown(self, user_input):
		""" Handles user input """
		
		# dictionary of possible user inputs with matching names of methods to call for each
		inputs = {"n": self.move, 
	  	  		  "s": self.move,
	  	  		  "e": self.move,
	      		  "w": self.move,
	      		  "h": self.help_menu,	  	  		
	  	  		  "i": self.inv_list,
	  	  		  "a": self.player.attrib_list,
	  	  		  "x": self.search_area,
	  	  		  "q": self.quit_game}
		
		if user_input in inputs:
			if user_input in ["n", "s", "e", "w"]:
				inputs[user_input](self.player, user_input)  # call the function that matches the key pressed by the user, passing the parameter if it is a direction of travel
			else:  # otherwise don't pass a parameter
				inputs[user_input]()
		else:
			prRed("Command not recognized.  Please type 'h' for help.")
		self.narrative(self.player.get_coords())
