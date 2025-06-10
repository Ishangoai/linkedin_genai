FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.7.12 /uv /uvx /bin/

WORKDIR /app

# Copy only the essential files first for Docker layer caching.
COPY pyproject.toml .

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Copy the project into the image
COPY . .

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Expose the port your application uses
EXPOSE 8080

# Define the command to run when the container starts
CMD ["uv", "run", "uvicorn", "src.genai_linkedin.main:app", "--host", "0.0.0.0", "--port", "8080"] # Example using uvicorn
# CMD ["genai_linkedin"]
