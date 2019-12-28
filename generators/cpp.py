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
		file.write(f"            buf.add<uint8_t>({index});\n")
		file.write(f"            buf.add<{native_type}>({name});\n")
		file.write(f"        }}\n")

	file.write(f"        uint8_t* data() {{\n")
	file.write(f"            return buf.data();\n")
	file.write(f"        }}\n")

	file.write(f"    private:\n")
	file.write(f"        iota::buffer<uint8_t> buf;\n")

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

def generate_c_struct(file, message):
	file.write(f"    struct {message.name} {{\n")

	for field in message.fields:
		file.write(f"        {get_native_type(field.type_)} {field.name};\n")

	file.write(f"    }};\n")

def generate(messages, module):
	file = open('out.hpp', 'w')

	
	file.write("#pragma once\n\n")
	file.write("#include <stdint.h>\n\n")

	module_parts = module.split('.')
	formatted_module_name = ''
	for part in module_parts:
		formatted_module_name += part
		formatted_module_name += '::'

	formatted_module_name = formatted_module_name[:-2]

	file.write(f"namespace {formatted_module_name} {{\n")

	for message in messages:
		if message.type_ == 'binary':
			generate_builder(file, message)
			generate_parser(file, message)
		elif message.type_ == 'raw_struct':
			generate_c_struct(file, message)
		else:
			print(f"cpp: Unknown generate type: {message.type_}")
			exit()

	file.write("}")

	print("Generated C++ header")