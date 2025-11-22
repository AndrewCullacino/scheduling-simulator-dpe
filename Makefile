.PHONY: run build stop dev clean

# Run the full application using Docker Compose
run:
	@echo "🚀 Starting Scheduling Simulator..."
	docker-compose up --build

# Build the containers without starting
build:
	@echo "🔨 Building containers..."
	docker-compose build

# Stop all running services
stop:
	@echo "🛑 Stopping services..."
	docker-compose down

# Run in development mode (local python/node)
dev:
	@echo "⚠️  Starting in DEV mode (requires Python & Node.js installed locally)"
	@echo "Starting Backend..."
	@(cd backend && source ../.venv/bin/activate && uvicorn app.main:app --reload --port 8000) &
	@echo "Starting Frontend..."
	@(cd frontend && npm run dev)

# Clean up containers and images
clean:
	docker-compose down --rmi all --volumes --remove-orphans
