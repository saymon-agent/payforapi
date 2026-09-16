# Builds the Saymon RU Data API stdio MCP server.
#
# Used by Glama (and anyone else) to run the server in a container: it starts and
# answers MCP introspection (initialize / tools/list) with no network and no
# secrets required, because the tool catalogue ships inside tools.json.
# Actual tool calls are proxied to the hosted x402 endpoint (USDC on Base).
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PAYFORAPI_MCP_URL=https://payforapi.com/mcp

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY tools.json server.py ./

ENTRYPOINT ["python", "server.py"]
