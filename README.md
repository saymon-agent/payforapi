# Saymon RU Data API — PAYFORAPI

> 🇷🇺 Российские данные для AI-агентов · 🇨🇳 面向AI代理的俄罗斯数据API · 🇯🇵 AIエージェント向けロシア語データAPI · 🇰🇷 AI 에이전트를 위한 러시아어 데이터 API

**Russian-language (Runet) data APIs for AI agents.** Official state-registry company checks, Russian Post, CBR/MOEX market data, page-to-Markdown. Pay per request in USDC via **x402** (HTTP 402 Payment Required). **No API keys, no accounts, no subscriptions.**

Base URL: `https://payforapi.com` · Site: `https://payforapi.com` · MCP: `https://payforapi.com/mcp` · Health: `https://payforapi.com/health` · Manifest: `https://payforapi.com/.well-known/x402.json`

Network: Base mainnet (`eip155:8453`) · Asset: USDC · Facilitator: `https://x402.primer.systems`

## Endpoints (13, live)

Prices verified live against production on 2026-11-03 (unpaid call → `402` with `accepts[0].amount`).

| Endpoint | Price | Description |
|---|---|---|
| `POST /v1/inn-lookup` | $0.01 | **Russian company check by INN** — official EGRUL state registry, unavailable to foreign checkers (merchant KYB before a deal). |
| `POST /v1/fns-npd-check` | $0.01 | **RU self-employed (NPD) status** by INN via FNS. Run before paying a contractor. |
| `POST /v1/ru-page` | $0.01 | Clean **Russian-language page** → LLM-ready Markdown (trafilatura): product card, store, news. |
| `POST /v1/pochta-tariff` | $0.01 | **Russian Post**: delivery cost between postcodes (official API) — shipping math for checkout. |
| `POST /v1/pochta-track` | $0.01 | **Russian Post**: parcel tracking by track number (SOAP) — official RU tracking. |
| `POST /v1/pochta-delivery-time` | $0.01 | **Russian Post**: control delivery times between postcodes (days). |
| `POST /v1/pochta-offices` | $0.01 | **Russian Post**: offices by postcode or coordinates — pickup points. |
| `POST /v1/pochta-zip` | $0.01 | **Russian postal codes** by address or office. |
| `POST /v1/pochta-address` | $0.01 | **RU address normalization** to Russian Post standard (index, region, street, house). |
| `POST /v1/pochta-delivery` | $0.04 | **Russian Post delivery bundle**: address + postcode + office + rate + time in one payment (5 services in 1). |
| `POST /v1/ticker` | $0.005 | Bybit spot crypto tickers: last price, 24h change, volume. |
| `POST /v1/cbr-rates` | $0.008 | **Central Bank of Russia** official daily FX rates (USD, EUR, CNY…) — state reference for RUB pricing. |
| `POST /v1/moex-quote` | $0.008 | **Moscow Exchange** quotes: stocks (SBER, GAZP…), FX pairs, indices (IMOEX) — live Russian market data. |

### Temporarily paused (7) — search-dependent

These routes still exist in the OpenAPI schema but currently answer **`503 {"error":"search temporarily unavailable","reason":"yandex_search_disabled","note":"payment not required"}`**. No payment is taken, no money is lost. They are **not** part of the x402 discovery manifest.

| Endpoint | Price when live |
|---|---|
| `POST /v1/ru-search` | $0.02 |
| `POST /v1/web-search` | $0.02 |
| `POST /v1/research` | $0.02 |
| `POST /v1/research/deep` | $0.05 |
| `POST /v1/company-report` | $0.05 |
| `POST /v1/ru-search/x10` | $0.18 |
| `POST /v1/ru-search/x100` | $1.60 |

Check `GET /health` (`tool_count`) or the manifest before wiring a paid flow: the authoritative list of payable routes is `https://payforapi.com/.well-known/x402.json`.

## Referral program — earn 20%

Bring other agents to payforapi.com and earn **20% of the revenue they generate** — for life, on every paid call.

- Your **wallet is your referral ID** — no codes, no sign-up: `https://payforapi.com/r/<wallet>`
- Pass your wallet on the agent's first call: header `X-Referral: <wallet>` or query `?ref=<wallet>`
- Attribution is first-touch and lifetime. Self-referral and circular referrals are rejected.
- Payouts: minimum **$1.00**, settled weekly (Sunday 23:59 UTC) in USDC on Base.
- Check your numbers — free API: `GET /v1/referral/stats?wallet=<wallet>` · `GET /v1/referral/earnings?wallet=<wallet>` · `GET /v1/referral/link?wallet=<wallet>`
- Human-readable page with a live counter for any wallet: `https://payforapi.com/referral`

## Contacts

- Support: `support@payforapi.com`
- Abuse / content complaints: `abuse@payforapi.com`
- Telegram channel (news): https://t.me/payforapicom
- Telegram support chat: https://t.me/payforapichat

## Examples

```bash
# 1. Unpaid request -> 402 Payment Required (accepts[0].amount = price in USDC micro-units)
curl -X POST https://payforapi.com/v1/inn-lookup \
  -H "Content-Type: application/json" -d '{"inn": "7707083893"}'

# 2. Sign EIP-3009 transferWithAuthorization for USDC (Base) to payTo from the 402 response
# 3. Resend with PAYMENT-SIGNATURE header -> 200 OK + payment-response
```

## MCP

Remote MCP server (streamable-http): `https://payforapi.com/mcp` — **13 tools**: `inn_lookup`, `fns_npd_check`, `ru_page`, `cbr_rates`, `moex_quote`, `pochta_tariff`, `pochta_track`, `pochta_delivery_time`, `pochta_offices`, `pochta_zip`, `pochta_address`, `pochta_delivery`, `ticker`. Agents pay via `_meta["x402/payment"]`; server version reported by `initialize` is `1.30.0`.

### Local stdio server (Docker)

Clients that only speak stdio (Claude Desktop, Cursor, Cline, …) can run the same tool catalogue locally. The container starts and answers MCP introspection (`initialize` / `tools/list`) with **no network and no secrets**; tool calls are proxied to the hosted x402 endpoint, so payment stays per call in USDC on Base.

```bash
docker build -t saymon-ru-data-api-mcp .
```

```json
{
  "mcpServers": {
    "saymon-ru-data-api": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "saymon-ru-data-api-mcp"],
      "env": { "PAYFORAPI_MCP_URL": "https://payforapi.com/mcp" }
    }
  }
}
```

Files: `server.py` (stdio server), `tools.json` (EN tool catalogue), `Dockerfile`, `glama.json`.

## Also available via PayAPI Market

The same paid routes are listed on the [PayAPI Market](https://payapi.market) warehouse — agents can discover and call them from there as well as from payforapi.com. Same x402 payment (USDC on Base to the same seller wallet), no extra fees.

- MCP discovery: `https://payapi.market/mcp`
- Listing: `https://payapi.market/api/saymon-ru-data-api`

Claude Desktop / Cursor config:

```json
{
  "mcpServers": {
    "payapi": {
      "url": "https://payapi.market/mcp"
    }
  }
}
```

## 中文 (Chinese)

面向AI代理的俄罗斯数据API。按次付费（x402 / HTTP 402），Base链USDC结算。无需注册、无需API密钥、无订阅。当前可用 **13** 个接口。

- **企业核实**：`POST /v1/inn-lookup`（$0.01）— 通过ИНН查询俄罗斯企业（ЕГРЮЛ/ФНС官方数据）
- **个体户（НПД）状态核实**：`POST /v1/fns-npd-check`（$0.01）
- **俄语网页转Markdown**：`POST /v1/ru-page`（$0.01）
- **俄罗斯邮政**：`POST /v1/pochta-track`（$0.01，包裹跟踪）· `pochta-tariff` · `pochta-delivery-time` · `pochta-offices` · `pochta-zip` · `pochta-address`（各$0.01）· **投递包 `pochta-delivery`（$0.04，5合1）**
- **金融数据**：`cbr-rates`（央行汇率，$0.008）· `moex-quote`（莫斯科交易所报价，$0.008）· `ticker`（加密货币，$0.005）
- **搜索类接口暂停**（`ru-search`、`web-search`、`research`、`company-report` 及批量搜索）— 返回 503，不收费
- **推荐计划**：带来其他代理，终身获其付费调用收入的 20% — https://payforapi.com/referral

中俄贸易背景下的应用：进口商/出口商在交易前核验俄方企业真实性，物流团队跟踪俄罗斯邮政包裹。

## 日本語 (Japanese)

AIエージェント向けロシア語データAPI。x402（HTTP 402）従量課金、BaseチェーンUSDC。APIキー・アカウント・サブスク不要。現在 **13** エンドポイントが利用可能。

- **法人照会**：`POST /v1/inn-lookup`（$0.01）— ИННによるロシア法人確認（ЕГРЮЛ/ФНС公式データ）
- **個人事業主（НПД）確認**：`POST /v1/fns-npd-check`（$0.01）
- **ページ変換**：`POST /v1/ru-page`（$0.01）— LLM対応Markdown
- **ロシア郵便**：`POST /v1/pochta-track`（$0.01，追跡）ほか5エンドポイント（各$0.01）· **配送バンドル `pochta-delivery`（$0.04，5in1）**
- **金融データ**：`cbr-rates`（中央銀行為替，$0.008）· `moex-quote`（モスクワ取引所，$0.008）· `ticker`（仮想通貨，$0.005）
- **検索系は一時停止**（`ru-search`・`web-search`・`research`・`company-report`・一括検索）— 503を返し、課金なし
- **紹介プログラム**：他エージェントを紹介すると、その支払いの20%を生涯獲得 — https://payforapi.com/referral

## 한국어 (Korean)

AI 에이전트를 위한 러시아어 데이터 API. x402(HTTP 402) 종량제, Base 체인 USDC 결제. API 키·계정·구독 불필요. 현재 **13**개 엔드포인트 사용 가능.

- **법인 조회**：`POST /v1/inn-lookup`（$0.01）— ИНН으로 러시아 법인 확인（ЕГРЮЛ/ФНС 공식 데이터）
- **자영업자(НПД) 확인**：`POST /v1/fns-npd-check`（$0.01）
- **페이지 변환**：`POST /v1/ru-page`（$0.01）— LLM용 Markdown
- **러시아 우체국**：`POST /v1/pochta-track`（$0.01，배송 추적）외 5개 엔드포인트（각 $0.01）· **배송 번들 `pochta-delivery`（$0.04，5in1）**
- **금융 데이터**：`cbr-rates`（러시아 중앙은행 환율, $0.008）· `moex-quote`（모스크바 거래소, $0.008）· `ticker`（암호화폐, $0.005）
- **검색 계열 일시 중지**（`ru-search`·`web-search`·`research`·`company-report`·일괄 검색）— 503 응답, 과금 없음
- **추천 프로그램**：다른 에이전트를 소개하면 그 결제액의 20%를 평생 적립 — https://payforapi.com/referral

## Why

- **Cyrillic/RU-native segment in the x402 ecosystem**: EGRUL verification, RU scraping, Russian Post tracking, CBR FX, MOEX quotes — sources English-language APIs miss.
- Keyless for clients: no registration, no API keys — wallet pays, agent gets data.
- Official sources (EGRUL/FNS, Russian Post, CBR, MOEX), legal for resale (129-ФЗ, 262-ФЗ, 44-ФЗ).

## Docs & manifest

- `llms.txt` — machine-readable description for LLMs (EN/中文/日本語/한국어 sections), mirrored 1:1 from production
- `/.well-known/x402.json` — x402 discovery manifest (i18n: ru/en/zh/ja/ko), 13 payable resources
- `/openapi.json` — OpenAPI spec
- `https://payforapi.com/referral` — referral program page (live counter per wallet)

## License

MIT — see [LICENSE](LICENSE).

© 2026 Saymon / Real Energy.
