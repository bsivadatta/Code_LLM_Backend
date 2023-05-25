{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 20,
   "id": "a1fdb388",
   "metadata": {},
   "outputs": [],
   "source": [
    "import torch, time\n",
    "from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "cf5d2525",
   "metadata": {},
   "outputs": [],
   "source": [
    "tokenizer = AutoTokenizer.from_pretrained(\"Salesforce/codegen-350M-mono\")\n",
    "model = AutoModelForCausalLM.from_pretrained(\"Salesforce/codegen-350M-mono\").to('cpu')\n",
    "config = AutoConfig.from_pretrained('Salesforce/codegen-350M-mono')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "id": "a26b6dc4",
   "metadata": {},
   "outputs": [],
   "source": [
    "tokenizer.save_pretrained('./tokenizer_350M')\n",
    "config.save_pretrained('./config_350M.pt')\n",
    "model.save_pretrained('./model_350M.pt')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "d5bf5018",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Setting `pad_token_id` to `eos_token_id`:50256 for open-end generation.\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "# function to parse all files in directory and count words in each file\n",
      "#\n",
      "# @param directory directory to parse\n",
      "# @return dictionary of words and their counts\n",
      "def parse_files(directory):\n",
      "    # create dictionary of words and their counts\n",
      "    words = {}\n",
      "    # count words in each file\n",
      "    for filename in os.listdir(directory):\n",
      "        # get file path\n",
      "        file_path = os.path.join(directory, filename)\n",
      "        # if file is a directory\n",
      "        if os.path.isdir(file_path):\n",
      "            # parse all files in\n",
      "6.966887950897217\n"
     ]
    }
   ],
   "source": [
    "a =time.time()\n",
    "inputs = tokenizer(\"# function to parse all files in directory and count words\", return_tensors=\"pt\").to('cpu')\n",
    "sample = model.generate(**inputs, max_length=128)\n",
    "print(tokenizer.decode(sample[0], truncate_before_pattern=[r\"\\n\\n^#\", \"^'''\", \"\\n\\n\\n\"]))\n",
    "print(time.time()-a)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
