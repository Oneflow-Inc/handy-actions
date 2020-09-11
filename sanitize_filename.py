from pathvalidate import sanitize_filename
import argparse

parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument("--img_name", required=True, help="docker img name")
args = parser.parse_args()
print(sanitize_filename(args.img_name))
