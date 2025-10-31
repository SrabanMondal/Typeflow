import InputNode from "./InputNode";
import FunctionNode from "./FunctionNode";
import ClassNode from "./ClassNode";
import MethodNode from "./MethodNode";

const nodeTypes = {
  X: InputNode,
  F: FunctionNode,
  C: ClassNode,
  M: MethodNode,
};

export default nodeTypes;
