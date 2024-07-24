import utils.tmp as tmp
from utils.utils import *

def get_paths(path, files):
    paths = []
    for file in files:
        paths.append(os.path.join(path, file))
    return paths

def create_txt_files(directory, num_files, content):
  """Creates multiple text files in a specified directory.

  Args:
    directory: The path to the directory where files will be created.
    num_files: The number of files to create.
    content: The content to be written to each file.
  """

  if not os.path.exists(directory):
    os.makedirs(directory)

  for i in range(num_files):
    filename = f"file_{i+1}.txt"
    file_path = os.path.join(directory, filename)
    with open(file_path, "w") as f:
      f.write(content)

nums = [1,2,3,4]

bob = tmp.TempDir()
bob_path = bob.make_tempdir("booba")
create_txt_files(bob_path, 4, '')
files = get_folder_files(bob_path)

paths = get_paths(bob_path, files)
for num, file in zip(nums, paths):
  print(num, file)

