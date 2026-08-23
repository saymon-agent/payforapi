# Saymon RU Data API

Russian-language data endpoints for AI agents. Pay per request in USDC via **x402** (HTTP 402 Payment Required). **No API keys, no accounts, no subscriptions.**

Base URL: `https://payforapi.com` · MCP: `https://payforapi.com/mcp` · Health: `https://payforapi.com/health` · Manifest: `https://payforapi.com/.well-known/x402.json`

Network: Base mainnet (`eip155:8453`) · Asset: USDC · Facilitator: `https://x402.primer.systems`

## Endpoints (11)

| Endpoint | Price | Description |
|---|---|---|
| `POST /v1/inn-lookup` | $0.01 | Verify Russian legal entity by INN from official EGRUL (Federal Tax Service). Returns INN, OGRN, KPP, name, director, registration date, region. |
| `POST /v1/ru-search` | $0.02 | Cyrillic web search (Yandex Search API upstream). Returns URL, title, snippet. |
| `POST /v1/ru-page` | $0.01 | Russian-language page → clean LLM-ready Markdown (trafilatura). |
| `POST /v1/research` | $0.02 | Research pack: Cyrillic search + top pages assembled into one Markdown answer (one payment instead of a search+page chain). |
| `POST /v1/research/deep` | $0.05 | Deep research pack: 3 search variants + up to 10 pages in one Markdown answer — full counterparty check. |
| `POST /v1/pochta-tariff` | $0.01 | Russian Post: delivery cost & time between postal indexes (official API, postal contract). |
| `POST /v1/pochta-track` | $0.01 | Russian Post: track a shipment by barcode (SOAP tracking.russianpost.ru). |
| `POST /v1/pochta-delivery-time` | $0.01 | Russian Post: delivery time (days) between postal indexes. |
| `POST /v1/pochta-offices` | $0.01 | Russian Post: post offices by postal code or nearest by coordinates. |
| `POST /v1/pochta-zip` | $0.01 | Russian Post: office address and locality by postal code. |
| `POST /v1/pochta-address` | $0.01 | Russian Post: Russian address normalization (index, region, street, house). |

## Examples

```bash
# 1. Unpaid request -> 402 Payment Required
curl -X POST https://payforapi.com/v1/inn-lookup \
  -H "Content-Type: application/json" -d '{"inn": "7707083893"}'

# 2. Sign EIP-3009 transferWithAuthorization for USDC (Base) to payTo from the 402 response
# 3. Resend with PAYMENT-SIGNATURE header -> 200 OK + payment-response
```

## MCP

Remote MCP server (streamable-http): `https://payforapi.com/mcp` — 11 tools: `inn_lookup`, `ru_search`, `ru_page`, `ru_research`, `ru_research_deep`, `pochta_tariff`, `pochta_track`, `pochta_delivery_time`, `pochta_offices`, `pochta_zip`, `pochta_address`. Agents pay via `_meta["x402/payment"]`.

## Why

- **Only Cyrillic/RU-native segment in the x402 ecosystem**: EGRUL verification, Russian web search, RU scraping, Russian Post data.
- Keyless for clients: no registration, no API keys — wallet pays, agent gets data.
- Official sources (EGRUL/FNS, Russian Post contract), legal for resale (129-ФЗ, 262-ФЗ, 44-ФЗ).

## Docs & manifest

- `llms.txt` — machine-readable description for LLMs
- `/.well-known/x402.json` — x402 discovery manifest
- `/openapi.json` — OpenAPI spec

© 2026 Saymon / Real Energy.
