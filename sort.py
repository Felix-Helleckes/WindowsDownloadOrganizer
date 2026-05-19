#!/usr/bin/env python3
"""
Downloads sorter
- Moves files in Downloads into category folders by extension
- If a subfolder contains matching files, move the entire folder into the category
- Removes empty folders (except the category target folders)
- Supports --dry-run to preview actions
"""
import argparse
import os
import shutil
from pathlib import Path

CATEGORIES = {
    'VIDEOS': ['mp4', 'avi', 'mov', 'wmv', 'mkv'],
    'BILDER': ['jpg', 'jpeg', 'png', 'gif', 'bmp'],
    'DOKUMENTE': ['pdf', 'docx', 'doc', 'xlsx', 'pptx'],
    'ARCHIVE': ['zip', 'rar', '7z', 'tar', 'gz'],
    'MUSIK': ['mp3', 'wav', 'flac'],
}

# Order matters for category precedence
CATEGORY_ORDER = ['VIDEOS', 'BILDER', 'DOKUMENTE', 'ARCHIVE', 'MUSIK']


def ensure_dir(p: Path, dry_run=False):
    if not p.exists():
        if dry_run:
            print(f"[DRY] mkdir {p}")
        else:
            p.mkdir(parents=True, exist_ok=True)


def unique_dest(dest: Path) -> Path:
    """If dest exists, append suffix to make unique."""
    if not dest.exists():
        return dest
    base = dest.stem
    parent = dest.parent
    suffix = 1
    while True:
        new_name = f"{base}_{suffix}" + dest.suffix
        candidate = parent / new_name
        if not candidate.exists():
            return candidate
        suffix += 1


def find_category_for_extension(ext: str):
    for cat in CATEGORY_ORDER:
        if ext in CATEGORIES[cat]:
            return cat
    return None


def find_category_for_folder(folder: Path):
    """Walk folder recursively and return first matching category (or None)."""
    for root, dirs, files in os.walk(folder):
        for f in files:
            ext = Path(f).suffix.lower().lstrip('.')
            if ext:
                cat = find_category_for_extension(ext)
                if cat:
                    return cat
    return None


def move_folder(src: Path, target_root: Path, dry_run=False):
    dest = target_root / src.name
    if dest.exists():
        # make unique folder name
        dest = unique_dest(dest)
    if dry_run:
        print(f"[DRY] Move folder: '{src}' -> '{dest}'")
    else:
        shutil.move(str(src), str(dest))
        print(f"Moved folder: '{src}' -> '{dest}'")


def move_files_in_root(downloads: Path, targets: dict, dry_run=False):
    for entry in downloads.iterdir():
        if entry.is_file():
            ext = entry.suffix.lower().lstrip('.')
            cat = find_category_for_extension(ext)
            if cat:
                target = targets[cat]
                ensure_dir(target, dry_run=dry_run)
                dest = target / entry.name
                if dest.exists():
                    dest = unique_dest(dest)
                if dry_run:
                    print(f"[DRY] Move file: '{entry}' -> '{dest}'")
                else:
                    shutil.move(str(entry), str(dest))
                    print(f"Moved file: '{entry.name}' -> '{dest}'")


def remove_empty_folders(downloads: Path, targets: set, dry_run=False):
    # Remove empty directories in Downloads except target dirs
    for root, dirs, files in os.walk(downloads, topdown=False):
        root_path = Path(root)
        if root_path == downloads:
            continue
        if root_path.name in targets:
            continue
        # Skip if contains files
        if any(root_path.iterdir()):
            continue
        if dry_run:
            print(f"[DRY] rmdir '{root_path}'")
        else:
            try:
                root_path.rmdir()
                print(f"Removed empty folder: {root_path}")
            except Exception as e:
                print(f"Failed to remove {root_path}: {e}")


def main():
    parser = argparse.ArgumentParser(description='Sort Downloads into categorized folders')
    parser.add_argument('--downloads', '-d', help='Downloads folder (default: current user Downloads)', default=None)
    parser.add_argument('--dry-run', action='store_true', help='Show actions without performing them')
    args = parser.parse_args()

    downloads = Path(args.downloads) if args.downloads else Path.home() / 'Downloads'
    if not downloads.exists():
        print(f"Downloads folder not found: {downloads}")
        return 1

    # prepare target dirs
    targets = {cat: downloads / cat.capitalize() for cat in CATEGORIES.keys()}
    # Note: user uses German names; mapping keeps earlier names: VIDEOS->Videos, BILDER->Bilder etc.

    # ensure target dirs exist (only in non-dry-run create them)
    for t in targets.values():
        ensure_dir(t, dry_run=args.dry_run)

    # 1) Move files in the root of Downloads
    move_files_in_root(downloads, targets, dry_run=args.dry_run)

    # 2) For each subfolder in Downloads (not the target folders), check content and move whole folder
    for entry in downloads.iterdir():
        if entry.is_dir():
            name = entry.name
            if name in [p.name for p in targets.values()]:
                continue
            cat = find_category_for_folder(entry)
            if cat:
                move_folder(entry, targets[cat], dry_run=args.dry_run)

    # 3) Remove empty folders
    remove_empty_folders(downloads, set(p.name for p in targets.values()), dry_run=args.dry_run)

    print('Done')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
