import shutil
from pathlib import Path
import sys

def get_extensions_install_path():
    if sys.platform == "win32":
        return Path.home() / "Documents" / "Kit" / "shared" / "exts" / "omni.isaacsim_bridge.extension"
    else:
        return Path.home() / ".local" / "share" / "ov" / "kit" / "shared" / "exts" / "omni.isaacsim_bridge.extension"

def main():
    ext_src = Path(__file__).parent / "omni.isaacsim_bridge.extension"
    ext_dst = get_extensions_install_path()
    if ext_src.exists():
        if ext_dst.exists():
            shutil.rmtree(ext_dst)
        shutil.copytree(ext_src, ext_dst)
        print(f"Copied extension to: {ext_dst}")
