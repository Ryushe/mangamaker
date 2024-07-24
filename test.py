array = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]

def has_decimal(numbers):
  for num in numbers:
    if isinstance(num, float):
      return True
  return False  

print(has_decimal(array))