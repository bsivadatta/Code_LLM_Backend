from fastapi import FastAPI
from pydantic import BaseModel
import generate_suggestion as GS
my_obj = GS.SuggestionClass()

class Item(BaseModel):
  suggestion: str

app = FastAPI()

@app.post("/suggestion/")
async def create_item(item: Item):
  if not item:
    return {"suggestion":"a"}
  a = (my_obj.generate_suggestion(item.suggestion))
  # a = a.lstrip("\r\n")
  # a = a.lstrip()
  # a = a.rstrip()
  # if "\r\n\r\n" in a:
  #   a = a.split("\r\n\r\n")[0]
  return {"suggestion":a}

@app.get("/")
async def root():
  return "API RETURN"