"""
Character is a class which stores information pertaining to the player.  It's imported by Realm.py and it deals with player attributes, inventory and coordinates. 
"""
import movement
import loc_mgr

class Character(object):
	""" Represents the player with methods for inventory management, searching areas, generating narrative, moving and dying. """

	def __init__(self, sex, name, hp, stam, mp, gld, inv, coords, move_dir):
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
		self.move_dir = move_dir

	def __str__(self):
		return "\nPlayer attributes for " + str(self._name) + ":\nsex: \t\t" + str(self._sex) + "\nhit points: \t" + str(self.hp) + "\nstamina: \t" + str(self.stamina) + "\nmagic points: \t" + str(self.mp) + "\ngold: \t\t" + str(self.gold) + "\ninventory items: \n" + str(self.inventory) + "\nNew player? " + str(self.newplayer) + "\nInventory size: " + str(self._max_inv_size) + "\nLocation: " + str(self.get_coords())

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

	def set_move_dir(self, move_dir):
		""" sets the player's direction of most recent movement
            possible values are n, s, e or w """
		self.move_dir = move_dir

	def get_move_dir(self):
		""" returns the player's direction of most recent movement """
		return self.move_dir

	def attrib_list(self):
		print(self)

	def get_inventory(self):
		return self.inventory

	def add_to_inventory(self, item):
		""" adds an item to player's inventory if inventory isn't yet full; otherwise returns a boolean indicating success (True) or failure (False) """
		if len(self.inventory) < self._max_inv_size:
			self.get_inventory().append(item)
			return True
		else:
			return False

	def teleport(self, coords):
		""" move character to the specified coordinates. """
		self.coords = coords