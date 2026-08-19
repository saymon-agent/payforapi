# Saymon RU Data API

Russian-language data endpoints for AI agents. Pay per request in USDC via **x402** (HTTP 402 Payment Required). **No API keys, no accounts, no subscriptions.**

Base URL: `https://payforapi.com` · MCP: `https://payforapi.com/mcp` · Health: `https://payforapi.com/health` · Manifest: `https://payforapi.com/.well-known/x402.json`

Network: Base mainnet (`eip155:8453`) · Asset: USDC · Facilitator: `https://x402.primer.systems`

## Endpoints

| Endpoint | Price | Description |
|---|---|---|
| `POST /v1/inn-lookup` | $0.01 | Verify Russian legal entity by INN from official EGRUL (Federal Tax Service). Returns INN, OGRN, KPP, name, director, registration date, region. |
| `POST /v1/ru-search` | $0.02 | Cyrillic web search (Yandex Search API upstream). Returns URL, title, snippet. |
| `POST /v1/ru-page` | $0.01 | Russian-language page → clean LLM-ready Markdown (trafilatura). |
| `POST /v1/research` | $0.02 | Research pack: Cyrillic search + top pages assembled into one Markdown answer (one payment instead of a search+page chain). |

## Examples

```bash
# 1. Unpaid request -> 402 Payment Required
curl -X POST https://payforapi.com/v1/inn-lookup \
  -H "Content-Type: application/json" -d '{"inn": "7707083893"}'

# 2. Sign EIP-3009 transferWithAuthorization for USDC (Base) to payTo from the 402 response
# 3. Resend with PAYMENT-SIGNATURE header -> 200 OK + payment-response
```

## MCP

Remote MCP server (streamable-http): `https://payforapi.com/mcp` — 4 tools: `inn_lookup`, `ru_search`, `ru_page`, `ru_research`. Agents pay via `_meta["x402/payment"]`.

## Why

- **Only Cyrillic/RU-native segment in the x402 ecosystem**: EGRUL verification, Russian web search, RU scraping.
- Keyless for clients: no registration, no API keys — wallet pays, agent gets data.
- Official sources (EGRUL/FNS), legal for resale (129-ФЗ, 262-ФЗ, 44-ФЗ).

## Docs & manifest

- `llms.txt` — machine-readable description for LLMs
- `/.well-known/x402.json` — x402 discovery manifest
- `/openapi.json` — OpenAPI spec

© 2026 Saymon / Real Energy.
