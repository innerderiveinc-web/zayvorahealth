#!/usr/bin/env python3
"""
ZAYVORA Health OS™ — Distribution Package Builder
Builds:
1. zayvora-health-os-full.zip (codebase without .git)
2. zayvora-health-os-complete-with-git.zip (codebase with full git history)
"""
import os
import zipfile

def make_zip(zip_name: str, include_git: bool = False):
    print(f"Packaging {zip_name} (include_git={include_git})...")
    count = 0
    with zipfile.ZipFile(zip_name, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk("."):
            parts = root.split(os.sep)
            if not include_git and ".git" in parts:
                continue
            if any(p in parts for p in ["node_modules", ".venv", "__pycache__", ".next", ".turbo", ".gemini"]):
                continue
            for file in files:
                if file.endswith(".zip") or file.endswith(".pyc") or file == ".DS_Store":
                    continue
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, ".")
                z.write(file_path, arc_name)
                count += 1
    size_mb = os.path.getsize(zip_name) / (1024 * 1024)
    print(f"✓ {zip_name}: {count} files packaged ({size_mb:.2f} MB)")

if __name__ == "__main__":
    os.makedirs("dist", exist_ok=True)
    full_zip = "dist/zayvora-health-os-full.zip"
    git_zip = "dist/zayvora-health-os-complete-with-git.zip"
    make_zip(full_zip, include_git=False)
    make_zip(git_zip, include_git=True)
    
    import shutil
    # Mirror full zip to user convenience paths
    convenience_targets = [
        "/Users/irfanashraf/Downloads/zayvora-health-os-full.zip",
        "/Users/irfanashraf/Desktop/zayvora-health-os-full.zip"
    ]
    for target in convenience_targets:
        try:
            target_dir = os.path.dirname(target)
            if os.path.isdir(target_dir):
                shutil.copy(full_zip, target)
                print(f"✓ Mirrored distribution bundle to {target}")
        except Exception as e:
            print(f"Notice: could not copy to {target}: {e}")
    print("✓ Distribution bundles successfully built in dist/")

