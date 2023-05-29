special_numbers = [2, 5, 7]
special_words = ["two", "five", "seven"]

# Function to check if number is in special numbers
def is_special_number(number):
    for i in special_numbers:
        if i == number:
            return True
    return False


# Function to check if word is in special words
def is_special_word(word):
    for i in special_words:
        if i == word:
            return True
    return False

def print_special_numbers_words_in_list(list):
  for ele in list:
    if is_special_number(ele) or is_special_word(ele):
      print(ele)