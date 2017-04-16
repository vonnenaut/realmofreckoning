import random

class Character(object):
    """ Represents the player with methods for inventory management, searching areas, generating narrative, moving and dying. 
		details is a list of items:  sex, name, hp, ap, mp, gld, inv; inv is itself a list.
    """

    def __init__(self, details, coords):
        self._sex = details[0]
        self._name = details[1]
        self.hp = details[2]
        self.ap = details[3]
        self.mp = details[4]
        self.gold = details[5]
        self.inventory = details[6]
        self.newplayer = True
        self._max_inv_size = 5
        self.coords = [0, 0]

    def __str__(self):
        return "\nPlayer attributes for " + str(self._name) + ":\nsex: " + str(self._sex) + "\nhit points: " + str(self.hp) + "\naction points: " + str(self.ap) + "\nmagic points: " + str(self.mp) + "\ngold: " + str(self.gold) + "\ninventory items: " + str(self.inventory) + "\nNew player? " + str(self.newplayer) + "\nMax # inventory items: " + str(self._max_inv_size) + "\nLocation: " + str(self.get_coords())

    def get_name(self):
    	""" returns character's name """
    	return self._name

    def get_hp(self):
    	""" returns character's current hit points """
    	return self.hp

    def set_hp(self, amount):
    	""" modifies character's current hit points by amount.  Use negative number to subtract, positive to add. """
    	self.hp = self.get_hp() + amount
    	if self.hp <= 0:
    		self.die()

    def get_mp(self):
    	""" returns character's current magic points """
    	return self.mp

    def set_mp(self, amount):
        """ modifies character's current magic points by amount.  Use negative number to subtract, positive to add. """
        self.mp = self.get_mp() + amount

    def get_ap(self):
    	""" returns character's current action points """
    	return self.ap

    def set_ap(self, amount):
    	""" modifies character's current action points by amount.  Use negative number to subtract, positive to add. """
    	self.ap = self.get_ap() + amount

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

    def attrib_list(self):
        print self

    def get_inventory(self):
        return self.inventory

    def add_to_inventory(self, item):
        """ adds an item to player's inventory if inventory isn't yet full; otherwise returns a boolean indicating success (True) or failure (False) """
        if len(self.inventory) < self._max_inv_size:
            self.get_inventory().append(item)
            return True
        else:
            return False

    def attack(self, target):
    	""" character attacks target returning true if hit, false if miss """
    	roll = random.randrange(1,7)
    	amount = 0
    	if roll > 3:
    		hit = True
    		amount = -1  # TO-DO:  modify this to account for weapon and stats
    	else:
    		hit = False
    	return [hit, amount]

    def die(self):
    	""" kills character """
    	print "%s has been killed." % self.get_name()

    def teleport(self, coords):
        """ move character to the specified coordinates.  NOTE:  need to update associated location in Realm module (to avoid circular imports) """
        self.coords = coords
