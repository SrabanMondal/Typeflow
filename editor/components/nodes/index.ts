import InputNode from "./InputNode";
import FunctionNode from "./FunctionNode";
import ClassNode from "./ClassNode";
import MethodNode from "./MethodNode";
import { OutputNode } from "./OutputNode";

const nodeTypes = {
  X: InputNode,
  F: FunctionNode,
  C: ClassNode,
  M: MethodNode,
  O: OutputNode
};

export default nodeTypes;
