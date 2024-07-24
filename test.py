def format_book_details(book_details):
  formatted_details = {}
  for key, value in book_details.items():
    formatted_details[key] = value.split(": ")[1]
  return formatted_details

book_details = {'asin': 'ASIN : B08JTYRXZB', 'publisher': 'Publisher : VIZ Media: SHONEN JUMP (October 6, 2020)', 'publication date': 'Publication date : October 6, 2020', 'print length': 'Print length : 192 pages'}

formatted_book_details = format_book_details(book_details)
print(formatted_book_details)