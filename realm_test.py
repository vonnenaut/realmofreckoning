# imports
##
import realm, sys, vtemu, TestSuite
from location import Location
from character import Character


def realm_test():
	""" Testing apparatus for realm of reckoning """
	suite = TestSuite.TestSuite()
	print("\n-----Testing Character-----")
	test_char = Character('male', 'Rick', 10, 5, 5, 0, [], [0,0], '')
	print("character:", test_char)
	print("\nTesting set_coords get_coords and get_coord...")
	suite.run_test(test_char.get_coords(), [0,0], "Test 1:")
	test_char.set_coords([1,1])
	suite.run_test(test_char.get_coords(), [1,1], "Test 2:")
	test_char.set_coords([5,3])
	suite.run_test(test_char.get_coord(0), 5, "Test 3:")
	test_char.set_coords([1,2])
	suite.run_test(test_char.get_coord(1), 2, "Test 4:")
	print("\nTesting attrib_list (check visually)...")
	suite.run_test(test_char.attrib_list(), None, "Test 5:")
	print("\nTesting add_to_inventory and get_inventory (check visually)...")
	print("Adding 'flint' and 'eggs' to inventory ...")
	suite.run_test(test_char.add_to_inventory('flint'), True, "Test 6:")
	suite.run_test(test_char.add_to_inventory('eggs'), True, "Test 7:")
	suite.run_test(test_char.get_inventory(), ['flint', 'eggs'], "Test 8:")
	
	print("\n")
	suite.report_results()

realm_test()
