(cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF'
diff --git a/demo.py b/demo.py
--- a/demo.py
+++ b/demo.py
@@ -0,0 +1,260 @@
+#!/usr/bin/env python3
+"""
+MRU Voice Chatbot Demonstration Script
+=====================================
+
+This script demonstrates the key features and capabilities of the 
+Manav Rachna University Voice Chatbot system.
+"""
+
+import time
+import sys
+from mru_chatbot_system import MRUVoiceChatbot, MRUKnowledgeBase, IntentClassifier, ResponseGenerator
+
+def print_header(title):
+    """Print a formatted header"""
+    print("\n" + "="*60)
+    print(f"🎯 {title.upper()}")
+    print("="*60)
+
+def print_section(title):
+    """Print a formatted section header"""
+    print(f"\n📋 {title}")
+    print("-" * 40)
+
+def simulate_conversation(chatbot, queries):
+    """Simulate a conversation with predefined queries"""
+    for i, query in enumerate(queries, 1):
+        print(f"\n👤 User {i}: {query}")
+        time.sleep(1)  # Simulate thinking time
+        
+        # Classify intent and generate response
+        intent = chatbot.intent_classifier.classify_intent(query)
+        response = chatbot.response_generator.generate_response(intent, query)
+        
+        print(f"🎯 Intent: {intent}")
+        print(f"🤖 Assistant: {response[:200]}...")  # Truncate for demo
+        
+        # Add to conversation history
+        chatbot.conversation_manager.add_interaction(query, response, intent)
+        
+        time.sleep(2)  # Pause between interactions
+
+def demo_knowledge_base():
+    """Demonstrate the knowledge base structure"""
+    print_header("Knowledge Base Demonstration")
+    
+    kb = MRUKnowledgeBase()
+    
+    print_section("Available Information Categories")
+    categories = list(kb.knowledge.keys())
+    for i, category in enumerate(categories, 1):
+        print(f"{i}. {category.replace('_', ' ').title()}")
+    
+    print_section("Sample University Information")
+    uni_info = kb.get_info("university_info")
+    for key, value in uni_info.items():
+        print(f"• {key.replace('_', ' ').title()}: {value}")
+    
+    print_section("Sample Course Information")
+    courses = kb.get_info("courses", "undergraduate")
+    print("🔧 Engineering Programs:")
+    for course in courses["engineering"][:3]:
+        print(f"  • {course}")
+    print("💼 Management Programs:")
+    for course in courses["management"][:3]:
+        print(f"  • {course}")
+
+def demo_intent_classification():
+    """Demonstrate intent classification capabilities"""
+    print_header("Intent Classification Demonstration")
+    
+    classifier = IntentClassifier()
+    
+    test_queries = [
+        ("Hello, how are you?", "greeting"),
+        ("I want to apply for admission", "admission_info"),
+        ("What courses do you offer?", "courses"),
+        ("How much are the fees?", "fees"),
+        ("Tell me about placements", "placements"),
+        ("What facilities do you have?", "facilities"),
+        ("How can I contact you?", "contact"),
+        ("What about campus life?", "campus_life"),
+        ("Thank you for the information", "goodbye")
+    ]
+    
+    print_section("Intent Classification Examples")
+    for query, expected_intent in test_queries:
+        predicted_intent = classifier.classify_intent(query)
+        status = "✅" if predicted_intent == expected_intent else "❌"
+        print(f"{status} Query: '{query}'")
+        print(f"   Expected: {expected_intent} | Predicted: {predicted_intent}")
+
+def demo_conversation_flows():
+    """Demonstrate different conversation flows"""
+    print_header("Conversation Flow Demonstration")
+    
+    # Initialize chatbot in text mode for demo
+    chatbot = MRUVoiceChatbot(voice_enabled=False)
+    
+    print_section("Admission Inquiry Flow")
+    admission_queries = [
+        "Hi, I'm interested in admissions",
+        "Tell me about MRNAT exam",
+        "What is the application process?",
+        "Are scholarships available?"
+    ]
+    simulate_conversation(chatbot, admission_queries)
+    
+    print_section("Course Information Flow")
+    course_queries = [
+        "What engineering programs do you offer?",
+        "Tell me about B.Tech Computer Science",
+        "Do you have industry partnerships?"
+    ]
+    simulate_conversation(chatbot, course_queries)
+    
+    print_section("Placement Inquiry Flow")
+    placement_queries = [
+        "How are the placements?",
+        "What is the highest package offered?",
+        "Which companies visit for recruitment?"
+    ]
+    simulate_conversation(chatbot, placement_queries)
+
+def demo_response_customization():
+    """Demonstrate response customization based on context"""
+    print_header("Response Customization Demonstration")
+    
+    kb = MRUKnowledgeBase()
+    response_gen = ResponseGenerator(kb)
+    
+    print_section("Context-Aware Responses")
+    
+    # Same intent, different queries - should get different responses
+    fee_queries = [
+        "What are the fees?",
+        "How much does B.Tech cost?",
+        "Tell me about scholarship opportunities",
+        "Is financial aid available?"
+    ]
+    
+    for query in fee_queries:
+        response = response_gen._handle_fees(query)
+        print(f"\n👤 Query: {query}")
+        print(f"🤖 Response Preview: {response[:150]}...")
+
+def demo_multilingual_support():
+    """Demonstrate potential for multilingual support"""
+    print_header("Multilingual Support (Future Feature)")
+    
+    print_section("Planned Language Support")
+    languages = [
+        "🇮🇳 Hindi - हिंदी",
+        "🇮🇳 Punjabi - ਪੰਜਾਬੀ", 
+        "🇮🇳 Urdu - اردو",
+        "🇬🇧 English (Current)",
+        "🇫🇷 French - Français",
+        "🇪🇸 Spanish - Español"
+    ]
+    
+    for lang in languages:
+        print(f"• {lang}")
+    
+    print("\n💡 Note: Currently supports English. Multilingual support planned for future releases.")
+
+def demo_error_handling():
+    """Demonstrate error handling capabilities"""
+    print_header("Error Handling Demonstration")
+    
+    chatbot = MRUVoiceChatbot(voice_enabled=False)
+    
+    print_section("Handling Unclear Queries")
+    unclear_queries = [
+        "",  # Empty query
+        "asdfghjkl",  # Random text
+        "What is the capital of Mars?",  # Irrelevant question
+        "Tell me everything about everything"  # Too broad
+    ]
+    
+    for query in unclear_queries:
+        if query:  # Skip empty query for demo
+            print(f"\n👤 User: '{query}'")
+            intent = chatbot.intent_classifier.classify_intent(query)
+            response = chatbot.response_generator.generate_response(intent, query)
+            print(f"🎯 Classified as: {intent}")
+            print(f"🤖 Response: {response[:100]}...")
+
+def demo_performance_metrics():
+    """Demonstrate performance and analytics"""
+    print_header("Performance Metrics Demonstration")
+    
+    chatbot = MRUVoiceChatbot(voice_enabled=False)
+    
+    # Simulate a conversation session
+    sample_queries = [
+        "Hello",
+        "Tell me about admissions",
+        "What courses are available?",
+        "How much are the fees?",
+        "Thank you"
+    ]
+    
+    print_section("Simulating User Session")
+    start_time = time.time()
+    
+    for query in sample_queries:
+        intent = chatbot.intent_classifier.classify_intent(query)
+        response = chatbot.response_generator.generate_response(intent, query)
+        chatbot.conversation_manager.add_interaction(query, response, intent)
+    
+    end_time = time.time()
+    
+    print(f"• Session duration: {end_time - start_time:.2f} seconds")
+    print(f"• Total interactions: {len(sample_queries)}")
+    print(f"• Average response time: {(end_time - start_time) / len(sample_queries):.2f} seconds")
+    
+    # Show conversation summary
+    print_section("Conversation Summary")
+    summary = chatbot.conversation_manager.get_conversation_summary()
+    print(summary)
+
+def main():
+    """Main demonstration function"""
+    print_header("MRU Voice Chatbot System Demonstration")
+    print("🚀 Welcome to the comprehensive demo of the MRU Voice Chatbot!")
+    print("This demonstration will showcase all key features and capabilities.")
+    
+    demos = [
+        ("Knowledge Base Structure", demo_knowledge_base),
+        ("Intent Classification", demo_intent_classification),
+        ("Conversation Flows", demo_conversation_flows),
+        ("Response Customization", demo_response_customization),
+        ("Error Handling", demo_error_handling),
+        ("Performance Metrics", demo_performance_metrics),
+        ("Multilingual Support (Future)", demo_multilingual_support)
+    ]
+    
+    try:
+        for i, (demo_name, demo_func) in enumerate(demos, 1):
+            print(f"\n🎯 Demo {i}/{len(demos)}: {demo_name}")
+            input("Press Enter to continue...")
+            demo_func()
+            time.sleep(1)
+        
+        print_header("Demonstration Complete")
+        print("✅ All demos completed successfully!")
+        print("\n🎉 Thank you for exploring the MRU Voice Chatbot system!")
+        print("\n📞 For more information:")
+        print("• Run: python mru_chatbot_system.py")
+        print("• Email: admissions@manavrachna.edu.in")
+        print("• Phone: +91-129-4259000")
+        
+    except KeyboardInterrupt:
+        print("\n\n👋 Demo interrupted by user. Goodbye!")
+    except Exception as e:
+        print(f"\n❌ Demo error: {e}")
+        print("Please check your installation and try again.")
+
+if __name__ == "__main__":
+    main()
EOF
)
