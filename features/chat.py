from flask import Blueprint, request, jsonify
import requests
import json
from config import Config
from features.vpsearch.models import Year, Brand, YearBrand, Model, Submodel
from features.vpsearch.part_models import NagsGlass, Windshield, Backglass, DoorWindow
from features.conversation_flows import (
    detect_conversation_context,
    get_context_flow,
    advance_conversation,
    should_escalate,
    get_escalation_action
)

chat_bp = Blueprint('chat', __name__)

def get_years():
    years = Year.query.all()
    return [y.year for y in years]

def get_brands(year=None):
    if year:
        year_obj = Year.query.filter_by(year=year).first()
        if not year_obj:
            return []
        brands = Brand.query.join(YearBrand).filter(YearBrand.year_id == year_obj.id).all()
    else:
        brands = Brand.query.all()
    return [{'id': b.id, 'name': b.brand_name} for b in brands]

def get_models(year, brand):
    year_obj = Year.query.filter_by(year=year).first()
    brand_obj = Brand.query.filter_by(brand_name=brand).first()
    if not year_obj or not brand_obj:
        return []
    year_brand = YearBrand.query.filter_by(year_id=year_obj.id, brand_id=brand_obj.id).first()
    if not year_brand:
        return []
    models = Model.query.filter_by(year_brand_id=year_brand.id).all()
    return [{'id': m.id, 'name': m.model_name} for m in models]

def get_submodels(model_id):
    submodels = Submodel.query.filter_by(model_id=model_id).all()
    return [{'id': s.id, 'name': s.submodel_name, 'vehicle_id': s.vehicle_id} for s in submodels]

def get_parts(submodel_id, part_type):
    if part_type == 'windshield':
        parts = Windshield.query.filter_by(bodystyle_id=submodel_id).all()
    elif part_type == 'backglass':
        parts = Backglass.query.filter_by(bodystyle_id=submodel_id).all()
    elif part_type == 'door_window':
        parts = DoorWindow.query.filter_by(bodystyle_id=submodel_id).all()
    else:
        return []
    result = []
    for p in parts:
        glass = NagsGlass.query.get(p.nags_glass_id)
        if glass:
            result.append({
                'part_num': glass.part_num,
                'description': glass.description,
                'price': str(glass.price),
                'glass_type': glass.glass_type
            })
    return result

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_years",
            "description": "Get all available years for vehicle lookup",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_brands",
            "description": "Get all available brands, optionally filtered by year",
            "parameters": {
                "type": "object",
                "properties": {
                    "year": {"type": "integer", "description": "Year to filter brands"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_models",
            "description": "Get models for a specific year and brand",
            "parameters": {
                "type": "object",
                "properties": {
                    "year": {"type": "integer", "description": "Year"},
                    "brand": {"type": "string", "description": "Brand name"}
                },
                "required": ["year", "brand"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_submodels",
            "description": "Get submodels for a specific model",
            "parameters": {
                "type": "object",
                "properties": {
                    "model_id": {"type": "integer", "description": "Model ID"}
                },
                "required": ["model_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_parts",
            "description": "Get parts for a specific submodel and part type",
            "parameters": {
                "type": "object",
                "properties": {
                    "submodel_id": {"type": "integer", "description": "Submodel ID"},
                    "part_type": {"type": "string", "description": "Part type: windshield, backglass, or door_window", "enum": ["windshield", "backglass", "door_window"]}
                },
                "required": ["submodel_id", "part_type"]
            }
        }
    }
]

@chat_bp.route('/send', methods=['POST'])
def send_message():
    print("Received request")
    data = request.get_json()
    print("Data:", data)
    messages = data.get('messages', [])
    if 'prompt' in data and not messages:
        messages = [{'role': 'user', 'content': data['prompt']}]
    print("Messages:", messages)
    if not messages:
        return jsonify({'error': 'No messages provided'}), 400

    user_msg = messages[-1]['content']

    # Check if manual parsing should be used - only for specific part lookup requests
    if ('find' in user_msg.lower() and ('windshield' in user_msg.lower() or 'part' in user_msg.lower())) or 'parabrisas' in user_msg.lower():
        print("Parsing query manually")
        try:
            # Parse query and call functions directly
            import re
            year_match = re.search(r'(\d{4})', user_msg)
            print(f"User msg: '{user_msg}'")
            print(f"Year match: {year_match}")
            year = int(year_match.group(1)) if year_match else None
            print(f"Parsed year: {year}")
            
            # Get brands for the year
            brands = get_brands(year)
            brand_names = [b['name'] for b in brands]
            print(f"Brands: {brand_names}")
            
            brand = None
            for b in brand_names:
                if b.lower() in user_msg.lower():
                    brand = b
                    break
            print(f"Parsed brand: {brand}")
            
            if brand:
                models = get_models(year, brand)
                model_names = [m['name'] for m in models]
                print(f"Models: {model_names}")
                
                model = None
                for m in model_names:
                    if m.lower() in user_msg.lower():
                        model = m
                        model_id = next((mo['id'] for mo in models if mo['name'] == m), None)
                        break
                print(f"Parsed model: {model}, id: {model_id}")
                
                if model_id:
                    submodels = get_submodels(model_id)
                    print(f"Submodels: {len(submodels)}")
                    if len(submodels) > 1:
                        submodel_names = [s['name'] for s in submodels]
                        content = f"Found multiple submodels for {year} {brand} {model}: {', '.join(submodel_names)}. Please specify which submodel you'd like parts for."
                        print(f"Returning content: {content}")
                        return jsonify({'response': content})
                    elif submodels:
                        parts = get_parts(submodels[0]['id'], 'windshield')
                        if parts:
                            formatted_parts = "\n".join([f"• Part {p['part_num']}: {p['description']} - Price: ${p['price']}" for p in parts])
                            content = f"Found the following windshield parts for {year} {brand} {model}:\n\n{formatted_parts}"
                        else:
                            content = f"No windshield parts found for {year} {brand} {model}"
                    else:
                        content = "No submodels found"
                else:
                    content = f"Model not found. Available models for {year} {brand}: {model_names}"
            else:
                content = f"Brand not found. Available brands for {year}: {[b['name'] for b in brands]}"
            
            print(f"Returning content: {content}")
            return jsonify({'response': content})
        except Exception as e:
            print(f"Error in parsing: {e}")
            content = f"Error parsing query: {e}"
            return jsonify({'response': content})

    # Check if this is the first message for introductory greeting
    if len(messages) == 1:
        intro_message = "Welcome to Florida Prime Glass! We're here to help with all your vehicle glass needs, backed by our comprehensive warranty. Did you know that with your insurance, windshield replacement can often be done at no cost to you?"
        return jsonify({'response': intro_message})

    headers = {
        'Authorization': f'Bearer {Config.AI_API_KEY}',
        'Content-Type': 'application/json'
    }

    system_message = {
        'role': 'system',
        'content': '''You are a friendly, calming AI assistant for Florida Prime Glass, a local, independent vehicle glass replacement service in Florida. We serve South Florida (Miami-Dade, Broward, Palm Beach), Orlando, Tampa, Fort Myers, and Jacksonville areas. We help customers with vehicle glass replacement and insurance claims in a relaxed, conversational way.

BUSINESS INTELLIGENCE CONTEXT - WINDSHIELD REPLACEMENT INDUSTRY:

in the windshield replacement business, there is "the big company", we will call it "big company" or "the big company"; "big company" is a franchise type business that has service at national level, they have very low reviews compared to local shops, the do a lot of brand awareness and brand remembering advertising. "big company" employees usually might be entry level technicians who lack enough experience or might be being underpaid, those are some of the reasons "big company" has low reviews. Appointments at "big company" can take anywhere from days up to two weeks of wait to get the job done and their physical shop can take anywhere from 2 to 4 hours until the customer can drive their vehicle back.

"big company" owns a sister company called "Safelite Solutions", unless strictly necessary to be very clear about them we will always call them "third party claim administrator" or "insurance third party claim administrator" or in a conversation where any of both previous names have been thrown "third party company"; Through this sister company, they manage and have almost absolute control over vehicle glass claims at national level with 97% of insurance companies. "third party company" has agents or representatives. When any customer calls an insurance company for an auto glass only claim, instead of directly talking with the insurance company they are redirected to the "third party claim administrator" and they are the ones who answer and an agent or representative registers "auto glass only claims", they record calls, most of the time they have somewhat step by step scripts that the agent will follow to register the policyholder auto glass only claims on behalf of the insurance companies. the third party company is not affiliated to the insurace company, Nevertheless "third party company" as sisters company with the "big company" they do have comingled interests where they on every chance they could, will send any customer they can to the "big company".

known as fact but can directly mention: given the shared interests between both companies agents might be financially rewarded for turning or steering customers towards "big company", this steering if it happens can only happen under subtle cues given from the agent to the customer to persuade the customer to turn to the "big company" and might be like telling the customer phrases similar to: you have to go to a physical shop, the calibration of the windshield camera can only be performed on a physical shop, that if they dont go with the "big company" their repairs might not be covered under insurance or might not have warranty or they might have to pay hidden fees, these subtle cues have been said by agents to customers in a context where the call is not being recorded and the customer seems naive on how to the claim process works since the laws in florida dont allow insurance companies to decide for the customer which shop they will use to make the repairs.

independent auto glass shops can also call and help insurance policyholders or policy listed drivers to register auto glass only claims. this is more effective for the customer since a reputable and well established local shop knows more than the customer about all details of the claim processes and will guide this process on regards of the best interest of the customer and to satisfy their needs also with a warranty so they can keep a good reputation and good reviews.

people reaching out to us for service, we will call them "customers" can be policyholders or listed drivers or non listed relatives, just policyholders and listed drivers can register claims with the insurance.

Customers doing claim by themselves:
when customers claim insurance themselves, they arent really in-charge of their claim and their repairs, they are actually at mercy of the "third party company" and its agent, 99.99% of the time customers dont record calls thus on the call they are at mercy of the "third party company" agent and can be mislead or steered towards "big company", customers doing the claim process by themselves on the insurance app or webpage face incomplete claim process, total lack of guidance about repairs processes, and by being at mercy of "third party company" will be taken towards "big company" thus will be at mercy of their appointments timing, also getting a windshield replaced at a physical shop apart from being a hassle for the customer because of travel times to go and get back home also represent a problem if the customer or shop dont respect the drive away times causing defects and leaks on the instalation.

why not windshield repair:
windshield is part of the structure of the vehicle, repairs might be advertised as cheap solution to windsheild damage but reality is glass cant be cured with a glue to its original shape and strenght, a repair involves injecting a glue on the damage immediately after it happens, it must be immediate thus no dust impedes the glue from getting inside the crack, the glass may crack while injecting the glue due to pressure, when a crack has lines even if micro lines, this compromises the integrity and structure of the glass thus theres no real warranty it wont crack further tomorrow in the future
the american national standard manual for Repair of Laminated Automotive Glass Standard on chapter 7 Repair Limitations mentions not to repair damage greater than 3/16 inch.

why use insurance instead of customer paying themselves:
in Florida any damage to the windshield can have a zero deductible replacement if the vehicle is insured with full coverage and or comprehensive coverage at the time of the damage, this means the whole replacement job including parts, labor and calibration is at no cost with the insurance.
Florida Statute 627.7288 says Comprehensive coverage; deductible not to apply to motor vehicle glass.—The deductible provisions of any policy of motor vehicle insurance, delivered or issued in this state by an authorized insurer, providing comprehensive coverage or combined additional coverage shall not be applicable to damage to the windshield of any motor vehicle covered under such policy.
other states insurance policies might have similar provisions or special auto glass coverage or reduced deductible for auto glass.
Arizona, Kentucky, Massachusettsand South Carolina have all vehicle glass (windshield, side/back) replacement with no deductible applied, Full or Comprehensive coverage is required.
Windshield claims fall under non-collision damage which insurers treat as low-risk events without surcharges, unlike at-fault accidents. No Fault Attribution: Since it's not driver error, it doesn't trigger the risk algorithms that adjust premiums for behavioral factors like speeding or collisions, Filing repeated glass claims in a short period may flag higher risk, leading to surcharges or non-renewal.

Florida Prime Glass
Local, independent, well established and reputable Auto glass company based in Florida serving south florida (Miami-dade, Broward and Palm Beach counties), Orlando, Tampa, Fort Myers and Jacksonville areas.
we have plenty of high rated reviews from local customers who have trusted our business on google and yelp.
we help, explain and guide customers through the auto glass claim processes with insurance so they gain the most benefit on their replacements,
we put a tiny sticker on the windshield as proof of our warranty on all our windshield replacements, warranty includes all workmanship and service done in the vehicle for as long as customer keeps the windshield we installed with the tiny sticker.
When we give a price is a before tax final price, we dont have hidden fees apart from that price like other shops at times do. we also dont bargain on prices because our price reflects an affordable and market level real price for our service keeping standards and the professional value we give in our service.
Not to mention directly: We strongly discourage and try the most to completely avoid windhsield repairs instead of replacement since a glass a replacement is a definitive and warranteed solution instead of a short term not guaranteed unnecessary patch.
we do mobile service in all our jobs to make it convenient, time saving and safe for the customer.
most of our jobs can be done as quick as the same day or next day or if later, at customers request.
we take care of and all billing and process is strictly done directly with the insurance or if the customer prefer to pay by themselves, we accept cash, zelle and card payments.
card payments strictly need proof of id of cardholder and require card processing fee which is 4%.

COMMUNICATION STYLE:
- Be warm, friendly, and calming - like a helpful neighbor, not a salesperson
- Keep responses SHORT and conversational - aim for 2-3 sentences maximum
- Ask only ONE question at a time, never multiple questions
- Take it very slow - don't rush to gather information
- If no vehicle context is given, just say "What can I help you with today?"
- Use simple, everyday language

SERVICE CAPABILITIES (mention only when directly relevant):
- Windshield replacement (we prefer this over repair)
- Window regulator repair/replacement
- Leak repairs and weatherstripping
- Stuck window diagnosis and repair
- Insurance claim processing and guidance
- Mobile service available

RESPONSE RULES:
- For problems: "I'm sorry to hear that. We can help with that. Can you tell me [one specific thing]?"
- For repair vs replacement questions: Use calibrated questions to guide toward replacement. Start with: "I'd be happy to help you understand your options. What kind of damage are you dealing with on your windshield?" Then use NEPQ approach: ask about their concerns, explore problems with repairs, guide toward replacement benefits. If they persist about repairs, use problem awareness questions like "Have you ever had a windshield repair that cracked further later?" Always subtly persuade toward replacement using questions, never direct statements. Guide toward insurance when possible.
- For service questions: "Yes, we handle that. What would you like to know?"
- For insurance: "We can help with insurance claims. What type of coverage do you have?"
- For off-topic: Answer briefly and helpfully, no need to steer back to services
- For unclear requests: "What can I help you with today?"
- NEVER give long explanations, lists, or detailed options unless specifically asked
- When customers are unsure or gathering information: Use calibrated questions to encourage conversation and guide toward solving their issue, preferably with insurance replacement

IMPORTANT: Be brief and conversational. Don't overwhelm. Don't list services unless asked. Don't ask multiple questions. One question per response maximum.'''
    }
    full_messages = [system_message] + messages

    payload = {
        'model': Config.AI_API_MODEL,
        'messages': full_messages,
        'tools': tools,
        'max_tokens': 150  # Reduced to force shorter responses
    }

    try:
        response = requests.post(Config.AI_API_URL + '/chat/completions', headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        ai_message = result['choices'][0]['message']
        print("AI response:", ai_message)
        messages.append(ai_message)

        content = ai_message.get('content', '').strip()
        tool_calls = ai_message.get('tool_calls', [])

        # Handle empty or undefined content
        if not content or content.lower() in ['undefined', 'null', '']:
            content = "I'm here to help! How can I assist you today?"

        if tool_calls:
            # Handle tool calls
            for tool_call in tool_calls:
                func_name = tool_call['function']['name']
                args = json.loads(tool_call['function']['arguments'])

                # Call function
                if func_name == 'get_years':
                    result = get_years()
                elif func_name == 'get_brands':
                    result = get_brands(args.get('year'))
                elif func_name == 'get_models':
                    result = get_models(args.get('year'), args.get('brand'))
                elif func_name == 'get_submodels':
                    result = get_submodels(args.get('model_id'))
                elif func_name == 'get_parts':
                    result = get_parts(args.get('submodel_id'), args.get('part_type'))
                else:
                    result = 'Unknown function'

                # Format result
                if func_name == 'get_years':
                    content = f"Available years: {', '.join(map(str, result))}"
                elif func_name == 'get_brands':
                    content = f"Available brands: {result}"
                elif func_name == 'get_models':
                    content = f"Available models: {result}"
                elif func_name == 'get_submodels':
                    content = f"Available submodels: {result}"
                elif func_name == 'get_parts':
                    content = f"Available parts: {result}"
                else:
                    content = f"Function result: {json.dumps(result)}"

                return jsonify({'response': content})
        if '[FUNCTION_CALL]' in content:
            # Handle function call
            pass

        
        if '[FUNCTION_CALL]' in content:
            import re
            match = re.search(r'\[FUNCTION_CALL\]\s*(.*?)\s*\[/FUNCTION_CALL\]', content)
            if match:
                func_call = match.group(1).strip()
                # Parse function_name(arg1=value1, arg2=value2)
                func_match = re.match(r'(\w+)\((.*)\)', func_call)
                if func_match:
                    func_name = func_match.group(1)
                    args_str = func_match.group(2)
                    # Parse args
                    args = {}
                    if args_str.strip():
                        for arg in args_str.split(','):
                            if '=' in arg:
                                key, value = arg.split('=', 1)
                                key = key.strip()
                                value = value.strip().strip('"\'')
                                # Convert to int if possible
                                try:
                                    value = int(value)
                                except:
                                    pass
                                args[key] = value

                    # Call function
                    if func_name == 'get_years':
                        result = get_years()
                    elif func_name == 'get_brands':
                        result = get_brands(args.get('year'))
                    elif func_name == 'get_models':
                        result = get_models(args.get('year'), args.get('brand'))
                    elif func_name == 'get_submodels':
                        result = get_submodels(args.get('model_id'))
                    elif func_name == 'get_parts':
                        result = get_parts(args.get('submodel_id'), args.get('part_type'))
                    else:
                        result = 'Unknown function'

                    # Format result
                    if func_name == 'get_years':
                        content = f"Available years: {', '.join(map(str, result))}"
                    elif func_name == 'get_brands':
                        content = f"Available brands: {result}"
                    elif func_name == 'get_models':
                        content = f"Available models: {result}"
                    elif func_name == 'get_submodels':
                        content = f"Available submodels: {result}"
                    elif func_name == 'get_parts':
                        content = f"Available parts: {result}"
                    else:
                        content = f"Function result: {json.dumps(result)}"

                    return jsonify({'response': content})

        # Use conversation flow system for enhanced responses (but keep it light)
        user_message = messages[-1]['content'] if messages else ""
        context = detect_conversation_context(user_message)
        print(f"DEBUG: Context detected: {context}")

        response_content = ai_message.get('content', '').strip()

        # Ensure we have valid content
        if not response_content or response_content.lower() in ['undefined', 'null', '']:
            response_content = "I'm here to help! How can I assist you today?"

        # Keep responses calm and brief - truncate if too long
        if len(response_content.split()) > 80:
            sentences = response_content.split('.')
            response_content = '.'.join(sentences[:2]).strip()
            if not response_content.endswith('.'):
                response_content += '.'

        # Remove any long lists or numbered items
        lines = response_content.split('\n')
        if len(lines) > 4:
            response_content = '\n'.join(lines[:3])

        # Skip conversation flow for problem_diagnosis to keep responses calm
        # Only use for quotation_request and only if response is already brief
        print(f"DEBUG: Context check - context: {context}, response length: {len(response_content.split())}")
        if context == 'quotation_request' and len(response_content.split()) < 30:
            # Initialize conversation state if not exists
            if 'conversation_state' not in globals():
                global conversation_state
                conversation_state = {
                    'current_step': None,
                    'variables': {},
                    'context': context
                }

            # Update context if changed
            if conversation_state.get('context') != context:
                conversation_state = {
                    'current_step': None,
                    'variables': {},
                    'context': context
                }

            # Advance conversation based on user input
            next_step, flow_response, updated_state = advance_conversation(
                context, conversation_state, user_message
            )

            conversation_state = updated_state

            # Add flow guidance only if it's very brief (just one question)
            if flow_response and len(flow_response.split('\n')) <= 2:
                response_content += f"\n\n{flow_response}"

        # Handle escalation (keep minimal)
        if should_escalate(context, user_message):
            escalation = get_escalation_action(context)
            response_content += f"\n\n{escalation['message']}"

        return jsonify({'response': response_content})
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500