# Configuration constants for different domains

DOMAIN_CONFIGS = {
    "backend": {
        "key_skills": [
            "RestFul API",
            "Authentication",
            "Database Design",
            "Authorization",
            "Database Architecture",
            "System Design",
            "Security",
            "Performance"
        ],
        "technologies": [
            "Python", "SQL", "RESTful APIs", "GraphQL",
            "Microservices", "Cloud Platforms",
            "Message Brokers", "Caching", 
            "Databases", "Docker"
        ]
    },
    "frontend": {
        "key_skills": [
            "UI/UX",
            "React",
            "Hooks",
            "State Management",
            "Performance",
            "Responsive Design",
            "API Integration"
        ],
        "technologies": [
            "React", "JavaScript/TypeScript", 
            "HTML/CSS", "REST APIs"
        ]
    },
    "web_development": {
        "key_skills": [
            "Full Stack Development",
            "Database Design",
            "API Development",
            "UI/UX",
            "Security"
        ],
        "technologies": [
            "Python", "JavaScript", "SQL",
            "REST APIs", "HTML/CSS"
        ]
    },
    "data_science": {
        "key_skills": [
            "Machine Learning",
            "Data Analysis",
            "Data Visualization",
            "Feature Engineering",
            "Statistics"
        ],
        "technologies": [
            "Python", "SQL", "Pandas",
            "Scikit-learn", "Visualization Tools"
        ]
    }
}

DIFFICULTY_GUIDELINES = {
    "junior": {
        "focus_areas": ["Basic concepts", "Code readability"],
        "complexity_level": "Low to Medium",
        "practical_weight": 0,
        "theoretical_weight": 1
    },
    "mid": {
        "focus_areas": ["Design patterns", "System components"],
        "complexity_level": "Medium",
        "practical_weight": 0,
        "theoretical_weight": 1
    },
    "senior": {
        "focus_areas": ["Architecture", "System design"],
        "complexity_level": "High",
        "practical_weight": 0.3,
        "theoretical_weight": 0.7
    },
    "lead": {
        "focus_areas": ["System architecture", "Technical strategy"],
        "complexity_level": "Very High",
        "practical_weight": 0.4,
        "theoretical_weight": 0.6
    }
}
