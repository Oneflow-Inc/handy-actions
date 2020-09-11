from pathvalidate import sanitize_filename
import argparse
import os

parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument(
    "--img_name", required=False, help="docker img name", default=os.getenv("IMG_NAME")
)
args = parser.parse_args()
assert args.img_name
print(sanitize_filename(args.img_name))
