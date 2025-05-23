# Configuration constants for different domains

DOMAIN_CONFIGS = {
    "backend": {
        "key_skills": [
            "API Design",
            "Database Architecture",
            "System Design",
            "Security",
            "Performance"
        ],
        "technologies": [
            "Python", "SQL", "RESTful APIs", 
            "Databases", "Docker"
        ]
    },
    "frontend": {
        "key_skills": [
            "UI/UX",
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
        "practical_weight": 0.7,
        "theoretical_weight": 0.3
    },
    "mid": {
        "focus_areas": ["Design patterns", "System components"],
        "complexity_level": "Medium",
        "practical_weight": 0.6,
        "theoretical_weight": 0.4
    },
    "senior": {
        "focus_areas": ["Architecture", "System design"],
        "complexity_level": "High",
        "practical_weight": 0.5,
        "theoretical_weight": 0.5
    },
    "lead": {
        "focus_areas": ["System architecture", "Technical strategy"],
        "complexity_level": "Very High",
        "practical_weight": 0.4,
        "theoretical_weight": 0.6
    }
}
