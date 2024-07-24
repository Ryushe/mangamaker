import utils.tmp as tmp
from utils.utils import *


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
for num, file in zip(nums, files):
  print(num, file)
# attempting to fix


#   File "D:\Code\Python\mangamaker\utils\apply_metadata.py", line 11, in good_ol_metadata
#     cover_files = sorted(get_folder_files(cover_folder))
#                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "D:\Code\Python\mangamaker\utils\utils.py", line 77, in get_folder_files
#     return [file for file in os.listdir(path)
#                              ^^^^^^^^^^^^^^^^
# OSError: [WinError 123] The filename, directory name, or volume label syntax is incorrect: '<utils.tmp.TempDir object at 0x000002CA6951E3F0>'