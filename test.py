import os

def remove_extension(filename):
  """Removes the file extension from a filename.

  Args:
    filename: The filename with extension.

  Returns:
    The filename without the extension.
  """

  base_name, _ = os.path.splitext(filename)
  return base_name

# Example usage:
file_path = "image.mobi"
base_name = remove_extension(file_path)
print(base_name)  # Output: image