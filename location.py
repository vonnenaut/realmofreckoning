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
		self.monsters = monsters
		self.loot = loot	
		current_location = self

	def __str__(self):
		return "Current player location " + str(self.name) + " is at " + str(self.coords) + ", monsters present? " + str(self.monsters_present) + "\nMonster list: " + str(self.monster_list) + "\nLoot present? " + str(self.loot_present)

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
