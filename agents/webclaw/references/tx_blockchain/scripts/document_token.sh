#!/bin/bash
set -e

echo "📝 Creating TESTUSD token documentation..."

# Create docs directory if it doesn't exist
mkdir -p docs

# Create the main token documentation
cat > docs/TESTUSD_TOKEN_CREATION.md << 'DOCEOF'
# TESTUSD Token - Live on Coreum Testnet ✅

## 🎉 Successfully Created!
**Date:** $(date)
**Transaction:** 37EC84596A02687D8F77E7D92538F518CCE847D8B4A325732B911FD0B0D35E9A

## Token Details
- **Symbol:** TESTUSD
- **Denom:** utestusd-testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6
- **Decimals:** 6
- **Initial Supply:** 1000 tokens
- **Issuer:** testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6

## Current Distribution
- **Issuer Wallet:** 900 TESTUSD
- **Test Wallet (testcore1u5mnmlezme6nw9d9xtk086p2az9jk96syrnn67):** 100 TESTUSD

## Status: ✅ OPERATIONAL
Token is live, transferable, and visible in Leap Wallet.

## Wallet Configuration
For Leap Wallet:
- **Coin minimal denom:** utestusd-testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6
- **Coin denom:** TESTUSD
- **Coin decimals:** 6

## Next Steps for PhoenixPME
With TESTUSD operational, development focuses on:
1. Auction smart contract (1.1% fee enforcement)
2. Backend blockchain integration
3. Frontend token interaction
DOCEOF

echo "✅ Created docs/TESTUSD_TOKEN_CREATION.md"

# Update README if it exists
if [ -f README.md ]; then
    echo "📖 Updating README.md..."
    
    # Check if we already have a token section
    if ! grep -q "TESTUSD Token" README.md; then
        # Add token section at the end
        echo "" >> README.md
        echo "## 🪙 TESTUSD Token Status" >> README.md
        echo "" >> README.md
        echo "✅ **LIVE ON COREM TESTNET**" >> README.md
        echo "" >> README.md
        echo "The foundation token for PhoenixPME auctions is now operational." >> README.md
        echo "" >> README.md
        echo "- **Symbol:** TESTUSD" >> README.md
        echo "- **Denom:** \`utestusd-testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6\`" >> README.md
        echo "- **Decimals:** 6" >> README.md
        echo "- **Created:** $(date)" >> README.md
        echo "- **Transaction:** [37EC84...5E9A](https://explorer.testnet-1.coreum.dev/coreum/transaction/37EC84596A02687D8F77E7D92538F518CCE847D8B4A325732B911FD0B0D35E9A)" >> README.md
        echo "" >> README.md
        echo "See [docs/TESTUSD_TOKEN_CREATION.md](docs/TESTUSD_TOKEN_CREATION.md) for details." >> README.md
    fi
    
    echo "✅ Updated README.md"
else
    echo "⚠️ README.md not found - creating basic one"
    echo "# PhoenixPME" > README.md
    echo "## 🪙 TESTUSD Token Status" >> README.md
    echo "✅ **LIVE ON COREM TESTNET**" >> README.md
fi

echo ""
echo "🎉 Documentation created successfully!"
echo "Files:"
ls -la docs/
echo ""
echo "To commit to GitHub:"
echo "  git add docs/ README.md"
echo "  git commit -m 'docs: Add TESTUSD token documentation'"
echo "  git push"
