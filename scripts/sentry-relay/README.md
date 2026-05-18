# sentry-discord-relay

Cloudflare Worker that receives Sentry webhook payloads and forwards them as
Discord embeds to per-project webhook URLs.

## Endpoint

`https://sentry-discord-relay.623dgk511522.workers.dev`

| Path | Forwards to |
|---|---|
| `POST /sentry/miracle` | `DISCORD_WEBHOOK_MIRACLE` (Miracle channel) |
| `POST /sentry/royal`   | `DISCORD_WEBHOOK_ROYAL` (Royal channel) |
| `GET /`                | health check (`ok`) |

Discord webhook URLs are stored as Worker secrets (not in this repo).

## Sentry side configuration

For each project (Miracle / Royal):

1. Sentry → Settings → Integrations → **Webhooks** → enable + Configure
2. Add the relay URL above with the matching path (`/sentry/miracle` or `/sentry/royal`)
3. Sentry → Alerts → Create Alert (or edit existing) → Action: **Send a notification via an integration → Webhooks** and pick the URL just registered
4. Save

## Adding a new channel route

1. Create a Discord webhook in the new channel, copy URL
2. `printf '%s' '<url>' | npx wrangler secret put DISCORD_WEBHOOK_<NAME>`
3. Add `"/sentry/<slug>": "DISCORD_WEBHOOK_<NAME>"` to `ROUTES` in `src/index.js`
4. `npx wrangler deploy`

## Local iteration

```sh
npx wrangler dev    # local
npx wrangler tail   # stream prod logs
```
