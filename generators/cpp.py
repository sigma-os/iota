def get_message_native_type(type):
	dictionary = {
		'uint8': 'uint8_t',
		'uint16': 'uint16_t',
		'uint32': 'uint32_t',
		'uint64': 'uint64_t',
		'int8': 'int8_t',
		'int16': 'int16_t',
		'int32': 'int32_t',
		'int64': 'int64_t',
		'buffer': 'iota::vector<uint8_t>',
		'list': 'iota::vector<uint64_t>',
		'string': 'iota::string'
	}

	return dictionary.get(type)

def get_message_default_initializer(type):
	dictionary = {
		'uint8': '{}',
		'uint16': '{}',
		'uint32': '{}',
		'uint64': '{}',
		'int8': '{}',
		'int16': '{}',
		'int32': '{}',
		'int64': '{}',
		'buffer': 'iota::create_vector<uint8_t>()',
		'list': 'iota::create_vector<uint64_t>()',
		'string': 'iota::create_string()'
	}

	return dictionary.get(type)

def generate_builder(file, message):
	class_name = f"{message.name}_builder"
	file.write(f"\tclass {class_name} {{\n")
	file.write(f"\tpublic:\n")

	file.write(f"\t\t{class_name}(): buf{{}} {{}}\n")

	for field in message.items:
		name = field.name
		native_type = get_message_native_type(field.type)
		index = field.index

		file.write(f"\t\tvoid add_{name}({native_type} {name}) {{\n")
		file.write(f"\t\t\tbuf.add<{native_type}>({index}, {name});\n")
		file.write(f"\t\t}}\n")

	file.write(f"\t\tuint8_t* serialize() {{\n")
	file.write(f"\t\t\tbuf.serialize();\n")
	file.write(f"\t\t\treturn buf.data();\n")
	file.write(f"\t\t}}\n")

	file.write(f"\t\tsize_t length() {{\n")
	file.write(f"\t\t\treturn buf.length();\n")
	file.write(f"\t\t}}\n")

	file.write(f"\tprivate:\n")
	file.write(f"\t\tiota::buffer_generator buf;\n")

	file.write(f"\t}};\n\n")

def generate_parser(file, message):
	class_name = f"{message.name}_parser"
	file.write(f"\tclass {class_name} {{\n")
	file.write(f"\tpublic:\n")

	file.write(f"\t\t{class_name}(uint8_t* buf, size_t size) {{\n")
	file.write(f"\t\t\tfor(size_t i = 0; i < size;){{\n")
	file.write(f"\t\t\t\tiota::index_type index = buf[i];\n")
	file.write(f"\t\t\t\ti++;\n")
	file.write(f"\t\t\t\tswitch(index){{\n")

	for field in message.items:
		file.write(f"\t\t\t\t// {field.type}\n")
		file.write(f"\t\t\t\tcase {field.index}: {{\n")
		file.write(f"\t\t\t\t\tthis->_p_{field.name} = true;\n")
		file.write(f"\t\t\t\t\ti += iota::parse_item<{get_message_native_type(field.type)}>(&buf[i], this->_m_{field.name});\n")
		file.write(f"\t\t\t\t\tbreak;\n")
		file.write(f"\t\t\t\t}}\n")


	file.write(f"\t\t\t\t}}\n")
	file.write(f"\t\t\t}}\n")
	file.write(f"\t\t}}\n")

	for field in message.items:
		name = field.name
		native_type = get_message_native_type(field.type)

		file.write(f"\t\t{native_type}& get_{name}() {{\n")
		file.write(f"\t\t\treturn this->_m_{field.name};\n")
		file.write(f"\t\t}}\n")

		file.write(f"\t\tbool has_{name}() {{\n")
		file.write(f"\t\t\treturn this->_p_{field.name};\n")
		file.write(f"\t\t}}\n")

	file.write(f"\tprivate:\n")
	for field in message.items:
		name = field.name
		native_type = get_message_native_type(field.type)
		
		file.write(f"\t\t{native_type} _m_{name} = {get_message_default_initializer(field.type)}; bool _p_{name} = false;\n")

	file.write(f"\t}};\n\n")

def get_enum_native_type(type):
	dictionary = {
		'uint8': 'uint8_t',
		'uint16': 'uint16_t',
		'uint32': 'uint32_t',
		'uint64': 'uint64_t',
		'int8': 'int8_t',
		'int16': 'int16_t',
		'int32': 'int32_t',
		'int64': 'int64_t'
	}

	return dictionary.get(type)

def generate_enum(file, enum):
	file.write(f"\tenum class {enum.name} : {get_enum_native_type(enum.item_type)} {{\n")

	for entry in enum.items:
		file.write(f"\t\t{entry.name} = {entry.value},\n")

	file.write(f"\t}};\n\n")

def copy_file_contents(file1, file2):
	for line in file1:
		file2.write(line)

	file2.write("\n\n")

def generate(subgenerator, output, items, module):
	file = open(output, 'w')
	
	file.write("#pragma once\n\n")
	file.write("#include <stdint.h>\n")
	file.write("#include <stddef.h>\n")

	if not subgenerator:
		subgenerator = 'std' # use std as default subgen

	if subgenerator == 'std':
		lib_file = open('lib/cpp/lib-std.hpp', 'r')
		copy_file_contents(lib_file, file)
		lib_file.close()
	elif subgenerator == 'frigg':
		lib_file = open('lib/cpp/lib-frigg.hpp', 'r')
		copy_file_contents(lib_file, file)
		lib_file.close()
	elif subgenerator == 'sigma-kernel':
		lib_file = open('lib/cpp/lib-sigma-kernel.hpp', 'r')
		copy_file_contents(lib_file, file)
		lib_file.close()
	else:	
		print(f"cpp: Unknown subgenerator: {subgenerator}")
		exit()

	buffer_builder_file = open('lib/cpp/buffer_builder.hpp', 'r')
	copy_file_contents(buffer_builder_file, file)
	buffer_builder_file.close()

	buffer_parser_file = open('lib/cpp/buffer_parser.hpp', 'r')
	copy_file_contents(buffer_parser_file, file)
	buffer_parser_file.close()

	module_parts = module.split('.')

	for part in module_parts:
		file.write(f"namespace [[gnu::visibility(\"hidden\")]] {part} {{ ")

	file.write("\n")

	for item in items:
		if(item.type == 'message'):
			generate_builder(file, item)
			generate_parser(file, item)
		elif(item.type == 'enum'):
			generate_enum(file, item)
		else:
			print(f"cpp: Unknown item type: {item.type}")
			exit()

	for part in module_parts:
		file.write("} ")

	file.close()

	print("Generated C++ header")