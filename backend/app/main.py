from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import QuestionRequest, QuestionResponse
from .services.question_generator import QuestionGenerator

app = FastAPI(title="Technical Interview Question Generator")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend development server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

generator = QuestionGenerator()

@app.post("/generate", response_model=QuestionResponse)
def generate_questions(request: QuestionRequest):
    try:
        questions = generator.generate(**request.dict())
        return QuestionResponse(questions=questions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
