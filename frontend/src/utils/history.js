const KEY = "passwordguard-history-v1";

export function loadHistory() {
  try {
    return JSON.parse(sessionStorage.getItem(KEY) || "[]");
  } catch {
    return [];
  }
}

export function saveHistoryItem(analysis) {
  const item = {
    id: crypto.randomUUID(),
    timestamp: new Date().toISOString(),
    score: analysis.score,
    risk_level: analysis.risk_level,
    entropy: analysis.entropy,
    strength: analysis.strength,
  };
  const next = [item, ...loadHistory()].slice(0, 40);
  sessionStorage.setItem(KEY, JSON.stringify(next));
  return next;
}

export function clearHistory() {
  sessionStorage.removeItem(KEY);
  return [];
}

export function groupHistory(items) {
  const groups = {};
  for (const item of items) {
    const day = new Date(item.timestamp).toDateString();
    groups[day] = groups[day] || [];
    groups[day].push(item);
  }
  return groups;
}
