#!/bin/bash
# Claw-Coder Installation Script for Laptop

set -e

echo "🦞 Installing Claw-Coder..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.10+"
    exit 1
fi

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo "📦 Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Install Python dependencies
echo "📦 Installing Python packages..."
pip3 install -r requirements.txt

# Make scripts executable
chmod +x *.py *.sh 2>/dev/null || true

echo "✅ Installation complete!"
echo ""
echo "To run:"
echo "  ./run_all_agents.sh     # Run all agents"
echo "  ollama serve            # Start Ollama (if not running)"

# Optional model setup
echo ""
read -p "Setup AI models? (y/n): " setup_models
if [[ $setup_models == "y" ]]; then
    ./setup_models.sh
fi
