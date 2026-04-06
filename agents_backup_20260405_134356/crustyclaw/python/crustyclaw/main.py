#!/usr/bin/env python3
"""CrustyClaw - Bug detection and code audit"""

import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(description="CrustyClaw AI Assistant")
    parser.add_argument("--ask", "-a", help="Ask a question")
    parser.add_argument("--pinch", "-p", help="Pinch a directory")
    parser.add_argument("--audit", help="Audit a directory")
    
    args = parser.parse_args()
    
    if args.ask:
        print(f"🤖 CrustyClaw: {args.ask}")
        print("   (AI response would go here)")
    elif args.pinch:
        print(f"🦞 Pinching {args.pinch}...")
        # Call the Rust binary
        rust_binary = os.path.expanduser("~/dev/crustyclaw/target/release/crustyclaw")
        if os.path.exists(rust_binary):
            os.system(f"{rust_binary} pinch {args.pinch}")
        else:
            print("⚠️ Rust binary not found. Run: cd ~/dev/crustyclaw && cargo build --release")
    elif args.audit:
        print(f"🔍 Auditing {args.audit}...")
        rust_binary = os.path.expanduser("~/dev/crustyclaw/target/release/crustyclaw")
        if os.path.exists(rust_binary):
            os.system(f"{rust_binary} audit {args.audit}")
        else:
            print("⚠️ Rust binary not found. Run: cd ~/dev/crustyclaw && cargo build --release")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
