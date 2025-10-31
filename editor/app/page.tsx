import Editor from "@/components/NodeEditor/NodeEditor";
import Sidebar from "@/components/NodeEditor/SideBar";

export default function Page() {
  return (
    <div className="flex h-screen">
      <Editor />
      <Sidebar />
    </div>
  );
}
