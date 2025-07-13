#!/bin/bash

# LinkedIn Monitor - Mac Installation Script
# This script sets up the LinkedIn monitor on macOS

set -e  # Exit on any error

echo "🍎 LinkedIn Monitor - Mac Installation"
echo "======================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is designed for macOS only."
    exit 1
fi

print_status "Checking system requirements..."

# Check macOS version
MACOS_VERSION=$(sw_vers -productVersion)
print_status "macOS version: $MACOS_VERSION"

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    print_warning "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for this session
    if [[ -f "/opt/homebrew/bin/brew" ]]; then
        export PATH="/opt/homebrew/bin:$PATH"
    elif [[ -f "/usr/local/bin/brew" ]]; then
        export PATH="/usr/local/bin:$PATH"
    fi
    print_success "Homebrew installed successfully"
else
    print_success "Homebrew is already installed"
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_warning "Python 3 not found. Installing Python 3..."
    brew install python@3.11
    print_success "Python 3 installed successfully"
else
    PYTHON_VERSION=$(python3 --version)
    print_success "Python 3 is already installed: $PYTHON_VERSION"
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    print_warning "pip3 not found. Installing pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
    print_success "pip installed successfully"
else
    print_success "pip3 is already installed"
fi

# Create virtual environment
print_status "Setting up Python virtual environment..."
if [[ ! -d "venv" ]]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt
print_success "Dependencies installed successfully"

# Setup configuration
print_status "Setting up configuration..."
if [[ ! -f ".env" ]]; then
    if [[ -f "config.env.example" ]]; then
        cp config.env.example .env
        print_success "Configuration file created (.env)"
        print_warning "Please edit .env file with your API keys:"
        echo "   - SERPAPI_KEY: Get from https://serpapi.com/"
        echo "   - SLACK_WEBHOOK_URL: Get from your Slack workspace"
        echo "   - SEARCH_TERMS: Add the terms you want to monitor"
    else
        print_error "config.env.example not found"
        exit 1
    fi
else
    print_warning ".env file already exists. Skipping configuration setup."
fi

# Make scripts executable
print_status "Setting up executable permissions..."
chmod +x setup_mac.sh
chmod +x install.sh

# Create a convenient run script
print_status "Creating run script..."
cat > run_monitor.sh << 'EOF'
#!/bin/bash
# LinkedIn Monitor - Run Script for Mac
echo "🚀 Starting LinkedIn Monitor..."
source venv/bin/activate
python3 linkedin_monitor.py
EOF

chmod +x run_monitor.sh

# Create a demo script
print_status "Creating demo script..."
cat > run_demo.sh << 'EOF'
#!/bin/bash
# LinkedIn Monitor - Demo Script for Mac
echo "🎮 Running LinkedIn Monitor Demo..."
source venv/bin/activate
python3 demo.py
EOF

chmod +x run_demo.sh

echo
print_success "🎉 Installation complete!"
echo
echo "📋 Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run the monitor: ./run_monitor.sh"
echo "3. Try the demo: ./run_demo.sh"
echo
echo "📚 For help, see README.md"
echo
echo "🔗 Quick commands:"
echo "   ./run_monitor.sh    - Start the monitor"
echo "   ./run_demo.sh       - Run the demo"
echo "   source venv/bin/activate  - Activate virtual environment"
echo "   deactivate          - Deactivate virtual environment"
echo

# Check if user wants to run the demo
read -p "Would you like to run the demo now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Running demo..."
    source venv/bin/activate
    python3 demo.py
fi

print_success "Setup complete! 🎉" 