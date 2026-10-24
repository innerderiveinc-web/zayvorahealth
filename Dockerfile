# ==============================================================================
# ZAYVORA Health OS™ — Production Container Specification
# Multi-platform (linux/amd64, linux/arm64) Standard OCI Image
# ==============================================================================

FROM python:3.11-slim

LABEL maintainer="ZAYVORA Healthcare Technologies <engineering@zayvorahealth.com>"
LABEL description="ZAYVORA Health OS Classical Medicine & Unani Clinical Platform"
LABEL version="5.0.0"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    APP_HOME=/app

WORKDIR ${APP_HOME}

# Install essential runtime tools (curl for healthchecks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Create non-privileged service user for 21 CFR Part 11 / HIPAA container compliance
RUN groupadd -g 1001 zayvora && \
    useradd -u 1001 -g zayvora -m -s /bin/bash zayvora

# Copy platform source and assets
COPY --chown=zayvora:zayvora . ${APP_HOME}/

# Ensure runtime directories have appropriate permissions
RUN mkdir -p ${APP_HOME}/database ${APP_HOME}/logs && \
    chown -R zayvora:zayvora ${APP_HOME}

# Switch to non-root execution
USER zayvora

# Expose dynamic application port
EXPOSE 8000

# Container healthcheck via platform REST probe
HEALTHCHECK --interval=20s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT}/api/v1/health || exit 1

# Production entrypoint
CMD ["sh", "-c", "python3 services/live_api_server.py ${PORT}"]
