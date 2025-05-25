export enum ExperienceLevel {
    JUNIOR = "junior",
    MID = "mid",
    SENIOR = "senior",
    LEAD = "lead"
}

export enum Domain {
    BACKEND = "backend",
    FRONTEND = "frontend",
    WEB_DEVELOPMENT = "web_development",
    DATA_SCIENCE = "data_science"
}

export interface Question {
    question: string;
    difficulty: number;
    skill_area: string;
    evaluation_criteria: string[];
    example_answer: string;
}

export interface GenerateQuestionsRequest {
    job_requirements: string[];
    experience_level: ExperienceLevel;
    domain: Domain;
    num_questions: number;
}

export interface GenerateQuestionsResponse {
    questions: Question[];
}
