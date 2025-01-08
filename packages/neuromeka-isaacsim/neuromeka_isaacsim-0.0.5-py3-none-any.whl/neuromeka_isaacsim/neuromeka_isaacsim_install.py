import shutil
from pathlib import Path
import sys
import zipfile

def get_install_path(type="extension"):
    if sys.platform == "win32":
        paths = []
        username = Path.home().parts[2]
        
        if type=="extension":
            extension_path = Path("Kit") / "shared" / "exts" / "omni.isaacsim_bridge.extension"

            if (Path.home() / "Documents").exists():
                paths.append(Path.home() / "Documents" / extension_path)
            else:
                print("Skip not found folder: ", Path.home() / "Documents")
                
            if (Path.home() / "OneDrive" / "Documents").exists():
                paths.append(Path.home() / "OneDrive" / "Documents" / extension_path)
            else:
                print("Skip not found folder: ", Path.home() / "OneDrive" / "Documents")
            
            if (Path.home() / ("OneDrive - " + username) / "Documents").exists():
                paths.append(Path.home() / ("OneDrive - " + username) / "Documents" / extension_path)
            else:
                print("Skip not found folder: ", Path.home() / ("OneDrive - " + username) / "Documents")
            
        elif type=="data":
            paths.append(Path.home() / "neuromeka-isaacsim")

        return paths
    else:
        paths = []
        
        if type=="extension":
            if (Path.home() / ".local" / "share").exists():
                paths.append(Path.home() / ".local" / "share" / "ov" / "kit" / "shared" / "exts" / "omni.isaacsim_bridge.extension")    
            else:
                print("Skip not found folder: ", Path.home() / ".local" / "share")
        
        elif type=="data":
            paths.append(Path.home() / "neuromeka-isaacsim")
        
        return paths

def main():
    # Copy extension to Isaac Sim extensions folder
    ext_src = Path(__file__).parent / "omni.isaacsim_bridge.extension.zip"
    ext_dst_list = get_install_path(type="extension")
    if ext_src.exists():
        for ext_dst in ext_dst_list:
            try:
                if ext_dst.exists():
                    shutil.rmtree(ext_dst)
                # -----------------------------------
                # shutil.copytree(ext_src, ext_dst)
                with zipfile.ZipFile(ext_src, 'r') as zip_ref:
                    zip_ref.extractall(ext_dst.parent)
                # -----------------------------------
                print(f"Copied extension to: {ext_dst}")
            except PermissionError as e:
                print("Permission error: ", e)
            except Exception as e:
                print("Failed to copy extension: ", e)
    
    # Copy data to user's desktop
    data_src = Path(__file__).parent / "neuromeka-isaacsim"
    data_dst_list = get_install_path(type="data")
    if data_src.exists():
        for data_dst in data_dst_list:
            try:
                if data_dst.exists():
                    shutil.rmtree(data_dst)
                shutil.copytree(data_src, data_dst)
                print(f"Copied data to: {data_dst}")
            except PermissionError as e:
                print("Permission error: ", e)
            except Exception as e:
                print("Failed to copy data: ", e)
