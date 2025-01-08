FROM node:18-slim as builder

# Install Python and other dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN poetry install --no-dev
RUN npm install

# Build the application
RUN npm run build

# Production image
FROM node:18-slim

WORKDIR /app

# Copy built assets from builder
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.venv ./.venv
COPY package.json .

EXPOSE 3000
CMD ["npm", "start"] 