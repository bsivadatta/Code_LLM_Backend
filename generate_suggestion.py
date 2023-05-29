import torch, time
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
config = AutoConfig.from_pretrained('./config_santacoder.pt', trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained("./tokenizer_santacoder/")
model = AutoModelForCausalLM.from_pretrained('./model_santacoder.pt', trust_remote_code=True).to('cpu')

class SuggestionClass:
  def __init__(self):
    # Initialize any necessary variables or resources here
    pass

  def generate_suggestion(self, comment):
    inputs = tokenizer(comment, return_tensors="pt").to('cpu')
    generated_ids = model.generate(**inputs, max_new_tokens = 35)
    return tokenizer.decode(generated_ids[:, inputs["input_ids"].shape[1]:][0])

def main():
    # Create an instance of MyClass
    my_object = SuggestionClass()
    # Call functions from the MyClass instance
    print(my_object.generate_suggestion("# function to parse all files in directory and count words"))

if __name__ == "__main__":
    main()
