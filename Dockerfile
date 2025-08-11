FROM python:3.12-slim

# Install system dependencies including bash
RUN apt-get update && apt-get install -y \
    git \
    curl \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.7.12 /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy project files and install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# Copy source code
COPY ./src /app/src
COPY .env.sample /app/

# Create nonroot user with bash shell
ARG USER_UID=1000
ARG USER_GID=1000
RUN groupadd nonroot \
    && useradd -u ${USER_UID} -g nonroot -m -s /bin/bash nonroot \
    && chown -R nonroot:nonroot /app
USER nonroot

# Set environment variables
ENV PATH="/app/.venv/bin:${PATH}"
ENV PYTHONPATH=/app/src

# Use bash as default command for interactive use
CMD ["/bin/bash"]