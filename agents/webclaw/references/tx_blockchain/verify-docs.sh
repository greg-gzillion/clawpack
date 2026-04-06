#!/bin/bash
# Verify all documentation files exist

echo "🔍 TX Documentation Verification"
echo "================================"
echo ""

# Count markdown files
MD_COUNT=$(find ~/dev/TXdocumentation -name "*.md" | wc -l)
echo "📄 Total markdown files: $MD_COUNT"

# Count by category
echo ""
echo "📁 By category:"
echo "  Nodes: $(find ~/dev/TXdocumentation/nodes -name "*.md" 2>/dev/null | wc -l)"
echo "  Tutorials: $(find ~/dev/TXdocumentation/tutorials -name "*.md" 2>/dev/null | wc -l)"
echo "  Modules: $(ls -d ~/dev/TXdocumentation/modules/*/ 2>/dev/null | wc -l)"
echo "  Root: $(find ~/dev/TXdocumentation -maxdepth 1 -name "*.md" | wc -l)"

# Check critical files
echo ""
echo "✅ Critical files:"
for file in README.md VISION.md MANIFESTO.md; do
    if [ -f "$HOME/dev/TXdocumentation/$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file MISSING"
    fi
done

echo ""
echo "🎯 AI Agent ready to learn TX Blockchain!"
