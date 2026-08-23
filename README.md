# Saymon RU Data API

> 🇷🇺 Российские данные для AI-агентов · 🇨🇳 面向AI代理的俄罗斯数据API · 🇯🇵 AIエージェント向けロシア語データAPI · 🇰🇷 AI 에이전트를 위한 러시아어 데이터 API

Russian-language data endpoints for AI agents. Pay per request in USDC via **x402** (HTTP 402 Payment Required). **No API keys, no accounts, no subscriptions.**

Base URL: `https://payforapi.com` · MCP: `https://payforapi.com/mcp` · Health: `https://payforapi.com/health` · Manifest: `https://payforapi.com/.well-known/x402.json`

Network: Base mainnet (`eip155:8453`) · Asset: USDC · Facilitator: `https://x402.primer.systems`

## Endpoints

| Endpoint | Price | Description |
|---|---|---|
| `POST /v1/inn-lookup` | $0.01 | Verify Russian legal entity by INN from official EGRUL (Federal Tax Service). Returns INN, OGRN, KPP, name, director, registration date, region. |
| `POST /v1/ru-search` | $0.02 | Cyrillic web search (Yandex Search API upstream). Returns URL, title, snippet. |
| `POST /v1/ru-page` | $0.01 | Russian-language page → clean LLM-ready Markdown (trafilatura). |
| `POST /v1/research` | $0.02 | Research pack: search + top pages in one Markdown dossier. |
| `POST /v1/research/deep` | $0.05 | Deep research: 3 searches + up to 10 pages (full counterparty check). |
| `POST /v1/pochta-tariff` | $0.01 | Russian Post: delivery cost & time between postcodes (official API). |
| `POST /v1/pochta-track` | $0.01 | Russian Post: track a parcel by tracking number (SOAP). |
| `POST /v1/pochta-delivery-time` | $0.01 | Russian Post: delivery time between postcodes (days). |
| `POST /v1/pochta-offices` | $0.01 | Russian Post: offices by postcode or coordinates. |
| `POST /v1/pochta-zip` | $0.01 | Russian Post: office address by postcode. |
| `POST /v1/pochta-address` | $0.01 | Russian Post: Russian address normalization. |

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

## 中文 (Chinese)

面向AI代理的俄罗斯数据API。按次付费（x402 / HTTP 402），Base链USDC结算。无需注册、无需API密钥、无订阅。

- **企业核实**：`POST /v1/inn-lookup`（$0.01）— 通过ИНН查询俄罗斯企业（ЕГРЮЛ/ФНС官方数据）：ОГРН、КПП、负责人、注册日期、地区
- **俄语搜索**：`POST /v1/ru-search`（$0.02）— 西里尔文网页搜索
- **俄语网页转Markdown**：`POST /v1/ru-page`（$0.01）
- **研究包**：`POST /v1/research`（$0.02）· `POST /v1/research/deep`（$0.05）— 供应商/客户尽调
- **俄罗斯邮政**：`POST /v1/pochta-track`（$0.01，包裹跟踪）· `pochta-tariff` · `pochta-delivery-time` · `pochta-offices` · `pochta-zip` · `pochta-address`（各$0.01）

中俄贸易背景下的应用：进口商/出口商在交易前核验俄方企业真实性，物流团队跟踪俄罗斯邮政包裹（17TRACK等免费平台无API接口，本服务提供按次计费的机器可读API）。

## 日本語 (Japanese)

AIエージェント向けロシア語データAPI。x402（HTTP 402）従量課金、BaseチェーンUSDC。APIキー・アカウント・サブスク不要。

- **法人照会**：`POST /v1/inn-lookup`（$0.01）— ИННによるロシア法人確認（ЕГРЮЛ/ФНС公式データ）
- **ロシア語検索**：`POST /v1/ru-search`（$0.02）
- **ページ変換**：`POST /v1/ru-page`（$0.01）— LLM対応Markdown
- **リサーチ**：`POST /v1/research`（$0.02）· `/v1/research/deep`（$0.05）
- **ロシア郵便**：`POST /v1/pochta-track`（$0.01，追跡）ほか5エンドポイント（各$0.01）

## 한국어 (Korean)

AI 에이전트를 위한 러시아어 데이터 API. x402(HTTP 402) 종량제, Base 체인 USDC 결제. API 키·계정·구독 불필요.

- **법인 조회**：`POST /v1/inn-lookup`（$0.01）— ИНН으로 러시아 법인 확인（ЕГРЮЛ/ФНС 공식 데이터）
- **러시아어 검색**：`POST /v1/ru-search`（$0.02）
- **페이지 변환**：`POST /v1/ru-page`（$0.01）— LLM용 Markdown
- **리서치**：`POST /v1/research`（$0.02）· `/v1/research/deep`（$0.05）
- **러시아 우체국**：`POST /v1/pochta-track`（$0.01，배송 추적）외 5개 엔드포인트（각 $0.01）

## Why

- **Only Cyrillic/RU-native segment in the x402 ecosystem**: EGRUL verification, Russian web search, RU scraping, Russian Post tracking.
- Keyless for clients: no registration, no API keys — wallet pays, agent gets data.
- Official sources (EGRUL/FNS, Russian Post), legal for resale (129-ФЗ, 262-ФЗ, 44-ФЗ).

## Docs & manifest

- `llms.txt` — machine-readable description for LLMs (EN/中文/日本語/한국어 sections)
- `/.well-known/x402.json` — x402 discovery manifest (i18n: ru/en/zh/ja/ko)
- `/openapi.json` — OpenAPI spec

© 2026 Saymon / Real Energy.
