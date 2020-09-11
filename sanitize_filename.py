from pathvalidate import sanitize_filename
import argparse
import os

parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument(
    "--img_name", required=True, help="docker img name", default=os.getenv("IMG_NAME")
)
args = parser.parse_args()
print(sanitize_filename(args.img_name))
