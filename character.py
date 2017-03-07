# imports
##
import sys, vtemu


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


# classes
##
class Character(object):
	""" Represents the player with methods for inventory management, searching areas, generating narrative, moving and dying. """
	global current_location

	def __init__(self, sex, name, hp, stam, mp, gld, inv, coords):
		self._sex = sex
		self._name = name
		self.hp = hp
		self.stamina = stam
		self.mp = mp
		self.gold = gld
		self.inventory =  inv
		self.newplayer = True
		self._max_inv_size = 5
		self.coords = [0,0]

	def __str__(self):
		return "\nPlayer attributes for " + str(self._name) + ":\nsex: " + str(self._sex) + "\nhit points: " + str(self.hp) + "\nstamina: " + str(self.stamina) + "\nmagic points: " + str(self.mp) + "\ngold: " + str(self.gold) + "\ninventory items: " + str(self.inventory) + "\nNew player? " + str(self.newplayer) + "\nMax # inventory items: " + str(self._max_inv_size) + "\nLocation: " + str(self.get_coords())

	def set_coords(self, coords):
		""" sets the player's coordinates in the Realm """
		self.coords[0] = coords[0]
		self.coords[1] = coords[1]

	def get_coord(self, element):
		""" returns the player's specified coordinate, x or y, in the Realm """
		return self.coords[element]

	def get_coords(self):
		""" returns the player's coordinates, (x, y) in the Realm """
		return self.coords

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
		print self

	def search_area(self):
		""" Searches area upon player pressing 'x' to find and collect loot.  You really should try the goat's milk. """
		# cast list representing player's x/y coordinates as a tuple for comparison to loot_list dictionary's keys
		area = tuple(self.get_coords())

		lp = current_location.loot_present

		# define a dictionary which contains a tuple representing each Realm location's coordinates, paired with a list containing (1) a print statement description of the area and (2+) any accompanying commands required to add items to the player's inventory
		# loot_list = {(0,0): ["After searching the area you find a bit of rope useful for tinder and a strangely-chilled glass of goat's milk.", "tinder", "goat milk"],
					 # (0,1): ["Upon looking around the ruins, you find very little of use, all having been picked clean long ago by scavengers.  You did however manage to find a bit of flint near an old campfire.", "flint"], 
					 # (0,2): ["You stumble upon a rusty blade.", "rusty blade"],
					 # (-1,0): ["While searching the area, you begin to rifle through the pockets of the two bodies.  On the first, you find a notebook.  The second appears to still be alive so you don't approach him just yet.", "notebook"]}

		if lp is True:	# if loot is present in the area
			if area in loot_list:  # if the area has items contained in the loot list (redundant)
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

	def die(self):
		"""	this function ends the program """
		message = prRed("\nGame Over.\n")
		sys.exit(message)
