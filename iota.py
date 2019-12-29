import xml.etree.ElementTree as ElementTree
import generators.cpp
import sys
import argparse

iota_version = '0.0.1'
iota_messages = []

class iota_field:
	def __init__(self, name, type_, index):
		self.name = name
		self.type_ = type_
		self.index = index
	
	name = ''
	type_ = ''
	index = 0

class iota_message:
	def __init__(self, name, type_):
		self.name = name
		self.type_ = type_;
		self.fields = []

	name = ''
	type_ = ''
	fields = []

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
		else:
			print(f"Unknown tag {child.tag}, ignoring...")

	
	print("Parsing done!")

	if args.generator == 'cpp':
		generators.cpp.generate(args.subgenerator, args.o, iota_messages, root.attrib['module'])
	else:
		print(f"Unknown generator: {args.generator}")
		exit()



def parse_message(xml_message):
	message_type = xml_message.get('type', 'binary') # Assume default binary representation by default
	message = iota_message(xml_message.attrib['name'], message_type)

	print(f"IDL Message, name: {xml_message.attrib['name']}, type: {message_type}")

	i = 0
	for child in xml_message:
		assert child.tag == 'field'

		field_name = child.text
		field_type = child.attrib['type']

		print(f"    Field: Type: {field_type}, Name: {field_name}, index: {i}")
		
		message.fields.append(iota_field(field_name, field_type, i))
		i += 1

	iota_messages.append(message)


main()