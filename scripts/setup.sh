#!/bin/bash
# Academic Grievance DSS - One-Command Setup Script
# This script sets up the entire development environment

set -e  # Exit on error

echo "🎓 Academic Grievance Decision Support System"
echo "=============================================="
echo "Setting up proof-of-concept environment..."
echo ""

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC}  $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "ℹ  $1"
}

# Step 1: Check prerequisites
echo "Step 1/7: Checking prerequisites..."
echo "-----------------------------------"

# Check Docker
if command -v docker >/dev/null 2>&1; then
    DOCKER_VERSION=$(docker --version | cut -d ' ' -f3 | cut -d ',' -f1)
    print_success "Docker found (version $DOCKER_VERSION)"
else
    print_error "Docker not found. Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check Java
if command -v java >/dev/null 2>&1; then
    JAVA_VERSION=$(java -version 2>&1 | head -n 1 | cut -d '"' -f2)
    print_success "Java found (version $JAVA_VERSION)"
else
    print_error "Java not found. Please install OpenJDK 17: https://openjdk.org/install/"
    exit 1
fi

# Check Python
if command -v python3 >/dev/null 2>&1; then
    PYTHON_VERSION=$(python3 --version | cut -d ' ' -f2)
    print_success "Python found (version $PYTHON_VERSION)"
else
    print_error "Python 3.11+ not found. Please install: https://www.python.org/downloads/"
    exit 1
fi

# Check Node.js
if command -v node >/dev/null 2>&1; then
    NODE_VERSION=$(node --version | cut -d 'v' -f2)
    print_success "Node.js found (version $NODE_VERSION)"
else
    print_error "Node.js not found. Please install: https://nodejs.org/"
    exit 1
fi

# Check Maven
if command -v mvn >/dev/null 2>&1; then
    MVN_VERSION=$(mvn --version | head -n 1 | cut -d ' ' -f3)
    print_success "Maven found (version $MVN_VERSION)"
else
    print_error "Maven not found. Please install: https://maven.apache.org/install.html"
    exit 1
fi

echo ""

# Step 2: Build Java components
echo "Step 2/7: Building Java components..."
echo "--------------------------------------"
cd java-bridge

if [ -f "pom.xml" ]; then
    print_info "Compiling Java classes and packaging JAR..."
    mvn clean package -q
    if [ $? -eq 0 ]; then
        print_success "Java components built successfully"
    else
        print_error "Java build failed"
        exit 1
    fi
else
    print_warning "pom.xml not found, skipping Java build"
fi

cd ..
echo ""

# Step 3: Install Python dependencies
echo "Step 3/7: Installing Python dependencies..."
echo "--------------------------------------------"
cd backend

if [ -f "requirements.txt" ]; then
    print_info "Installing Python packages..."
    python3 -m pip install -r requirements.txt -q
    if [ $? -eq 0 ]; then
        print_success "Python dependencies installed"
    else
        print_error "Python installation failed"
        exit 1
    fi
else
    print_warning "requirements.txt not found, skipping Python install"
fi

cd ..
echo ""

# Step 4: Install frontend dependencies
echo "Step 4/7: Installing frontend dependencies..."
echo "----------------------------------------------"
cd frontend

if [ -f "package.json" ]; then
    print_info "Installing Node.js packages..."
    npm install --silent
    if [ $? -eq 0 ]; then
        print_success "Frontend dependencies installed"
    else
        print_error "npm install failed"
        exit 1
    fi
else
    print_warning "package.json not found, skipping npm install"
fi

cd ..
echo ""

# Step 5: Start Docker services
echo "Step 5/7: Starting PostgreSQL database..."
echo "------------------------------------------"
print_info "Starting Docker containers..."
docker-compose up -d postgres

if [ $? -eq 0 ]; then
    print_success "PostgreSQL container started"
else
    print_error "Failed to start PostgreSQL"
    exit 1
fi

echo ""

# Step 6: Initialize database
echo "Step 6/7: Initializing database..."
echo "-----------------------------------"
print_info "Waiting for PostgreSQL to be ready..."
sleep 5

# Check if database is ready
docker exec grievance-postgres pg_isready -U grievance_user -d grievance_db > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_success "Database is ready"
    
    # Run initialization script
    print_info "Running database initialization..."
    docker exec -i grievance-postgres psql -U grievance_user -d grievance_db < database/init.sql > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        print_success "Database schema created"
    fi
    
    # Run seed script
    print_info "Seeding database with sample data..."
    docker exec -i grievance-postgres psql -U grievance_user -d grievance_db < database/seed.sql > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        print_success "Database seeded successfully"
    fi
else
    print_warning "Database not ready yet, you may need to run init scripts manually"
fi

echo ""

# Step 7: Configure environment
echo "Step 7/7: Configuring environment..."
echo "-------------------------------------"
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_success "Created .env file from template"
    print_warning "Please add your OpenAI API key to .env file:"
    print_warning "  OPENAI_API_KEY=sk-your-api-key-here"
else
    print_info ".env file already exists"
fi

echo ""
echo "=============================================="
echo -e "${GREEN}✅ Setup complete!${NC}"
echo "=============================================="
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Add your OpenAI API key to .env file:"
echo "   nano .env"
echo ""
echo "2. Start the backend server:"
echo "   cd backend"
echo "   uvicorn main:app --reload"
echo ""
echo "3. In a new terminal, start the frontend:"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "4. Access the application:"
echo "   Web UI:  http://localhost:3000"
echo "   API:     http://localhost:8000/docs"
echo ""
echo "5. Run tests:"
echo "   cd backend"
echo "   pytest tests/ -v --cov=."
echo ""
echo "📚 Documentation: See README.md for more details"
echo ""
