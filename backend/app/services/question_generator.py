from typing import List, Optional, Dict, Any
from ..models import Question, ExperienceLevel, Domain
from ..config import DOMAIN_CONFIGS, DIFFICULTY_GUIDELINES
from together import Together
import os
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential
from ..utils.logging import setup_logger

load_dotenv()
logger = setup_logger("question_generator")

class QuestionGenerationError(Exception):
    pass

class QuestionGenerator:
    def __init__(self):
        self.together_api_key = os.getenv("TOGETHER_API_KEY")
        if not self.together_api_key:
            raise ValueError("Together API key not found in environment variables")
        
        self.client = Together(api_key=self.together_api_key)
        self.difficulty_ranges = {
            ExperienceLevel.JUNIOR: (1, 4),
            ExperienceLevel.MID: (3, 7),
            ExperienceLevel.SENIOR: (6, 9),
            ExperienceLevel.LEAD: (8, 10)
        }
        
    def _get_default_difficulty(self, experience_level: ExperienceLevel) -> int:
        """Calculate a default difficulty based on experience level."""
        min_diff, max_diff = self.difficulty_ranges[experience_level]
        # Use the middle of the range as default
        return (min_diff + max_diff) // 2

    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate a simple similarity score between two texts."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        return intersection / union if union > 0 else 0
    
    def _create_prompt(self, job_requirements: List[str], experience_level: ExperienceLevel, 
                      domain: Domain, focus_requirement: str = None) -> str:
        domain_config = DOMAIN_CONFIGS[domain]
        level_config = DIFFICULTY_GUIDELINES[experience_level]
        min_diff, max_diff = self.difficulty_ranges[experience_level]        # If no specific requirement is provided, use a general prompt
        focus_text = ""
        if focus_requirement:
            focus_text = f"\nFocus: {focus_requirement}"
            return f"""Generate a technical interview question for:
                Domain: {domain}
                Level: {experience_level} (Difficulty {min_diff}-{max_diff})
                Skills: {', '.join(domain_config['key_skills'])}
                Tech: {', '.join(domain_config['technologies'])}
                Requirements: {', '.join(job_requirements)}{focus_text}

                Format:
                Question: [Detailed technical question with context]

                Skill Area: [Primary skill being assessed]

                Evaluation Criteria:
                - Technical Knowledge: [Required technical concepts]
                - Implementation: [Solution structure and approach]
                - Best Practices: [Code quality and architecture]
                - Problem-Solving: [Analysis and trade-offs]

                Example Answer:
                - Approach and analysis
                - Implementation with code examples
                - Technical considerations
                - Best practices
                - Optimizations

                Difficulty: [number {min_diff}-{max_diff}]"""

    def _parse_response(self, response_text: str, experience_level: ExperienceLevel) -> Dict[str, Any]:
        try:
            sections = [p.strip() for p in response_text.split("\n\n") if p.strip()]
            
            question = next((p for p in sections if p.lower().startswith("question:")), sections[0])
            question = question.replace("Question:", "").strip()
            
            skill = next((p for p in sections if any(p.lower().startswith(x) for x in ["skill area:", "skill:"])), None)
            if not skill:
                raise QuestionGenerationError("Missing skill area")
            skill = skill.split(":", 1)[1].strip()
            
            criteria_section = next((p for p in sections if "evaluation criteria:" in p.lower()), None)
            if not criteria_section:
                raise QuestionGenerationError("Missing evaluation criteria")
            criteria = [
                line.lstrip("- ").lstrip("* ").lstrip("• ").strip()
                for line in criteria_section.split("\n")[1:]
                if line.strip()
            ]
            
            difficulty_section = next((p for p in sections if "difficulty:" in p.lower()), None)
            if difficulty_section:
                # Try to extract difficulty from response
                import re
                difficulty_match = re.search(r'\d+', difficulty_section.split(":", 1)[1].strip())
                if difficulty_match:
                    difficulty = int(difficulty_match.group())
                else:
                    logger.warning("Could not parse difficulty from response, using default")
                    difficulty = self._get_default_difficulty(experience_level)
            else:
                logger.info("No difficulty provided in response, using default")
                difficulty = self._get_default_difficulty(experience_level)
            example = next((p for p in sections if any(p.lower().startswith(x) for x in ["example answer:", "example:", "example solution:"])), None)
            if not example:
                logger.warning("Could not find example answer section")
                raise QuestionGenerationError("Missing example answer")
            # Split and join by ':' to handle cases where there might be colons in the answer
            example = ':'.join(example.split(':')[1:]).strip()
            
            return {
                "question": question,
                "skill_area": skill,
                "difficulty": difficulty,
                "evaluation_criteria": criteria,
                "example_answer": example
            }
        except Exception as e:
            raise QuestionGenerationError(f"Failed to parse response: {str(e)}")    
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _generate_single_question(self, job_requirements: List[str], experience_level: ExperienceLevel, 
                                domain: Domain, focus_requirement: str = None) -> Optional[Question]:
        try:
            prompt = self._create_prompt(job_requirements, experience_level, domain, focus_requirement)
            logger.info("Generating question...")
            if focus_requirement:
                logger.info("Focusing on requirement: %s", focus_requirement)            
                system_prompt = "You are an expert technical interviewer. Generate challenging practical interview questions that test both theoretical knowledge and implementation skills, focus on real-world scenarios, and include clear evaluation criteria with example solutions."
            
            response = self.client.chat.completions.create(
                model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,  # Slightly reduced for more focused outputs
                max_tokens=1000
            )
            
            response_text = response.choices[0].message.content
            logger.debug("Response: %s", response_text)
            
            question_data = self._parse_response(response_text, experience_level)
            logger.info("Successfully parsed question")
            
            min_diff, max_diff = self.difficulty_ranges[experience_level]
            if not (min_diff <= question_data["difficulty"] <= max_diff):
                # If outside range, adjust to nearest valid value
                question_data["difficulty"] = min(max(question_data["difficulty"], min_diff), max_diff)
                logger.info("Adjusted difficulty to %d to match experience level", question_data["difficulty"])
            
            return Question(**question_data)
                
        except Exception as e:
            logger.exception("Failed to generate question: %s", str(e))
            return None    
        
    def generate(self, job_requirements: List[str], experience_level: ExperienceLevel, 
                domain: Domain, num_questions: int = 1) -> List[Question]:
        questions = []
        attempts = 0
        max_attempts = num_questions * 3  # Increased max attempts for better diversity
        used_skills = set()
        
        logger.info("Starting generation of %d questions", num_questions)
        
        # First pass: Generate one question for each distinct requirement
        for req in job_requirements:
            if len(questions) >= num_questions:
                break
            
            # Skip if we've already covered this skill area
            req_key = ' '.join(req.lower().split()[:3])
            if req_key in used_skills:
                continue
            
            if question := self._generate_single_question(job_requirements, experience_level, domain, req):
                if not any(self._calculate_similarity(question.question, q.question) > 0.7 for q in questions):
                    questions.append(question)
                    used_skills.add(req_key)
                    logger.info("Generated question for requirement: %s", req)
            attempts += 1
        
        # Second pass: Fill remaining slots with additional questions
        while len(questions) < num_questions and attempts < max_attempts:
            # Choose an unused requirement if available
            unused_reqs = [req for req in job_requirements 
                         if not any(self._calculate_similarity(req.lower(), q.skill_area.lower()) > 0.5 
                                  for q in questions)]
            
            focus_req = unused_reqs[attempts % len(unused_reqs)] if unused_reqs else None
            if question := self._generate_single_question(job_requirements, experience_level, domain, focus_req):
                if not any(self._calculate_similarity(question.question, q.question) > 0.7 for q in questions):
                    questions.append(question)
                    logger.info("Generated additional question %d/%d", len(questions), num_questions)
            attempts += 1
        
        logger.info("Completed generation with %d/%d questions", len(questions), num_questions)
        return questions
