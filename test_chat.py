import requests
import json

def test_chat_endpoint():
    """Test various chat scenarios with the comprehensive business intelligence"""
    url = 'http://localhost:8080/chat/send'

    test_cases = [
        {
            'name': 'Introductory Message',
            'messages': [{'role': 'user', 'content': 'Hello'}]
        },
        {
            'name': 'Competitive Positioning',
            'messages': [
                {'role': 'user', 'content': 'Hello'},
                {'role': 'assistant', 'content': 'Welcome message'},
                {'role': 'user', 'content': 'Why should I choose you over the big company?'}
            ]
        },
        {
            'name': 'Insurance Guidance',
            'messages': [
                {'role': 'user', 'content': 'Hello'},
                {'role': 'assistant', 'content': 'Welcome message'},
                {'role': 'user', 'content': 'How do I file an insurance claim?'}
            ]
        },
        {
            'name': 'Repair vs Replacement',
            'messages': [
                {'role': 'user', 'content': 'Hello'},
                {'role': 'assistant', 'content': 'Welcome message'},
                {'role': 'user', 'content': 'Should I repair or replace my windshield?'}
            ]
        },
        {
            'name': 'Part Lookup',
            'messages': [{'role': 'user', 'content': 'Find windshield parts for 2020 Toyota Camry'}]
        }
    ]

    for test_case in test_cases:
        print(f"\n=== Testing: {test_case['name']} ===")
        data = {'messages': test_case['messages']}

        try:
            response = requests.post(url, json=data)
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"Response: {result.get('response', 'No response')[:200]}...")
            else:
                print(f"Error Response: {response.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_chat_endpoint()