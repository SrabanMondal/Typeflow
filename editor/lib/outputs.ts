import { OutputNodeDef } from "@/types/node";

export const OutputNodes: OutputNodeDef[] = [
  {
    entity: "O",
    name: "text_output",
    description: "Display plain text output",
    inputPorts: ["input"],
    outputType: "text",
    value: ""
  },
  {
    entity: "O",
    name: "json_output",
    description: "Display JSON structured output",
    inputPorts: ["input"],
    outputType: "json",
    value: ""
  },
  {
    entity: "O",
    name: "image_output",
    description: "Display image output (base64 encoded)",
    inputPorts: ["input"],
    outputType: "image",
    value: ""
  },
  {
    entity: "O",
    name: "table_output",
    description: "Display tabular output from JSON array",
    inputPorts: ["input"],
    outputType: "table",
    value: ""
  }
];
