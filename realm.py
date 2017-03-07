# imports
##
import character
from location import Location


# classes
## 			 
class Realm(object):
	""" creates, stores and retrieves locations; presents narratives for each """
	
	# class variables
	##
	# define a dictionary which contains a tuple representing each Realm location's coordinates, paired with a list containing (1) a print statement description of the area and (2+) any accompanying commands required to add items to the player's inventory
	LOOT_LIST = {(0,0): ["After searching the area you find a bit of rope useful for tinder and a strangely-chilled glass of goat's milk.", "tinder", "goat milk"],
			 	 (0,1): ["Upon looking around the ruins, you find very little of use, all having been picked clean long ago by scavengers.  You did however manage to find a bit of flint near an old campfire.", "flint"], 
			 	 (0,2): ["You stumble upon a rusty blade.", "rusty blade"],
			 	 (-1,0): ["While searching the area, you begin to rifle through the pockets of the two bodies.  On the first, you find a notebook.  The second appears to still be alive so you don't approach him just yet.", "notebook"]
			 	}

	# TO_DO:  Add further items to these monster lists, including loot drops (randomized tiers of loot item lists) and NPC level (somewhat randomized also from tiers of NPC level lists)
	MONSTER_LIST = {(0,0): ['spider'],
				 	(0,1): ['spider', 'spider'],
					(0,2): ['spider'],
			   		(-1,0): ['bandit']
				   }

	#defines the input prompt
	PROMPT = '=---> '

	# methods
	##
	def __init__(self):
		self.locations = {}								# dictionary containing instances of Location class representing each traversible area of the Realm
		starting_coords = [0,0]
		self.add_location(starting_coords)
		self.player = self.create_Char()				# create player instance of character class
		self.narrative(self.player.get_coords())		# this line starts the loop which gets user input for interacting with the environment

		# coords = self.player.get_coords()
		# exists = self.check_location_existence(coords)
		# print exists
# 
		# if exists:
			# self.location = rmgr.get_location(self.coords)
		# else:
			# realm.add_location(self.coords)
			# self.location = rmgr.get_location(self.coords)
		

	def create_Char(self):
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
		return character.Character("male", "Drizzt", 10, 5, 3, 0, [], [0,0])

	def get_master_loot_list():
		return self.loot_list

	def get__master_monster_list():
		return self.monster_list

	def get_name(self, coords):
		""" takes Location coordinates as input, returning a string name for a Location """
		name = str(coords[0]) + str(coords[1])
		return name

	def add_location(self, coords):
		""" adds a location to the Realm """
		# check for existence of loot entry in dictionary before assigning loot listed there to this instance's loot list
		location_name = self.get_name(coords)

		if location_name in self.LOOT_LIST:
			loot = self.LOOT_LIST[location_name]
			self.loot_present = True
		else:
			loot = []
			loot_present = False

		if location_name in self.MONSTER_LIST:
			monsters = self.get__master_monster_list()[self.name]
			monsters_present = True
		else:
			monsters = []
			monsters_present = False
		
		new_location = Location(coords, monsters_present, loot_present, monsters, loot)
		self.locations[new_location.name] = new_location
		self.current_player_location = self.locations[new_location.name]

	def get_locations_dict(self):
		return self.locations

	def check_location_existence(self, coords):
		""" Check for the existence of a Location object and create it if it doesn't exist yet.  This is called when moving to a different location on the Realm """
		name = self.get_name(coords)

		if name in self.get_locations_dict():
			return True
		else:
			return False

	def get_location(self, current_location_coords):
		""" attempts to return an object with a name based on the current location coordinates 	if the object name doesn't exist, throws NameError exception """
		try:
			string = self.get_name(current_location_coords)
			return self.locations[string]
		except NameError:
			print "Location does not exist."

	def teleport(self, coords):
		self.player.set_coords(coords)
		self.narrative(self.player.get_coords())

	def narrative(self, area):
		""" Handles delivery of narrative text based on location as well as any choices available in any given location """
		global narratives

		key = tuple(area)

		narratives = {(0,0): ["\n     You are standing in the same field in which you first awoke\nwithout any memory of how you got here.  Which way?\n"],
					  (-1,0): ["\nAs you proceed west, you come upon signs of a battle, \nincluding two bodies lying face-down at the edge of a wood\n near the field in which you awoke.  There are no signs of\n life.  Do you approach the bodies? (y/n)", self.encounter],
					  (0,1): ["\n     You walk for some time to finally arrive at an old, \napparently abandoned fortress which has crumbled with time.  \nThere is nothing here but ruin.  As you approach an outcrop of rock, you realize there is a narrow passage leading down into the ground, perhaps an old cellar entrance.  Do you enter? (y/n)", self.encounter],
					  (0,2): ["\n     As you head north around the abandoned and crumbling\nfortress you see a valley spread out before you.  In the\ndistance to the north is a village with wafts of smoke being\ncarried off by the breeze trailing over the scene like\nthe twisted tails of many kites.  To the west gently\nsloping foothills transition into distant blue mountains\nand to the east, a vast forest conspires to block out all \nsurface detail."]}

		if self.player.newplayer == True:
			print "\n     You awaken to the distant sound of commotion to your west.  \nYou open your eyes and realize you are in a vulnerable spot\n in an open field.  You look west toward the direction of\n the distant sounds and hear that it is now quiet.  To your \nnorth in the distance is a fortress.  To your east is a \nforest and to your south is a riverbank with \aa boat tied at a pier.  \n\nWhich direction do you go? (Press 'h' for help)"
			self.player.newplayer = False

		elif key in narratives:
			if len(narratives[key]) > 1:  # if there are commands associated with this area, execute them
				for i in range(1,len(narratives[key])):
					temp_list = area[:]
					temp_list.append(i)
					choice_key = tuple(temp_list)
					narratives[key][i](choice_key)

 		else:
			prRed("Under construction.  Returning to the beginning.")
			self.teleport([0,0])
	
		# get user input
		user_input = raw_input(self.PROMPT)
		# get rid of any capitalized typing by the user
		user_input.lower()

		# call keydown method of player instance of Character class to handle user input
		self.keydown(user_input)

	def next_choice(self, choice_key):
		""" increments choice_key's 3rd number to proceed a deeper level in the branching choices for any location """
		# cast choice_key back as a list so that it can be modified.  I'm pretty sure others would frown on this approach but it works and I have no idea of how else to create this functionality
		choice_key = list(choice_key)
		choice_key[2] += 1
		self.encounter(choice_key)

	def encounter(self, choice_key):
		# a third number has been added to the tuple key to represent level of depth (decision/choice 1: outcome, decision/choice 2/outcome, etc.)  The Value of each of these keys goes in the form:  ['user-input choice', print narrative, command(s) to execute]
		
		# prompt user for input in respose to encounter
		input = raw_input(self.PROMPT).lower()

		# cast choice_key as a tuple so it can be used as a dictionary key
		choice_key = tuple(choice_key)

		outcomes = { (-1,0,1): 
								{'y': ["\nAs you approach one of the bodies closely, you realize\n that he is feigning death when he rolls quickly and \nsinks a blade into your neck.  Your life fades slowly.", self.player.die], 'n': ["\nWell, daylight's a-wasting.  Where to now?"]}, 
					 (0,1,1):
					 			{'y': ["\nYou steal yourself and proceed down the cracked and disintegrating steps only to find a locked wooden door.  Do you attempt to force the lock? (y/n)", self.next_choice], 'n': ["\nWhere to now?"]},
					 (0,1,2):   {'y': ["\nYou put all your force into it as you drive your shoulder into the door.  It gives way in a sudden explosion of splinters, dust and debris.  It's too dark to proceed safely without a lantern."], 'n': ["\nWhere to now?"]} }
		if choice_key in outcomes:
			if len(outcomes[choice_key][input]) > 1:
				for i in range (1,len(outcomes[choice_key][input])):
					if outcomes[choice_key][input][i] == self.next_choice:
						self.next_choice(choice_key)
					else:
						outcomes[choice_key][input][i]()
		else:
			# for k in outcomes[choice_key]:
				# print "Please type "
				# for i in outcomes[choice_key]:
					# print "",outcomes[choice_key].key()
			print "Please type 'h' for help."

	def move(self, char, direction):
		""" taking character instance and user input direction as parameters, handles player movement between Locations """
		# pair all options with an action in a dictionary
		directions = { "n": [char.get_coord(0),(char.get_coord(1)+1)], "s": [char.get_coord(0),(char.get_coord(1)-1)], "e": [(char.get_coord(0)+1),char.get_coord(1)], "w": [(char.get_coord(0)-1), char.get_coord(1)] }
		# execute directional movement by updating player's coords
		if direction in directions:
			char.set_coords(directions[direction])
		# check for the existence of the Location to which the player has moved 
		self.check_location_existence(char.get_coords())

	def keydown(self, user_input):
		""" Handles user input """

		# dictionary of possible user inputs with matching names of methods to call for each
		inputs = {"n": self.move, "s": self.move, "e": self.move, "w": self.move, "q": self.player.quit_game, "h": self.player.help_menu, "i": self.player.inv_list, "a": self.player.attrib_list, "x": self.player.search_area, "t": self.player.check_time}		

		if user_input in inputs:
			if user_input in ["n", "s", "e", "w"]:
				inputs[user_input](self.player, user_input)  # call the function that matches the key pressed by the user, passing the parameter if it is a direction of travel
			else:  # otherwise don't pass a parameter
				inputs[user_input]()
		if user_input not in inputs:
			print "Please type 'h' for help."
		self.narrative(self.player.get_coords())
