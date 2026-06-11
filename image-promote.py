import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--source", required=True)
parser.add_argument("--target", required=True)

args = parser.parse_args()

print("Pulling image...")
subprocess.run(["docker", "pull", args.source], check=True)

print("Tagging image...")
subprocess.run(["docker", "tag", args.source, args.target], check=True)

print("Pushing image...")
subprocess.run(["docker", "push", args.target], check=True)

print("IMAGE PROMOTION COMPLETE")
