""" loc_mgr.py serves as a static set of functions related to location management and is imported by
    both realm and character to manage player movement among locations """
# define a dictionary which contains a tuple representing each Realm location's coordinates, paired with a list containing (1) a print statement description of the area and (2+) any accompanying commands required to add items to the player's inventory
# TODO: convert this to either a separate file or place text into a database for lookup
LOOT_LIST = {(0,0): ["After searching the area you find a bit of rope useful for tinder and a strangely-chilled glass of goat's milk.", "tinder", "tinder", "goat milk", "goat milk"],
                (0,1): ["Upon looking around the ruins, you find very little of use, all having been picked clean long ago by scavengers.  You did however manage to find a bit of flint near an old campfire.", "flint"],
                (0,2): ["You stumble upon a rusty blade.", "rusty blade"],
                (-1,0): ["While searching the area, you begin to rifle through the pockets of the two bodies.  On the first, you find a notebook.  The second appears to still be alive so you don't approach him just yet.", "notebook"]
            }

# TODO:  Add further items to MONSTER_LIST, including loot drops (randomized tiers of loot item lists) and NPC level (somewhat randomized also from tiers of NPC level lists)
# TODO: also convert this data into either a separate file or a database
MONSTER_LIST = {(0,0): ['spider'],
                (0,1): ['spider', 'spider'],
                (0,2): ['spider'],
                (-1,0): ['bandit']
                }

def get_master_loot_list():
    return LOOT_LIST

def get_master_monster_list():
    return MONSTER_LIST



