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
    ossutil_bin = args.ossutil_bin
    oss_url = args.oss_url
    if oss_url.endswith("/"):
        oss_url = oss_url[0:-1]
    basename = os.path.basename(oss_url)
    assert basename
    dl_cmd = f"""set -x
chmod +x {ossutil_bin}
{ossutil_bin} config -e oss-cn-beijing.aliyuncs.com -i "$OSS_ACCESS_KEY_ID" -k "$OSS_ACCESS_KEY_SECRET"  -L EN -c $HOME/.ossutilconfig
{ossutil_bin} cp -r {oss_url} .
{ossutil_bin} cp {oss_url}.tag {basename}.tag
docker run --rm -v $PWD:$PWD -w $PWD ananace/skopeo copy dir:./{basename}  docker-archive:./{basename}.tar
"""
    subprocess.check_call(dl_cmd, shell=True)
    # Loaded image ID: sha256:f0b02e9d092d905d0d87a8455a1ae3e9bb47b4aa3dc125125ca5cd10d6441c9f
    load_cmd = f"docker load -i {basename}.tar"
    print(load_cmd)
    loaded_output = subprocess.check_output(load_cmd, shell=True)
    loaded_output = loaded_output.decode('ascii').strip()
    print(loaded_output)
    sha256 = loaded_output.split(":")[-1]
    tag = None
    with open(f"{basename}.tag") as f:
        tag = f.read()
    tag = tag.strip()
    assert tag
    tag_cmd = f"docker tag {sha256} {tag}"
    print(tag_cmd)
    subprocess.check_call(tag_cmd, shell=True)
