#!/bin/bash
# Build Phoenix Auction for Coreum (no bulk memory)

set -e

echo "=== Setting up environment ==="

# Clean previous builds
cargo clean
rm -f Cargo.lock

# Use specific Rust version that doesn't enable bulk memory by default
# Rust 1.59.0 (March 2022) is safe
RUST_VERSION=1.59.0
echo "Using Rust $RUST_VERSION"

# Set explicit compile flags
export RUSTFLAGS="-C target-feature=-bulk-memory,-reference-types,-simd128,-sign-ext"
export CARGO_PROFILE_RELEASE_OPT_LEVEL="z"
export CARGO_PROFILE_RELEASE_LTO="fat"
export CARGO_PROFILE_RELEASE_CODEGEN_UNITS=1
export CARGO_PROFILE_RELEASE_PANIC="abort"
export CARGO_PROFILE_RELEASE_STRIP="symbols"

echo "=== Building ==="
cargo +$RUST_VERSION build --release --target wasm32-unknown-unknown

echo "=== Checking result ==="
WASM_FILE="target/wasm32-unknown-unknown/release/phoenix_auction.wasm"
if [ -f "$WASM_FILE" ]; then
    echo "✅ Build successful!"
    ls -lh "$WASM_FILE"
    
    # Verify no bulk memory
    echo "=== Checking for bulk memory ==="
    if hexdump -C "$WASM_FILE" | grep -q " fc "; then
        echo "⚠ WARNING: Still contains bulk memory ops"
    else
        echo "✅ No bulk memory ops found"
    fi
    
    # Copy to artifacts
    cp "$WASM_FILE" "artifacts/coreum_compatible_$(date +%s).wasm"
else
    echo "❌ Build failed"
    exit 1
fi
