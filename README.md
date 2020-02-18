# Iota is the IDL and compiler of Sigma

## Compiler
The iota compiler is iota.py and an example call looks like

`python3 iota.py /path/to/some/idl/file.xml --generator cpp -o /path/to/some/header.hpp`

Which will take `/path/to/some/idl/file.xml` and generate a C++ header in `/path/to/some/header.hpp`

## IDL
The IDL is written in XML

### <iota>

The root node is a `<iota>` node with 2 required attributes `version` which describes the language version and `module` which describes the module it is in

An example is

`<iota version="0.0.1" module="foo.bar">`

### <message>

Under the root node various `<message>` nodes exist which describe a message, it has 1 attribute `name` which tells us the name of the module

An example node would be

`<message name="baz">`

### <field>

Under said `<message>` nodes `<field>` nodes exist which describe the varies entries in a message. It has 1 attribute `type` which has the 
following possible values:

- `int8`
- `uint8`
- `int16`
- `uint16`
- `int32`
- `uint32`
- `int64`
- `uint64`
- `buffer`: Array of uint8's
- `string`: Array of ASCII characters
- `list`: Array of uint64's

And in between the `<field>` and `</field>` nodes the name is placed

### <enum>

Under the root node various `<enum>` nodes can exist which describe an enumeration, it has 2 attributes `name` which tells us the name of the module and `type` which tells us the name of the enumeration

Possible types are
- `int8`
- `uint8`
- `int16`
- `uint16`
- `int32`
- `uint32`
- `int64`
- `uint64`

An example node would be

`<enum name="baz" type="int32">`

### <entry>

Under said `<enum>` nodes `<entry>` nodes exist which describe the varies entries in a enum. It has 1 attribute `value` which is the value of the entry


And in between the `<field>` and `</field>` nodes the name is placed

This makes for the following example node

`<entry value="2">myEnumEntry</entry>`

### All together

In this way we can create an example IDL file

```xml
<iota version="0.0.1" module="foo">
    <enum name="request" type="uint8">
        <entry value="0">nop</entry>
        <entry value="1">open</entry>
        <entry value="2">close</entry>
    </enum>

    <message name="bar">
        <field type="uint64">test</field>
        <field type="uint32">abc</field>
        <field type="buffer">buf</field>
    </message>
</iota>
```

for other examples look in the `examples/` directory
