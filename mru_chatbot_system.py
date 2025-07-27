(cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF'
diff --git a/mru_chatbot_system.py b/mru_chatbot_system.py
--- a/mru_chatbot_system.py
+++ b/mru_chatbot_system.py
@@ -0,0 +1,842 @@
+#!/usr/bin/env python3
+"""
+Voice-Enabled Chatbot for Manav Rachna University
+==================================================
+
+A comprehensive chatbot system that provides information about MRU using voice recognition,
+natural language processing, and text-to-speech capabilities.
+
+Features:
+- Voice input/output support
+- Comprehensive MRU knowledge base
+- Intent classification
+- Context-aware responses
+- Multi-turn conversation support
+- Emergency contact integration
+"""
+
+import json
+import logging
+import re
+import random
+import sqlite3
+from datetime import datetime
+from typing import Dict, List, Tuple, Optional
+import threading
+import queue
+
+# Core libraries
+try:
+    import speech_recognition as sr
+    import pyttsx3
+    import spacy
+    from sklearn.feature_extraction.text import TfidfVectorizer
+    from sklearn.metrics.pairwise import cosine_similarity
+    import numpy as np
+    print("All required libraries imported successfully!")
+except ImportError as e:
+    print(f"Missing required library: {e}")
+    print("Please install with: pip install speechrecognition pyttsx3 spacy scikit-learn numpy")
+    print("Also run: python -m spacy download en_core_web_sm")
+
+
+class MRUKnowledgeBase:
+    """Comprehensive knowledge base for Manav Rachna University"""
+    
+    def __init__(self):
+        self.knowledge = {
+            "university_info": {
+                "name": "Manav Rachna University",
+                "type": "State Private University",
+                "established": "2014 (evolved from Manav Rachna College of Engineering established in 2004)",
+                "location": "Sector 43, Aravalli Hills, Delhi-Surajkund Road, Faridabad, Haryana 121004",
+                "recognition": "UGC recognized under Section 2(f), NAAC A++ accredited",
+                "motto": "Creating a better human being",
+                "ranking": "Ranked No. 1 for Research and Placement among emerging universities"
+            },
+            
+            "admissions": {
+                "entrance_test": {
+                    "name": "MRNAT (Manav Rachna National Aptitude Test)",
+                    "description": "Entrance cum Scholarship Test for UG and PG programs",
+                    "duration": "90 minutes",
+                    "format": "Online objective-type examination",
+                    "sections_ug": ["Arithmetic & Logical Reasoning (25 MCQs)", "General English (25 MCQs)", "General Awareness (25 MCQs)"],
+                    "sections_pg": ["Arithmetic & Logical Reasoning (15 MCQs)", "Verbal Ability (15 MCQs)", "General Awareness (15 MCQs)", "Domain Specific (30 Questions)"],
+                    "dates_2025": "Phase I: January 18, 2025 | Phase II: April 20, 2025"
+                },
+                "application_process": [
+                    "Visit official website and click 'Apply Now'",
+                    "Fill online application form with accurate information",
+                    "Upload required documents (photo, certificates)",
+                    "Pay application fee of INR 1,200",
+                    "Take MRNAT exam",
+                    "Attend Vision & Values Round (VVR)",
+                    "Physical counseling if selected",
+                    "Fee payment and admission confirmation"
+                ],
+                "scholarships": {
+                    "utkarsh_scheme": "For admissions from 25th January 2025 to 29th April 2025",
+                    "uttam_scheme": "For admissions from 30th April 2025 to 30th June 2025",
+                    "percentage": "Up to 100% tuition fee waiver based on MRNAT performance",
+                    "merit_scholarships": "Available for top performers in each semester"
+                }
+            },
+            
+            "courses": {
+                "undergraduate": {
+                    "engineering": [
+                        "B.Tech Computer Science & Engineering",
+                        "B.Tech Electronics & Communication",
+                        "B.Tech Mechanical Engineering",
+                        "B.Tech Civil Engineering",
+                        "B.Tech Biotechnology",
+                        "B.Tech Robotics and AI (with L&T)",
+                        "B.Tech Cyber Security (with Quick Heal)",
+                        "B.Tech Data Science (with Xebia)",
+                        "B.Tech Cloud Computing (with Microsoft)"
+                    ],
+                    "management": [
+                        "BBA Finance & Accounts",
+                        "BBA Entrepreneurship & Family Business",
+                        "BBA Global Operations Management",
+                        "BBA Health Care Management",
+                        "BBA Business Analytics (with ISDC)",
+                        "BBA Banking & Financial Markets"
+                    ],
+                    "law": [
+                        "BA LLB (Hons)",
+                        "BBA LLB (Hons)",
+                        "BCom LLB (Hons)",
+                        "LLB"
+                    ],
+                    "sciences": [
+                        "B.Sc (Hons) Mathematics",
+                        "B.Sc (Hons) Physics", 
+                        "B.Sc (Hons) Chemistry",
+                        "B.Sc (Hons) Microbiology",
+                        "B.Sc Food Science & Technology"
+                    ],
+                    "other": [
+                        "BCA (with specializations)",
+                        "B.Ed",
+                        "Integrated B.A. B.Ed",
+                        "Integrated B.Sc. B.Ed"
+                    ]
+                },
+                "postgraduate": {
+                    "engineering": [
+                        "M.Tech Computer Engineering",
+                        "M.Tech Electronics & Communication",
+                        "M.Tech Mechanical Engineering",
+                        "M.Tech ECE - Embedded System & VLSI"
+                    ],
+                    "management": [
+                        "MBA (various specializations)",
+                        "MBA Business Analytics (with ISDC)"
+                    ],
+                    "law": [
+                        "LLM",
+                        "LLM Part Time"
+                    ],
+                    "sciences": [
+                        "M.Sc Mathematics",
+                        "M.Sc Physics",
+                        "M.Sc Chemistry"
+                    ]
+                },
+                "doctoral": [
+                    "Ph.D in Engineering",
+                    "Ph.D in Management & Commerce",
+                    "Ph.D in Law",
+                    "Ph.D in Sciences",
+                    "Ph.D in Education"
+                ]
+            },
+            
+            "facilities": {
+                "academic": [
+                    "State-of-the-art laboratories",
+                    "Modern classrooms with smart boards",
+                    "Digital library with 24/7 access",
+                    "Research centers",
+                    "Innovation and incubation center"
+                ],
+                "residential": [
+                    "Separate hostels for boys and girls",
+                    "805 bed capacity",
+                    "24/7 WiFi",
+                    "Hygienic mess with RO water",
+                    "Power backup with generators"
+                ],
+                "sports": [
+                    "Indoor sports arena",
+                    "Shooting range",
+                    "Volleyball courts",
+                    "Soccer ground",
+                    "Squash court",
+                    "Cricket ground",
+                    "Basketball courts",
+                    "Sports academy in Faridabad"
+                ],
+                "other": [
+                    "Multiple cafeterias",
+                    "Medical facilities",
+                    "Transportation services",
+                    "Gym facilities"
+                ]
+            },
+            
+            "placements": {
+                "statistics": {
+                    "highest_package": "60 LPA (KPMG Canada)",
+                    "placements_last_5_years": "5000+",
+                    "recent_highlights": [
+                        "Karan Aditya Ghoshal - 60 LPA (KPMG Canada)",
+                        "Sarthak Rastogi - 55 LPA (Spacetime)",
+                        "Ananya Kamra - 54 LPA (Paloalto)",
+                        "Deepanshu Sharma - 30 LPA (Niagra)",
+                        "Lokdeep Saluja - 23 LPA (Tekion)"
+                    ]
+                },
+                "recruiters": [
+                    "KPMG Canada", "Spacetime", "Paloalto", "Niagra", "Tekion",
+                    "TCS", "IBM", "Infosys", "Wipro", "Accenture", "Amazon",
+                    "Microsoft", "Google", "LinkedIn", "Extramarks",
+                    "NIIT", "Cognizant", "Nokia", "Indigo", "Federal Bank"
+                ]
+            },
+            
+            "contact_info": {
+                "main_numbers": {
+                    "mru": "+91-129-4268500",
+                    "admissions": "+91-129-4259000",
+                    "general_queries": "+91-129-4198200"
+                },
+                "email": "admissions@manavrachna.edu.in",
+                "address": "Sector 43, Aravalli Hills, Delhi-Surajkund Road, Faridabad, Haryana 121004",
+                "city_offices": "Delhi | Guwahati | Indore | Kota | Lucknow | Varanasi | Patna | Hyderabad",
+                "website": "https://manavrachna.edu.in"
+            },
+            
+            "fees": {
+                "application_fee": "INR 1,200",
+                "approximate_annual_fees": {
+                    "btech": "INR 1.82 - 2.44 Lakhs",
+                    "bba": "INR 1.65 Lakhs",
+                    "bsc_hons": "INR 1.06 Lakhs",
+                    "msc": "INR 1.06 Lakhs",
+                    "phd": "INR 1.3 Lakhs",
+                    "bed": "INR 1.16 Lakhs"
+                }
+            },
+            
+            "campus_life": {
+                "clubs": [
+                    "Technical clubs",
+                    "Cultural societies",
+                    "Sports clubs",
+                    "Literary societies",
+                    "Entrepreneurship cell",
+                    "Innovation clubs"
+                ],
+                "events": [
+                    "Annual technical fest",
+                    "Cultural festivals",
+                    "Sports tournaments",
+                    "Industry seminars",
+                    "Research conferences"
+                ]
+            }
+        }
+    
+    def get_info(self, category: str, subcategory: str = None) -> dict:
+        """Retrieve information from knowledge base"""
+        if subcategory:
+            return self.knowledge.get(category, {}).get(subcategory, {})
+        return self.knowledge.get(category, {})
+
+
+class IntentClassifier:
+    """Classify user intents using keyword matching and pattern recognition"""
+    
+    def __init__(self):
+        self.intent_patterns = {
+            "greeting": [
+                r"(?i)\b(hi|hello|hey|good\s*(morning|afternoon|evening)|namaste)\b",
+                r"(?i)\b(how\s*are\s*you|what's\s*up)\b"
+            ],
+            "admission_info": [
+                r"(?i)\b(admission|admissions|apply|application|entrance|mrnat)\b",
+                r"(?i)\b(how\s*to\s*(apply|get\s*admission))\b",
+                r"(?i)\b(eligibility|requirements|criteria)\b"
+            ],
+            "courses": [
+                r"(?i)\b(courses?|programs?|degrees?|btech|mtech|bba|mba|bsc|msc|phd)\b",
+                r"(?i)\b(what\s*(courses|programs).*available)\b",
+                r"(?i)\b(engineering|management|law|science|computer|mechanical)\b"
+            ],
+            "fees": [
+                r"(?i)\b(fees?|fee\s*structure|cost|tuition|payment|scholarship)\b",
+                r"(?i)\b(how\s*much.*cost|expensive|affordable)\b"
+            ],
+            "placements": [
+                r"(?i)\b(placement|placements|job|career|salary|package|recruiter)\b",
+                r"(?i)\b(highest\s*package|companies|employment)\b"
+            ],
+            "facilities": [
+                r"(?i)\b(facilities|infrastructure|hostel|library|sports|lab)\b",
+                r"(?i)\b(campus|accommodation|dining|transport)\b"
+            ],
+            "contact": [
+                r"(?i)\b(contact|phone|email|address|location|visit)\b",
+                r"(?i)\b(how\s*to\s*(contact|reach))\b"
+            ],
+            "campus_life": [
+                r"(?i)\b(campus\s*life|student\s*life|clubs|activities|events)\b",
+                r"(?i)\b(extracurricular|cultural|technical\s*fest)\b"
+            ],
+            "goodbye": [
+                r"(?i)\b(bye|goodbye|see\s*you|thanks?|thank\s*you)\b",
+                r"(?i)\b(that's\s*all|no\s*more\s*questions)\b"
+            ]
+        }
+    
+    def classify_intent(self, text: str) -> str:
+        """Classify the intent of user input"""
+        text = text.lower().strip()
+        
+        for intent, patterns in self.intent_patterns.items():
+            for pattern in patterns:
+                if re.search(pattern, text):
+                    return intent
+        
+        return "general_info"
+
+
+class VoiceHandler:
+    """Handle voice input and output"""
+    
+    def __init__(self):
+        self.recognizer = sr.Recognizer()
+        self.microphone = sr.Microphone()
+        self.tts_engine = pyttsx3.init()
+        
+        # Configure TTS settings
+        self.tts_engine.setProperty('rate', 150)  # Speed of speech
+        self.tts_engine.setProperty('volume', 0.8)  # Volume level
+        
+        # Adjust for ambient noise
+        with self.microphone as source:
+            self.recognizer.adjust_for_ambient_noise(source)
+    
+    def listen(self, timeout: int = 5) -> Optional[str]:
+        """Listen for voice input and convert to text"""
+        try:
+            print("🎤 Listening...")
+            with self.microphone as source:
+                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
+            
+            print("🔄 Processing speech...")
+            text = self.recognizer.recognize_google(audio)
+            print(f"👤 User: {text}")
+            return text
+            
+        except sr.WaitTimeoutError:
+            print("⏰ No speech detected within timeout")
+            return None
+        except sr.UnknownValueError:
+            print("❌ Could not understand audio")
+            return None
+        except sr.RequestError as e:
+            print(f"❌ Speech recognition service error: {e}")
+            return None
+    
+    def speak(self, text: str):
+        """Convert text to speech"""
+        print(f"🤖 Assistant: {text}")
+        self.tts_engine.say(text)
+        self.tts_engine.runAndWait()
+
+
+class ResponseGenerator:
+    """Generate contextual responses based on intents and knowledge base"""
+    
+    def __init__(self, knowledge_base: MRUKnowledgeBase):
+        self.kb = knowledge_base
+        self.conversation_context = []
+        
+    def generate_response(self, intent: str, user_input: str) -> str:
+        """Generate appropriate response based on intent"""
+        self.conversation_context.append({"user": user_input, "intent": intent})
+        
+        response_map = {
+            "greeting": self._handle_greeting,
+            "admission_info": self._handle_admissions,
+            "courses": self._handle_courses,
+            "fees": self._handle_fees,
+            "placements": self._handle_placements,
+            "facilities": self._handle_facilities,
+            "contact": self._handle_contact,
+            "campus_life": self._handle_campus_life,
+            "goodbye": self._handle_goodbye,
+            "general_info": self._handle_general
+        }
+        
+        handler = response_map.get(intent, self._handle_general)
+        return handler(user_input)
+    
+    def _handle_greeting(self, user_input: str) -> str:
+        greetings = [
+            "Hello! Welcome to Manav Rachna University. I'm your virtual assistant.",
+            "Hi there! I'm here to help you with information about MRU.",
+            "Namaste! Welcome to Manav Rachna University. How can I assist you today?"
+        ]
+        
+        intro = random.choice(greetings)
+        info = " I can help you with admissions, courses, fees, placements, facilities, and more. What would you like to know?"
+        
+        return intro + info
+    
+    def _handle_admissions(self, user_input: str) -> str:
+        admission_info = self.kb.get_info("admissions")
+        
+        if "mrnat" in user_input.lower() or "entrance" in user_input.lower():
+            mrnat = admission_info["entrance_test"]
+            return f"""MRNAT (Manav Rachna National Aptitude Test) is our entrance cum scholarship test. Here are the key details:
+            
+📅 Exam Dates 2025: {mrnat['dates_2025']}
+⏱️ Duration: {mrnat['duration']}
+📝 Format: {mrnat['format']}
+
+For UG programs: {', '.join(mrnat['sections_ug'])}
+For PG programs: {', '.join(mrnat['sections_pg'])}
+
+Students can earn scholarships up to 100% based on their MRNAT performance!"""
+        
+        elif "process" in user_input.lower() or "apply" in user_input.lower():
+            process = admission_info["application_process"]
+            steps = "\n".join([f"{i+1}. {step}" for i, step in enumerate(process)])
+            return f"Here's the admission process for MRU:\n\n{steps}\n\nApplication fee is {self.kb.get_info('fees')['application_fee']}."
+        
+        elif "scholarship" in user_input.lower():
+            scholarships = admission_info["scholarships"]
+            return f"""MRU offers excellent scholarship opportunities:
+
+🎯 {scholarships['utkarsh_scheme']}
+🎯 {scholarships['uttam_scheme']}
+💰 {scholarships['percentage']}
+🏆 {scholarships['merit_scholarships']}
+
+Scholarships are awarded based on MRNAT performance and academic merit."""
+        
+        else:
+            return """MRU admissions are primarily through MRNAT - our entrance cum scholarship test. Key highlights:
+
+✅ Online application process
+✅ Scholarships up to 100% available
+✅ Multiple intake opportunities
+✅ Comprehensive support throughout
+
+Would you like specific information about MRNAT, application process, or scholarships?"""
+    
+    def _handle_courses(self, user_input: str) -> str:
+        courses = self.kb.get_info("courses")
+        
+        if any(word in user_input.lower() for word in ["btech", "engineering", "computer", "mechanical"]):
+            eng_courses = courses["undergraduate"]["engineering"]
+            return f"""MRU offers excellent B.Tech programs with industry partnerships:
+
+🔧 Core Engineering:
+{chr(10).join([f"• {course}" for course in eng_courses[:4]])}
+
+🤖 Specialized Programs:
+{chr(10).join([f"• {course}" for course in eng_courses[4:]])}
+
+Our engineering programs feature industry collaborations with companies like L&T, Microsoft, Xebia, and Quick Heal!"""
+        
+        elif any(word in user_input.lower() for word in ["bba", "mba", "management", "business"]):
+            mgmt_ug = courses["undergraduate"]["management"]
+            mgmt_pg = courses["postgraduate"]["management"]
+            return f"""MRU Management Programs:
+
+🎓 Undergraduate (BBA):
+{chr(10).join([f"• {course}" for course in mgmt_ug])}
+
+🎓 Postgraduate (MBA):
+{chr(10).join([f"• {course}" for course in mgmt_pg])}
+
+Our management programs include industry partnerships and practical exposure!"""
+        
+        elif any(word in user_input.lower() for word in ["law", "llb", "llm", "legal"]):
+            law_courses = courses["undergraduate"]["law"] + courses["postgraduate"]["law"]
+            return f"""MRU Law Programs:
+
+⚖️ Undergraduate:
+{chr(10).join([f"• {course}" for course in courses['undergraduate']['law']])}
+
+⚖️ Postgraduate:
+{chr(10).join([f"• {course}" for course in courses['postgraduate']['law']])}
+
+Our law programs are approved by Bar Council of India and focus on practical legal education."""
+        
+        else:
+            return f"""MRU offers 100+ courses across multiple disciplines:
+
+🔧 Engineering: B.Tech, M.Tech programs with industry partnerships
+💼 Management: BBA, MBA with various specializations
+⚖️ Law: BA LLB, BBA LLB, LLM programs
+🔬 Sciences: B.Sc, M.Sc in Mathematics, Physics, Chemistry
+🎓 Education: B.Ed, Integrated programs
+📚 Computer Applications: BCA, MCA
+🔬 Research: Ph.D programs in all disciplines
+
+Which specific area interests you? I can provide detailed information!"""
+    
+    def _handle_fees(self, user_input: str) -> str:
+        fees = self.kb.get_info("fees")
+        
+        return f"""MRU Fee Structure (Approximate Annual Fees):
+
+💰 B.Tech: {fees['approximate_annual_fees']['btech']}
+💰 BBA: {fees['approximate_annual_fees']['bba']}
+💰 B.Sc (Hons): {fees['approximate_annual_fees']['bsc_hons']}
+💰 M.Sc: {fees['approximate_annual_fees']['msc']}
+💰 Ph.D: {fees['approximate_annual_fees']['phd']}
+💰 B.Ed: {fees['approximate_annual_fees']['bed']}
+
+📋 Application Fee: {fees['application_fee']}
+
+💡 Great News: Scholarships up to 100% are available based on MRNAT performance!
+🏦 Educational loans available at low interest rates
+💳 Flexible payment options
+
+Would you like information about scholarships or specific course fees?"""
+    
+    def _handle_placements(self, user_input: str) -> str:
+        placements = self.kb.get_info("placements")
+        stats = placements["statistics"]
+        
+        recent_highlights = "\n".join([f"• {highlight}" for highlight in stats["recent_highlights"]])
+        
+        return f"""MRU Placement Highlights:
+
+🎯 Highest Package: {stats['highest_package']}
+📈 Total Placements (Last 5 Years): {stats['placements_last_5_years']}
+
+🌟 Recent Top Placements:
+{recent_highlights}
+
+🏢 Top Recruiters include:
+{', '.join(placements['recruiters'][:10])}... and many more!
+
+Our dedicated Career Resource & Career Development Centre (CRCDC) provides:
+✅ 100% placement assistance
+✅ Industry training programs
+✅ Mock interviews and preparation
+✅ Internship opportunities
+✅ Career counseling
+
+MRU is ranked No. 1 for placements among emerging universities!"""
+    
+    def _handle_facilities(self, user_input: str) -> str:
+        facilities = self.kb.get_info("facilities")
+        
+        if "hostel" in user_input.lower() or "accommodation" in user_input.lower():
+            hostel_info = facilities["residential"]
+            return f"""MRU Hostel Facilities:
+
+🏠 Accommodation:
+{chr(10).join([f"• {facility}" for facility in hostel_info])}
+
+The hostels provide a safe, comfortable environment for students with modern amenities and a homely atmosphere."""
+        
+        elif "sports" in user_input.lower():
+            sports_info = facilities["sports"]
+            return f"""MRU Sports Facilities:
+
+🏃‍♂️ Sports Infrastructure:
+{chr(10).join([f"• {facility}" for facility in sports_info])}
+
+MRU has produced 35 Arjuna Awardees and has a dedicated Sports Academy!"""
+        
+        else:
+            all_facilities = []
+            for category, items in facilities.items():
+                all_facilities.extend(items)
+            
+            return f"""MRU World-Class Facilities:
+
+🎓 Academic Facilities:
+{chr(10).join([f"• {facility}" for facility in facilities['academic']])}
+
+🏠 Residential Facilities:
+{chr(10).join([f"• {facility}" for facility in facilities['residential']])}
+
+🏃‍♂️ Sports Facilities:
+{chr(10).join([f"• {facility}" for facility in facilities['sports'][:4]])}
+
+🍽️ Other Amenities:
+{chr(10).join([f"• {facility}" for facility in facilities['other']])}
+
+Our campus provides a comprehensive environment for holistic development!"""
+    
+    def _handle_contact(self, user_input: str) -> str:
+        contact = self.kb.get_info("contact_info")
+        
+        return f"""Contact Manav Rachna University:
+
+📞 Main Numbers:
+• MRU: {contact['main_numbers']['mru']}
+• Admissions: {contact['main_numbers']['admissions']}
+• General Queries: {contact['main_numbers']['general_queries']}
+
+📧 Email: {contact['email']}
+
+📍 Address: {contact['address']}
+
+🌐 Website: {contact['website']}
+
+🏢 City Offices: {contact['city_offices']}
+
+Feel free to contact us for any queries. Our admission counselors are available to guide you!"""
+    
+    def _handle_campus_life(self, user_input: str) -> str:
+        campus_life = self.kb.get_info("campus_life")
+        
+        return f"""Life at MRU Campus:
+
+🎭 Student Clubs & Societies:
+{chr(10).join([f"• {club}" for club in campus_life['clubs']])}
+
+🎉 Regular Events:
+{chr(10).join([f"• {event}" for event in campus_life['events']])}
+
+MRU believes in holistic development and provides numerous opportunities for students to explore their interests beyond academics. Our vibrant campus life ensures a well-rounded educational experience!
+
+Would you like to know more about any specific activities or facilities?"""
+    
+    def _handle_goodbye(self, user_input: str) -> str:
+        goodbyes = [
+            "Thank you for your interest in Manav Rachna University! Feel free to contact us for any further assistance.",
+            "It was great helping you learn about MRU. Best wishes for your academic journey!",
+            "Thank you for connecting with us. We look forward to welcoming you to the MRU family!"
+        ]
+        
+        contact_reminder = "\n\nFor admissions: +91-129-4259000 | Email: admissions@manavrachna.edu.in"
+        
+        return random.choice(goodbyes) + contact_reminder
+    
+    def _handle_general(self, user_input: str) -> str:
+        university_info = self.kb.get_info("university_info")
+        
+        return f"""About Manav Rachna University:
+
+🎓 {university_info['name']} is a leading {university_info['type']}
+📅 Established: {university_info['established']}
+🏆 Recognition: {university_info['recognition']}
+📍 Location: {university_info['location']}
+🥇 Ranking: {university_info['ranking']}
+
+Mission: "{university_info['motto']}"
+
+I can help you with:
+• Admissions and MRNAT information
+• Course details and specializations
+• Fee structure and scholarships
+• Placement statistics and recruiters
+• Campus facilities and hostel information
+• Contact details and location
+
+What specific information would you like to know about MRU?"""
+
+
+class ConversationManager:
+    """Manage the conversation flow and context"""
+    
+    def __init__(self):
+        self.conversation_history = []
+        self.session_start = datetime.now()
+        self.user_preferences = {}
+    
+    def add_interaction(self, user_input: str, bot_response: str, intent: str):
+        """Add interaction to conversation history"""
+        self.conversation_history.append({
+            "timestamp": datetime.now(),
+            "user_input": user_input,
+            "bot_response": bot_response,
+            "intent": intent
+        })
+    
+    def get_conversation_summary(self) -> str:
+        """Generate a summary of the conversation"""
+        if not self.conversation_history:
+            return "No conversation yet."
+        
+        intents = [interaction["intent"] for interaction in self.conversation_history]
+        intent_counts = {intent: intents.count(intent) for intent in set(intents)}
+        
+        duration = datetime.now() - self.session_start
+        
+        return f"""Conversation Summary:
+Duration: {duration.total_seconds():.0f} seconds
+Total interactions: {len(self.conversation_history)}
+Topics discussed: {', '.join(intent_counts.keys())}
+Most discussed: {max(intent_counts, key=intent_counts.get)}"""
+
+
+class MRUVoiceChatbot:
+    """Main chatbot class that orchestrates all components"""
+    
+    def __init__(self, voice_enabled: bool = True):
+        print("🚀 Initializing MRU Voice Chatbot...")
+        
+        self.voice_enabled = voice_enabled
+        self.knowledge_base = MRUKnowledgeBase()
+        self.intent_classifier = IntentClassifier()
+        self.response_generator = ResponseGenerator(self.knowledge_base)
+        self.conversation_manager = ConversationManager()
+        
+        if voice_enabled:
+            try:
+                self.voice_handler = VoiceHandler()
+                print("🎤 Voice features enabled")
+            except Exception as e:
+                print(f"⚠️ Voice features disabled due to error: {e}")
+                self.voice_enabled = False
+        
+        print("✅ MRU Chatbot initialized successfully!")
+    
+    def get_user_input(self) -> Optional[str]:
+        """Get user input via voice or text"""
+        if self.voice_enabled:
+            print("\n🎤 Speak your question or type 'text' to switch to text mode:")
+            user_input = self.voice_handler.listen()
+            
+            if user_input and user_input.lower() == "text":
+                self.voice_enabled = False
+                print("📝 Switched to text mode")
+                return input("👤 You: ")
+            
+            return user_input
+        else:
+            return input("👤 You: ")
+    
+    def provide_response(self, response: str):
+        """Provide response via voice or text"""
+        if self.voice_enabled:
+            self.voice_handler.speak(response)
+        else:
+            print(f"🤖 Assistant: {response}")
+    
+    def handle_special_commands(self, user_input: str) -> bool:
+        """Handle special chatbot commands"""
+        if not user_input:
+            return False
+        
+        command = user_input.lower().strip()
+        
+        if command in ["quit", "exit", "stop", "end"]:
+            response = "Thank you for using MRU Voice Assistant. Have a great day!"
+            self.provide_response(response)
+            return True
+        
+        elif command == "help":
+            help_text = """Available commands:
+• Ask about admissions, courses, fees, placements
+• Say 'voice' to enable voice mode
+• Say 'text' to switch to text mode
+• Say 'summary' for conversation summary
+• Say 'quit' to exit"""
+            self.provide_response(help_text)
+            return False
+        
+        elif command == "voice" and not self.voice_enabled:
+            try:
+                self.voice_handler = VoiceHandler()
+                self.voice_enabled = True
+                self.provide_response("Voice mode enabled! You can now speak your questions.")
+            except Exception as e:
+                self.provide_response(f"Could not enable voice mode: {e}")
+            return False
+        
+        elif command == "summary":
+            summary = self.conversation_manager.get_conversation_summary()
+            self.provide_response(summary)
+            return False
+        
+        return False
+    
+    def run(self):
+        """Main chatbot loop"""
+        print("\n" + "="*60)
+        print("🎓 WELCOME TO MANAV RACHNA UNIVERSITY VOICE ASSISTANT 🎓")
+        print("="*60)
+        
+        # Initial greeting
+        welcome_message = """Hello! I'm your virtual assistant for Manav Rachna University. 
+I can help you with information about admissions, courses, fees, placements, facilities, and more.
+
+You can speak naturally or type your questions. Say 'help' for commands or 'quit' to exit.
+
+How can I assist you today?"""
+        
+        self.provide_response(welcome_message)
+        
+        while True:
+            try:
+                # Get user input
+                user_input = self.get_user_input()
+                
+                if not user_input:
+                    continue
+                
+                # Handle special commands
+                if self.handle_special_commands(user_input):
+                    break
+                
+                # Classify intent and generate response
+                intent = self.intent_classifier.classify_intent(user_input)
+                response = self.response_generator.generate_response(intent, user_input)
+                
+                # Provide response
+                self.provide_response(response)
+                
+                # Log interaction
+                self.conversation_manager.add_interaction(user_input, response, intent)
+                
+                # Ask for follow-up
+                if intent != "goodbye":
+                    follow_up = "Is there anything else you'd like to know about MRU?"
+                    if not self.voice_enabled:
+                        print(f"\n💭 {follow_up}")
+                
+            except KeyboardInterrupt:
+                print("\n\n👋 Chatbot stopped by user. Goodbye!")
+                break
+            except Exception as e:
+                error_message = f"Sorry, I encountered an error: {e}. Please try again."
+                self.provide_response(error_message)
+
+
+def main():
+    """Main function to run the chatbot"""
+    print("🔧 Setting up MRU Voice Chatbot...")
+    
+    # Check if voice is available
+    voice_available = True
+    try:
+        import speech_recognition as sr
+        import pyttsx3
+        sr.Microphone()
+    except:
+        voice_available = False
+        print("⚠️ Voice features not available. Running in text mode.")
+    
+    # Initialize and run chatbot
+    chatbot = MRUVoiceChatbot(voice_enabled=voice_available)
+    chatbot.run()
+
+
+if __name__ == "__main__":
+    main()
EOF
)
