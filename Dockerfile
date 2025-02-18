FROM python:3.12.9

WORKDIR /app

# Copy only the essential files first for Docker layer caching.
COPY pyproject.toml .
COPY . .

# Install system dependencies if any (example)
# RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev  # If needed

# Install project dependencies using pip (and uv)
RUN pip install -U uv && uv pip install .

# Expose the port your application uses
EXPOSE 8000

# Define the command to run when the container starts
# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"] # Example using uvicorn
CMD ["genai_linkedin"]
