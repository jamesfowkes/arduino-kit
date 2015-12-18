import sys
import argparse

from collections import namedtuple

# Per-kit numbers of things:
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
	"USB Cable" : 1
}

StockItem = namedtuple("StockItem", ["name", "qty"])

def get_required_stock(required_kits, contents):
	return {k : v * required_kits for (k, v) in contents.items()}

def stock_item(l):
	try:
		parts = l.split(" ")
		qty = int(parts[-1])
		name = ' '.join(parts[0:-1])
		return StockItem(name, qty)
	except:
		return None

def subtract_stock(required, current):

	to_buy = {}

	for k, v in required.items():
		to_buy[k] = max(v - current.get(k, 0), 0)

	return to_buy

def nice_format(stock):

	return '\n'.join(sorted(["{}: {}".format(k, v) for k, v in stock.items()]))

if __name__ == "__main__":

	current_stock = dict([s for s in map(stock_item, sys.stdin) if s])

	required_kits = int(sys.argv[1])

	required_stock = get_required_stock(required_kits, KIT_CONTENTS)

	to_buy_stock = subtract_stock(required_stock, current_stock)

	print(nice_format(to_buy_stock))
