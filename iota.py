import xml.etree.ElementTree as ElementTree
import generators.cpp
import sys;

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
	print(f"Initializing Iota {iota_version}")

	assert len(sys.argv) == 2
	filename = sys.argv[1]

	xmldoc = ElementTree.parse(filename)
	
	root = xmldoc.getroot()

	if not root.attrib['version']:
		print('No version detected in <iota> statement')
		exit()

	print(f"    IDL version: {root.attrib['version']}")
	print(f"    IDL module: {root.attrib['module']}")

	for child in root:
		if child.tag == 'message':
			parse_message(child)
		else:
			print(f"Unknown tag {child.tag}, ignoring...")

	
	print("Parsing done!")

	generators.cpp.generate(iota_messages, root.attrib['module'])



def parse_message(xml_message):
	message_type = xml_message.get('type', 'binary') # Assume default binary representation by default
	message = iota_message(xml_message.attrib['name'], message_type)

	print(f"    Message name: {xml_message.attrib['name']}, type: {message_type}")

	i = 0
	for child in xml_message:
		assert child.tag == 'field'

		field_name = child.text
		field_type = child.attrib['type']

		print(f"        Field: Type: {field_type}, Name: {field_name}, index: {i}")
		
		message.fields.append(iota_field(field_name, field_type, i))
		i += 1

	iota_messages.append(message)


main()