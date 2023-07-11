from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from transformers import T5ForConditionalGeneration, AutoTokenizer
from transformers import TextIteratorStreamer
from threading import Thread

prompt='''

'''

print('Before server startup')
checkpoint = "Salesforce/codet5p-770m-py"
device = "cpu" # for GPU usage or "cpu" for CPU usage

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = T5ForConditionalGeneration.from_pretrained(checkpoint).to(device)
streamer = TextIteratorStreamer(tokenizer, skip_special_tokens=True)
inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)
generation_kwargs = dict(inputs=inputs, streamer=streamer, max_new_tokens=90)

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

@app.websocket("/stream")
async def stream_text(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)


    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()
    for token in streamer:
        for client in connected_clients:
            await client.send_text(token)
    connected_clients.remove(websocket)

@app.get("/")
async def root():
  return "API RETURN"