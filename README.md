# Saymon RU Data API

> 🇷🇺 Российские данные для AI-агентов · 🇨🇳 面向AI代理的俄罗斯数据API · 🇯🇵 AIエージェント向けロシア語データAPI · 🇰🇷 AI 에이전트를 위한 러시아어 데이터 API

**The only legal window into the Russian market for AI agents.** Russian-language (Runet) data: state-registry company checks, Runet search, Russian Post delivery, CBR/MOEX market data. Pay per request in USDC via **x402** (HTTP 402 Payment Required). **No API keys, no accounts, no subscriptions.**

Base URL: `https://payforapi.com` · MCP: `https://payforapi.com/mcp` · Health: `https://payforapi.com/health` · Manifest: `https://payforapi.com/.well-known/x402.json`

Network: Base mainnet (`eip155:8453`) · Asset: USDC · Facilitator: `https://x402.primer.systems`

## Endpoints (20)

| Endpoint | Price | Description |
|---|---|---|
| `POST /v1/inn-lookup` | $0.01 | **Russian company check by INN** — official EGRUL state registry, unavailable to foreign checkers (merchant KYB before a deal). |
| `POST /v1/fns-npd-check` | $0.01 | **RU self-employed (NPD) status** by INN via FNS. Run before paying a contractor. |
| `POST /v1/ru-search` | $0.02 | **Runet search** (Russian-language internet) via Yandex — products, prices, sellers, reviews English engines miss. The only legal window into the Russian market. |
| `POST /v1/web-search` | $0.02 | Global web search (Tavily) — the Western half of the pair with Runet search: sources the runet lacks. |
| `POST /v1/ru-page` | $0.01 | Clean **Russian-language page** → LLM-ready Markdown (trafilatura): product card, store, news. |
| `POST /v1/research` | $0.02 | **Runet dossier**: search + top pages in one Markdown report — seller, product, company. |
| `POST /v1/research/deep` | $0.05 | **Deep Runet dossier**: 3 searches + up to 10 pages — RU courts, media, registries. Vet before a large order. |
| `POST /v1/company-report` | $0.05 | **KYB dossier in one payment**: official EGRUL check + NPD status + deep Runet dossier — 3 services for the price of the dossier (vs $0.07 retail). |
| `POST /v1/ru-search/x10` | $0.18 | **Bulk Runet search**: up to 10 queries in one payment (10% off vs single calls). |
| `POST /v1/ru-search/x100` | $1.60 | **Bulk Runet search**: up to 100 queries in one payment (20% off) — catalogs, suppliers, price monitoring. |
| `POST /v1/pochta-tariff` | $0.01 | **Russian Post**: delivery cost between postcodes (official API) — shipping math for checkout. |
| `POST /v1/pochta-track` | $0.01 | **Russian Post**: parcel tracking by track number (SOAP) — the only legal RU tracking. |
| `POST /v1/pochta-delivery-time` | $0.01 | **Russian Post**: control delivery times between postcodes (days). |
| `POST /v1/pochta-offices` | $0.01 | **Russian Post**: offices by postcode or coordinates — pickup points. |
| `POST /v1/pochta-zip` | $0.01 | **Russian postal codes** by address or office. |
| `POST /v1/pochta-address` | $0.01 | **RU address normalization** to Russian Post standard (index, region, street, house). |
| `POST /v1/pochta-delivery` | $0.04 | **Russian Post delivery bundle**: address + postcode + office + rate + time in one payment (5 services in 1). |
| `POST /v1/ticker` | $0.005 | Bybit spot crypto tickers: last price, 24h change, volume. |
| `POST /v1/cbr-rates` | $0.008 | **Central Bank of Russia** official daily FX rates (USD, EUR, CNY…) — state reference for RUB pricing. |
| `POST /v1/moex-quote` | $0.008 | **Moscow Exchange** quotes: stocks (SBER, GAZP…), FX pairs, indices (IMOEX) — live Russian market data. |

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
# 1. Unpaid request -> 402 Payment Required
curl -X POST https://payforapi.com/v1/inn-lookup \
  -H "Content-Type: application/json" -d '{"inn": "7707083893"}'

# 2. Sign EIP-3009 transferWithAuthorization for USDC (Base) to payTo from the 402 response
# 3. Resend with PAYMENT-SIGNATURE header -> 200 OK + payment-response
```

## MCP

Remote MCP server (streamable-http): `https://payforapi.com/mcp` — 15 tools: `inn_lookup`, `ru_search`, `ru_page`, `ru_research`, `ru_research_deep`, `company_report`, `cbr_rates`, `moex_quote`, `pochta_tariff`, `pochta_track`, `pochta_delivery_time`, `pochta_offices`, `pochta_zip`, `pochta_address`, `pochta_delivery`. Agents pay via `_meta["x402/payment"]`.

## Also available via PayAPI Market

The same 20 routes are listed on the [PayAPI Market](https://payapi.market) warehouse — agents can discover and call them from there as well as from payforapi.com. Same x402 payment (USDC on Base to the same seller wallet), no extra fees.

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

面向AI代理的俄罗斯数据API。按次付费（x402 / HTTP 402），Base链USDC结算。无需注册、无需API密钥、无订阅。

- **企业核实**：`POST /v1/inn-lookup`（$0.01）— 通过ИНН查询俄罗斯企业（ЕГРЮЛ/ФНС官方数据）：ОГРН、КПП、负责人、注册日期、地区
- **个体户（НПД）状态核实**：`POST /v1/fns-npd-check`（$0.01）
- **俄语搜索**：`POST /v1/ru-search`（$0.02）· 全球搜索 `web-search`（$0.02）
- **俄语网页转Markdown**：`POST /v1/ru-page`（$0.01）
- **研究包**：`POST /v1/research`（$0.02）· `POST /v1/research/deep`（$0.05）— 供应商/客户尽调
- **KYB尽调包**：`POST /v1/company-report`（$0.05）— ЕГРЮЛ核实+НПД状态+深度俄网报告
- **批量俄语搜索**：`POST /v1/ru-search/x10`（$0.18）· `POST /v1/ru-search/x100`（$1.60）
- **俄罗斯邮政**：`POST /v1/pochta-track`（$0.01，包裹跟踪）· `pochta-tariff` · `pochta-delivery-time` · `pochta-offices` · `pochta-zip` · `pochta-address`（各$0.01）· **投递包 `pochta-delivery`（$0.04，5合1）**
- **金融数据**：`cbr-rates`（央行汇率，$0.008）· `moex-quote`（莫斯科交易所报价，$0.008）· `ticker`（加密货币，$0.005）
- **推荐计划**：带来其他代理，终身获其付费调用收入的 20% — https://payforapi.com/referral

中俄贸易背景下的应用：进口商/出口商在交易前核验俄方企业真实性，物流团队跟踪俄罗斯邮政包裹（17TRACK等免费平台无API接口，本服务提供按次计费的机器可读API）。

## 日本語 (Japanese)

AIエージェント向けロシア語データAPI。x402（HTTP 402）従量課金、BaseチェーンUSDC。APIキー・アカウント・サブスク不要。

- **法人照会**：`POST /v1/inn-lookup`（$0.01）— ИННによるロシア法人確認（ЕГРЮЛ/ФНС公式データ）
- **個人事業主（НПД）確認**：`POST /v1/fns-npd-check`（$0.01）
- **ロシア語検索**：`POST /v1/ru-search`（$0.02）· グローバル検索 `web-search`（$0.02）
- **ページ変換**：`POST /v1/ru-page`（$0.01）— LLM対応Markdown
- **リサーチ**：`POST /v1/research`（$0.02）· `/v1/research/deep`（$0.05）
- **KYBパック**：`POST /v1/company-report`（$0.05）— 法人確認+НПД+ロシア語ディープ調査を一括
- **一括ロシア語検索**：`POST /v1/ru-search/x10`（$0.18）· `/v1/ru-search/x100`（$1.60）
- **ロシア郵便**：`POST /v1/pochta-track`（$0.01，追跡）ほか5エンドポイント（各$0.01）· **配送バンドル `pochta-delivery`（$0.04，5in1）**
- **金融データ**：`cbr-rates`（中央銀行為替，$0.008）· `moex-quote`（モスクワ取引所，$0.008）· `ticker`（仮想通貨，$0.005）
- **紹介プログラム**：他エージェントを紹介すると、その支払いの20%を生涯獲得 — https://payforapi.com/referral

## 한국어 (Korean)

AI 에이전트를 위한 러시아어 데이터 API. x402(HTTP 402) 종량제, Base 체인 USDC 결제. API 키·계정·구독 불필요.

- **법인 조회**：`POST /v1/inn-lookup`（$0.01）— ИНН으로 러시아 법인 확인（ЕГРЮЛ/ФНС 공식 데이터）
- **자영업자(НПД) 확인**：`POST /v1/fns-npd-check`（$0.01）
- **러시아어 검색**：`POST /v1/ru-search`（$0.02）· 글로벌 검색 `web-search`（$0.02）
- **페이지 변환**：`POST /v1/ru-page`（$0.01）— LLM용 Markdown
- **리서치**：`POST /v1/research`（$0.02）· `/v1/research/deep`（$0.05）
- **KYB 패키지**：`POST /v1/company-report`（$0.05）— 법인확인+НПД+러시아어 딥 리포트 일괄
- **일괄 러시아어 검색**：`POST /v1/ru-search/x10`（$0.18）· `/v1/ru-search/x100`（$1.60）
- **러시아 우체국**：`POST /v1/pochta-track`（$0.01，배송 추적）외 5개 엔드포인트（각 $0.01）· **배송 번들 `pochta-delivery`（$0.04，5in1）**
- **금융 데이터**：`cbr-rates`（러시아 중앙은행 환율, $0.008）· `moex-quote`（모스크바 거래소, $0.008）· `ticker`（암호화폐, $0.005）
- **추천 프로그램**：다른 에이전트를 소개하면 그 결제액의 20%를 평생 적립 — https://payforapi.com/referral

## Why

- **Only Cyrillic/RU-native segment in the x402 ecosystem**: EGRUL verification, Russian web search, RU scraping, Russian Post tracking, CBR FX, MOEX quotes.
- Keyless for clients: no registration, no API keys — wallet pays, agent gets data.
- Official sources (EGRUL/FNS, Russian Post, CBR, MOEX), legal for resale (129-ФЗ, 262-ФЗ, 44-ФЗ).

## Docs & manifest

- `llms.txt` — machine-readable description for LLMs (EN/中文/日本語/한국어 sections)
- `/.well-known/x402.json` — x402 discovery manifest (i18n: ru/en/zh/ja/ko)
- `/openapi.json` — OpenAPI spec

- `https://payforapi.com/referral` — referral program page (live counter per wallet)

© 2026 Saymon / Real Energy.
