from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
	return{"meanining full message" : "be happy"}
@app.get("/health")
async def health():
	return{"status":"im healthy, tell now"}
