import { SerializedWorkflow } from "@/types/workflow";

const counters: Record<string, number> = {};

export function generateId(type: string): string {
  counters[type] = (counters[type] || 0) + 1;
  return `${counters[type]}`;
}

export function updateCountersFromDag(dag: SerializedWorkflow) {

  for (const node of dag.nodes) {
    const entity = node.data.entity;   // F, X, C, M (?)
    const id = node.id;

    // Extract last number after last "@"
    const match = id.match(/@(\d+)$/);
    if (!match) continue;

    const num = parseInt(match[1], 10);

    // Track max id per entity
    if (!counters[entity] || num > counters[entity]) {
      counters[entity] = num;
    }
  }

  // Now +1 so next generated id starts correctly
  for (const key in counters) {
    counters[key] = counters[key]; // keep max; generateId will add +1 when used
  }

  return counters;
}
