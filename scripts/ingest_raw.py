#!/usr/bin/env python3
"""
Ingest Raw Sources → Wiki
Watches raw/ directory, extracts concepts to wiki/ with citations.
Run manually or as a file watcher.
"""
import json
import subprocess
import time
import re
import sys
import os
from pathlib import Path

VAULT_ROOT = Path(__file__).parent.parent
RAW_DIR = VAULT_ROOT / "raw"
WIKI_DIR = VAULT_ROOT / "wiki"
PROPOSED_DIR = VAULT_ROOT / "proposed"
INDEX_FILE = WIKI_DIR / "index.md"

CATEGORIES = {
    "youtube": "sources",
    "papers": "sources",
    "web": "sources",
}

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "timeout", 124
    except Exception as e:
        return "", str(e), 1

def strip_ansi(text):
    """Remove ANSI escape codes"""
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m|\x1b\[[0-9;]*[A-Z]|\x1b\[[?0-9]*[hl]|\x1b[@-Z\\-_]|\x1b\][0-9];[^\x07]*\x07|\x1b\][0-9];[^\x1b]*\x1b\\')
    return ansi_escape.sub('', text)

def extract_concepts(source_path, source_type):
    """
    Extract concepts from raw source.
    In production, this calls an LLM (local or remote).
    Returns list of concept dicts.
    """
    content = source_path.read_text(encoding="utf-8")
    title = source_path.stem
    
    # Simple heuristic extraction for demo
    concepts = []
    if "omniroute" in content.lower():
        concepts.append({
            "name": "OmniRoute",
            "type": "entity",
            "summary": "AI gateway for multi-provider LLMs",
            "source": str(source_path.relative_to(VAULT_ROOT)),
        })
    if "openviking" in content.lower():
        concepts.append({
            "name": "OpenViking",
            "type": "entity",
            "summary": "Context database for AI agents",
            "source": str(source_path.relative_to(VAULT_ROOT)),
        })
    if "llm wiki" in content.lower():
        concepts.append({
            "name": "LLM Wiki",
            "type": "concept",
            "summary": "Shared memory layer methodology",
            "source": str(source_path.relative_to(VAULT_ROOT)),
        })
    return concepts

def write_concept(concept, category):
    """Write concept to wiki/ or proposed/ directory."""
    # Proper pluralization
    plural_map = {
        "entity": "entities",
        "concept": "concepts",
        "project": "projects",
        "source": "sources",
    }
    plural = plural_map.get(concept["type"], concept["type"] + "s")
    target_dir = WIKI_DIR / category / plural
    target_dir.mkdir(parents=True, exist_ok=True)
    
    safe_name = concept["name"].lower().replace(" ", "-")
    file_path = target_dir / f"{safe_name}.md"
    
    is_new = not file_path.exists()
    
    content = f"""# {concept['name']}

**Type:** {concept['type'].title()}  
**Category:** {category}  
**Source:** [{concept['source']}](../{concept['source']})  
**Extracted:** {time.strftime('%Y-%m-%dT%H:%M:%S')}

## Summary
{concept['summary']}

---
*Auto-extracted from [{concept['source']}](../{concept['source']})*
"""
    file_path.write_text(content, encoding="utf-8")
    return file_path, is_new

def update_index():
    """Rebuild index.md from wiki/ structure."""
    lines = ["# LLM Wiki Index\n", "Catalog of all structured knowledge in this wiki. Updated on every ingest.\n"]
    
    for category in ["entities", "concepts", "projects", "sources"]:
        cat_dir = WIKI_DIR / category
        if not cat_dir.exists():
            continue
        lines.append(f"\n## {category.title()}\n")
        for subdir in sorted(cat_dir.iterdir()):
            if not subdir.is_dir():
                continue
            for md_file in sorted(subdir.glob("*.md")):
                title = md_file.stem
                rel_path = md_file.relative_to(WIKI_DIR)
                content = md_file.read_text(encoding="utf-8")
                summary = ""
                for line in content.split("\n"):
                    if line.startswith("## Summary"):
                        continue
                    if line.strip() and not line.startswith("#"):
                        summary = line.strip()[:200]
                        break
                lines.append(f"- [{title}]({rel_path}) — {summary}")
    
    lines.append(f"\n---\n*Last updated: {time.strftime('%Y-%m-%dT%H:%M:%S')}*\n*Total pages: {sum(1 for _ in WIKI_DIR.rglob('*.md'))}*")
    INDEX_FILE.write_text("\n".join(lines), encoding="utf-8")

def main():
    print("🔍 Scanning raw/ for new sources...")
    new_files = 0
    new_concepts = 0
    
    for source_type, category in CATEGORIES.items():
        source_dir = RAW_DIR / source_type
        if not source_dir.exists():
            continue
        for source_file in source_dir.rglob("*"):
            if not source_file.is_file() or source_file.suffix not in [".md", ".txt", ".json"]:
                continue
            
            print(f"  Processing: {source_file.relative_to(VAULT_ROOT)}")
            concepts = extract_concepts(source_file, source_type)
            
            for concept in concepts:
                file_path, is_new = write_concept(concept, category)
                if is_new:
                    new_concepts += 1
                    print(f"    ✅ Created: {file_path.relative_to(VAULT_ROOT)}")
                else:
                    print(f"    🔄 Updated: {file_path.relative_to(VAULT_ROOT)}")
            new_files += 1
    
    if new_concepts > 0:
        print("📝 Updating index.md...")
        update_index()
    
    print(f"\n✅ Done. {new_files} sources processed, {new_concepts} new concepts.")

if __name__ == "__main__":
    main()
