const counters: Record<string, number> = {};

export function generateId(type: string): string {
  counters[type] = (counters[type] || 0) + 1;
  return `${counters[type]}`;
}
