"""
Knowledge base with indexed online references for all supported languages
"""

KNOWLEDGE_BASE = {
    # Rust Ecosystem
    "rust": {
        "book": "https://doc.rust-lang.org/book/",
        "std": "https://doc.rust-lang.org/std/",
        "crates": "https://crates.io/",
        "rust_by_example": "https://doc.rust-lang.org/rust-by-example/",
        "rust_nomicon": "https://doc.rust-lang.org/nomicon/",
        "rust_embedded": "https://docs.rust-embedded.org/book/",
    },
    
    # CosmWasm
    "cosmwasm": {
        "book": "https://book.cosmwasm.com/",
        "docs": "https://docs.cosmwasm.com/",
        "github": "https://github.com/CosmWasm/cosmwasm",
        "cw_plus": "https://github.com/CosmWasm/cw-plus",
        "wasmd": "https://github.com/CosmWasm/wasmd",
    },
    
    # TX Blockchain
    "tx": {
        "main_docs": "https://docs.tx.org/",
        "general_overview": "https://docs.tx.org/docs/next/overview/general",
        "smart_tokens": "https://docs.tx.org/docs/next/overview/smart-tokens",
        "bridge_docs": "https://docs.tx.org/docs-bridge/overview",
        "run_full_node": "https://docs.tx.org/docs/next/nodes-and-validators/run-full-node",
        "community": "https://tx.org/community",
        "ecosystem_projects": "https://tx.org/projects",
        "team": "https://tx.org/tx-team",
        "github": "https://github.com/tx-org",
        "explorer": "https://explorer.tx.org/",
    },
    
    # General Resources
    "general": {
        "stackoverflow": "https://stackoverflow.com/",
        "github": "https://github.com/",
        "freecodecamp": "https://www.freecodecamp.org/",
        "w3schools": "https://www.w3schools.com/",
    }
}

def get_references(language: str) -> dict:
    """Get references for a specific language"""
    return KNOWLEDGE_BASE.get(language.lower(), KNOWLEDGE_BASE["general"])

def list_languages() -> list:
    """List all languages with references"""
    return list(KNOWLEDGE_BASE.keys())

def search_references(query: str) -> list:
    """Search for relevant references based on query"""
    results = []
    query_lower = query.lower()
    
    for lang, refs in KNOWLEDGE_BASE.items():
        if lang in query_lower:
            for name, url in refs.items():
                results.append(f"[{lang.upper()}] {name}: {url}")
    
    if not results:
        for name, url in KNOWLEDGE_BASE["general"].items():
            results.append(f"[General] {name}: {url}")
    
    return results
