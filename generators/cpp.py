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
		'string': 'iota::string'
	}

	return dictionary.get(type)

def generate_builder(file, message):
	class_name = f"{message.name}_builder"
	file.write(f"    class {class_name} {{\n")
	file.write(f"    public:\n")

	file.write(f"        {class_name}() {{}}\n")

	for field in message.items:
		name = field.name
		native_type = get_message_native_type(field.type)
		index = field.index

		file.write(f"        void add_{name}({native_type} {name}) {{\n")
		file.write(f"            buf.add<{native_type}>({index}, {name});\n")
		file.write(f"        }}\n")

	file.write(f"        uint8_t* serialize() {{\n")
	file.write(f"            buf.serialize();\n")
	file.write(f"            return buf.data();\n")
	file.write(f"        }}\n")

	file.write(f"        size_t length() {{\n")
	file.write(f"            return buf.length();\n")
	file.write(f"        }}\n")

	file.write(f"    private:\n")
	file.write(f"        iota::buffer_generator buf;\n")

	file.write(f"    }};\n\n")

def generate_parser(file, message):
	field_internal_names = []
	for field in message.items:
		field_internal_names.append(f"_{field.name}")

	class_name = f"{message.name}_parser"
	file.write(f"    class {class_name} {{\n")
	file.write(f"    public:\n")

	file.write(f"        {class_name}(uint8_t* buf, size_t size) {{\n")
	file.write(f"            for(size_t i = 0; i < size; i++){{\n")
	file.write(f"                switch(buf[i]){{\n")

	for field in message.items:
		file.write(f"                // {field.type}\n")
		file.write(f"                case {field.index}: {{\n")
		if field.type == 'uint8':
			file.write(f"                    this->{field_internal_names[field.index]} = buf[i + 1];\n")
			file.write(f"                    i++; // 1 byte size beyond the index\n")
		elif field.type == 'uint16':
			file.write(f"                    this->{field_internal_names[field.index]} = ({get_message_native_type(field.type)})(buf[i + 1] | (({get_message_native_type(field.type)})buf[i + 2] << 8));\n")
			file.write(f"                    i += 2;\n")
		elif field.type == 'uint32':
			file.write(f"                    this->{field_internal_names[field.index]} = ({get_message_native_type(field.type)})(buf[i + 1] | (({get_message_native_type(field.type)})buf[i + 2] << 8) | (({get_message_native_type(field.type)})buf[i + 3] << 16) | (({get_message_native_type(field.type)})buf[i + 4] << 24));\n")
			file.write(f"                    i += 4;\n")
		elif field.type == 'uint64':
			file.write(f"                    this->{field_internal_names[field.index]} = ({get_message_native_type(field.type)})(buf[i + 1] | (({get_message_native_type(field.type)})buf[i + 2] << 8) | (({get_message_native_type(field.type)})buf[i + 3] << 16) | (({get_message_native_type(field.type)})buf[i + 4] << 24) | (({get_message_native_type(field.type)})buf[i + 5] << 32) | (({get_message_native_type(field.type)})buf[i + 6] << 40) | (({get_message_native_type(field.type)})buf[i + 7] << 48) | (({get_message_native_type(field.type)})buf[i + 8] << 56));\n")
			file.write(f"                    i += 8;\n")
		elif field.type == 'int8':
			file.write(f"                    this->{field_internal_names[field.index]} = ({get_message_native_type(field.type)})buf[i + 1];\n")
			file.write(f"                    i++; // 1 byte size beyond the index\n")
		elif field.type == 'int16':
			file.write(f"                    this->{field_internal_names[field.index]} = ({get_message_native_type(field.type)})(buf[i + 1] | (({get_message_native_type(field.type)})buf[i + 2] << 8));\n")
			file.write(f"                    i += 2;\n")
		elif field.type == 'int32':
			file.write(f"                    this->{field_internal_names[field.index]} = ({get_message_native_type(field.type)})(buf[i + 1] | (({get_message_native_type(field.type)})buf[i + 2] << 8) | (({get_message_native_type(field.type)})buf[i + 3] << 16) | (({get_message_native_type(field.type)})buf[i + 4] << 24));\n")
			file.write(f"                    i += 4;\n")
		elif field.type == 'int64':
			file.write(f"                    this->{field_internal_names[field.index]} = ({get_message_native_type(field.type)})(buf[i + 1] | (({get_message_native_type(field.type)})buf[i + 2] << 8) | (({get_message_native_type(field.type)})buf[i + 3] << 16) | (({get_message_native_type(field.type)})buf[i + 4] << 24) | (({get_message_native_type(field.type)})buf[i + 5] << 32) | (({get_message_native_type(field.type)})buf[i + 6] << 40) | (({get_message_native_type(field.type)})buf[i + 7] << 48) | (({get_message_native_type(field.type)})buf[i + 8] << 56));\n")
			file.write(f"                    i += 8;\n")
		elif field.type == 'string':
			file.write(f"                    size_t size = (size_t)(buf[i + 1] | ((size_t)buf[i + 2] << 8) | ((size_t)buf[i + 3] << 16) | ((size_t)buf[i + 4] << 24) | ((size_t)buf[i + 5] << 32) | ((size_t)buf[i + 6] << 40) | ((size_t)buf[i + 7] << 48) | ((size_t)buf[i + 8] << 56));\n")
			file.write(f"                    this->{field_internal_names[field.index]} = {get_message_native_type(field.type)}{{}};\n")
			file.write(f"                    for(size_t j = 9/*start index after size*/; j < (size + 9); j++)\n")
			file.write(f"                        this->{field_internal_names[field.index]}->push_back(buf[j]);\n")
			file.write(f"                    i += (8 + size);\n")
		elif field.type == 'buffer':
			file.write(f"                    size_t size = (size_t)(buf[i + 1] | ((size_t)buf[i + 2] << 8) | ((size_t)buf[i + 3] << 16) | ((size_t)buf[i + 4] << 24) | ((size_t)buf[i + 5] << 32) | ((size_t)buf[i + 6] << 40) | ((size_t)buf[i + 7] << 48) | ((size_t)buf[i + 8] << 56));\n")
			file.write(f"                    this->{field_internal_names[field.index]} = {get_message_native_type(field.type)}{{}};\n")
			file.write(f"                    for(size_t j = 9/*start index after size*/; j < (size + 9); j++)\n")
			file.write(f"                        this->{field_internal_names[field.index]}->push_back(buf[j]);\n")
			file.write(f"                    i += (8 + size);\n")
		
		file.write(f"                    break;\n")
		file.write(f"                }}\n")


	file.write(f"                }}\n")
	file.write(f"            }}\n")
	file.write(f"        }}\n")

	for field in message.items:
		name = field.name
		native_type = get_message_native_type(field.type)

		file.write(f"        const {native_type}& get_{name}() {{\n")
		file.write(f"            return *this->{field_internal_names[field.index]};\n")
		file.write(f"        }}\n")

		file.write(f"        bool has_{name}() {{\n")
		file.write(f"            return this->{field_internal_names[field.index]}.has_value();\n")
		file.write(f"        }}\n")

	file.write(f"    private:\n")
	for field in message.items:
		name = field.name
		native_type = get_message_native_type(field.type)
		
		file.write(f"        iota::optional<{native_type}> _{name};\n")

	file.write(f"    }};\n\n")

def get_enum_native_type(type):
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
		'string': 'iota::string'
	}

	return dictionary.get(type)

def generate_enum(file, enum):
	file.write(f"    enum class {enum.name} : {get_enum_native_type(enum.item_type)} {{\n")

	for entry in enum.items:
		file.write(f"        {entry.name} = {entry.value},\n")

	file.write(f"    }};\n\n")

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
	else:	
		print(f"cpp: Unknown subgenerator: {subgenerator}")
		exit()

	buffer_builder_file = open('lib/cpp/buffer_builder.hpp', 'r')
	copy_file_contents(buffer_builder_file, file)

	formatted_module_name = module.replace('.', '::')

	file.write(f"namespace {formatted_module_name} {{\n")

	for item in items:
		if(item.type == 'message'):
			generate_builder(file, item)
			generate_parser(file, item)
		elif(item.type == 'enum'):
			generate_enum(file, item)
		else:
			print(f"cpp: Unknown item type: {item.type}")
			exit()

	file.write("}")

	file.close()

	print("Generated C++ header")