from app.services.question_generator import QuestionGenerator, QuestionGenerationError
from app.models import ExperienceLevel, Domain

def main():
    """Generate interview questions based on specified requirements."""
    try:
        # Initialize generator
        generator = QuestionGenerator()

        # Configure question parameters
        job_requirements = [
            "Python backend development",
            "API design",
            "Database optimization"
        ]
        
        # Generate questions
        print("\n🔄 Generating interview questions...")
        questions = generator.generate(
            job_requirements=job_requirements,
            experience_level=ExperienceLevel.MID,
            domain=Domain.BACKEND,
            num_questions=1
        )
        
        if not questions:
            print("\n❌ No questions were generated. Please check the logs for details.")
            return
            
        # Display results
        print(f"\n✅ Generated {len(questions)} questions:\n")
        for i, q in enumerate(questions, 1):
            print(f"Question {i}:")
            print("=" * 50)
            print(f"\n📝 Question:\n{q.question}")
            print(f"\n🎯 Skill Area: {q.skill_area}")
            print(f"📊 Difficulty: {q.difficulty}/10")
            print("\n✔️ Evaluation Criteria:")
            for criterion in q.evaluation_criteria:
                print(f"  • {criterion}")
            print(f"\n💡 Example Answer:\n{q.example_answer}\n")
            print("=" * 50 + "\n")

    except QuestionGenerationError as e:
        print(f"\n❌ Failed to generate questions: {str(e)}")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
