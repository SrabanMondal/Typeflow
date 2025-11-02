export interface MethodDef extends Record<string, unknown> {
  name: string;
  entity:"C";
  inputPorts: string[];
  outputPorts: string[];
  description?: string;
  is_static?: boolean;
}

export interface ClassNodeDef extends Record<string, unknown> {
  entity: "C";
  name: string;
  description: string;
  inputPorts: string[];
  outputPorts: string[];
  methods: MethodDef[];
}

export interface FunctionNodeDef extends Record<string, unknown> {
  entity: "F";
  name: string;
  description: string;
  inputPorts: string[];
  outputPorts: string[];
  returns?: string;
}

export interface InputNodeDef extends Record<string, unknown> {
  entity: "X";
  name: string;
  valueType: "str" | "number" | "int" | "float" | "bool" | "list" | "dict" | "set";
  description: string;
  outputPorts: string[];
  value: string;
}

export type CatalogueType =  ClassNodeDef|FunctionNodeDef|InputNodeDef
export interface NodeCatalog extends Record<string, unknown> {
  classes: ClassNodeDef[];
  functions: FunctionNodeDef[];
  inputs: InputNodeDef[];
}