FROM python:3.13-slim-bookworm AS builder
COPY --from=ghcr.io/astral-sh/uv:0.11.8 /uv /uvx /bin/

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    UV_LINK_MODE=copy

# Change workdir
WORKDIR /app

# Install dependencies and compile into bytecode
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev --compile-bytecode


FROM python:3.13-slim-bookworm AS runner

# Set workdir
WORKDIR /app

RUN groupadd -r runner && useradd --no-log-init -r -g runner runner \
    && mkdir -p /app/data && chown -R runner:runner /app/data

COPY --from=builder --chown=runner:runner /app/.venv /app/.venv

COPY --chown=runner:runner src /app/src

USER runner

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src" \
    DATA_DIR="/app/data"

VOLUME ["/app/data"]

CMD ["python", "-m", "tpl_scraping"]