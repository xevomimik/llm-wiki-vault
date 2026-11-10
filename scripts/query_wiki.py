#!/usr/bin/env python3
"""
Query Wiki - Semantic Search + Cite
Searches wiki content and returns cited results.
In production, uses embeddings. Here uses text search for demo.
"""
import sys
import re
from pathlib import Path

VAULT_ROOT = Path(__file__).parent.parent
WIKI_DIR = VAULT_ROOT / "wiki"

def search_wiki(query, limit=10):
    """Simple text search over wiki files. Replace with embeddings in production."""
    query_lower = query.lower()
    results = []
    
    for md_file in WIKI_DIR.rglob("*.md"):
        if md_file.name == "index.md":
            continue
        content = md_file.read_text(encoding="utf-8")
        
        # Score by frequency of query terms
        score = 0
        for term in query_lower.split():
            score += content.lower().count(term)
        
        if score > 0:
            rel_path = md_file.relative_to(VAULT_ROOT)
            # Extract summary
            summary = ""
            for line in content.split("\n"):
                if line.startswith("## Summary"):
                    continue
                if line.strip() and not line.startswith("#"):
                    summary = line.strip()[:200]
                    break
            
            results.append({
                "path": str(rel_path),
                "title": md_file.stem,
                "score": score,
                "summary": summary,
            })
    
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]

def format_result(result):
    """Format a single result for display."""
    return f"""
📄 **{result['title']}** (score: {result['score']})
   Path: {result['path']}
   Summary: {result['summary']}
"""

def main():
    if len(sys.argv) < 2:
        print("Usage: query_wiki.py \"search query\" [limit]")
        sys.exit(1)
    
    query = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    print(f"🔍 Searching wiki for: \"{query}\"")
    results = search_wiki(query, limit)
    
    if not results:
        print("No results found.")
        return
    
    print(f"\nFound {len(results)} results:\n")
    for r in results:
        print(format_result(r))

if __name__ == "__main__":
    main()
