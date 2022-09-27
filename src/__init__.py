import os
import platform

os_default_root_path_mapping = {
    "Windows": "c://",
    "Darwin": "/",
    "Linux": "/",
    "Java": "/",
    "": "/",
}
ROOT_PATH = os.getenv("DFM_ROOT_PATH", os_default_root_path_mapping[platform.system()])
