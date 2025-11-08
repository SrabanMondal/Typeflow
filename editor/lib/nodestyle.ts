// lib/nodeStyles.ts

export const baseNodeStyle = {
  boxShadow: "none",
  border: "1px solid #e5e7eb",
  transition: "all 0.3s ease",
  borderRadius: "12px",
};

export const nodeStateStyles: Record<string, React.CSSProperties> = {
  start: {
    ...baseNodeStyle,
    boxShadow: "0 0 15px 3px rgba(255, 193, 7, 0.7)", // yellow glow
    border: "1px solid #facc15",
  },
  success: {
    ...baseNodeStyle,
    boxShadow: "0 0 15px 3px rgba(34, 197, 94, 0.7)", // green glow
    border: "1px solid #22c55e",
  },
  error: {
    ...baseNodeStyle,
    boxShadow: "0 0 15px 3px rgba(239, 68, 68, 0.7)", // red glow
    border: "1px solid #ef4444",
  },
  reset: {
    ...baseNodeStyle,
  },
};
