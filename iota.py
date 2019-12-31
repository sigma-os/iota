import xml.etree.ElementTree as ElementTree
import generators.cpp
import sys
import argparse

iota_version = '0.0.1'
iota_nodes = []

class iota_message_field:
	def __init__(self, name, type, index):
		self.name = name
		self.type = type
		self.index = index
	
	name = ''
	type = ''
	index = 0

class iota_enum_entry:
	def __init__(self, name, value, index):
		self.name = name
		self.value = value
		self.index = index

	name = ''
	value = 0
	index = 0

class iota_node:
	def __init__(self, name, type):
		self.name = name
		self.items = []
		self.type = type

	name = ''
	type = ''
	item_type = ''
	items = []

def main():
	parser = argparse.ArgumentParser(description='Generate iota files')
	parser.add_argument('input', help="Select file to generate")
	parser.add_argument('-g', '--generator', help='Select code generator to use', required=True)
	parser.add_argument('-s', '--subgenerator', help='Select sub code generator to use', required=True)
	parser.add_argument('-o', metavar='OUTPUT', help='Select output file', required=True)
	args = parser.parse_args()

	xmldoc = ElementTree.parse(args.input)
	
	root = xmldoc.getroot()

	if not root.attrib['version']:
		print('No version detected in <iota> statement')
		exit()

	print(f"IDL version: {root.attrib['version']}")
	print(f"IDL module: {root.attrib['module']}")

	for child in root:
		if child.tag == 'message':
			parse_message(child)
		elif child.tag == 'enum':
			parse_enum(child)
		else:
			print(f"Unknown tag {child.tag}, ignoring...")

	
	print("Parsing done!")

	if args.generator == 'cpp':
		generators.cpp.generate(args.subgenerator, args.o, iota_nodes, root.attrib['module'])
	else:
		print(f"Unknown generator: {args.generator}")
		exit()

def parse_enum(xml_enum):
	enum = iota_node(xml_enum.attrib['name'], 'enum')
	enum.item_type = xml_enum.attrib['type']

	print(f"IDL Enum: {xml_enum.attrib['name']}, type: {enum.item_type}")

	i = 0
	for child in xml_enum:
		assert child.tag == 'entry'

		entry_name = child.text
		entry_value = child.attrib['value']

		print(f"    Entry: name: {entry_name}, value: {entry_value}")

		enum.items.append(iota_enum_entry(entry_name, entry_value, i))
		i += 1

	iota_nodes.append(enum)

def parse_message(xml_message):
	message = iota_node(xml_message.attrib['name'], 'message')

	print(f"IDL Message: {xml_message.attrib['name']}")

	i = 0
	for child in xml_message:
		assert child.tag == 'field'

		field_name = child.text
		field_type = child.attrib['type']

		print(f"    Field: Type: {field_type}, Name: {field_name}, index: {i}")
		
		message.items.append(iota_message_field(field_name, field_type, i))
		i += 1

	iota_nodes.append(message)


main()