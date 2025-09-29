import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import re
import json
import datetime
from typing import Dict, List, Tuple, Set
import threading
import time

class StudentProfile:
    def __init__(self):
        self.student_id = None
        self.name = None
        self.email = None
        self.major = None
        self.year = None
        self.registered_courses = set()
        self.schedule = {}
        self.credits_total = 0
        self.is_authenticated = False

    def authenticate(self, student_id: str, name: str) -> bool:
        if student_id and name:
            self.student_id = student_id
            self.name = name
            self.is_authenticated = True
            return True
        return False

    def register_course(self, course_code: str) -> bool:
        if course_code not in self.registered_courses:
            self.registered_courses.add(course_code)
            return True
        return False

    def drop_course(self, course_code: str) -> bool:
        if course_code in self.registered_courses:
            self.registered_courses.remove(course_code)
            return True
        return False


class UniversityKnowledgeBase:
    def __init__(self):
        self.courses = {
            "CS101": {
                "name": "Introduction to Computer Science",
                "credits": 3,
                "prerequisites": [],
                "description": "Basic programming concepts and problem-solving techniques",
                "schedule": "MWF 9:00-10:00 AM",
                "instructor": "Dr. Smith",
                "room": "Tech Building 101",
                "capacity": 30,
                "enrolled": 15,
                "available": True
            },
            "CS201": {
                "name": "Data Structures and Algorithms",
                "credits": 4,
                "prerequisites": ["CS101"],
                "description": "Advanced data structures, algorithm design and analysis",
                "schedule": "TTh 2:00-3:30 PM",
                "instructor": "Dr. Johnson",
                "room": "Tech Building 205",
                "capacity": 25,
                "enrolled": 20,
                "available": True
            },
            "MATH101": {
                "name": "Calculus I",
                "credits": 4,
                "prerequisites": [],
                "description": "Differential and integral calculus",
                "schedule": "MWF 11:00-12:00 PM",
                "instructor": "Dr. Williams",
                "room": "Math Building 301",
                "capacity": 40,
                "enrolled": 35,
                "available": True
            },
            "ENG101": {
                "name": "English Composition",
                "credits": 3,
                "prerequisites": [],
                "description": "Academic writing and communication skills",
                "schedule": "TTh 10:00-11:30 AM",
                "instructor": "Prof. Brown",
                "room": "Liberal Arts 150",
                "capacity": 20,
                "enrolled": 18,
                "available": True
            },
            "PHY201": {
                "name": "Physics I",
                "credits": 4,
                "prerequisites": ["MATH101"],
                "description": "Mechanics, waves, and thermodynamics",
                "schedule": "MWF 1:00-2:00 PM, Lab: W 3:00-5:00 PM",
                "instructor": "Dr. Davis",
                "room": "Science Building 220",
                "capacity": 24,
                "enrolled": 22,
                "available": True
            },
            "CS301": {
                "name": "Database Systems",
                "credits": 3,
                "prerequisites": ["CS201"],
                "description": "Database design, SQL, and data management",
                "schedule": "MW 3:00-4:30 PM",
                "instructor": "Dr. Miller",
                "room": "Tech Building 301",
                "capacity": 20,
                "enrolled": 8,
                "available": True
            }
        }

        self.departments = {
            "computer_science": {
                "name": "Computer Science",
                "head": "Dr. Anderson",
                "location": "Tech Building, 3rd Floor",
                "phone": "(555) 123-4567",
                "email": "cs@university.edu",
                "popular_courses": ["CS101", "CS201", "CS301"]
            },
            "mathematics": {
                "name": "Mathematics",
                "head": "Dr. Wilson",
                "location": "Math Building, 2nd Floor",
                "phone": "(555) 234-5678",
                "email": "math@university.edu",
                "popular_courses": ["MATH101"]
            },
            "english": {
                "name": "English",
                "head": "Prof. Thompson",
                "location": "Liberal Arts Building, 1st Floor",
                "phone": "(555) 345-6789",
                "email": "english@university.edu",
                "popular_courses": ["ENG101"]
            },
            "physics": {
                "name": "Physics",
                "head": "Dr. Garcia",
                "location": "Science Building, 4th Floor",
                "phone": "(555) 456-7890",
                "email": "physics@university.edu",
                "popular_courses": ["PHY201"]
            }
        }

        self.general_info = {
            "registration_dates": {
                "fall_2024": "August 1-15, 2024",
                "spring_2025": "December 1-15, 2024",
                "summer_2025": "April 1-15, 2025"
            },
            "academic_calendar": {
                "fall_start": "August 28, 2024",
                "fall_end": "December 15, 2024",
                "spring_start": "January 15, 2025",
                "spring_end": "May 10, 2025"
            },
            "services": {
                "library": "Main Library - Open 24/7 during finals",
                "tutoring": "Academic Success Center - Free tutoring available",
                "counseling": "Student Counseling Center - Mental health support",
                "career": "Career Services - Job placement assistance"
            }
        }


class NLPProcessor:
    def __init__(self, knowledge_base: UniversityKnowledgeBase):
        self.kb = knowledge_base
        self.intent_patterns = {
            "course_info": [
                r"(tell me about|what is|describe) (course )?(\w+\d+)",
                r"(\w+\d+) (course|class) (info|information|details)",
                r"(info|information|details) (about|on) (\w+\d+)"
            ],
            "course_schedule": [
                r"when (is|does) (\w+\d+) (meet|held|scheduled)",
                r"(\w+\d+) (schedule|time|timing)",
                r"what time (is )?(\w+\d+)"
            ],
            "prerequisites": [
                r"(what are the )?(prerequisites|prereqs) (for )?(\w+\d+)",
                r"(\w+\d+) (prerequisites|prereqs|requirements)",
                r"what (do i need|courses needed) (for|before) (\w+\d+)"
            ],
            "department_info": [
                r"(tell me about|what is|describe) (the )?(\w+) department",
                r"(\w+) department (info|information|contact)",
                r"who (is the head|heads) (of )?(the )?(\w+) department"
            ],
            "registration": [
                r"when (is|does) registration (start|begin|open)",
                r"registration (dates|schedule|period)",
                r"how (do i|to) register (for courses|for classes)"
            ],
            "register_course": [
                r"register (for|me for) (\w+\d+)",
                r"enroll (in|me in) (\w+\d+)",
                r"add (\w+\d+) (to my schedule|to schedule)",
                r"i want to (register for|take) (\w+\d+)"
            ],
            "drop_course": [
                r"drop (\w+\d+)",
                r"remove (\w+\d+) (from my schedule)",
                r"unregister (from )?(\w+\d+)",
                r"i want to drop (\w+\d+)"
            ],
            "my_schedule": [
                r"(show|what is|display) my (schedule|courses)",
                r"what (courses|classes) am i (taking|registered for)",
                r"my (current )?schedule",
                r"what (courses|classes) do i have"
            ],
            "available_courses": [
                r"(what|which) courses are available",
                r"show (me )?available courses",
                r"list (all )?courses",
                r"what can i take"
            ],
            "login": [
                r"login|log in|sign in|authenticate",
                r"i am (\w+)",
                r"my name is (\w+)"
            ],
            "confirm": [
                r"(yes|yeah|yep|confirm|ok|okay|proceed)",
                r"do it|go ahead"
            ],
            "cancel": [
                r"(no|nope|cancel|abort|stop)",
                r"never mind|forget it"
            ],
            "services": [
                r"(what|tell me about) (university )?services",
                r"(library|tutoring|counseling|career) (services|hours|info)",
                r"where (is|can i find) (the )?(library|tutoring|counseling)"
            ]
        }

    def extract_course_code(self, text: str) -> str:
        match = re.search(r'([A-Z]{2,4}\d{3})', text.upper())
        return match.group(1) if match else None

    def extract_department(self, text: str) -> str:
        text_lower = text.lower()
        for dept_key, dept_info in self.kb.departments.items():
            if (dept_key.replace('_', ' ') in text_lower or
                    dept_info['name'].lower() in text_lower):
                return dept_key
        dept_mapping = {
            'cs': 'computer_science',
            'comp sci': 'computer_science',
            'math': 'mathematics',
            'eng': 'english',
            'phys': 'physics'
        }

        for abbrev, full_name in dept_mapping.items():
            if abbrev in text_lower:
                return full_name

        return None

    def classify_intent(self, text: str) -> Tuple[str, Dict]:
        text_lower = text.lower()

        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text_lower)
                if match:
                    entities = {}
                    course_code = self.extract_course_code(text)
                    if course_code:
                        entities['course_code'] = course_code

                    department = self.extract_department(text)
                    if department:
                        entities['department'] = department

                    return intent, entities

        return "general", {}


class UniversityChatbot:
    def __init__(self):
        self.kb = UniversityKnowledgeBase()
        self.nlp = NLPProcessor(self.kb)
        self.conversation_history = []
        self.student = StudentProfile()
        self.pending_action = None
        self.pending_course = None

    def generate_response(self, user_input: str) -> str:
        intent, entities = self.nlp.classify_intent(user_input)

        self.conversation_history.append({
            "user": user_input,
            "intent": intent,
            "entities": entities,
            "timestamp": datetime.datetime.now()
        })

        if self.pending_action:
            if intent == "confirm":
                return self._execute_pending_action()
            elif intent == "cancel":
                return self._cancel_pending_action()

        if intent == "login":
            return self._handle_login(user_input)
        elif intent == "course_info":
            return self._handle_course_info(entities)
        elif intent == "course_schedule":
            return self._handle_course_schedule(entities)
        elif intent == "prerequisites":
            return self._handle_prerequisites(entities)
        elif intent == "department_info":
            return self._handle_department_info(entities)
        elif intent == "registration":
            return self._handle_registration()
        elif intent == "register_course":
            return self._handle_register_course(entities)
        elif intent == "drop_course":
            return self._handle_drop_course(entities)
        elif intent == "my_schedule":
            return self._handle_my_schedule()
        elif intent == "available_courses":
            return self._handle_available_courses()
        elif intent == "services":
            return self._handle_services(user_input)
        else:
            return self._handle_general(user_input)

    def _handle_login(self, user_input: str) -> str:
        if self.student.is_authenticated:
            return f"You're already logged in as {self.student.name} (ID: {self.student.student_id})"

        name_match = re.search(r'(my name is|i am) (\w+)', user_input.lower())
        if name_match:
            name = name_match.group(2).capitalize()
            student_id = f"STU{hash(name) % 10000:04d}"
            self.student.authenticate(student_id, name)
            return f"Welcome, {name}! You're now logged in with ID: {student_id}.\nYou can now register for courses, view your schedule, and more!"
        else:
            return "Please tell me your name to log in (e.g., 'My name is John' or 'I am Sarah')"

    def _handle_register_course(self, entities: Dict) -> str:
        if not self.student.is_authenticated:
            return "Please log in first to register for courses. Just tell me your name!"

        course_code = entities.get('course_code')
        if not course_code or course_code not in self.kb.courses:
            return "Please specify a valid course code (e.g., CS101, MATH101)"

        course = self.kb.courses[course_code]
        if course_code in self.student.registered_courses:
            return f"You're already registered for {course_code}!"

        missing_prereqs = []
        for prereq in course['prerequisites']:
            if prereq not in self.student.registered_courses:
                missing_prereqs.append(prereq)

        if missing_prereqs:
            return f"❌ Cannot register for {course_code}. Missing prerequisites: {', '.join(missing_prereqs)}"

        if course['enrolled'] >= course['capacity']:
            return f"❌ {course_code} is full! ({course['enrolled']}/{course['capacity']} enrolled)"

        self.pending_action = "register"
        self.pending_course = course_code

        response = f"📝 **Registration Confirmation**\n\n"
        response += f"Course: {course_code} - {course['name']}\n"
        response += f"Credits: {course['credits']}\n"
        response += f"Schedule: {course['schedule']}\n"
        response += f"Instructor: {course['instructor']}\n"
        response += f"Available spots: {course['capacity'] - course['enrolled']}/{course['capacity']}\n\n"
        response += "Do you want to register for this course? (Type 'yes' to confirm or 'no' to cancel)"

        return response

    def _handle_drop_course(self, entities: Dict) -> str:
        if not self.student.is_authenticated:
            return "Please log in first to drop courses. Just tell me your name!"

        course_code = entities.get('course_code')
        if not course_code:
            return "Please specify which course you want to drop"

        if course_code not in self.student.registered_courses:
            return f"You're not registered for {course_code}"

        self.pending_action = "drop"
        self.pending_course = course_code

        course = self.kb.courses.get(course_code, {})
        response = f"🗑️ **Drop Course Confirmation**\n\n"
        response += f"Are you sure you want to drop {course_code}"
        if course:
            response += f" - {course['name']}"
        response += "?\n\nType 'yes' to confirm or 'no' to cancel"

        return response

    def _handle_my_schedule(self) -> str:
        if not self.student.is_authenticated:
            return "Please log in first to view your schedule. Just tell me your name!"

        if not self.student.registered_courses:
            return "📅 You're not registered for any courses yet.\nUse 'register for [course]' to add courses to your schedule!"

        response = f"📅 **{self.student.name}'s Schedule**\n\n"
        total_credits = 0

        for course_code in sorted(self.student.registered_courses):
            if course_code in self.kb.courses:
                course = self.kb.courses[course_code]
                response += f"• **{course_code}**: {course['name']}\n"
                response += f"  Credits: {course['credits']} | {course['schedule']}\n"
                response += f"  Instructor: {course['instructor']} | Room: {course['room']}\n\n"
                total_credits += course['credits']

        response += f"**Total Credits: {total_credits}**"
        return response

    def _handle_available_courses(self) -> str:
        response = "📚 **Available Courses**\n\n"

        for course_code, course in self.kb.courses.items():
            if course['available'] and course['enrolled'] < course['capacity']:
                spots_left = course['capacity'] - course['enrolled']
                response += f"• **{course_code}**: {course['name']}\n"
                response += f"  Credits: {course['credits']} | Spots left: {spots_left}\n"
                response += f"  Schedule: {course['schedule']}\n"
                if course['prerequisites']:
                    response += f"  Prerequisites: {', '.join(course['prerequisites'])}\n"
                response += "\n"

        response += "To register for a course, type: 'register for [course code]'"
        return response

    def _execute_pending_action(self) -> str:
        if not self.pending_action or not self.pending_course:
            return "No pending action to execute."

        action = self.pending_action
        course_code = self.pending_course
        self.pending_action = None
        self.pending_course = None

        if action == "register":
            self.student.register_course(course_code)
            self.kb.courses[course_code]['enrolled'] += 1

            course = self.kb.courses[course_code]
            response = f"✅ **Registration Successful!**\n\n"
            response += f"You're now registered for:\n"
            response += f"{course_code} - {course['name']}\n"
            response += f"Schedule: {course['schedule']}\n"
            response += f"Room: {course['room']}\n\n"
            response += "Type 'my schedule' to see all your courses!"
            return response

        elif action == "drop":
            self.student.drop_course(course_code)
            if course_code in self.kb.courses:
                self.kb.courses[course_code]['enrolled'] -= 1

            return f"✅ Successfully dropped {course_code} from your schedule."

        return "Action completed."

    def _cancel_pending_action(self) -> str:
        action = self.pending_action
        course_code = self.pending_course

        self.pending_action = None
        self.pending_course = None

        if action == "register":
            return f"❌ Registration for {course_code} cancelled."
        elif action == "drop":
            return f"❌ Drop request for {course_code} cancelled."

        return "Action cancelled."

    def _handle_course_info(self, entities: Dict) -> str:
        course_code = entities.get('course_code')

        if not course_code or course_code not in self.kb.courses:
            available_courses = ', '.join(self.kb.courses.keys())
            return f"I don't have information about that course. Available courses: {available_courses}"

        course = self.kb.courses[course_code]
        spots_left = course['capacity'] - course['enrolled']

        response = f"📚 **{course_code}: {course['name']}**\n\n"
        response += f"Credits: {course['credits']}\n"
        response += f"Instructor: {course['instructor']}\n"
        response += f"Schedule: {course['schedule']}\n"
        response += f"Room: {course['room']}\n"
        response += f"Description: {course['description']}\n"
        response += f"Capacity: {course['enrolled']}/{course['capacity']} (🟢 {spots_left} spots left)\n"

        if course['prerequisites']:
            response += f"Prerequisites: {', '.join(course['prerequisites'])}\n"
        else:
            response += "Prerequisites: None\n"

        if self.student.is_authenticated:
            if course_code in self.student.registered_courses:
                response += "\n✅ You're registered for this course!"
            else:
                response += f"\nTo register, type: 'register for {course_code}'"

        return response

    def _handle_course_schedule(self, entities: Dict) -> str:
        course_code = entities.get('course_code')

        if not course_code or course_code not in self.kb.courses:
            return "Please specify a valid course code (e.g., CS101, MATH101)"

        course = self.kb.courses[course_code]
        return f"🕐 {course_code} ({course['name']}) meets:\n{course['schedule']}\nRoom: {course['room']}"

    def _handle_prerequisites(self, entities: Dict) -> str:
        course_code = entities.get('course_code')

        if not course_code or course_code not in self.kb.courses:
            return "Please specify a valid course code to check prerequisites."

        course = self.kb.courses[course_code]
        if course['prerequisites']:
            prereqs = ', '.join(course['prerequisites'])
            return f"📋 Prerequisites for {course_code}: {prereqs}"
        else:
            return f"📋 {course_code} has no prerequisites."

    def _handle_department_info(self, entities: Dict) -> str:
        department = entities.get('department')

        if not department or department not in self.kb.departments:
            available_depts = ', '.join([d['name'] for d in self.kb.departments.values()])
            return f"Please specify a valid department. Available departments: {available_depts}"

        dept = self.kb.departments[department]
        response = f"🏛️ **{dept['name']} Department**\n\n"
        response += f"Department Head: {dept['head']}\n"
        response += f"Location: {dept['location']}\n"
        response += f"Phone: {dept['phone']}\n"
        response += f"Email: {dept['email']}\n"
        response += f"Popular Courses: {', '.join(dept['popular_courses'])}"

        return response

    def _handle_registration(self) -> str:
        response = "📅 **Registration Information**\n\n"
        response += "Registration Periods:\n"
        for term, dates in self.kb.general_info['registration_dates'].items():
            response += f"• {term.replace('_', ' ').title()}: {dates}\n"

        response += "\nTo register for courses:\n"
        response += "1. Log in (tell me your name)\n"
        response += "2. Check available courses: 'show available courses'\n"
        response += "3. Register: 'register for [course code]'\n"
        response += "4. View your schedule: 'my schedule'\n"

        if not self.student.is_authenticated:
            response += "\n💡 Start by telling me your name to log in!"

        return response

    def _handle_services(self, user_input: str) -> str:
        response = "🎓 **University Services**\n\n"

        user_lower = user_input.lower()
        specific_service = None
        for service in self.kb.general_info['services']:
            if service in user_lower:
                specific_service = service
                break

        if specific_service:
            return f"ℹ️ {specific_service.title()}: {self.kb.general_info['services'][specific_service]}"
        else:
            for service, info in self.kb.general_info['services'].items():
                response += f"• **{service.title()}**: {info}\n"

        return response

    def _handle_general(self, user_input: str) -> str:
        user_lower = user_input.lower()
        if any(greeting in user_lower for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            base_message = "Hello! I'm your University Helper chatbot. I can help you with:\n• Course information and registration\n• Schedules and prerequisites\n• Department contacts\n• University services"

            if not self.student.is_authenticated:
                base_message += "\n\n💡 Tell me your name to get started with course registration!"
            else:
                base_message += f"\n\n👋 Welcome back, {self.student.name}!"

            return base_message

        if any(thanks in user_lower for thanks in ['thank', 'thanks']):
            return "You're welcome! Is there anything else I can help you with?"

        if 'help' in user_lower:
            help_msg = "I can help you with:\n"
            help_msg += "• Course info: 'Tell me about CS101'\n"
            help_msg += "• Registration: 'Register for MATH101'\n"
            help_msg += "• Schedule: 'My schedule' or 'When is CS101?'\n"
            help_msg += "• Available courses: 'Show available courses'\n"
            help_msg += "• Drop courses: 'Drop CS101'\n"
            help_msg += "• Department info: 'Computer Science department'\n"
            help_msg += "• Services: 'University services'\n\n"

            if not self.student.is_authenticated:
                help_msg += "Start by telling me your name to log in!"

            return help_msg

        return "I'm not sure I understand. You can ask me about courses, registration, schedules, departments, or services. Type 'help' for more information."


class ChatbotGUI:

    def __init__(self, root):
        self.root = root
        self.chatbot = UniversityChatbot()
        self.setup_gui()
        self.setup_styles()

        welcome_msg = "Hello! I'm your University Helper chatbot. I can assist you with:\n"
        welcome_msg += "• Course registration and information\n"
        welcome_msg += "• Schedule management\n"
        welcome_msg += "• Prerequisites and requirements\n"
        welcome_msg += "• Department contacts\n\n"
        welcome_msg += "💡 Tell me your name to get started with course registration!"

        self.display_bot_message(welcome_msg)

    def setup_gui(self):
        self.root.title("University Helper Chatbot - Registration & Scheduling")
        self.root.geometry("1000x750")
        self.root.configure(bg='#1a1a2e')

        main_frame = ttk.Frame(self.root, padding="15", style="Main.TFrame")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        title_frame = ttk.Frame(main_frame, style="Title.TFrame")
        title_frame.grid(row=0, column=0, pady=(0, 15), sticky=(tk.W, tk.E))
        title_frame.columnconfigure(0, weight=1)

        title_label = ttk.Label(title_frame, text="🎓 University Helper Chatbot",
                                font=('Segoe UI', 20, 'bold'), style="Title.TLabel")
        title_label.grid(row=0, column=0)

        subtitle_label = ttk.Label(title_frame, text="Course Registration & Schedule Management",
                                   font=('Segoe UI', 11), style="Subtitle.TLabel")
        subtitle_label.grid(row=1, column=0)

        self.status_frame = ttk.Frame(title_frame, style="Status.TFrame")
        self.status_frame.grid(row=2, column=0, pady=(10, 0))

        self.status_label = ttk.Label(self.status_frame, text="👤 Not logged in",
                                      font=('Segoe UI', 10), style="Status.TLabel")
        self.status_label.grid(row=0, column=0)

        self.chat_frame = ttk.Frame(main_frame, style="Chat.TFrame")
        self.chat_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        self.chat_frame.columnconfigure(0, weight=1)
        self.chat_frame.rowconfigure(0, weight=1)

        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap=tk.WORD,
            width=85,
            height=30,
            font=('Consolas', 11),
            bg='#0f0f23',
            fg='#e6e6fa',
            insertbackground='#00ff88',
            selectbackground='#16537e',
            relief='flat',
            bd=2
        )
        self.chat_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=2, pady=2)
        self.chat_display.config(state=tk.DISABLED)

        input_frame = ttk.Frame(main_frame, style="Input.TFrame")
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        input_frame.columnconfigure(0, weight=1)
        self.user_input = ttk.Entry(
            input_frame,
            font=('Segoe UI', 12),
            width=70,
            style="Input.TEntry"
        )
        self.user_input.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.user_input.bind('<Return>', self.send_message)

        self.send_button = ttk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            style="Send.TButton"
        )
        self.send_button.grid(row=0, column=1)

        action_frame = ttk.Frame(main_frame, style="Status.TFrame")
        action_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        action_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(action_frame, style="Status.TFrame")
        button_frame.grid(row=0, column=0)

        ttk.Button(button_frame, text="📚 Courses",
                   command=lambda: self.quick_query("Show available courses"),
                   style="Quick.TButton").grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="📝 Register",
                   command=lambda: self.quick_query("How do I register for courses?"),
                   style="Quick.TButton").grid(row=0, column=1, padx=2)
        ttk.Button(button_frame, text="📅 My Schedule",
                   command=lambda: self.quick_query("Show my schedule"),
                   style="Quick.TButton").grid(row=0, column=2, padx=2)
        ttk.Button(button_frame, text="🏛️ Departments",
                   command=lambda: self.quick_query("Tell me about departments"),
                   style="Quick.TButton").grid(row=0, column=3, padx=2)

        utility_frame = ttk.Frame(action_frame, style="Status.TFrame")
        utility_frame.grid(row=0, column=2)

        ttk.Button(utility_frame, text="👤 Login",
                   command=self.show_login_dialog,
                   style="Login.TButton").grid(row=0, column=0, padx=5)
        ttk.Button(utility_frame, text="ℹ️ Help",
                   command=lambda: self.quick_query("help"),
                   style="Help.TButton").grid(row=0, column=1, padx=2)
        ttk.Button(utility_frame, text="🗑️ Clear",
                   command=self.clear_chat,
                   style="Clear.TButton").grid(row=0, column=2, padx=(5, 0))

        self.user_input.focus()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        colors = {
            'bg_dark': '#1a1a2e',
            'bg_medium': '#16213e',
            'bg_light': '#0f3460',
            'accent_purple': '#e94560',
            'accent_cyan': '#0f4c75',
            'accent_green': '#00ff88',
            'text_light': '#e6e6fa',
            'text_white': '#ffffff',
            'success': '#00ff88',
            'warning': '#ff6b35',
            'info': '#74b9ff',
        }

        self.style.configure('Main.TFrame', background=colors['bg_dark'])
        self.style.configure('Title.TFrame', background=colors['bg_dark'])
        self.style.configure('Chat.TFrame', background=colors['bg_dark'])
        self.style.configure('Input.TFrame', background=colors['bg_dark'])
        self.style.configure('Status.TFrame', background=colors['bg_dark'])

        self.style.configure('Title.TLabel',
                             background=colors['bg_dark'],
                             foreground=colors['text_white'],
                             font=('Segoe UI', 20, 'bold'))

        self.style.configure('Subtitle.TLabel',
                             background=colors['bg_dark'],
                             foreground=colors['text_light'],
                             font=('Segoe UI', 11))

        self.style.configure('Status.TLabel',
                             background=colors['bg_dark'],
                             foreground=colors['info'],
                             font=('Segoe UI', 10))

        self.style.configure('Input.TEntry',
                             fieldbackground=colors['bg_medium'],
                             foreground=colors['text_white'],
                             bordercolor=colors['accent_purple'],
                             lightcolor=colors['accent_purple'],
                             darkcolor=colors['accent_purple'],
                             insertcolor=colors['success'],
                             selectbackground=colors['accent_cyan'])

        self.style.configure('Send.TButton',
                             background=colors['accent_purple'],
                             foreground=colors['text_white'],
                             bordercolor=colors['accent_purple'],
                             lightcolor=colors['accent_purple'],
                             darkcolor=colors['accent_purple'],
                             font=('Segoe UI', 11, 'bold'),
                             padding=(15, 8))

        self.style.map('Send.TButton',
                       background=[('active', '#ff4757'),
                                   ('pressed', '#c44569')])

        self.style.configure('Quick.TButton',
                             background=colors['bg_light'],
                             foreground=colors['text_white'],
                             bordercolor=colors['bg_light'],
                             font=('Segoe UI', 9),
                             padding=(10, 5))

        self.style.map('Quick.TButton',
                       background=[('active', colors['accent_cyan']),
                                   ('pressed', colors['bg_medium'])])

        self.style.configure('Login.TButton',
                             background=colors['success'],
                             foreground=colors['text_white'],
                             bordercolor=colors['success'],
                             font=('Segoe UI', 9, 'bold'),
                             padding=(10, 5))

        self.style.map('Login.TButton',
                       background=[('active', '#00d268'),
                                   ('pressed', '#00a653')])

        self.style.configure('Help.TButton',
                             background=colors['info'],
                             foreground=colors['text_white'],
                             bordercolor=colors['info'],
                             font=('Segoe UI', 9),
                             padding=(10, 5))

        self.style.map('Help.TButton',
                       background=[('active', '#5dacf2'),
                                   ('pressed', '#4a9fe7')])

        self.style.configure('Clear.TButton',
                             background=colors['warning'],
                             foreground=colors['text_white'],
                             bordercolor=colors['warning'],
                             font=('Segoe UI', 9),
                             padding=(10, 5))

        self.style.map('Clear.TButton',
                       background=[('active', '#ff7675'),
                                   ('pressed', '#fd5e53')])

    def show_login_dialog(self):
        if self.chatbot.student.is_authenticated:
            result = messagebox.askquestion(
                "Already Logged In",
                f"You're logged in as {self.chatbot.student.name}.\nDo you want to log out?",
                icon='question'
            )
            if result == 'yes':
                self.chatbot.student = StudentProfile()
                self.update_status_display()
                self.display_bot_message("You've been logged out. Tell me your name to log in again!")
            return

        name = simpledialog.askstring("Student Login", "Please enter your name:")
        if name and name.strip():
            self.quick_query(f"My name is {name.strip()}")

    def update_status_display(self):
        if self.chatbot.student.is_authenticated:
            status_text = f"👤 {self.chatbot.student.name} (ID: {self.chatbot.student.student_id})"
            if self.chatbot.student.registered_courses:
                course_count = len(self.chatbot.student.registered_courses)
                status_text += f" | 📚 {course_count} courses"
        else:
            status_text = "👤 Not logged in"

        self.status_label.config(text=status_text)

    def quick_query(self, query: str):
        self.user_input.delete(0, tk.END)
        self.user_input.insert(0, query)
        self.send_message()

    def send_message(self, event=None):
        message = self.user_input.get().strip()
        if not message:
            return

        self.display_user_message(message)

        self.user_input.delete(0, tk.END)

        self.send_button.config(state='disabled')
        self.user_input.config(state='disabled')

        threading.Thread(target=self.get_bot_response, args=(message,), daemon=True).start()

    def get_bot_response(self, message: str):
        time.sleep(0.8)

        try:
            response = self.chatbot.generate_response(message)

            self.root.after(0, self.display_bot_response, response)
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            self.root.after(0, self.display_bot_response, error_msg)

    def display_bot_response(self, response: str):
        self.display_bot_message(response)
        self.update_status_display()
        self.send_button.config(state='normal')
        self.user_input.config(state='normal')
        self.user_input.focus()

    def display_user_message(self, message: str):
        self.chat_display.config(state=tk.NORMAL)

        timestamp = datetime.datetime.now().strftime("%H:%M")

        self.chat_display.insert(tk.END, f"\n[{timestamp}] ", "timestamp")

        if self.chatbot.student.is_authenticated:
            self.chat_display.insert(tk.END, f"{self.chatbot.student.name}: ", "user_label")
        else:
            self.chat_display.insert(tk.END, "You: ", "user_label")

        self.chat_display.insert(tk.END, f"{message}\n", "user_message")

        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def display_bot_message(self, message: str):
        self.chat_display.config(state=tk.NORMAL)

        timestamp = datetime.datetime.now().strftime("%H:%M")

        self.chat_display.insert(tk.END, f"\n[{timestamp}] ", "timestamp")
        self.chat_display.insert(tk.END, "🤖 University Bot: ", "bot_label")
        self.chat_display.insert(tk.END, f"{message}\n", "bot_message")

        self.chat_display.tag_configure("timestamp",
                                        foreground="#74b9ff",
                                        font=('Consolas', 9))

        self.chat_display.tag_configure("user_label",
                                        foreground="#00ff88",
                                        font=('Consolas', 11, 'bold'))

        self.chat_display.tag_configure("user_message",
                                        foreground="#a8e6cf",
                                        font=('Consolas', 11))

        self.chat_display.tag_configure("bot_label",
                                        foreground="#e94560",
                                        font=('Consolas', 11, 'bold'))

        self.chat_display.tag_configure("bot_message",
                                        foreground="#ffeaa7",
                                        font=('Consolas', 11))

        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def clear_chat(self):
        result = messagebox.askyesno("Clear Chat", "Are you sure you want to clear the chat history?")
        if result:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.config(state=tk.DISABLED)

            self.chatbot.conversation_history = []

            welcome_msg = "Chat cleared! I'm still here to help with course registration and scheduling."
            if self.chatbot.student.is_authenticated:
                welcome_msg += f" Welcome back, {self.chatbot.student.name}!"
            else:
                welcome_msg += " Tell me your name to get started!"

            self.display_bot_message(welcome_msg)


def main():
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.minsize(800, 650)

    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")

    try:
        root.iconbitmap(default='')
    except:
        pass

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nChatbot shutting down...")
        root.quit()


if __name__ == "__main__":
    main()