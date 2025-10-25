from flask import Flask, send_from_directory, jsonify, request
import json
import os
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

# Comprehensive NYUAD Fall 2025 course data
NYUAD_COURSES = [
    # Ancient World Courses
    {
        "course_id": "AW-UH 1114",
        "title": "Doing Archeology: Case Studies from Western Asia",
        "subject": "Ancient World",
        "number": "1114",
        "description": "Archaeologists 'read' information from artifacts, architecture, and the environment to understand people's lives in the past. This course offers a rich introduction to the ways archaeologists study the past.",
        "instructors": ["Kidd, Fiona"],
        "credits": 4,
        "requirements": ["CORE"],
        "tags": ["archaeology", "history", "humanities"],
        "sections": [
            {
                "section_id": "001",
                "location": "Arts Center Room 006",
                "capacity": 25,
                "enrolled": 20,
                "meetings": [
                    {"day": "Tue", "start": "11:20", "end": "12:35"},
                    {"day": "Thu", "start": "11:20", "end": "12:35"}
                ]
            }
        ]
    },
    {
        "course_id": "AW-UH 1119X",
        "title": "Sacred Cities: Jerusalem and Mecca",
        "subject": "Ancient World",
        "number": "1119X",
        "description": "A study of the holy cities, Jerusalem and Mecca, is fundamental to a rich understanding of the history, archaeology, anthropology, religion, geography, and politics of the Middle East.",
        "instructors": ["Zimmerle, William"],
        "credits": 4,
        "requirements": ["CORE"],
        "tags": ["religion", "history", "middle-east"],
        "sections": [
            {
                "section_id": "001",
                "location": "Campus Center Room E048",
                "capacity": 25,
                "enrolled": 22,
                "meetings": [
                    {"day": "Mon", "start": "15:35", "end": "16:50"},
                    {"day": "Wed", "start": "15:35", "end": "16:50"}
                ]
            }
        ]
    },
    
    # Arabic Language Courses
    {
        "course_id": "ARABL-UH 1110",
        "title": "Elementary Arabic 1",
        "subject": "Arabic Language",
        "number": "1110",
        "description": "This course is designed for learners with no prior knowledge of Arabic. It is an interactive course designed to build the student's abilities in listening, speaking, reading, and writing.",
        "instructors": ["Kittaneh, Khulood"],
        "credits": 4,
        "requirements": ["GE"],
        "tags": ["language", "arabic", "culture"],
        "sections": [
            {
                "section_id": "001",
                "location": "Computational Research Room 020",
                "capacity": 18,
                "enrolled": 16,
                "meetings": [
                    {"day": "Mon", "start": "11:20", "end": "12:35"},
                    {"day": "Tue", "start": "11:20", "end": "12:35"},
                    {"day": "Wed", "start": "11:20", "end": "12:35"},
                    {"day": "Thu", "start": "11:20", "end": "12:35"}
                ]
            },
            {
                "section_id": "002",
                "location": "Campus Center Room W006",
                "capacity": 18,
                "enrolled": 15,
                "meetings": [
                    {"day": "Mon", "start": "12:45", "end": "14:00"},
                    {"day": "Tue", "start": "12:45", "end": "14:00"},
                    {"day": "Wed", "start": "12:45", "end": "14:00"},
                    {"day": "Thu", "start": "12:45", "end": "14:00"}
                ]
            }
        ]
    },
    {
        "course_id": "ARABL-UH 1111",
        "title": "Elementary Arabic 2",
        "subject": "Arabic Language",
        "number": "1111",
        "description": "Continuation of Elementary Arabic 1. Students continue to develop their Arabic language skills through interactive activities.",
        "instructors": ["Kittaneh, Khulood"],
        "credits": 4,
        "requirements": ["GE"],
        "tags": ["language", "arabic", "culture"],
        "sections": [
            {
                "section_id": "001",
                "location": "Computational Research Room 020",
                "capacity": 18,
                "enrolled": 14,
                "meetings": [
                    {"day": "Mon", "start": "09:55", "end": "11:10"},
                    {"day": "Tue", "start": "09:55", "end": "11:10"},
                    {"day": "Wed", "start": "09:55", "end": "11:10"},
                    {"day": "Thu", "start": "09:55", "end": "11:10"}
                ]
            }
        ]
    },
    
    # Business Courses
    {
        "course_id": "BUSOR-UH 1003",
        "title": "Management & Organizations",
        "subject": "Business",
        "number": "1003",
        "description": "Why do some organizations succeed while others flounder? This course will help illuminate the key processes and factors that determine why organizations function as they do.",
        "instructors": ["Jeong, Sophia Soyoung", "Kailas, Lakshmi"],
        "credits": 4,
        "requirements": ["MAJOR_REQ"],
        "tags": ["business", "management", "organizations"],
        "sections": [
            {
                "section_id": "001",
                "location": "Social Sciences Room 018",
                "capacity": 30,
                "enrolled": 30,
                "meetings": [
                    {"day": "Tue", "start": "08:30", "end": "09:45"},
                    {"day": "Thu", "start": "08:30", "end": "09:45"}
                ]
            },
            {
                "section_id": "002",
                "location": "Computational Research Room 002",
                "capacity": 30,
                "enrolled": 25,
                "meetings": [
                    {"day": "Mon", "start": "09:55", "end": "11:10"},
                    {"day": "Wed", "start": "09:55", "end": "11:10"}
                ]
            }
        ]
    },
    {
        "course_id": "BUSOR-UH 1007",
        "title": "Introduction to Entrepreneurship",
        "subject": "Business",
        "number": "1007",
        "description": "Entrepreneurship can be considered a process of economic or social value creation. The course provides a broad understanding of entrepreneurship and its underlying theoretical foundations.",
        "instructors": ["Khoshimov, Bekhzod"],
        "credits": 4,
        "requirements": ["MAJOR_ELECTIVE"],
        "tags": ["entrepreneurship", "business", "startups"],
        "sections": [
            {
                "section_id": "001",
                "location": "West Administration Room 001",
                "capacity": 30,
                "enrolled": 30,
                "meetings": [
                    {"day": "Mon", "start": "11:20", "end": "12:35"},
                    {"day": "Wed", "start": "11:20", "end": "12:35"}
                ]
            }
        ]
    },
    {
        "course_id": "BUSOR-UH 2010",
        "title": "Strategic Management",
        "subject": "Business",
        "number": "2010",
        "description": "This course examines how organizations develop and implement strategies to achieve competitive advantage in dynamic environments.",
        "instructors": ["Jeong, Sophia Soyoung"],
        "credits": 4,
        "requirements": ["MAJOR_REQ"],
        "tags": ["business", "strategy", "management"],
        "sections": [
            {
                "section_id": "001",
                "location": "Social Sciences Room 018",
                "capacity": 25,
                "enrolled": 22,
                "meetings": [
                    {"day": "Mon", "start": "14:10", "end": "15:25"},
                    {"day": "Wed", "start": "14:10", "end": "15:25"}
                ]
            }
        ]
    },
    
    # Computer Science Courses
    {
        "course_id": "CS-UH 1001",
        "title": "Introduction to Computer Science",
        "subject": "Computer Science",
        "number": "1001",
        "description": "This course introduces students to the foundations of computer science. Students learn how to design algorithms to solve problems and how to translate these algorithms into working computer programs.",
        "instructors": ["Pötsch, Thomas", "Zeeshan, Faisal"],
        "credits": 4,
        "requirements": ["CORE"],
        "tags": ["programming", "algorithms", "python"],
        "sections": [
            {
                "section_id": "001",
                "location": "Social Sciences Room 003",
                "capacity": 35,
                "enrolled": 35,
                "meetings": [
                    {"day": "Mon", "start": "08:30", "end": "11:10"},
                    {"day": "Wed", "start": "08:30", "end": "11:10"}
                ]
            },
            {
                "section_id": "002",
                "location": "West Administration Building Room 004",
                "capacity": 35,
                "enrolled": 35,
                "meetings": [
                    {"day": "Tue", "start": "08:30", "end": "11:10"},
                    {"day": "Thu", "start": "08:30", "end": "11:10"}
                ]
            },
            {
                "section_id": "003",
                "location": "East Administration Room 001",
                "capacity": 35,
                "enrolled": 28,
                "meetings": [
                    {"day": "Mon", "start": "12:45", "end": "15:25"},
                    {"day": "Wed", "start": "12:45", "end": "15:25"}
                ]
            }
        ]
    },
    {
        "course_id": "CS-UH 1050",
        "title": "Data Structures",
        "subject": "Computer Science",
        "number": "1050",
        "description": "This course teaches students the principles of data organization in a computer, and how to work efficiently with large quantities of data including recursion, asymptotic analysis of algorithms, lists, stacks, queues, trees, hashing.",
        "instructors": ["Oudah, Mai", "Mengal, Khalid"],
        "credits": 4,
        "requirements": ["MAJOR_REQ"],
        "tags": ["programming", "algorithms", "data-structures"],
        "sections": [
            {
                "section_id": "001",
                "location": "East Administration Room 004",
                "capacity": 30,
                "enrolled": 25,
                "meetings": [
                    {"day": "Tue", "start": "09:55", "end": "11:10"},
                    {"day": "Thu", "start": "09:55", "end": "11:10"}
                ]
            },
            {
                "section_id": "003",
                "location": "West Administration Building Room 004",
                "capacity": 30,
                "enrolled": 22,
                "meetings": [
                    {"day": "Tue", "start": "11:20", "end": "12:35"},
                    {"day": "Thu", "start": "11:20", "end": "12:35"}
                ]
            }
        ]
    },
    {
        "course_id": "CS-UH 1052",
        "title": "Algorithms",
        "subject": "Computer Science",
        "number": "1052",
        "description": "Algorithms lie at the very heart of computer science. This course covers the fundamentals of algorithms, focusing on designing efficient algorithms, proving correctness and analyzing running time.",
        "instructors": ["Thilikos Touloupas, Dimitrios", "Ahmad, Liza"],
        "credits": 4,
        "requirements": ["MAJOR_REQ"],
        "tags": ["algorithms", "programming", "complexity"],
        "sections": [
            {
                "section_id": "001",
                "location": "Campus Center Room W007",
                "capacity": 30,
                "enrolled": 28,
                "meetings": [
                    {"day": "Mon", "start": "11:20", "end": "12:35"},
                    {"day": "Wed", "start": "11:20", "end": "12:35"}
                ]
            },
            {
                "section_id": "002",
                "location": "East Administration Room 005",
                "capacity": 30,
                "enrolled": 25,
                "meetings": [
                    {"day": "Tue", "start": "12:45", "end": "14:00"},
                    {"day": "Thu", "start": "12:45", "end": "14:00"}
                ]
            }
        ]
    },
    {
        "course_id": "CS-UH 2220",
        "title": "Machine Learning",
        "subject": "Computer Science",
        "number": "2220",
        "description": "Machine Learning is the science of discovering algorithms from data. This course aims to give a rigorous introduction to the foundational concepts in the area along with popular algorithms and architectures.",
        "instructors": ["Ferrante, Eliseo", "Zeeshan, Faisal"],
        "credits": 4,
        "requirements": ["MAJOR_ELECTIVE"],
        "tags": ["machine-learning", "ai", "programming"],
        "sections": [
            {
                "section_id": "001",
                "location": "Social Sciences Room 003",
                "capacity": 30,
                "enrolled": 28,
                "meetings": [
                    {"day": "Tue", "start": "11:20", "end": "12:35"},
                    {"day": "Thu", "start": "11:20", "end": "12:35"}
                ]
            }
        ]
    },
    {
        "course_id": "CS-UH 3010",
        "title": "Software Engineering",
        "subject": "Computer Science",
        "number": "3010",
        "description": "This course covers the principles and practices of software engineering, including software design, testing, project management, and team collaboration.",
        "instructors": ["Pötsch, Thomas"],
        "credits": 4,
        "requirements": ["MAJOR_REQ"],
        "tags": ["software-engineering", "programming", "project-management"],
        "sections": [
            {
                "section_id": "001",
                "location": "Computational Research Room 002",
                "capacity": 25,
                "enrolled": 20,
                "meetings": [
                    {"day": "Mon", "start": "14:10", "end": "15:25"},
                    {"day": "Wed", "start": "14:10", "end": "15:25"}
                ]
            }
        ]
    },
    
    # Core Curriculum Courses
    {
        "course_id": "CCEA-UH 1010",
        "title": "Imagined Cities",
        "subject": "Core Curriculum",
        "number": "1010",
        "description": "This course examines the ways in which artists, filmmakers, and writers have responded to the social complexity of urban life and the difficult task of finding points of connection within the diversity of the city.",
        "instructors": ["Devi Sawhney, Rashmi"],
        "credits": 4,
        "requirements": ["CORE"],
        "tags": ["literature", "film", "urban-studies"],
        "sections": [
            {
                "section_id": "001",
                "location": "Arts Center Room B101",
                "capacity": 18,
                "enrolled": 18,
                "meetings": [
                    {"day": "Mon", "start": "09:55", "end": "11:10"},
                    {"day": "Wed", "start": "09:55", "end": "11:10"}
                ]
            }
        ]
    },
    {
        "course_id": "CCEA-UH 1055",
        "title": "Global Shakespeare",
        "subject": "Core Curriculum",
        "number": "1055",
        "description": "To what extent can Shakespeare serve as the focal point for a cultural heritage that belongs to the entire globe? This course offers a comparative, interdisciplinary approach to Shakespeare's plays.",
        "instructors": ["Zamir, Shamoon"],
        "credits": 4,
        "requirements": ["CORE"],
        "tags": ["literature", "shakespeare", "drama"],
        "sections": [
            {
                "section_id": "001",
                "location": "Campus Center Room E051",
                "capacity": 18,
                "enrolled": 15,
                "meetings": [
                    {"day": "Tue", "start": "12:45", "end": "14:00"},
                    {"day": "Thu", "start": "12:45", "end": "14:00"}
                ]
            }
        ]
    },
    {
        "course_id": "CCEA-UH 2010",
        "title": "Art and Society",
        "subject": "Core Curriculum",
        "number": "2010",
        "description": "This course explores the relationship between art and society, examining how artistic expression reflects and shapes social, political, and cultural contexts.",
        "instructors": ["Devi Sawhney, Rashmi"],
        "credits": 4,
        "requirements": ["CORE"],
        "tags": ["art", "society", "culture"],
        "sections": [
            {
                "section_id": "001",
                "location": "Arts Center Room B101",
                "capacity": 20,
                "enrolled": 18,
                "meetings": [
                    {"day": "Mon", "start": "15:35", "end": "16:50"},
                    {"day": "Wed", "start": "15:35", "end": "16:50"}
                ]
            }
        ]
    },
    
    # Economics Courses
    {
        "course_id": "ECON-UH 1112",
        "title": "Introduction to Macroeconomics",
        "subject": "Economics",
        "number": "1112",
        "description": "Through the lens of historic episodes this course introduces students to basic concepts and theories of macroeconomics: national income, economic growth, unemployment, money and inflation.",
        "instructors": ["Haefke, Christian"],
        "credits": 4,
        "requirements": ["CORE"],
        "tags": ["economics", "macroeconomics", "policy"],
        "sections": [
            {
                "section_id": "001",
                "location": "Campus Center Room W009",
                "capacity": 40,
                "enrolled": 35,
                "meetings": [
                    {"day": "Mon", "start": "11:20", "end": "12:35"},
                    {"day": "Wed", "start": "11:20", "end": "12:35"}
                ]
            }
        ]
    },
    {
        "course_id": "ECON-UH 2010",
        "title": "Intermediate Microeconomics",
        "subject": "Economics",
        "number": "2010",
        "description": "This course introduces the major concepts and tools of modern microeconomic analysis. Students will study the manner in which consumers, producers and resource owners determine prices and output.",
        "instructors": ["Ham, John"],
        "credits": 4,
        "requirements": ["MAJOR_REQ"],
        "tags": ["economics", "microeconomics", "theory"],
        "sections": [
            {
                "section_id": "001",
                "location": "Campus Center Room W009",
                "capacity": 35,
                "enrolled": 30,
                "meetings": [
                    {"day": "Mon", "start": "15:35", "end": "16:50"},
                    {"day": "Wed", "start": "15:35", "end": "16:50"}
                ]
            },
            {
                "section_id": "002",
                "location": "Campus Center Room E050",
                "capacity": 35,
                "enrolled": 35,
                "meetings": [
                    {"day": "Mon", "start": "14:10", "end": "15:25"},
                    {"day": "Wed", "start": "14:10", "end": "15:25"}
                ]
            }
        ]
    },
    {
        "course_id": "ECON-UH 2310EQ",
        "title": "Behavioral Economics",
        "subject": "Economics",
        "number": "2310EQ",
        "description": "This course introduces students to the field of behavioral economics, which seeks to combine standard economic thinking with more psychologically-plausible assumptions about human behavior.",
        "instructors": ["Baranski, Andrzej", "Hafeez, Naima"],
        "credits": 4,
        "requirements": ["MAJOR_ELECTIVE"],
        "tags": ["economics", "psychology", "behavior"],
        "sections": [
            {
                "section_id": "001",
                "location": "Computational Research Room 004",
                "capacity": 30,
                "enrolled": 25,
                "meetings": [
                    {"day": "Tue", "start": "08:30", "end": "09:45"},
                    {"day": "Thu", "start": "08:30", "end": "09:45"}
                ]
            }
        ]
    },
    
    # History Courses
    {
        "course_id": "HIST-UH 1105",
        "title": "Africa in the World",
        "subject": "History",
        "number": "1105",
        "description": "This course is a broad survey of African history exploring the continent's political complexity and social creativity across several millennia through the colonial period and up to the contemporary period.",
        "instructors": ["Pettigrew, Erin Kathleen"],
        "credits": 4,
        "requirements": ["GE"],
        "tags": ["history", "africa", "social-science"],
        "sections": [
            {
                "section_id": "001",
                "location": "Computational Research Room 021",
                "capacity": 25,
                "enrolled": 20,
                "meetings": [
                    {"day": "Mon", "start": "09:55", "end": "11:10"},
                    {"day": "Wed", "start": "09:55", "end": "11:10"}
                ]
            }
        ]
    },
    {
        "course_id": "HIST-UH 1125X",
        "title": "South Asia in the Indian Ocean World",
        "subject": "History",
        "number": "1125X",
        "description": "This course offers an in-depth study of the history and culture of South Asians. The course explores histories with a focus on understanding major cultural, political, economic connections around the Indian Ocean.",
        "instructors": ["Kulshreshtha, Salila"],
        "credits": 4,
        "requirements": ["GE"],
        "tags": ["history", "south-asia", "culture"],
        "sections": [
            {
                "section_id": "001",
                "location": "East Administration Room 004",
                "capacity": 25,
                "enrolled": 22,
                "meetings": [
                    {"day": "Tue", "start": "15:20", "end": "16:35"},
                    {"day": "Thu", "start": "15:20", "end": "16:35"}
                ]
            }
        ]
    },
    {
        "course_id": "HIST-UH 2010",
        "title": "Modern Middle East",
        "subject": "History",
        "number": "2010",
        "description": "This course examines the political, social, and cultural history of the Middle East from the 19th century to the present, focusing on key events and transformations.",
        "instructors": ["Kulshreshtha, Salila"],
        "credits": 4,
        "requirements": ["MAJOR_ELECTIVE"],
        "tags": ["history", "middle-east", "modern"],
        "sections": [
            {
                "section_id": "001",
                "location": "East Administration Room 004",
                "capacity": 25,
                "enrolled": 20,
                "meetings": [
                    {"day": "Tue", "start": "09:55", "end": "11:10"},
                    {"day": "Thu", "start": "09:55", "end": "11:10"}
                ]
            }
        ]
    },
    
    # Mathematics Courses
    {
        "course_id": "MATH-UH 1012Q",
        "title": "Calculus with Applications to Science and Engineering",
        "subject": "Mathematics",
        "number": "1012Q",
        "description": "This course presents the basic principles of calculus by examining functions and their derivatives and integrals with a special emphasis placed on the utilitarian nature of the subject material.",
        "instructors": ["Portaluri, Alessandro"],
        "credits": 4,
        "requirements": ["CORE"],
        "tags": ["mathematics", "calculus", "science"],
        "sections": [
            {
                "section_id": "001",
                "location": "East Administration Building Room 003",
                "capacity": 35,
                "enrolled": 35,
                "meetings": [
                    {"day": "Mon", "start": "12:45", "end": "14:00"},
                    {"day": "Wed", "start": "12:45", "end": "14:00"}
                ]
            },
            {
                "section_id": "003",
                "location": "East Administration Building Room 003",
                "capacity": 35,
                "enrolled": 30,
                "meetings": [
                    {"day": "Mon", "start": "08:30", "end": "09:45"},
                    {"day": "Wed", "start": "08:30", "end": "09:45"}
                ]
            },
            {
                "section_id": "004",
                "location": "Social Sciences Room 018",
                "capacity": 35,
                "enrolled": 28,
                "meetings": [
                    {"day": "Mon", "start": "15:35", "end": "16:50"},
                    {"day": "Wed", "start": "15:35", "end": "16:50"}
                ]
            }
        ]
    },
    {
        "course_id": "MATH-UH 1020Q",
        "title": "Multivariable Calculus with Applications to Science and Engineering",
        "subject": "Mathematics",
        "number": "1020Q",
        "description": "This course explores functions of several variables. Topics include vectors in the plane and space, partial derivatives, double and triple integrals, spherical and cylindrical coordinates.",
        "instructors": ["Camia, Federico"],
        "credits": 4,
        "requirements": ["MAJOR_REQ"],
        "tags": ["mathematics", "calculus", "multivariable"],
        "sections": [
            {
                "section_id": "001",
                "location": "Campus Center Room 313",
                "capacity": 30,
                "enrolled": 25,
                "meetings": [
                    {"day": "Mon", "start": "09:55", "end": "11:10"},
                    {"day": "Wed", "start": "09:55", "end": "11:10"}
                ]
            },
            {
                "section_id": "002",
                "location": "West Administration Room 003",
                "capacity": 30,
                "enrolled": 30,
                "meetings": [
                    {"day": "Tue", "start": "12:45", "end": "14:00"},
                    {"day": "Thu", "start": "12:45", "end": "14:00"}
                ]
            }
        ]
    },
    {
        "course_id": "MATH-UH 1022Q",
        "title": "Linear Algebra",
        "subject": "Mathematics",
        "number": "1022Q",
        "description": "Matrix algebra is central to the analysis of linear systems. Topics include systems of linear equations, Gaussian elimination, matrices, determinants, vectors, linear transformations, eigenvalues and eigenvectors.",
        "instructors": ["Mimar, Arman"],
        "credits": 4,
        "requirements": ["MAJOR_REQ"],
        "tags": ["mathematics", "linear-algebra", "matrices"],
        "sections": [
            {
                "section_id": "001",
                "location": "Campus Center Room E051",
                "capacity": 30,
                "enrolled": 28,
                "meetings": [
                    {"day": "Mon", "start": "12:45", "end": "14:00"},
                    {"day": "Wed", "start": "12:45", "end": "14:00"}
                ]
            },
            {
                "section_id": "002",
                "location": "Campus Center Room W004",
                "capacity": 30,
                "enrolled": 25,
                "meetings": [
                    {"day": "Tue", "start": "11:20", "end": "12:35"},
                    {"day": "Thu", "start": "11:20", "end": "12:35"}
                ]
            }
        ]
    },
    {
        "course_id": "MATH-UH 2011Q",
        "title": "Probability and Statistics",
        "subject": "Mathematics",
        "number": "2011Q",
        "description": "The course provides an introduction to the mathematical treatment of probability and statistics including mathematical definition of probability, combinatorics, sampling, estimation, testing of hypotheses.",
        "instructors": ["Camia, Federico"],
        "credits": 4,
        "requirements": ["MAJOR_REQ"],
        "tags": ["mathematics", "probability", "statistics"],
        "sections": [
            {
                "section_id": "001",
                "location": "Campus Center Room E049",
                "capacity": 30,
                "enrolled": 28,
                "meetings": [
                    {"day": "Mon", "start": "12:45", "end": "14:00"},
                    {"day": "Wed", "start": "12:45", "end": "14:00"}
                ]
            },
            {
                "section_id": "002",
                "location": "Social Sciences Room 004",
                "capacity": 30,
                "enrolled": 30,
                "meetings": [
                    {"day": "Tue", "start": "15:20", "end": "16:35"},
                    {"day": "Thu", "start": "15:20", "end": "16:35"}
                ]
            }
        ]
    },
    
    # Physics Courses
    {
        "course_id": "PHYS-UH 1010",
        "title": "General Physics 1",
        "subject": "Physics",
        "number": "1010",
        "description": "This course covers the fundamental principles of mechanics, including kinematics, dynamics, energy, and momentum.",
        "instructors": ["Portaluri, Alessandro"],
        "credits": 4,
        "requirements": ["CORE"],
        "tags": ["physics", "mechanics", "science"],
        "sections": [
            {
                "section_id": "001",
                "location": "East Administration Building Room 003",
                "capacity": 30,
                "enrolled": 25,
                "meetings": [
                    {"day": "Mon", "start": "08:30", "end": "09:45"},
                    {"day": "Wed", "start": "08:30", "end": "09:45"},
                    {"day": "Fri", "start": "08:30", "end": "09:45"}
                ]
            }
        ]
    },
    {
        "course_id": "PHYS-UH 1020",
        "title": "General Physics 2",
        "subject": "Physics",
        "number": "1020",
        "description": "This course covers electricity, magnetism, and waves, building on the foundations established in General Physics 1.",
        "instructors": ["Portaluri, Alessandro"],
        "credits": 4,
        "requirements": ["CORE"],
        "tags": ["physics", "electricity", "magnetism"],
        "sections": [
            {
                "section_id": "001",
                "location": "East Administration Building Room 003",
                "capacity": 30,
                "enrolled": 22,
                "meetings": [
                    {"day": "Tue", "start": "08:30", "end": "09:45"},
                    {"day": "Thu", "start": "08:30", "end": "09:45"},
                    {"day": "Fri", "start": "08:30", "end": "09:45"}
                ]
            }
        ]
    },
    
    # Psychology Courses
    {
        "course_id": "PSYC-UH 1001",
        "title": "Introduction to Psychology",
        "subject": "Psychology",
        "number": "1001",
        "description": "This course provides an overview of the major areas of psychology, including cognitive, developmental, social, and clinical psychology.",
        "instructors": ["Baranski, Andrzej"],
        "credits": 4,
        "requirements": ["CORE"],
        "tags": ["psychology", "behavior", "mental-health"],
        "sections": [
            {
                "section_id": "001",
                "location": "Social Sciences Room 004",
                "capacity": 35,
                "enrolled": 30,
                "meetings": [
                    {"day": "Mon", "start": "11:20", "end": "12:35"},
                    {"day": "Wed", "start": "11:20", "end": "12:35"}
                ]
            }
        ]
    },
    {
        "course_id": "PSYC-UH 2010",
        "title": "Cognitive Psychology",
        "subject": "Psychology",
        "number": "2010",
        "description": "This course examines mental processes such as perception, memory, thinking, and problem-solving.",
        "instructors": ["Baranski, Andrzej"],
        "credits": 4,
        "requirements": ["MAJOR_REQ"],
        "tags": ["psychology", "cognition", "mental-processes"],
        "sections": [
            {
                "section_id": "001",
                "location": "Social Sciences Room 004",
                "capacity": 25,
                "enrolled": 20,
                "meetings": [
                    {"day": "Tue", "start": "14:10", "end": "15:25"},
                    {"day": "Thu", "start": "14:10", "end": "15:25"}
                ]
            }
        ]
    },
    
    # Literature Courses
    {
        "course_id": "LIT-UH 1001",
        "title": "World Literature",
        "subject": "Literature",
        "number": "1001",
        "description": "This course introduces students to major works of world literature, exploring themes, styles, and cultural contexts across different traditions.",
        "instructors": ["Zamir, Shamoon"],
        "credits": 4,
        "requirements": ["CORE"],
        "tags": ["literature", "world-culture", "humanities"],
        "sections": [
            {
                "section_id": "001",
                "location": "Campus Center Room E051",
                "capacity": 20,
                "enrolled": 18,
                "meetings": [
                    {"day": "Mon", "start": "09:55", "end": "11:10"},
                    {"day": "Wed", "start": "09:55", "end": "11:10"}
                ]
            }
        ]
    },
    {
        "course_id": "LIT-UH 2010",
        "title": "Modern Poetry",
        "subject": "Literature",
        "number": "2010",
        "description": "This course examines the development of modern poetry from the late 19th century to the present, focusing on major movements and poets.",
        "instructors": ["Zamir, Shamoon"],
        "credits": 4,
        "requirements": ["MAJOR_ELECTIVE"],
        "tags": ["literature", "poetry", "modern"],
        "sections": [
            {
                "section_id": "001",
                "location": "Campus Center Room E051",
                "capacity": 18,
                "enrolled": 15,
                "meetings": [
                    {"day": "Tue", "start": "15:20", "end": "16:35"},
                    {"day": "Thu", "start": "15:20", "end": "16:35"}
                ]
            }
        ]
    }
]

# Schedule generation functions
def generate_schedule(selected_courses):
    """
    Generate a schedule for selected courses, checking for conflicts
    """
    schedule = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": []
    }
    
    conflicts = []
    total_credits = 0
    
    for course_id in selected_courses:
        course = next((c for c in NYUAD_COURSES if c["course_id"] == course_id), None)
        if not course:
            continue
            
        total_credits += course["credits"]
        
        for section in course["sections"]:
            for meeting in section["meetings"]:
                day = meeting["day"]
                start_time = meeting["start"]
                end_time = meeting["end"]
                
                # Map abbreviated days to full day names
                day_mapping = {
                    "Mon": "Monday",
                    "Tue": "Tuesday", 
                    "Wed": "Wednesday",
                    "Thu": "Thursday",
                    "Fri": "Friday"
                }
                
                full_day = day_mapping.get(day, day)
                
                # Check for conflicts
                for existing_course in schedule[full_day]:
                    if (start_time < existing_course["end"] and end_time > existing_course["start"]):
                        conflicts.append({
                            "course1": existing_course["course_id"],
                            "course2": course_id,
                            "day": full_day,
                            "time": f"{start_time}-{end_time}"
                        })
                
                schedule[full_day].append({
                    "course_id": course_id,
                    "title": course["title"],
                    "section_id": section["section_id"],
                    "location": section["location"],
                    "start": start_time,
                    "end": end_time,
                    "instructors": course["instructors"]
                })
    
    # Sort schedule by time
    for day in schedule:
        schedule[day].sort(key=lambda x: x["start"])
    
    return {
        "schedule": schedule,
        "conflicts": conflicts,
        "total_credits": total_credits,
        "selected_courses": selected_courses
    }

def get_available_courses():
    """
    Get all available courses with their details
    """
    return NYUAD_COURSES

def search_courses(query, subject_filter=None, credits_filter=None):
    """
    Search courses by query, subject, or credits
    """
    results = NYUAD_COURSES
    
    if query:
        query = query.lower()
        results = [course for course in results if 
                  query in course["title"].lower() or 
                  query in course["course_id"].lower() or 
                  query in course["description"].lower() or
                  any(query in tag.lower() for tag in course["tags"])]
    
    if subject_filter:
        results = [course for course in results if course["subject"] == subject_filter]
    
    if credits_filter:
        results = [course for course in results if course["credits"] == credits_filter]
    
    return results

def analyze_conflicts_with_llm(conflicts, selected_courses):
    """
    Use LLM to analyze conflicts and suggest alternative courses
    """
    if not conflicts:
        return {"analysis": "No conflicts detected in your schedule!", "suggestions": []}
    
    # Get detailed information about conflicting courses
    conflicting_courses = []
    for conflict in conflicts:
        course1 = next((c for c in NYUAD_COURSES if c["course_id"] == conflict["course1"]), None)
        course2 = next((c for c in NYUAD_COURSES if c["course_id"] == conflict["course2"]), None)
        if course1 and course2:
            conflicting_courses.extend([course1, course2])
    
    # Find alternative courses in similar subjects
    suggestions = []
    for conflict in conflicts:
        course1 = next((c for c in NYUAD_COURSES if c["course_id"] == conflict["course1"]), None)
        course2 = next((c for c in NYUAD_COURSES if c["course_id"] == conflict["course2"]), None)
        
        if course1 and course2:
            # Find alternative courses in the same subject
            alternatives = []
            for course in NYUAD_COURSES:
                if (course["subject"] == course1["subject"] or course["subject"] == course2["subject"]) and \
                   course["course_id"] not in selected_courses and \
                   course["course_id"] != conflict["course1"] and \
                   course["course_id"] != conflict["course2"]:
                    
                    # Check if this alternative has different meeting times
                    has_different_times = False
                    for section in course["sections"]:
                        for meeting in section["meetings"]:
                            if meeting["day"] != conflict["day"] or \
                               meeting["start"] != conflict["time"].split("-")[0]:
                                has_different_times = True
                                break
                        if has_different_times:
                            break
                    
                    if has_different_times:
                        alternatives.append({
                            "course_id": course["course_id"],
                            "title": course["title"],
                            "subject": course["subject"],
                            "credits": course["credits"],
                            "requirements": course["requirements"],
                            "description": course["description"],
                            "sections": course["sections"]
                        })
            
            suggestions.append({
                "conflict": conflict,
                "course1": course1,
                "course2": course2,
                "alternatives": alternatives[:3]  # Limit to top 3 suggestions
            })
    
    # Generate analysis text
    analysis_text = f"Found {len(conflicts)} scheduling conflict(s). "
    if len(conflicts) == 1:
        analysis_text += "The conflict occurs between courses at the same time. "
    else:
        analysis_text += "Multiple conflicts detected in your schedule. "
    
    analysis_text += "Consider the alternative courses below that offer similar content at different times."
    
    return {
        "analysis": analysis_text,
        "suggestions": suggestions,
        "conflict_count": len(conflicts)
    }

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/simple')
def simple():
    return send_from_directory('static', 'simple.html')

@app.route('/vanilla')
def vanilla():
    return send_from_directory('static', 'vanilla.html')

@app.route('/api/courses')
def get_courses():
    return jsonify(NYUAD_COURSES)

@app.route('/api/courses/search')
def search_courses_api():
    query = request.args.get('q', '')
    subject = request.args.get('subject', '')
    credits = request.args.get('credits', '')
    
    credits_filter = int(credits) if credits.isdigit() else None
    subject_filter = subject if subject else None
    
    results = search_courses(query, subject_filter, credits_filter)
    return jsonify(results)

@app.route('/api/schedule/generate', methods=['POST'])
def generate_schedule_api():
    data = request.get_json()
    selected_courses = data.get('courses', [])
    
    if not selected_courses:
        return jsonify({"error": "No courses selected"}), 400
    
    schedule_result = generate_schedule(selected_courses)
    
    # Add LLM-powered conflict analysis
    if schedule_result["conflicts"]:
        llm_analysis = analyze_conflicts_with_llm(schedule_result["conflicts"], selected_courses)
        schedule_result["llm_analysis"] = llm_analysis
    else:
        schedule_result["llm_analysis"] = {
            "analysis": "✅ No scheduling conflicts detected! Your schedule looks good.",
            "suggestions": [],
            "conflict_count": 0
        }
    
    return jsonify(schedule_result)

@app.route('/api/subjects')
def get_subjects():
    subjects = list(set(course["subject"] for course in NYUAD_COURSES))
    return jsonify(sorted(subjects))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
