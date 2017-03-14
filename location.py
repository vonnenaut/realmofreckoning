class Location(object):
	""" This class defines all of the attributes to be stored for each location object
		initializes attributes for:
		location 			point containing x and y coordinates
		name 				used to create the key for the dictionary storing each object
		monsters_present 	tracks whether monsters are in the present location
		loot_present 		keeps track of whether loot is in the present location 
							(either having been dropped or spawned initially) """	
	def __init__(self, current_location_coords, monsters_present, loot_present, monsters, loot):
		self.coords = current_location_coords
		self.x = current_location_coords[0]
		self.y = current_location_coords[1]		
		self.name = str(self.x) + str(self.y)
		self.monsters_present = monsters_present
		self.loot_present = loot_present
		self.monsters = monsters
		self.loot = loot

	def __str__(self):
		return "Location " + str(self.name) + " is at " + str(self.coords) + ", monsters present? " + str(self.monsters_present) + "\nMonster list: " + str(self.monsters) + "\nLoot present? " + str(self.loot_present) + "\nLoot list: " + str(self.loot)

	def get_coords(self):
		""" returns a list coordinate pair denoting location's position in  """
		return [self.x, self.y]

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y
	
	def get_name(self):
		"""
			Return a unique string made up of the x and y coordinates to be used for naming each Location object as it is created and for retrieval from the dictionary of Location objects.
		"""
		return str(self.x) + str(self.y)

	def get_loot_present(self):
		""" returns the value of the boolean 'loot_present' """
		return self.loot_present

	def set_loot_present(self, boolean):
		""" sets the boolean 'loot_present' to True or False """
		self.loot_present = boolean

	def get_monsters_present(self):
		""" returns the value of the boolean 'monsters_present' """
		return self.monsters_present

	def set_monsters_present(self, boolean):
		""" sets the boolean 'monsters_present' to True or False """
		if boolean is True or False:
			self.monsters_present = boolean
		else:
			print "Invalid parameter given to set_monsters_present: ", boolean

	def get_monsters(self):
		""" returns a list of all monsters present at this location """
		return self.monsters

	def get_loot(self):
		""" returns a list of all loot present at this location """
		return self.loot

	def remove_loot(self, loot):
		""" removes loot from location, testing for keyword 'all' which takes all loot from location if player has enough inventory space """
		loot_to_player = loot
		location_loot = self.get_loot()

		for item in loot:
			location_loot.remove(item)

		if len(location_loot) <= 1:
			self.set_loot_present(False)
		return loot_to_player

	def add_loot(self, loot):
		""" adds loot to location in case where player drops loot or player or monster dies, dropping loot """
		self.get_loot().append(loot)
