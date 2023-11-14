# pip3 install GitPython
from git import Repo
import os

repo_path = "/Users/tsai/Downloads/stable-diffusion-v1-5"
repo = Repo(repo_path)
dl_base_url = "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/"
aliyun_base_url = "oss://oneflow-static/hf_hub/stable-diffusion-v1-5"

repo_path = "/Users/tsai/Downloads/LCM_Dreamshaper_v7"
repo = Repo(repo_path)
dl_base_url = "https://huggingface.co/SimianLuo/LCM_Dreamshaper_v7/resolve/main/"
aliyun_base_url = "oss://oneflow-static/hf_hub/LCM_Dreamshaper_v7"


# Get the list of all tracked files
tracked_files = repo.git.ls_files().split("\n")

# Print the paths of all tracked files
for file_path in tracked_files:
    with open(os.path.join(repo_path, file_path), "rb") as file:
        content = file.read()

    # Check if the file is a Git LFS file
    if (
        b"version https://git-lfs.github.com/spec/"
        in content
        # and "fp16" in file_path
        # and file_path.endswith(".safetensors")
    ):
        from_path = os.path.join(dl_base_url, file_path)
        to_path = os.path.join(aliyun_base_url, file_path)
        # print(f"")
        # print(f"wget --quiet {from_path}")
        # file_name = os.path.basename(file_path)
        # print(f"ossutil64 cp -f {file_name} {aliyun_base_url}/{file_path}")
        # print(f"rm {file_name}")
        item = f"src_url: '{from_path}', dst_oss_url: '{aliyun_base_url}/{file_path}'"
        print("- {" + item + "}")
