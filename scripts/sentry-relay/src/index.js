// Sentry → Discord webhook relay.
//
// Routes (POST):
//   /sentry/miracle  → DISCORD_WEBHOOK_MIRACLE
//   /sentry/royal    → DISCORD_WEBHOOK_ROYAL
//
// Health: GET / → "ok"

const ROUTES = {
  "/sentry/miracle": "DISCORD_WEBHOOK_MIRACLE",
  "/sentry/royal": "DISCORD_WEBHOOK_ROYAL",
};

const LEVEL_COLOR = {
  fatal: 0xe03e2f,
  error: 0xe03e2f,
  warning: 0xf5a623,
  info: 0x4a90e2,
  debug: 0x95a5a6,
};

function truncate(s, n) {
  if (!s) return "";
  return s.length <= n ? s : s.slice(0, n - 1) + "…";
}

function sentryToDiscord(payload) {
  const ev = payload.event || {};
  const level = (ev.level || payload.level || "error").toLowerCase();
  const color = LEVEL_COLOR[level] ?? LEVEL_COLOR.error;
  const project = payload.project_name || payload.project_slug || payload.project || "sentry";
  const env = ev.environment || (Array.isArray(ev.tags) ? (ev.tags.find(([k]) => k === "environment") || [])[1] : undefined);
  const release = ev.release || (Array.isArray(ev.tags) ? (ev.tags.find(([k]) => k === "release") || [])[1] : undefined);

  const title = truncate(ev.title || payload.message || "Sentry alert", 240);
  const culprit = truncate(payload.culprit || ev.culprit || "", 200);
  const url = payload.url || ev.web_url || "";

  const fields = [];
  if (env) fields.push({ name: "env", value: String(env), inline: true });
  if (level) fields.push({ name: "level", value: level, inline: true });
  if (release) fields.push({ name: "release", value: truncate(String(release), 100), inline: true });
  if (culprit) fields.push({ name: "culprit", value: culprit, inline: false });

  return {
    username: `Sentry · ${project}`,
    embeds: [
      {
        title,
        url: url || undefined,
        color,
        fields,
        timestamp: ev.received ? new Date(ev.received * 1000).toISOString() : new Date().toISOString(),
        footer: { text: project },
      },
    ],
  };
}

async function forward(webhookUrl, body) {
  const res = await fetch(webhookUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return res;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === "GET" && url.pathname === "/") {
      return new Response("ok", { status: 200 });
    }

    if (request.method !== "POST") {
      return new Response("method not allowed", { status: 405 });
    }

    const secretName = ROUTES[url.pathname];
    if (!secretName) {
      return new Response("not found", { status: 404 });
    }

    const webhookUrl = env[secretName];
    if (!webhookUrl) {
      return new Response(`secret ${secretName} not set`, { status: 500 });
    }

    let payload;
    try {
      payload = await request.json();
    } catch {
      return new Response("invalid json", { status: 400 });
    }

    const discordBody = sentryToDiscord(payload);
    const res = await forward(webhookUrl, discordBody);

    if (!res.ok) {
      const text = await res.text();
      return new Response(`discord error ${res.status}: ${text.slice(0, 500)}`, { status: 502 });
    }
    return new Response("forwarded", { status: 200 });
  },
};
