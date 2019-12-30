def get_native_type(type):
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

	for field in message.fields:
		name = field.name
		native_type = get_native_type(field.type_)
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
	class_name = f"{message.name}_parser"
	file.write(f"    class {class_name} {{\n")
	file.write(f"    public:\n")

	file.write(f"        {class_name}(uint8_t* buf) {{\n")
	file.write(f"            // TODO\n")
	file.write(f"        }}\n")

	for field in message.fields:
		name = field.name
		native_type = get_native_type(field.type_)
		
		file.write(f"        const {native_type}& get_{name}() {{\n")
		file.write(f"            return *this->_{name};\n")
		file.write(f"        }}\n")

		file.write(f"        bool has_{name}() {{\n")
		file.write(f"            return this->_{name}.has_value();\n")
		file.write(f"        }}\n")

	file.write(f"    private:\n")
	for field in message.fields:
		name = field.name
		native_type = get_native_type(field.type_)
		
		file.write(f"        iota::optional<{native_type}> _{name};\n")

	file.write(f"    }};\n\n")

def copy_file_contents(file1, file2):
	for line in file1:
		file2.write(line)

	file2.write("\n\n")

def generate(subgenerator, output, messages, module):
	file = open(output, 'w')
	
	file.write("#pragma once\n\n")
	file.write("#include <stdint.h>\n")
	file.write("#include <stddef.h>\n")

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

	for message in messages:
		generate_builder(file, message)
		generate_parser(file, message)

	file.write("}")

	file.close()

	print("Generated C++ header")