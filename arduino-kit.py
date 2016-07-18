"""Usage:
	arduino-kit.py <required_kits> [--filter]
"""
import sys
import docopt
import unittest
import io
import pprint

from collections import namedtuple
from collections import Counter

# Per-kit numbers of things:

PARTIAL_KIT_CONTENTS = {
	"Base" : 1,
	"Wires": 1,
	"Standoffs (x3)" : 1,
	"M3 machine screws (x6)" : 1,
	"Rubber feet (x4)" : 1,
	"DC motor" : 1,
	"LED" : 3,
	"RGB LED" : 1,
	"LDR" : 1,
	"MOSFET" : 3,
	"Resistor pack" : 1,
	"Potentiometer" : 1,
	"Diodes" : 3,
	"Capacitors" : 3,
	"Switches" : 2,
	"Flatpack box" : 1
}

KIT_CONTENTS = {
	"Arduino" : 1,
	"Breadboard" : 1,
	"Base" : 1,
	"Wires": 1,
	"Standoffs (x3)" : 1,
	"M3 machine screws (x6)" : 1,
	"Rubber feet (x4)" : 1,
	"DC motor" : 1,
	"LED" : 3,
	"RGB LED" : 1,
	"LDR" : 1,
	"MOSFET" : 3,
	"Resistor pack" : 1,
	"Potentiometer" : 1,
	"Diodes" : 3,
	"Capacitors" : 3,
	"Switches" : 2,
	"USB Cable" : 1,
	"Flatpack box" : 1
}

StockItem = namedtuple("StockItem", ["name", "qty"])

def get_required_stock(required_kits, contents):
	return {k : v * required_kits for (k, v) in contents.items()}

def stock_item(l):
	try:
		parts = l.strip().split(" ")
		qty = int(parts[-1])
		name = ' '.join(parts[0:-1])
		return StockItem(name, qty)
	except:
		return None

def subtract_stock_lists(required, current):
	return {k:max(v - current.get(k, 0), 0) for k, v in required.items()}

def nice_format(stock, filter_zero_items=False):

	if filter_zero_items:
		stock = {k:v for k, v in stock.items() if v > 0}
	
	stock = ["{}: {}".format(k, v) for k, v in stock.items()]
	
	return '\n'.join(sorted(stock))

def merge_partial_kits(current_stock, partial_kit_contents):
	try:
		partial_kit_count = current_stock.pop('Partial Kits')
	except KeyError:
		return current_stock
		
	new_stock = Counter(current_stock)
	for _ in range(partial_kit_count):
		new_stock += Counter(partial_kit_contents)

	return dict(new_stock)

def get_current_stock_from_stream(stream):
	return dict([s for s in map(stock_item, stream) if s])
	
if __name__ == "__main__":

	args = docopt.docopt(__doc__)
	required_kits = int(args["<required_kits>"])

	current_stock = get_current_stock_from_stream(sys.stdin)

	current_stock = merge_partial_kits(current_stock, PARTIAL_KIT_CONTENTS)

	required_stock = get_required_stock(required_kits, KIT_CONTENTS)

	to_buy_stock = subtract_stock_lists(required_stock, current_stock)

	print(nice_format(to_buy_stock, args["--filter"]))

class ArduinoKitTestCases(unittest.TestCase):

	TEST_KIT_CONTENTS = {
		"Thing A" : 4,
		"Thing B" : 10,
		"Thing C" : 1
	}

	TEST_STOCK_LIST = """
	Partial Kits 9
	Thing A 1
	Thing B 2
	Thing C 3
	"""

	PARTIAL_KIT_CONTENTS = {
		"Thing B" : 2,
		"Thing C" : 3
	}

	def get_expected_stock(self):
		EXPECTED_STOCK_DICT = {
			"Partial Kits" : 9,
			"Thing A" : 1,
			"Thing B" : 2,
			"Thing C" : 3
		}

		return EXPECTED_STOCK_DICT.copy()

	def test_stock_item_parses_stock_entry_correctly(self):

		actual = stock_item("Arduino 3")
		expected = StockItem("Arduino", 3)

		self.assertEqual(expected, actual)

	def test_get_current_stock_from_stream(self):

		actual = get_current_stock_from_stream(io.StringIO(self.TEST_STOCK_LIST))

		self.assertEqual(self.get_expected_stock(), actual)
	
	def test_partial_kit_addition(self):
		
		stock = merge_partial_kits(self.get_expected_stock(), self.PARTIAL_KIT_CONTENTS)

		expected = self.get_expected_stock()
		expected["Thing B"] += 9 * self.PARTIAL_KIT_CONTENTS["Thing B"]
		expected["Thing C"] += 9 * self.PARTIAL_KIT_CONTENTS["Thing C"]
		expected.pop("Partial Kits")

		self.assertEqual(expected, stock)

	def test_subtract_stock_lists(self):
		self.maxDiff = None

		stock = merge_partial_kits(self.get_expected_stock(), self.PARTIAL_KIT_CONTENTS)
		required_stock = get_required_stock(15, self.TEST_KIT_CONTENTS)

		to_buy = subtract_stock_lists(required_stock, stock)

		expected = {
			"Thing A" : max(15 * self.TEST_KIT_CONTENTS["Thing A"] - stock['Thing A'], 0),
			"Thing B" : max(15 * self.TEST_KIT_CONTENTS["Thing B"] - stock['Thing B'], 0),
			"Thing C" : max(15 * self.TEST_KIT_CONTENTS["Thing C"] - stock['Thing C'], 0)
		}

		self.assertEqual(expected, to_buy)