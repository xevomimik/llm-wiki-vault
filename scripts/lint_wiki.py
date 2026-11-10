#!/usr/bin/env python3
"""
Lint Wiki - Link Check, Orphan Detection, Index Update
Run as Git pre-commit hook or manually.
"""
import os
import sys
import re
from pathlib import Path

VAULT_ROOT = Path(__file__).parent.parent
WIKI_DIR = VAULT_ROOT / "wiki"
INDEX_FILE = WIKI_DIR / "index.md"

def find_all_links():
    """Find all [[wiki-links]] and [markdown-links](path) in wiki files."""
    wiki_links = []
    md_links = []
    
    for md_file in WIKI_DIR.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        rel_path = md_file.relative_to(VAULT_ROOT)
        
        # Wiki links [[page]] or [[page|alias]]
        for match in re.finditer(r'\[\[([^\]]+)\]\]', content):
            wiki_links.append((str(rel_path), match.group(1)))
        
        # Markdown links [text](path)
        for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', content):
            md_links.append((str(rel_path), match.group(2)))
    
    return wiki_links, md_links

def resolve_wiki_link(from_file, link_target):
    """Resolve [[wiki-link]] to actual file path."""
    # Try direct match in wiki/
    for ext in [".md", ""]:
        candidate = WIKI_DIR / f"{link_target}{ext}"
        if candidate.exists():
            return candidate
    
    # Try in subdirectories
    for subdir in ["entities", "concepts", "projects", "sources"]:
        candidate = WIKI_DIR / subdir / f"{link_target}.md"
        if candidate.exists():
            return candidate
    
    return None

def resolve_md_link(from_file, link_target):
    """Resolve [markdown-link](path) relative to from_file."""
    from_dir = Path(from_file).parent
    candidate = (from_dir / link_target).resolve()
    if candidate.exists():
        return candidate
    # Try relative to vault root
    candidate = (VAULT_ROOT / link_target).resolve()
    if candidate.exists():
        return candidate
    return None

def find_orphans():
    """Find wiki pages with no incoming links."""
    all_files = set()
    linked_files = set()
    
    for md_file in WIKI_DIR.rglob("*.md"):
        all_files.add(str(md_file.relative_to(VAULT_ROOT)))
    
    wiki_links, md_links = find_all_links()
    
    for from_file, target in wiki_links:
        resolved = resolve_wiki_link(from_file, target)
        if resolved:
            linked_files.add(str(resolved.relative_to(VAULT_ROOT)))
    
    for from_file, target in md_links:
        resolved = resolve_md_link(from_file, target)
        if resolved and resolved.is_relative_to(WIKI_DIR):
            linked_files.add(str(resolved.relative_to(VAULT_ROOT)))
    
    # Index.md is always considered linked
    linked_files.add("wiki/index.md")
    
    orphans = all_files - linked_files
    return orphans

def check_broken_links():
    """Find broken wiki and markdown links."""
    broken = []
    wiki_links, md_links = find_all_links()
    
    for from_file, target in wiki_links:
        if not resolve_wiki_link(from_file, target):
            broken.append((from_file, f"[[{target}]]", "wiki-link"))
    
    for from_file, target in md_links:
        if not resolve_md_link(from_file, target):
            broken.append((from_file, f"[{target}]", "md-link"))
    
    return broken

def update_index():
    """Rebuild index.md from wiki structure."""
    # This would be a simplified version of ingest_raw.py's update_index
    pass

def main():
    print("🔍 Linting wiki...")
    
    broken = check_broken_links()
    if broken:
        print(f"\n❌ Broken links ({len(broken)}):")
        for from_file, target, link_type in broken:
            print(f"  {from_file}: {target} ({link_type})")
    else:
        print("✅ No broken links")
    
    orphans = find_orphans()
    if orphans:
        print(f"\n⚠️  Orphan pages ({len(orphans)}):")
        for orphan in sorted(orphans):
            print(f"  {orphan}")
    else:
        print("✅ No orphan pages")
    
    print("\n📝 Note: Run ingest_raw.py to update index.md")
    
    if broken or orphans:
        sys.exit(1)
    else:
        print("\n✅ All checks passed")

if __name__ == "__main__":
    main()
