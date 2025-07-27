(cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF'
diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -0,0 +1,324 @@
+# Voice-Enabled Chatbot for Manav Rachna University 🎓
+
+An advanced AI-powered chatbot that provides comprehensive information about Manav Rachna University through voice and text interactions. The system utilizes natural language processing, speech recognition, and text-to-speech capabilities to deliver a seamless user experience.
+
+## 🌟 Features
+
+### Core Capabilities
+- **🎤 Voice Recognition**: Converts speech to text for natural interaction
+- **🔊 Text-to-Speech**: Provides spoken responses for accessibility
+- **🧠 Intent Classification**: Understands user queries and context
+- **📚 Comprehensive Knowledge Base**: Detailed information about MRU
+- **💬 Multi-turn Conversations**: Maintains context across interactions
+- **🔄 Dual Mode**: Seamlessly switch between voice and text input
+
+### Information Coverage
+- **📋 Admissions**: MRNAT exam, application process, scholarships
+- **🎓 Courses**: UG, PG, and Doctoral programs across all disciplines
+- **💰 Fees**: Detailed fee structure and financial aid options
+- **🚀 Placements**: Statistics, top recruiters, salary packages
+- **🏫 Facilities**: Campus infrastructure, hostels, sports, labs
+- **📞 Contact**: Phone numbers, email, address, locations
+- **🎭 Campus Life**: Student activities, clubs, events
+
+## 🚀 Quick Start
+
+### Prerequisites
+- Python 3.8 or higher
+- Microphone (for voice input)
+- Speakers/headphones (for voice output)
+- Internet connection (for speech recognition)
+
+### Installation
+
+1. **Clone the repository:**
+```bash
+git clone <repository-url>
+cd mru-voice-chatbot
+```
+
+2. **Install dependencies:**
+```bash
+pip install -r requirements.txt
+```
+
+3. **Download spaCy language model:**
+```bash
+python -m spacy download en_core_web_sm
+```
+
+4. **Run the chatbot:**
+```bash
+python mru_chatbot_system.py
+```
+
+## 🎯 Usage Guide
+
+### Starting the Chatbot
+When you run the system, it will automatically detect if voice features are available and start in the appropriate mode.
+
+```
+🚀 Initializing MRU Voice Chatbot...
+🎤 Voice features enabled
+✅ MRU Chatbot initialized successfully!
+
+============================================================
+🎓 WELCOME TO MANAV RACHNA UNIVERSITY VOICE ASSISTANT 🎓
+============================================================
+```
+
+### Voice Mode
+- **Speak naturally** into your microphone
+- The system will process your speech and respond audibly
+- Say **"text"** to switch to text mode
+
+### Text Mode
+- **Type your questions** and press Enter
+- Responses will be displayed as text
+- Type **"voice"** to enable voice mode (if available)
+
+### Sample Interactions
+
+#### Admission Queries
+**User:** "Tell me about admissions"
+**Assistant:** Information about MRNAT, application process, and scholarships
+
+#### Course Information
+**User:** "What engineering courses do you offer?"
+**Assistant:** Detailed list of B.Tech programs with specializations
+
+#### Fee Inquiries
+**User:** "How much are the fees for B.Tech?"
+**Assistant:** Fee structure with scholarship information
+
+#### Placement Details
+**User:** "What about placements and job opportunities?"
+**Assistant:** Placement statistics, top recruiters, and packages
+
+### Available Commands
+- **"help"** - Show available commands
+- **"voice"** - Enable voice mode
+- **"text"** - Switch to text mode
+- **"summary"** - Get conversation summary
+- **"quit"** or **"exit"** - End the conversation
+
+## 🏗️ System Architecture
+
+### Components Overview
+
+```
+┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
+│   Voice Input   │───▶│  Intent Classifier│───▶│ Response Generator│
+│  (Speech-to-    │    │  (NLP Processing) │    │  (Context-aware)  │
+│     Text)       │    └──────────────────┘    └─────────────────┘
+└─────────────────┘                                       │
+                                                          ▼
+┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
+│  Voice Output   │◀───│  Knowledge Base  │◀───│ Conversation    │
+│  (Text-to-      │    │  (MRU Data)      │    │ Manager         │
+│    Speech)      │    └──────────────────┘    └─────────────────┘
+└─────────────────┘
+```
+
+### Key Classes
+
+1. **MRUKnowledgeBase**
+   - Stores comprehensive university information
+   - Organized by categories (admissions, courses, fees, etc.)
+   - Easy to update and maintain
+
+2. **IntentClassifier**
+   - Uses regex patterns for intent recognition
+   - Classifies user queries into categories
+   - Handles context and conversation flow
+
+3. **VoiceHandler**
+   - Manages speech recognition and synthesis
+   - Configurable voice settings
+   - Error handling for audio issues
+
+4. **ResponseGenerator**
+   - Creates contextual responses
+   - Handles different intent types
+   - Maintains conversation context
+
+5. **ConversationManager**
+   - Tracks conversation history
+   - Provides session summaries
+   - Manages user preferences
+
+## 📊 Knowledge Base Structure
+
+The chatbot's knowledge is organized into the following categories:
+
+### University Information
+- Basic details, history, recognition
+- Rankings and achievements
+- Mission and values
+
+### Admissions
+- MRNAT exam details and dates
+- Application process steps
+- Scholarship schemes and criteria
+
+### Academic Programs
+- Undergraduate courses (Engineering, Management, Law, Sciences)
+- Postgraduate programs
+- Doctoral studies
+- Industry partnerships
+
+### Infrastructure
+- Academic facilities (labs, library, classrooms)
+- Residential facilities (hostels, mess)
+- Sports and recreational facilities
+- Campus amenities
+
+### Career Services
+- Placement statistics and records
+- Top recruiting companies
+- Training and development programs
+- Alumni achievements
+
+### Contact Information
+- Phone numbers for different departments
+- Email addresses and websites
+- Campus address and directions
+- City office locations
+
+## 🔧 Configuration
+
+### Voice Settings
+You can customize voice parameters in the `VoiceHandler` class:
+
+```python
+# Speech rate (words per minute)
+self.tts_engine.setProperty('rate', 150)
+
+# Volume level (0.0 to 1.0)
+self.tts_engine.setProperty('volume', 0.8)
+
+# Timeout for voice input (seconds)
+audio = self.recognizer.listen(source, timeout=5)
+```
+
+### Intent Patterns
+Add new intent patterns in the `IntentClassifier` class:
+
+```python
+self.intent_patterns = {
+    "new_intent": [
+        r"(?i)\b(keyword1|keyword2)\b",
+        r"(?i)\b(pattern.*match)\b"
+    ]
+}
+```
+
+### Knowledge Base Updates
+Update information in the `MRUKnowledgeBase` class:
+
+```python
+self.knowledge = {
+    "new_category": {
+        "subcategory": {
+            "key": "value"
+        }
+    }
+}
+```
+
+## 🛠️ Troubleshooting
+
+### Common Issues
+
+1. **Voice Recognition Not Working**
+   - Check microphone permissions
+   - Ensure internet connectivity
+   - Try switching to text mode with "text" command
+
+2. **Text-to-Speech Not Working**
+   - Check audio drivers and speakers
+   - Verify pyttsx3 installation
+   - System will fallback to text-only mode
+
+3. **Import Errors**
+   - Install missing dependencies: `pip install -r requirements.txt`
+   - Download spaCy model: `python -m spacy download en_core_web_sm`
+
+4. **Audio Device Issues**
+   - Check microphone and speaker connections
+   - Update audio drivers
+   - Try different audio devices
+
+### Performance Optimization
+
+- **Reduce Speech Recognition Timeout**: Lower timeout values for faster response
+- **Optimize Response Length**: Shorter responses for better voice experience
+- **Cache Responses**: Store frequent responses for faster retrieval
+
+## 🤝 Contributing
+
+### Adding New Features
+
+1. **New Intent Types**
+   - Add patterns to `IntentClassifier`
+   - Create handler method in `ResponseGenerator`
+   - Update knowledge base if needed
+
+2. **Enhanced NLP**
+   - Integrate advanced NLP models
+   - Improve context understanding
+   - Add sentiment analysis
+
+3. **Additional Data Sources**
+   - Web scraping for real-time updates
+   - Database integration
+   - API connections
+
+### Code Style
+- Follow PEP 8 guidelines
+- Add comprehensive docstrings
+- Include type hints
+- Write unit tests
+
+## 📈 Future Enhancements
+
+### Planned Features
+- **🌐 Web Interface**: Browser-based interaction
+- **📱 Mobile App**: Native mobile application
+- **🔗 Integration**: Connect with university systems
+- **🎯 Personalization**: User-specific recommendations
+- **📊 Analytics**: Usage patterns and improvements
+- **🌍 Multi-language**: Support for regional languages
+
+### Technical Improvements
+- **Advanced NLP**: Transformer-based models
+- **Better Context**: Long-term conversation memory
+- **Real-time Updates**: Dynamic knowledge base updates
+- **Performance**: Optimized response times
+- **Security**: User data protection
+
+## 📞 Support
+
+For issues, suggestions, or contributions:
+
+- **Email**: support@example.com
+- **Documentation**: See inline code comments
+- **Issues**: Create GitHub issues for bugs
+- **Features**: Submit pull requests for enhancements
+
+## 📄 License
+
+This project is licensed under the MIT License - see the LICENSE file for details.
+
+## 🙏 Acknowledgments
+
+- **Manav Rachna University** for institutional information
+- **Speech Recognition Community** for open-source tools
+- **Python NLP Libraries** for language processing capabilities
+- **Contributors** who help improve the system
+
+---
+
+**Built with ❤️ for Manav Rachna University students and prospective applicants**
+
+*This chatbot aims to provide accurate and helpful information. For official university matters, please contact MRU directly at +91-129-4259000 or admissions@manavrachna.edu.in*
EOF
)
