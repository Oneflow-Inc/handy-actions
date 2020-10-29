import argparse
import os
import subprocess

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "--oss_url", required=False,
    )
    parser.add_argument(
        "--ossutil_bin", required=False, help="docker img name", default="ossutil64",
    )
    args = parser.parse_args()
    oss_url = args.oss_url
    basename = os.path.basename(args.oss_url)
    dl_cmd = f"""set -x
{ossutil_bin} cp -r {oss_url} {basename}
{ossutil_bin} cp {oss_url}.tag {basename}.tag
docker run --rm -v $PWD:$PWD -w $PWD ananace/skopeo copy dir:./{basename}  docker-archive:./{basename}.tar
"""
    subprocess.check_call(dl_cmd, shell=True)
    # Loaded image ID: sha256:f0b02e9d092d905d0d87a8455a1ae3e9bb47b4aa3dc125125ca5cd10d6441c9f
    loaded_output = subprocess.check_output("docker load -i {basename}.tar", shell=True)
    sha256 = loaded_output.split(":")[-1]
    tag = None
    with open("{basename}.tag") as f:
        tag = f.read()
    assert tag
    tag_cmd = f"docker tag {sha256} {tag}"
    subprocess.check_call(tag_cmd, shell=True)
