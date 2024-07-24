import os
import subprocess
def good_ol_metadata():
    path = os.path.join(os.getcwd(), "utils", "metadata.py")
    command = f"calibre-debug {path}"
    subprocess.run(command, shell=True, check=True)

good_ol_metadata()