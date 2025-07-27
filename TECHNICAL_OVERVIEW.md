(cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF'
diff --git a/TECHNICAL_OVERVIEW.md b/TECHNICAL_OVERVIEW.md
--- a/TECHNICAL_OVERVIEW.md
+++ b/TECHNICAL_OVERVIEW.md
@@ -0,0 +1,506 @@
+# Technical Overview: MRU Voice Chatbot System
+
+## 🏗️ System Architecture
+
+### High-Level Architecture
+
+```
+┌─────────────────────────────────────────────────────────────────┐
+│                    MRU Voice Chatbot System                     │
+├─────────────────────────────────────────────────────────────────┤
+│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────────┐ │
+│  │Voice Handler│  │Intent        │  │Response Generator       │ │
+│  │- Speech-to- │  │Classifier    │  │- Context-aware responses│ │
+│  │  Text       │  │- Regex       │  │- Template-based         │ │
+│  │- Text-to-   │  │  patterns    │  │- Dynamic content        │ │
+│  │  Speech     │  │- NLP         │  │- Multi-turn support     │ │
+│  └─────────────┘  └──────────────┘  └─────────────────────────┘ │
+│         │                │                         │            │
+│         │                │                         │            │
+│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────────┐ │
+│  │Conversation │  │Knowledge     │  │User Interface          │ │
+│  │Manager      │  │Base          │  │- Voice/Text modes      │ │
+│  │- History    │  │- University  │  │- Command handling      │ │
+│  │- Context    │  │  information │  │- Error management      │ │
+│  │- Analytics  │  │- Structured  │  │- Session management    │ │
+│  └─────────────┘  └──────────────┘  └─────────────────────────┘ │
+└─────────────────────────────────────────────────────────────────┘
+```
+
+### Component Interaction Flow
+
+```
+User Input (Voice/Text)
+         ↓
+    VoiceHandler (if voice)
+         ↓
+    IntentClassifier
+         ↓
+    ResponseGenerator ←→ KnowledgeBase
+         ↓
+    ConversationManager
+         ↓
+    VoiceHandler (TTS) / Text Output
+```
+
+## 🧠 Intent Classification System
+
+### Intent Categories
+
+| Intent | Description | Example Queries |
+|--------|-------------|-----------------|
+| `greeting` | Initial contact, greetings | "Hello", "Hi there", "Good morning" |
+| `admission_info` | Admission process, MRNAT | "How to apply?", "Tell me about admissions" |
+| `courses` | Academic programs | "What courses do you offer?", "B.Tech programs" |
+| `fees` | Fee structure, costs | "How much are fees?", "Cost of B.Tech" |
+| `placements` | Career services, jobs | "Placement statistics", "Job opportunities" |
+| `facilities` | Infrastructure, amenities | "Campus facilities", "Hostel information" |
+| `contact` | Contact information | "Phone number", "How to reach you" |
+| `campus_life` | Student activities | "Campus life", "Student clubs" |
+| `goodbye` | Conversation ending | "Thank you", "Goodbye" |
+| `general_info` | University overview | "About MRU", "Tell me about university" |
+
+### Pattern Matching System
+
+```python
+# Example pattern structure
+intent_patterns = {
+    "admission_info": [
+        r"(?i)\b(admission|admissions|apply|application|entrance|mrnat)\b",
+        r"(?i)\b(how\s*to\s*(apply|get\s*admission))\b",
+        r"(?i)\b(eligibility|requirements|criteria)\b"
+    ]
+}
+```
+
+## 📚 Knowledge Base Structure
+
+### Data Organization
+
+```
+knowledge_base/
+├── university_info/
+│   ├── basic_details
+│   ├── recognition_accreditation
+│   ├── rankings_achievements
+│   └── mission_values
+├── admissions/
+│   ├── entrance_test (MRNAT)
+│   ├── application_process
+│   ├── eligibility_criteria
+│   └── scholarship_schemes
+├── courses/
+│   ├── undergraduate/
+│   │   ├── engineering
+│   │   ├── management
+│   │   ├── law
+│   │   ├── sciences
+│   │   └── other
+│   ├── postgraduate/
+│   └── doctoral/
+├── facilities/
+│   ├── academic
+│   ├── residential
+│   ├── sports
+│   └── other
+├── placements/
+│   ├── statistics
+│   └── recruiters
+├── contact_info/
+├── fees/
+└── campus_life/
+```
+
+### Knowledge Base Interface
+
+```python
+class MRUKnowledgeBase:
+    def get_info(self, category: str, subcategory: str = None) -> dict
+    def search_content(self, query: str) -> List[dict]
+    def update_information(self, category: str, data: dict) -> bool
+```
+
+## 🗣️ Voice Processing Pipeline
+
+### Speech Recognition Flow
+
+```
+Audio Input
+    ↓
+Noise Reduction & Preprocessing
+    ↓
+Google Speech Recognition API
+    ↓
+Text Transcription
+    ↓
+Confidence Scoring
+    ↓
+Error Handling & Fallback
+```
+
+### Text-to-Speech Flow
+
+```
+Response Text
+    ↓
+Text Preprocessing
+    ↓
+pyttsx3 TTS Engine
+    ↓
+Voice Configuration (Rate, Volume)
+    ↓
+Audio Output
+```
+
+### Voice Configuration Options
+
+```python
+# TTS Settings
+voice_settings = {
+    'rate': 150,        # Words per minute
+    'volume': 0.8,      # Volume level (0.0-1.0)
+    'voice_id': 0,      # Voice selection
+    'language': 'en'    # Language code
+}
+
+# Speech Recognition Settings
+recognition_settings = {
+    'timeout': 5,           # Listening timeout
+    'phrase_time_limit': 10, # Max phrase duration
+    'energy_threshold': 300, # Noise threshold
+    'language': 'en-US'     # Recognition language
+}
+```
+
+## 💬 Conversation Flow Patterns
+
+### 1. Admission Inquiry Flow
+
+```
+User: "Hello, I want to know about admissions"
+├── Intent: greeting + admission_info
+├── Response: Welcome + MRNAT overview
+├── Follow-up: "Would you like to know about..."
+│   ├── MRNAT details
+│   ├── Application process
+│   ├── Scholarships
+│   └── Eligibility criteria
+└── Context: admission_focused = True
+```
+
+### 2. Course Information Flow
+
+```
+User: "What engineering courses do you offer?"
+├── Intent: courses + engineering
+├── Response: B.Tech programs list
+├── Follow-up: "Interested in specific program?"
+│   ├── Computer Science details
+│   ├── Mechanical Engineering
+│   ├── Electronics & Communication
+│   └── Industry partnerships
+└── Context: course_category = "engineering"
+```
+
+### 3. Multi-turn Conversation Example
+
+```
+Turn 1: User: "Hi"
+        Bot: "Welcome! How can I help?"
+        Context: greeting_completed = True
+
+Turn 2: User: "Tell me about fees"
+        Bot: "Here's our fee structure..."
+        Context: topic = "fees"
+
+Turn 3: User: "What about scholarships?"
+        Bot: "We offer scholarships up to 100%..."
+        Context: topic = "fees", subtopic = "scholarships"
+
+Turn 4: User: "How to apply for scholarship?"
+        Bot: "Scholarships are based on MRNAT..."
+        Context: topic = "admission", related_to = "scholarships"
+```
+
+## 🔧 Response Generation System
+
+### Template-Based Responses
+
+```python
+# Response templates for different intents
+response_templates = {
+    "admission_info": {
+        "general": "MRU admissions are through MRNAT...",
+        "mrnat_specific": "MRNAT exam details: {dates}, {duration}...",
+        "process": "Application process: {steps}...",
+        "scholarships": "Scholarship opportunities: {schemes}..."
+    }
+}
+```
+
+### Dynamic Content Generation
+
+```python
+def generate_course_response(self, courses: List[str], category: str) -> str:
+    if len(courses) <= 3:
+        return f"We offer {len(courses)} {category} programs: " + ", ".join(courses)
+    else:
+        preview = courses[:3]
+        return f"We offer {len(courses)} {category} programs including: " + \
+               ", ".join(preview) + f" and {len(courses)-3} more."
+```
+
+### Context-Aware Response Selection
+
+```python
+def select_response_variant(self, intent: str, context: dict, user_input: str) -> str:
+    # Consider conversation history
+    # Analyze user input specificity
+    # Select appropriate detail level
+    # Customize response format
+```
+
+## 🎯 Error Handling & Fallback Strategies
+
+### Voice Recognition Errors
+
+```python
+class VoiceErrorHandling:
+    def handle_recognition_error(self, error_type: str):
+        if error_type == "timeout":
+            return "No speech detected. Please try again."
+        elif error_type == "unknown_value":
+            return "Could not understand. Please speak clearly."
+        elif error_type == "request_error":
+            return "Service unavailable. Switching to text mode."
+```
+
+### Intent Classification Fallbacks
+
+```python
+def fallback_strategy(self, user_input: str) -> str:
+    # 1. Try fuzzy matching with known intents
+    # 2. Extract keywords and suggest topics
+    # 3. Provide general university information
+    # 4. Ask clarifying questions
+```
+
+### Response Generation Fallbacks
+
+```python
+def generate_fallback_response(self, intent: str) -> str:
+    fallback_responses = {
+        "general_info": "I can help with admissions, courses, fees, placements...",
+        "unknown": "I'm not sure about that. Let me provide general information..."
+    }
+```
+
+## 📊 Performance Metrics & Analytics
+
+### Response Time Metrics
+
+```python
+class PerformanceTracker:
+    def track_response_time(self):
+        # Speech recognition time
+        # Intent classification time
+        # Response generation time
+        # TTS processing time
+        # Total interaction time
+```
+
+### Conversation Analytics
+
+```python
+class ConversationAnalytics:
+    def analyze_session(self, conversation_history: List[dict]):
+        # Intent distribution
+        # Topic progression
+        # User satisfaction indicators
+        # Error rates
+        # Session duration
+```
+
+### Usage Statistics
+
+- **Intent Distribution**: Track most common user queries
+- **Session Metrics**: Average session length, interactions per session
+- **Error Rates**: Voice recognition failures, unrecognized intents
+- **Response Effectiveness**: Follow-up questions, clarification requests
+
+## 🔐 Security & Privacy Considerations
+
+### Data Protection
+
+```python
+class PrivacyManager:
+    def sanitize_input(self, user_input: str) -> str:
+        # Remove personal information
+        # Anonymize sensitive data
+        # Log minimal necessary information
+    
+    def secure_conversation_storage(self, conversation: dict):
+        # Encrypt conversation logs
+        # Implement data retention policies
+        # Ensure GDPR compliance
+```
+
+### Audio Data Handling
+
+- **No Local Storage**: Audio not stored locally
+- **Secure Transmission**: HTTPS for API calls
+- **Temporary Processing**: Immediate deletion after processing
+- **User Consent**: Clear privacy policy communication
+
+## 🚀 Deployment Considerations
+
+### System Requirements
+
+```yaml
+minimum_requirements:
+  python: ">=3.8"
+  memory: "2GB RAM"
+  storage: "500MB"
+  network: "Stable internet for speech recognition"
+
+recommended_requirements:
+  python: ">=3.9"
+  memory: "4GB RAM"
+  storage: "1GB"
+  network: "High-speed internet"
+  audio: "Quality microphone and speakers"
+```
+
+### Scaling Strategies
+
+```python
+# For high-traffic scenarios
+class ScalableDeployment:
+    def implement_caching(self):
+        # Cache frequent responses
+        # Preload knowledge base
+        # Optimize database queries
+    
+    def load_balancing(self):
+        # Multiple chatbot instances
+        # Session distribution
+        # Resource optimization
+```
+
+### Performance Optimization
+
+- **Response Caching**: Store common responses
+- **Knowledge Base Indexing**: Fast information retrieval
+- **Concurrent Processing**: Handle multiple users
+- **Resource Management**: Optimize memory usage
+
+## 🔮 Future Enhancement Roadmap
+
+### Phase 1: Core Improvements
+- Enhanced NLP with transformer models
+- Improved context understanding
+- Better error handling
+- Performance optimization
+
+### Phase 2: Advanced Features
+- Multilingual support
+- Voice customization
+- Personalization engine
+- Advanced analytics
+
+### Phase 3: Integration & Expansion
+- University system integration
+- Mobile application
+- Web interface
+- API development
+
+### Phase 4: AI Enhancement
+- Machine learning-based responses
+- Sentiment analysis
+- Predictive assistance
+- Advanced conversation flows
+
+## 📝 API Documentation
+
+### Core Classes API
+
+```python
+# Main chatbot interface
+class MRUVoiceChatbot:
+    def __init__(self, voice_enabled: bool = True)
+    def get_user_input(self) -> Optional[str]
+    def provide_response(self, response: str)
+    def run(self)
+
+# Knowledge base interface
+class MRUKnowledgeBase:
+    def get_info(self, category: str, subcategory: str = None) -> dict
+    
+# Intent classification
+class IntentClassifier:
+    def classify_intent(self, text: str) -> str
+    
+# Response generation
+class ResponseGenerator:
+    def generate_response(self, intent: str, user_input: str) -> str
+```
+
+### Configuration API
+
+```python
+# Voice settings configuration
+voice_config = {
+    'enabled': True,
+    'tts_rate': 150,
+    'tts_volume': 0.8,
+    'recognition_timeout': 5
+}
+
+# Knowledge base configuration
+kb_config = {
+    'update_frequency': 'daily',
+    'cache_responses': True,
+    'max_response_length': 500
+}
+```
+
+## 🧪 Testing Framework
+
+### Unit Tests
+
+```python
+class TestIntentClassification:
+    def test_greeting_intent(self):
+        classifier = IntentClassifier()
+        assert classifier.classify_intent("Hello") == "greeting"
+    
+    def test_admission_intent(self):
+        classifier = IntentClassifier()
+        assert classifier.classify_intent("How to apply?") == "admission_info"
+```
+
+### Integration Tests
+
+```python
+class TestChatbotIntegration:
+    def test_complete_conversation_flow(self):
+        chatbot = MRUVoiceChatbot(voice_enabled=False)
+        # Test full conversation cycle
+    
+    def test_voice_processing_pipeline(self):
+        # Test speech-to-text and text-to-speech
+```
+
+### Performance Tests
+
+```python
+class TestPerformance:
+    def test_response_time(self):
+        # Measure average response time
+        # Test under load conditions
+        # Memory usage profiling
+```
+
+---
+
+*This technical overview provides a comprehensive understanding of the MRU Voice Chatbot system architecture, implementation details, and future development plans.*
EOF
)
