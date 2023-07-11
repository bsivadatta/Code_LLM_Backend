from fastapi import FastAPI, Request
from pydantic import BaseModel
# import generate_suggestion as GS
#my_obj = GS.SuggestionClass()
from fastapi import FastAPI, WebSocket, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.responses import StreamingResponse
from threading import Thread
device = "cpu"
import torch, time
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
from transformers import TextIteratorStreamer, T5ForConditionalGeneration, AutoModelForSeq2SeqLM
import os 
checkpoint = "Salesforce/codet5p-770m"
device = "cpu" # for GPU usage or "cpu" for CPU usage


tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = T5ForConditionalGeneration.from_pretrained(checkpoint).to(device) # t5 770m
# # model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint,
# #                                                torch_dtype=torch.float16,
# #                                                trust_remote_code=True).to(device)

streamer = TextIteratorStreamer(tokenizer, skip_special_tokens=True, skip_prompt=True)
# prompt = "# Function to print prime numbers"
stream_thread = None

class Item(BaseModel):
  prompt: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app = FastAPI()
connected_clients = set()

# @app.post("/suggestion/")
# async def create_item(item: Item):
#   if not item:
#     return {"suggestion":"a"}
#   return {"suggestion":(my_obj.generate_suggestion(item.prompt))}

@app.get("/")
async def root():
  return "API RETURN"

@app.websocket("/stream")
async def stream_text(websocket: WebSocket):
  await websocket.accept()
  connected_clients.add(websocket)
  global prompt
  global stream_thread
  prompt = await websocket.receive_text()
  inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)
  generation_kwargs = dict(inputs=inputs, streamer=streamer, max_new_tokens=200)
  thread = Thread(target=model.generate, kwargs=generation_kwargs)
  stream_thread = thread
  stream_thread.start()
  for token in streamer:
      for client in connected_clients:
          await client.send_text(token)
  connected_clients.remove(websocket)

@app.get("/stop")
async def stop():
  print(stream_thread.native_id)
  stream_thread.join()


async def fake_video_streamer(received_string):
    for i in range(10):
      time.sleep(1)
      yield received_string 

@app.post("/test")
async def main(request: Request, background_tasks: BackgroundTasks):
    data = await request.body()
    # Handle the received string data
    received_string = data.decode('utf-8')
    return background_tasks.add_task(StreamingResponse, fake_video_streamer(received_string))