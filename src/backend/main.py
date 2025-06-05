import dotenv
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from services.service_initializer import initialize_services

dotenv.load_dotenv()

initialized_services = initialize_services()

data_ingestion_service = initialized_services["data_ingestion_service"]
chat_service = initialized_services["chat_service"]

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return "Hello World"

@app.get("/check-data")
async def check_data():
    print("Checking data and processing document if necessary...")
    try:
        await data_ingestion_service.process_data()
        return {"status": "Data check and processing complete."}
    except Exception as e:
        print(f"An error occurred during data check or processing: {e}")
        return {"status": f"Error: {e}"}

@app.get("/chat")
async def chat(q: str = Query(..., description="User query")):
    print(f"Received chat query: {q}")
    try:
        async def generate_response_chunks():
                async for chunk in chat_service.generate_response(q):
                    yield chunk

        return StreamingResponse(generate_response_chunks(), media_type="text/plain")
    except Exception as e:
        print(f"An error occurred during chat processing: {e}")
        return {"status": f"Error: {e}"}
