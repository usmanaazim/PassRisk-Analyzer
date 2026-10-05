const API = "/api";

async function parse(response) {
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.error || "Request failed.");
  }
  return data;
}

export async function analyzePassword(password) {
  return parse(
    await fetch(`${API}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password }),
    })
  );
}

export async function comparePasswords(password_a, password_b) {
  return parse(
    await fetch(`${API}/compare`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password_a, password_b }),
    })
  );
}

export async function fetchHealth() {
  return parse(await fetch(`${API}/health`));
}

export async function fetchMetrics() {
  return parse(await fetch(`${API}/metrics`));
}

export async function fetchModelInfo() {
  return parse(await fetch(`${API}/model-info`));
}
