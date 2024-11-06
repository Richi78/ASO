import subprocess
import string
import random

def whoami() -> str:
    iam = subprocess.run(['whoami'], capture_output=True, text=True)
    return iam.stdout.strip()

def generatePassword() -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(32))
    return password