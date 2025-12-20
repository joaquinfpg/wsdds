#!/usr/bin/env python3
"""
Test script for the quotation_request conversation flow
Demonstrates Chris Voss negotiation principles and variable extraction
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from features.conversation_flows import (
    detect_conversation_context,
    advance_conversation,
    extract_quotation_variables,
    detect_customer_intent,
    detect_urgency,
    detect_price_sensitivity
)

def test_context_detection():
    """Test detection of all conversation contexts"""
    print("=== Testing Context Detection ===")

    test_cases = [
        # Quotation requests
        ("Hi i need a quote for a glass in my toyota corolla", "quotation_request"),
        ("Hi im just shopping around for price for a repair in my 2000 hyundai sonata", "quotation_request"),
        ("Looking for the cheapest windshield replacement", "quotation_request"),
        ("My insurance wants me to get a quote for my damaged window", "quotation_request"),

        # Problem diagnosis (when reporting damage/issues)
        ("I have a cracked windshield on my 2020 Honda Civic", "problem_diagnosis"),

        # Competitive positioning
        ("Why should I choose you over the big company?", "competitive_positioning"),
        ("What's better than Safelite?", "competitive_positioning"),
        ("How are you different from the third party claim administrator?", "competitive_positioning"),

        # Insurance guidance
        ("How do I file an insurance claim?", "insurance_guidance"),
        ("Can you help with my insurance for windshield replacement?", "insurance_guidance"),

        # Third party questions go to competitive positioning
        ("What about the third party claim administrator?", "competitive_positioning"),

        # Repair vs replacement
        ("Should I repair or replace my windshield?", "repair_vs_replacement"),

        # Problem diagnosis for immediate issues
        ("Is it better to fix or replace the crack?", "problem_diagnosis"),
        ("What's the difference between repair and replacement?", "quotation_request")
    ]

    for message, expected_context in test_cases:
        context = detect_conversation_context(message)
        status = "✓" if context == expected_context else "✗"
        print(f"{status} '{message}' -> {context} (expected: {expected_context})")
        if context != expected_context:
            print(f"   Expected: {expected_context}, Got: {context}")

    print()

def test_intent_detection():
    """Test customer intent detection"""
    print("=== Testing Customer Intent Detection ===")

    test_cases = [
        ("I need this fixed today, I'll pay cash", "immediate_cash"),
        ("My insurance adjuster needs a quote", "immediate_insurance"),
        ("Can you give me a quote for next week?", "postponed_cash"),
        ("Just shopping around for prices", "just_looking"),
        ("What's your cheapest price?", "lower_price"),
        ("I'm scared of filing an insurance claim", "afraid_insurance")
    ]

    for message, expected_intent in test_cases:
        detected_intent = detect_customer_intent(message.lower())
        status = "✓" if detected_intent == expected_intent else "✗"
        print(f"{status} '{message}' -> {detected_intent} (expected: {expected_intent})")

    print()

def test_variable_extraction():
    """Test comprehensive variable extraction"""
    print("=== Testing Variable Extraction ===")

    test_message = "Hi i need a quote for a glass in my toyota corolla"
    variables = {}

    # Test quotation-specific extraction
    extracted = extract_quotation_variables(test_message, variables)
    print(f"Message: '{test_message}'")
    print("Extracted variables:")
    for key, value in extracted.items():
        if value is not None:
            print(f"  {key}: {value}")
    print()

def test_conversation_flow():
    """Test the complete conversation flow"""
    print("=== Testing Complete Conversation Flow ===")

    # Start with a customer inquiry
    initial_message = "Hi i need a quote for a glass in my toyota corolla"
    context = detect_conversation_context(initial_message)

    print(f"Initial message: '{initial_message}'")
    print(f"Context detected: {context}")
    print()

    # Initialize conversation state
    state = {
        'current_step': None,
        'variables': {'context': context},
        'conversation_history': []
    }

    # Simulate conversation flow
    current_message = initial_message
    max_steps = 10
    step_count = 0

    while step_count < max_steps:
        step_count += 1
        print(f"--- Step {step_count} ---")

        # Advance conversation
        next_step, response, new_state = advance_conversation(context, state, current_message)

        print(f"Current step: {state.get('current_step')}")
        print(f"Next step: {next_step}")
        print(f"Response: {response[:100]}...")
        print(f"Variables: {new_state.get('variables', {})}")
        print()

        # Update state
        state = new_state
        state['current_step'] = next_step

        # Break if conversation ends
        if next_step in ['end', 'end_conversation', None]:
            break

        # Simulate user responses based on step (simplified)
        if 'gather_vehicle_basics' in next_step:
            current_message = "It's a 2020 Toyota Corolla with a small crack"
        elif 'assess_damage_severity' in next_step:
            current_message = "It's about the size of a quarter"
        elif 'provide_repair_quote' in next_step:
            current_message = "That sounds reasonable, can you schedule it?"
        else:
            current_message = "yes"

def test_business_intelligence_contexts():
    """Test the new business intelligence conversation contexts"""
    print("=== Testing Business Intelligence Contexts ===")

    # Test competitive positioning context
    print("Competitive Positioning Context:")
    competitive_message = "Why should I choose you over the big company?"
    context = detect_conversation_context(competitive_message)
    print(f"Message: '{competitive_message}'")
    print(f"Context: {context}")

    # Test insurance guidance context
    print("\nInsurance Guidance Context:")
    insurance_message = "How do I file an insurance claim for my windshield?"
    context = detect_conversation_context(insurance_message)
    print(f"Message: '{insurance_message}'")
    print(f"Context: {context}")

    # Test repair vs replacement context
    print("\nRepair vs Replacement Context:")
    repair_message = "Should I repair or replace my cracked windshield?"
    context = detect_conversation_context(repair_message)
    print(f"Message: '{repair_message}'")
    print(f"Context: {context}")
    print()

def test_negotiation_tactics():
    """Test negotiation tactic application"""
    print("=== Testing Negotiation Tactics ===")

    # Test mirroring
    print("Mirroring example:")
    customer_says = "I'm worried about the cost"
    mirrored_response = f"I understand you're concerned about the cost. Many customers feel the same way initially."
    print(f"Customer: '{customer_says}'")
    print(f"Response: '{mirrored_response}'")
    print()

    # Test calibrated questions
    print("Calibrated questions example:")
    questions = [
        "What would you like to achieve with this repair?",
        "How is this damage affecting your driving?",
        "What concerns you most about getting this fixed?"
    ]
    print("Calibrated questions:")
    for q in questions:
        print(f"  • {q}")
    print()

    # Test labeling emotions
    print("Labeling emotions example:")
    emotion_label = "It sounds like you're concerned about the insurance process"
    print(f"Emotion label: '{emotion_label}'")
    print()

if __name__ == "__main__":
    print("Testing Quotation Request Conversation Flow")
    print("=" * 50)
    print()

    test_context_detection()
    test_intent_detection()
    test_variable_extraction()
    test_conversation_flow()
    test_business_intelligence_contexts()
    test_negotiation_tactics()

    print("Testing completed!")