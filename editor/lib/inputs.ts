import { InputNodeDef } from "@/types/node";

export const InputNodes: InputNodeDef[] = [
  {
    entity: "X",
    name: "string_val",
    description: "Provide a string constant",
    valueType: "str",
    outputPorts: ["val"],
    value: ""
  },
  {
    entity: "X",
    name: "num_val",
    description: "Provide a numeric constant",
    valueType: "number",
    outputPorts: ["val"],
    value: ""
  },
  {
    entity: "X",
    name: "int_val",
    description: "Provide an integer constant",
    valueType: "int",
    outputPorts: ["val"],
    value: ""
  },
  {
    entity: "X",
    name: "float_val",
    description: "Provide a floating-point constant",
    valueType: "float",
    outputPorts: ["val"],
    value: ""
  },
  {
    entity: "X",
    name: "bool_val",
    description: "Provide a boolean constant",
    valueType: "bool",
    outputPorts: ["val"],
    value: ""
  },
  {
    entity: "X",
    name: "list_val",
    description: "Provide a list of values",
    valueType: "list",
    outputPorts: ["val"],
    value: ""
  },
  {
    entity: "X",
    name: "tuple_val",
    description: "Provide a tuple of values",
    valueType: "tuple",
    outputPorts: ["val"],
    value: ""
  },
  {
    entity: "X",
    name: "dict_val",
    description: "Provide a dictionary object",
    valueType: "dict",
    outputPorts: ["val"],
    value: ''
  },
  {
    entity: "X",
    name: "set_val",
    description: "Provide a unique set of values",
    valueType: "set",
    outputPorts: ["val"],
    value: ""
  },
  {
    entity: "X",
    name: "file_input",
    description: "Upload a file to use as input",
    valueType: "str",
    outputPorts: ["val"],
    value: "",      
    file: true  
  }

];
