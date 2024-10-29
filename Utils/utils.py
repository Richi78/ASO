import subprocess

def whoami() -> str:
    iam = subprocess.run(['whoami'], capture_output=True, text=True)
    return iam.stdout.strip()
