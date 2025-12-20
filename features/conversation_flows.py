"""
Conversation Flow Matrix for Vehicle Glass Service Chat

This module defines dynamic conversation flows for different contexts.
Each context has:
- Keywords to detect intent
- Flow steps with transitions
- Variables collected during conversation
- Conditional branching logic
- Escalation paths
"""

CONVERSATION_FLOWS = {
    'competitive_positioning': {
        'keywords': ['big company', 'safelite', 'third party', 'claim administrator', 'why choose you', 'better than', 'vs', 'versus', 'comparison', 'competitor', 'other shop'],
        'description': 'Customer asking about competitive advantages over the big company or third party administrators',
        'initial_step': 'acknowledge_question',
        'business_intelligence_context': '''
        in the windshield replacement business, there is "the big company", we will call it "big company" or "the big company"; "big company" is a franchise type business that has service at national level, they have very low reviews compared to local shops, the do a lot of brand awareness and brand remembering advertising. "big company" employees usually might be entry level technicians who lack enough experience or might be being underpaid, those are some of the reasons "big company" has low reviews. Appointments at "big company" can take anywhere from days up to two weeks of wait to get the job done and their physical shop can take anywhere from 2 to 4 hours until the customer can drive their vehicle back.

        "big company" owns a sister company called "Safelite Solutions", unless strictly necessary to be very clear about them we will always call them "third party claim administrator" or "insurance third party claim administrator" or in a conversation where any of both previous names have been thrown "third party company"; Through this sister company, they manage and have almost absolute control over vehicle glass claims at national level with 97% of insurance companies. "third party company" has agents or representatives. When any customer calls an insurance company for an auto glass only claim, instead of directly talking with the insurance company they are redirected to the "third party claim administrator" and they are the ones who answer and an agent or representative registers "auto glass only claims", they record calls, most of the time they have somewhat step by step scripts that the agent will follow to register the policyholder auto glass only claims on behalf of the insurance companies. the third party company is not affiliated to the insurace company, Nevertheless "third party company" as sisters company with the "big company" they do have comingled interests where they on every chance they could, will send any customer they can to the "big company".

        known as fact but can directly mention: given the shared interests between both companies agents might be financially rewarded for turning or steering customers towards "big company", this steering if it happens can only happen under subtle cues given from the agent to the customer to persuade the customer to turn to the "big company" and might be like telling the customer phrases similar to: you have to go to a physical shop, the calibration of the windshield camera can only be performed on a physical shop, that if they dont go with the "big company" their repairs might not be covered under insurance or might not have warranty or they might have to pay hidden fees, these subtle cues have been said by agents to customers in a context where the call is not being recorded and the customer seems naive on how to the claim process works since the laws in florida dont allow insurance companies to decide for the customer which shop they will use to make the repairs.

        independent auto glass shops can also call and help insurance policyholders or policy listed drivers to register auto glass only claims. this is more effective for the customer since a reputable and well established local shop knows more than the customer about all details of the claim processes and will guide this process on regards of the best interest of the customer and to satisfy their needs also with a warranty so they can keep a good reputation and good reviews.
        ''',
        'variables': {
            'competitor_mentioned': None,  # big_company, third_party, other_local
            'customer_concern': None,  # price, timing, quality, insurance_steering
            'our_advantage_focus': None  # mobile_service, speed, warranty, local_expertise
        },
        'steps': {
            'acknowledge_question': {
                'message': 'I understand you\'re comparing options. We\'re a local, independent shop with great reviews and we can help explain the differences.',
                'transitions': {
                    'continue': 'explain_advantages'
                }
            },
            'explain_advantages': {
                'message': 'As a local independent shop, we offer mobile service (we come to you), same/next day scheduling, comprehensive warranty, and no hidden fees. We also guide you through insurance claims to ensure you get the best coverage.',
                'transitions': {
                    'ask_more': 'address_specific_concerns'
                }
            }
        }
    },
    'insurance_guidance': {
        'keywords': ['how do i file', 'how to file', 'file a claim', 'insurance claim process', 'third party administrator', 'safelite solutions', 'deductible amount', 'claim status', 'policy number'],
        'description': 'Customer seeking guidance on insurance claims and processes',
        'initial_step': 'assess_insurance_situation',
        'business_intelligence_context': '''
        people reaching out to us for service, we will call them "customers" can be policyholders or listed drivers or non listed relatives, just policyholders and listed drivers can register claims with the insurance.

        Customers doing claim by themselves:
        when customers claim insurance themselves, they arent really in-charge of their claim and their repairs, they are actually at mercy of the "third party company" and its agent, 99.99% of the time customers dont record calls thus on the call they are at mercy of the "third party company" agent and can be mislead or steered towards "big company", customers doing the claim process by themselves on the insurance app or webpage face incomplete claim process, total lack of guidance about repairs processes, and by being at mercy of "third party company" will be taken towards "big company" thus will be at mercy of their appointments timing, also getting a windshield replaced at a physical shop apart from being a hassle for the customer because of travel times to go and get back home also represent a problem if the customer or shop dont respect the drive away times causing defects and leaks on the instalation.

        why use insurance instead of customer paying themselves:
        in Florida any damage to the windshield can have a zero deductible replacement if the vehicle is insured with full coverage and or comprehensive coverage at the time of the damage, this means the whole replacement job including parts, labor and calibration is at no cost with the insurance.
        Florida Statute 627.7288 says Comprehensive coverage; deductible not to apply to motor vehicle glass.—The deductible provisions of any policy of motor vehicle insurance, delivered or issued in this state by an authorized insurer, providing comprehensive coverage or combined additional coverage shall not be applicable to damage to the windshield of any motor vehicle covered under such policy.
        other states insurance policies might have similar provisions or special auto glass coverage or reduced deductible for auto glass.
        Arizona, Kentucky, Massachusettsand South Carolina have all vehicle glass (windshield, side/back) replacement with no deductible applied, Full or Comprehensive coverage is required.
        Windshield claims fall under non-collision damage which insurers treat as low-risk events without surcharges, unlike at-fault accidents. No Fault Attribution: Since it's not driver error, it doesn't trigger the risk algorithms that adjust premiums for behavioral factors like speeding or collisions, Filing repeated glass claims in a short period may flag higher risk, leading to surcharges or non-renewal.
        ''',
        'variables': {
            'customer_type': None,  # policyholder, listed_driver, relative
            'insurance_coverage': None,  # comprehensive, collision, glass_only
            'claim_method': None,  # self_file, shop_assisted
            'state': 'florida'  # default to florida
        },
        'steps': {
            'assess_insurance_situation': {
                'message': 'I can help guide you through the insurance claim process. Are you the policyholder or a listed driver on the policy?',
                'transitions': {
                    'policyholder': 'explain_zero_deductible',
                    'listed_driver': 'explain_zero_deductible',
                    'relative': 'explain_eligibility'
                }
            },
            'explain_zero_deductible': {
                'message': 'In Florida, windshield replacement can be $0 out-of-pocket with comprehensive coverage under Florida Statute 627.7288. We can help you file the claim properly.',
                'transitions': {
                    'interested': 'offer_assistance'
                }
            }
        }
    },
    'repair_vs_replacement': {
        'keywords': ['repair or replace', 'should i repair', 'should i replace', 'repair vs replace', 'replacement vs repair', 'better to repair', 'better to replace', 'difference between repair', 'can you repair', 'is repair possible', 'repair my windshield', 'fix my crack'],
        'description': 'Customer asking about repair vs replacement options - guide toward replacement using calibrated questions and NEPQ approach',
        'initial_step': 'assess_damage_and_needs',
        'business_intelligence_context': '''
        why not windshield repair:
        windshield is part of the structure of the vehicle, repairs might be advertised as cheap solution to windsheild damage but reality is glass cant be cured with a glue to its original shape and strenght, a repair involves injecting a glue on the damage immediately after it happens, it must be immediate thus no dust impedes the glue from getting inside the crack, the glass may crack while injecting the glue due to pressure, when a crack has lines even if micro lines, this compromises the integrity and structure of the glass thus theres no real warranty it wont crack further tomorrow in the future
        the american national standard manual for Repair of Laminated Automotive Glass Standard on chapter 7 Repair Limitations mentions not to repair damage greater than 3/16 inch.

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
        ''',
        'variables': {
            'damage_type': None,  # crack, chip, shatter
            'damage_size': None,  # small, medium, large
            'customer_concerns': None,  # cost, time, warranty, safety
            'insurance_interest': None,  # yes, no, unsure
            'decision_stage': None  # exploring, considering, ready
        },
        'steps': {
            'assess_damage_and_needs': {
                'message': 'I\'d be happy to help you understand your options. What kind of damage are you dealing with on your windshield?',
                'transitions': {
                    'damage_described': 'explore_concerns_with_questions'
                },
                'negotiation_tactic': 'calibrated_questions'
            },
            'explore_concerns_with_questions': {
                'message': 'Thanks for sharing that. I\'m curious - what\'s most important to you when it comes to getting this fixed? Is it keeping costs down, having peace of mind with a warranty, or something else?',
                'transitions': {
                    'cost_concern': 'address_cost_with_evidence',
                    'warranty_concern': 'highlight_warranty_benefits',
                    'safety_concern': 'explain_structural_risks',
                    'time_concern': 'discuss_timeline_options',
                    'unsure': 'ask_problem_awareness_questions'
                },
                'negotiation_tactic': 'calibrated_questions'
            },
            'address_cost_with_evidence': {
                'message': 'I understand cost is a big factor. Have you considered that in Florida, windshield replacement can actually be $0 out-of-pocket with insurance? And while repairs might seem cheaper upfront, they often lead to more expensive problems down the road. What do you think about that?',
                'transitions': {
                    'interested_insurance': 'explore_insurance_path',
                    'still_cost_focused': 'ask_problem_awareness_questions'
                },
                'negotiation_tactic': 'evidence_based_framing'
            },
            'highlight_warranty_benefits': {
                'message': 'Peace of mind is so important. With our replacement service, you get a comprehensive warranty that covers the work for as long as you own the vehicle. Repairs typically don\'t come with any real warranty against future cracks. How does that sound to you?',
                'transitions': {
                    'interested_warranty': 'explain_our_warranty',
                    'still_unsure': 'ask_problem_awareness_questions'
                },
                'negotiation_tactic': 'value_framing'
            },
            'explain_structural_risks': {
                'message': 'Safety is absolutely the top priority. The windshield is part of your vehicle\'s structural integrity, and repairs can compromise that strength. Industry standards actually recommend against repairing damage over 3/16 inch. Have you thought about how important it is to have a windshield you can fully trust?',
                'transitions': {
                    'concerned_about_safety': 'emphasize_replacement_safety',
                    'still_unsure': 'ask_problem_awareness_questions'
                },
                'negotiation_tactic': 'problem_awareness'
            },
            'discuss_timeline_options': {
                'message': 'Time is valuable. We can often do replacements the same day or next day, and we come to you for mobile service. Repairs might seem faster, but they can lead to future issues that require more time later. What timeline works best for you?',
                'transitions': {
                    'needs_quick_service': 'offer_mobile_scheduling',
                    'can_wait': 'ask_problem_awareness_questions'
                },
                'negotiation_tactic': 'calibrated_questions'
            },
            'ask_problem_awareness_questions': {
                'message': 'I\'m curious - have you ever had a windshield repair that cracked further later? Or do you know anyone who\'s had that experience? What concerns you most about getting this resolved properly?',
                'transitions': {
                    'has_had_bad_experience': 'share_similar_stories',
                    'no_experience': 'explain_common_issues',
                    'still_exploring': 'guide_to_solution'
                },
                'negotiation_tactic': 'problem_awareness'
            },
            'explore_insurance_path': {
                'message': 'That\'s interesting you mentioned insurance. Are you the policyholder or listed driver? I ask because in Florida, windshield replacement can be completely covered at no cost to you.',
                'transitions': {
                    'policyholder': 'explain_zero_deductible',
                    'listed_driver': 'explain_zero_deductible',
                    'not_sure': 'ask_insurance_questions'
                },
                'negotiation_tactic': 'calibrated_questions'
            },
            'guide_to_solution': {
                'message': 'Based on what you\'ve shared, it sounds like replacement might give you the peace of mind you\'re looking for. Would you like me to help you explore that option, or is there anything specific you\'d like to know more about?',
                'transitions': {
                    'wants_to_explore': 'offer_next_steps',
                    'has_more_questions': 'answer_questions'
                },
                'negotiation_tactic': 'assumptive_close'
            }
        }
    },
    'quotation_request': {
        'keywords': ['quote', 'price', 'cost', 'how much', 'estimate', 'shopping', 'looking for', 'need', 'repair', 'replacement', 'service'],
        'description': 'Customer seeking price quotation for auto glass services',
        'initial_step': 'initial_greeting',
        'variables': {
            # Customer Intent Variables
            'primary_intent': None,  # immediate_cash, immediate_insurance, postponed_cash, postponed_insurance, just_looking, lower_price, afraid_insurance, not_matured, not_interested
            'urgency_level': 'normal',  # high, normal, low
            'price_sensitivity': 'medium',  # high, medium, low
            'insurance_readiness': None,  # ready, afraid, unsure, not_available

            # Vehicle Variables
            'service_type': None,  # repair, replacement, inspection
            'year': None,
            'make': None,
            'model': None,
            'submodel': None,
            'vin': None,

            # Service Variables
            'part_type': None,  # windshield, window, mirror, etc.
            'damage_type': None,  # crack, chip, shattered, leak
            'damage_severity': None,  # small, medium, large
            'damage_location': None,

            # Logistics Variables
            'location': None,
            'preferred_time': None,
            'mobile_service_needed': None,

            # Payment Variables
            'payment_form': None,  # insurance, cash, financing
            'insurance_company': None,
            'policy_number': None,
            'deductible_amount': None,
            'coverage_type': None,  # comprehensive, collision, glass_coverage

            # Business Logic Variables
            'vehicle_eligible': None,  # True/False based on year constraint
            'estimated_profitability': None,  # high, medium, low
            'recommended_payment': None,  # insurance_preferred, cash_ok
            'quote_amount': None,
            'customer_temperature': None  # hot, warm, cold (sales readiness)
        },
        'steps': {
            'initial_greeting': {
                'message': 'Hi! Thanks for reaching out about auto glass services. I understand you\'re looking for a quote. To give you the most accurate pricing, I\'ll need to ask a few questions about your vehicle and the damage.',
                'type': 'greeting',
                'transitions': {
                    'acknowledged': 'assess_primary_intent'
                },
                'negotiation_tactic': 'build_rapport'
            },

            'assess_primary_intent': {
                'message': 'What brings you in today? Are you looking to get something fixed, or just gathering some information?',
                'questions': [
                    'What are you hoping to accomplish today?'
                ],
                'intent_detection': {
                    'immediate_keywords': ['today', 'tomorrow', 'soon', 'urgent', 'asap', 'now'],
                    'insurance_keywords': ['insurance', 'claim', 'policy', 'adjuster'],
                    'price_shopping_keywords': ['cheapest', 'lowest price', 'compare', 'shopping around', 'best deal'],
                    'afraid_insurance_keywords': ['scared', 'worried', 'afraid', 'deductible', 'premium increase']
                },
                'transitions': {
                    'immediate_cash': 'gather_vehicle_basics',
                    'immediate_insurance': 'assess_insurance_readiness',
                    'postponed_cash': 'understand_timeline',
                    'postponed_insurance': 'assess_insurance_readiness',
                    'just_looking': 'gather_vehicle_basics',  # Changed to gather basics even for just looking
                    'lower_price_focus': 'gather_vehicle_basics',  # Need info first before addressing price
                    'afraid_insurance': 'gather_vehicle_basics',  # Need vehicle info first
                    'unclear': 'clarify_intent'
                },
                'variable_updates': ['primary_intent', 'urgency_level', 'price_sensitivity'],
                'negotiation_tactic': 'calibrated_questions'
            },

            'gather_vehicle_basics': {
                'message': 'Great! Let me get some basic information about your vehicle so I can provide an accurate quote.',
                'questions': [
                    'What year, make, and model is your vehicle?',
                    'What type of damage are we dealing with? (crack, chip, shattered glass, leak?)',
                    'Where is the damage located?'
                ],
                'required_vars': ['year', 'make', 'model', 'damage_type'],
                'variable_mapping': {
                    'year': r'\b(19\d{2}|20\d{2})\b',  # Fixed regex to capture full year
                    'make': None,  # Use extraction function
                    'model': None,  # Use extraction function
                    'damage_type': r'\b(crack|chip|shattered|broken|leak|damage)\b'
                },
                'transitions': {
                    'complete': 'check_vehicle_eligibility',
                    'incomplete': 'gather_vehicle_basics'
                },
                'actions': ['validate_vehicle_year'],
                'negotiation_tactic': 'mirroring'
            },

            'check_vehicle_eligibility': {
                'action': 'assess_eligibility',
                'conditions': {
                    'year_too_old': 'year < 2003',
                    'year_eligible_insurance': 'year >= 2018',  # Likely has comprehensive coverage
                    'standard_eligible': 'year >= 2003'
                },
                'responses': {
                    'year_too_old': 'I appreciate you reaching out, but we specialize in vehicles from 2003 and newer. For older vehicles, you might want to check with a general auto body shop.',
                    'year_eligible_insurance': 'Perfect! Vehicles from {year} typically have comprehensive coverage that includes glass damage.',
                    'standard_eligible': 'Your {year} {make} {model} is eligible for our services.'
                },
                'transitions': {
                    'eligible': 'assess_damage_severity',
                    'not_eligible': 'end_conversation',
                    'eligible_with_insurance_upsell': 'explain_insurance_benefits'
                },
                'negotiation_tactic': 'negative_framing'
            },

            'assess_damage_severity': {
                'message': 'Thanks for that information. Now let me understand the extent of the damage to give you the right solution.',
                'questions': [
                    'How big is the damage? (size of a quarter, palm-sized, etc.)',
                    'Is it in your line of sight while driving?',
                    'Has it gotten worse over time?'
                ],
                'transitions': {
                    'repair_eligible': 'provide_repair_quote',
                    'replacement_needed': 'provide_replacement_quote',
                    'needs_inspection': 'schedule_inspection'
                },
                'variable_updates': ['damage_severity', 'damage_location'],
                'negotiation_tactic': 'calibrated_questions'
            },

            'assess_insurance_readiness': {
                'message': 'Insurance can often cover glass damage completely. Let me help you understand your options.',
                'questions': [
                    'Which insurance company do you have?',
                    'Do you know if you have glass coverage or comprehensive coverage?',
                    'Have you filed a claim before?'
                ],
                'transitions': {
                    'insurance_ready': 'gather_policy_details',
                    'insurance_afraid': 'address_insurance_fears',
                    'insurance_unclear': 'explain_insurance_benefits',
                    'no_insurance': 'discuss_payment_options'
                },
                'negotiation_tactic': 'labeling_emotions'
            },

            'address_insurance_fears': {
                'message': 'I understand concerns about using insurance - many customers feel the same way initially.',
                'objection_handling': {
                    'deductible_concern': 'Many policies have $0 deductible for glass damage, and even if there\'s a deductible, it\'s often less than paying cash.',
                    'premium_increase': 'Glass claims typically don\'t affect your premium rates since they\'re separate from at-fault accidents.',
                    'claim_process': 'We handle the entire claim process for you - you just bring your vehicle in.'
                },
                'transitions': {
                    'fear_addressed': 'gather_policy_details',
                    'still_concerned': 'provide_cash_quote_alternative',
                    'need_more_info': 'explain_insurance_process'
                },
                'negotiation_tactic': 'address_objections'
            },

            'provide_repair_quote': {
                'action': 'calculate_repair_quote',
                'message': 'Based on what you\'ve described, this looks like a repair rather than replacement. For a {damage_severity} {damage_type} in a {year} {make} {model}, our repair quote would be ${quote_amount}.',
                'payment_options': {
                    'insurance': 'With insurance, this is typically $0 out of pocket.',
                    'cash': 'Cash price: ${quote_amount}',
                    'financing': 'Available financing options starting at ${monthly_payment}/month'
                },
                'transitions': {
                    'interested_insurance': 'schedule_claim_service',
                    'interested_cash': 'schedule_cash_service',
                    'price_too_high': 'handle_price_objection',
                    'need_time_to_decide': 'provide_takeaway_info'
                },
                'negotiation_tactic': 'provide_options'
            },

            'handle_price_objection': {
                'message': 'I understand price is important. Let me share why our service provides excellent value.',
                'value_propositions': [
                    'Lifetime warranty on repairs',
                    'Mobile service available',
                    'Faster than dealership service',
                    'Certified technicians with insurance training'
                ],
                'transitions': {
                    'value_recognized': 'schedule_service',
                    'still_concerned': 'offer_competitive_alternative',
                    'not_interested': 'end_positive'
                },
                'negotiation_tactic': 'value_framing'
            },

            'schedule_service': {
                'message': 'Excellent! Let\'s get this scheduled for you.',
                'questions': [
                    'What location works best for you?',
                    'What day/time works for your schedule?',
                    'Do you prefer mobile service or coming to our shop?'
                ],
                'transitions': {
                    'scheduled': 'confirm_appointment',
                    'need_different_time': 'find_alternative_slot'
                },
                'actions': ['book_appointment', 'send_confirmation'],
                'negotiation_tactic': 'create_scarcity'
            },

            'end_conversation': {
                'message': 'Thank you for considering our services. If your needs change or you have questions about older vehicles, feel free to reach out.',
                'type': 'closure',
                'actions': ['log_lost_lead'],
                'negotiation_tactic': 'positive_closing'
            },

            'understand_timeline': {
                'message': 'I understand you\'re not in a rush. When would be a good time for you to get this taken care of?',
                'questions': [
                    'What timeframe are you thinking?',
                    'Do you have any upcoming plans that might affect scheduling?'
                ],
                'transitions': {
                    'timeline_provided': 'gather_vehicle_basics',
                    'still_unclear': 'provide_general_info'
                },
                'negotiation_tactic': 'calibrated_questions'
            },

            'clarify_intent': {
                'message': 'I want to make sure I understand what you\'re looking for so I can give you the best service.',
                'questions': [
                    'Are you looking to get this repaired soon, or just gathering information?',
                    'Do you have insurance that might cover this?',
                    'What\'s most important to you - speed, price, or quality?'
                ],
                'transitions': {
                    'clarified': 'gather_vehicle_basics',
                    'still_unclear': 'provide_general_info'
                },
                'negotiation_tactic': 'calibrated_questions'
            },

            'provide_general_info': {
                'message': 'We specialize in auto glass repair and replacement. Our services include windshield repair, windshield replacement, and mobile service.',
                'questions': [
                    'What type of service are you interested in?',
                    'Do you have details about your vehicle?'
                ],
                'transitions': {
                    'interested': 'gather_vehicle_basics',
                    'not_interested': 'end_conversation'
                },
                'negotiation_tactic': 'providing_value'
            },

            'explain_insurance_benefits': {
                'message': 'For vehicles {year} and newer, you likely have comprehensive coverage that includes glass damage. This often means $0 out of pocket for you.',
                'questions': [
                    'Have you filed a glass claim before?',
                    'Do you know if your policy has a glass deductible?'
                ],
                'transitions': {
                    'interested_insurance': 'gather_policy_details',
                    'still_concerned': 'address_insurance_fears',
                    'prefer_cash': 'provide_cash_quote'
                },
                'negotiation_tactic': 'value_framing'
            },

            'gather_policy_details': {
                'message': 'To help with your insurance claim, I\'ll need some policy information.',
                'questions': [
                    'What insurance company do you have?',
                    'What\'s your policy number?',
                    'Do you know your deductible amount?'
                ],
                'required_vars': ['insurance_company', 'policy_number'],
                'transitions': {
                    'complete': 'provide_insurance_quote',
                    'incomplete': 'gather_policy_details'
                },
                'negotiation_tactic': 'building_rapport'
            },

            'provide_insurance_quote': {
                'message': 'Based on your {year} {make} {model} with {damage_severity} {damage_type}, your insurance claim should cover this completely.',
                'transitions': {
                    'interested': 'schedule_claim_service',
                    'have_questions': 'answer_insurance_questions'
                },
                'negotiation_tactic': 'creating_scarcity'
            },

            'schedule_claim_service': {
                'message': 'Great! We can schedule your insurance claim service. We\'ll handle everything with your adjuster.',
                'questions': [
                    'What location works best?',
                    'What day/time works for the adjuster appointment?'
                ],
                'transitions': {
                    'scheduled': 'confirm_appointment',
                    'need_different_time': 'find_alternative_slot'
                },
                'actions': ['schedule_with_adjuster', 'send_confirmation'],
                'negotiation_tactic': 'creating_urgency'
            },

            'schedule_cash_service': {
                'message': 'Perfect! Let\'s get your cash service scheduled.',
                'questions': [
                    'What location works best for you?',
                    'What day/time works for your schedule?'
                ],
                'transitions': {
                    'scheduled': 'confirm_appointment',
                    'need_different_time': 'find_alternative_slot'
                },
                'actions': ['book_appointment', 'send_confirmation'],
                'negotiation_tactic': 'creating_scarcity'
            },

            'confirm_appointment': {
                'message': 'Your appointment is confirmed for {appointment_date} at {appointment_time}. We\'ll send you a confirmation text with details.',
                'type': 'closure',
                'actions': ['send_confirmation_sms', 'log_booking'],
                'negotiation_tactic': 'positive_closing'
            },

            'find_alternative_slot': {
                'message': 'Let me check our availability for other times.',
                'transitions': {
                    'alternative_found': 'confirm_appointment',
                    'no_alternatives': 'provide_takeaway_info'
                },
                'negotiation_tactic': 'problem_solving'
            },

            'provide_takeaway_info': {
                'message': 'I understand you need more time to decide. Here\'s what you can expect with our service.',
                'value_points': [
                    'Lifetime warranty on repairs',
                    'Mobile service available',
                    'Same-day service for most repairs',
                    'Insurance claim assistance'
                ],
                'transitions': {
                    'ready_to_book': 'schedule_service',
                    'still_not_ready': 'end_positive'
                },
                'negotiation_tactic': 'providing_social_proof'
            },

            'end_positive': {
                'message': 'Thank you for your interest in our services. Feel free to reach out anytime you\'re ready.',
                'type': 'closure',
                'actions': ['log_warm_lead'],
                'negotiation_tactic': 'positive_closing'
            },

            'offer_competitive_alternative': {
                'message': 'While we pride ourselves on quality service, I understand you\'re looking for the best value.',
                'transitions': {
                    'interested_in_alternative': 'schedule_service',
                    'still_not_interested': 'end_positive'
                },
                'negotiation_tactic': 'value_framing'
            },

            'provide_cash_quote': {
                'message': 'For cash payment on your {year} {make} {model}, our price would be ${quote_amount}.',
                'payment_options': [
                    'Full payment due at service',
                    'Financing available through approved partners'
                ],
                'transitions': {
                    'interested': 'schedule_cash_service',
                    'price_too_high': 'handle_price_objection',
                    'need_time': 'provide_takeaway_info'
                },
                'negotiation_tactic': 'transparency'
            },

            'answer_insurance_questions': {
                'message': 'I\'d be happy to answer your insurance questions.',
                'transitions': {
                    'questions_answered': 'schedule_claim_service',
                    'still_concerned': 'provide_cash_quote'
                },
                'negotiation_tactic': 'building_credibility'
            },

            'explain_insurance_process': {
                'message': 'Here\'s how the insurance process works with us.',
                'process_steps': [
                    'We inspect and document the damage',
                    'We submit the claim to your insurance',
                    'Your adjuster approves the work',
                    'We repair/replace your glass',
                    'You pay only your deductible (often $0 for glass)'
                ],
                'transitions': {
                    'process_understood': 'gather_policy_details',
                    'still_afraid': 'address_insurance_fears'
                },
                'negotiation_tactic': 'reducing_uncertainty'
            }
        },
        'escalation_triggers': ['emergency', 'safety', 'immediate'],
        'escalation_action': 'prioritize_scheduling'
    },

    'parts_lookup': {
        'keywords': ['find', 'windshield', 'parabrisas', 'part', 'replacement', 'glass'],
        'description': 'Customer wants to find specific parts',
        'initial_step': 'gather_vehicle_info',
        'variables': {
            'year': None,
            'brand': None,
            'model': None,
            'submodel': None,
            'part_type': 'windshield',  # default
            'urgency_level': 'normal'
        },
        'steps': {
            'gather_vehicle_info': {
                'message': 'To find the right parts, I need some information about your vehicle.',
                'questions': [
                    'What year is your vehicle?',
                    'What make/brand is it?',
                    'What model is it?'
                ],
                'required_vars': ['year', 'brand', 'model'],
                'transitions': {
                    'complete': 'check_submodels',
                    'incomplete': 'gather_vehicle_info'
                },
                'variable_mapping': {
                    'year': r'(\d{4})',
                    'brand': None,  # Will be extracted from text
                    'model': None   # Will be extracted from text
                }
            },
            'check_submodels': {
                'action': 'query_submodels',
                'transitions': {
                    'single': 'show_parts',
                    'multiple': 'select_submodel',
                    'none': 'no_parts_found'
                }
            },
            'select_submodel': {
                'message': 'I found multiple versions of your {year} {brand} {model}. Please specify which one: {submodel_options}',
                'expected_input': 'submodel_selection',
                'transitions': {
                    'selected': 'show_parts',
                    'invalid': 'select_submodel'
                }
            },
            'show_parts': {
                'action': 'query_parts',
                'message': 'I found the following {part_type} parts for your {year} {brand} {model}:\n{parts_list}',
                'transitions': {
                    'success': 'offer_services',
                    'no_parts': 'no_parts_found'
                }
            },
            'offer_services': {
                'message': 'Would you like us to install this part, or do you prefer to do it yourself?',
                'options': ['installation', 'diy', 'not_sure'],
                'transitions': {
                    'installation': 'schedule_installation',
                    'diy': 'provide_instructions',
                    'not_sure': 'explain_options'
                }
            },
            'schedule_installation': {
                'message': 'Great! We can schedule professional installation. We also offer mobile service.',
                'questions': ['What\'s your preferred date/time?', 'Do you need mobile service?'],
                'transitions': {
                    'scheduled': 'confirm_booking',
                    'need_more_info': 'schedule_installation'
                }
            },
            'provide_instructions': {
                'message': 'For DIY installation, here are the general steps...',
                'transitions': {
                    'understood': 'offer_warranty',
                    'need_help': 'recommend_professional'
                }
            },
            'no_parts_found': {
                'message': 'I couldn\'t find exact matches, but here are some alternatives...',
                'transitions': {
                    'interested': 'show_alternatives',
                    'not_interested': 'offer_custom_quote'
                }
            }
        },
        'escalation_triggers': ['urgent', 'emergency', 'cracked', 'broken'],
        'escalation_action': 'emergency_flow'
    },

    'service_inquiry': {
        'keywords': ['repair', 'fix', 'service', 'installation', 'mobile', 'shop'],
        'description': 'Questions about services offered',
        'initial_step': 'identify_service_type',
        'variables': {
            'service_type': None,
            'urgency_level': 'normal',
            'location_preference': None
        },
        'steps': {
            'identify_service_type': {
                'message': 'I can help you with various auto glass services. What type of service are you interested in?',
                'options': ['windshield_repair', 'windshield_replacement', 'window_repair', 'mobile_service', 'general_info'],
                'transitions': {
                    'windshield_repair': 'explain_repair_process',
                    'windshield_replacement': 'explain_replacement_process',
                    'window_repair': 'diagnose_window_issue',
                    'mobile_service': 'explain_mobile_service',
                    'general_info': 'provide_service_overview'
                }
            },
            'explain_repair_process': {
                'message': 'Windshield repair can fix small chips and cracks. The process takes about 30 minutes.',
                'questions': ['How big is the damage?', 'Where is it located?'],
                'transitions': {
                    'eligible': 'schedule_repair',
                    'not_eligible': 'recommend_replacement'
                }
            },
            'schedule_repair': {
                'message': 'Great! We can repair that. Would you like mobile service or to come to our shop?',
                'transitions': {
                    'mobile': 'collect_location',
                    'shop': 'schedule_appointment'
                }
            }
        },
        'escalation_triggers': [],
        'escalation_action': 'schedule_appointment'
    },

    'problem_diagnosis': {
        'keywords': ['stuck', 'leak', 'noise', 'crack', 'chip', 'broken', 'won\'t work'],
        'description': 'Customer describing a vehicle problem',
        'initial_step': 'gather_problem_details',
        'variables': {
            'problem_type': None,
            'severity': None,
            'affected_parts': [],
            'symptoms': []
        },
        'steps': {
            'gather_problem_details': {
                'message': 'I\'m sorry to hear you\'re having issues. We can help figure this out.',
                'questions': [
                    'Can you tell me a bit more about what\'s happening?'
                ],
                'required_vars': ['problem_description'],
                'transitions': {
                    'window_issue': 'diagnose_window',
                    'windshield_issue': 'diagnose_windshield',
                    'leak_issue': 'diagnose_leak',
                    'unclear': 'ask_more_details'
                }
            },
            'diagnose_window': {
                'message': 'Window problems can have several causes. Let me ask a few questions to narrow it down.',
                'questions': [
                    'Is it electric or manual?',
                    'Does the window move at all?',
                    'Do you hear any unusual noises?'
                ],
                'transitions': {
                    'regulator_issue': 'recommend_regulator_repair',
                    'motor_issue': 'recommend_motor_replacement',
                    'switch_issue': 'recommend_switch_replacement'
                }
            },
            'diagnose_windshield': {
                'message': 'For windshield issues, the solution depends on the damage type and location.',
                'transitions': {
                    'small_crack': 'offer_repair',
                    'large_damage': 'recommend_replacement',
                    'edge_damage': 'recommend_replacement'
                }
            }
        },
        'escalation_triggers': ['safety', 'driving', 'emergency'],
        'escalation_action': 'immediate_assistance'
    },

    'insurance_claim': {
        'keywords': ['insurance', 'claim', 'policy', 'coverage', 'deductible', 'adjuster'],
        'description': 'Insurance-related questions or claims',
        'initial_step': 'gather_insurance_info',
        'variables': {
            'insurance_company': None,
            'policy_number': None,
            'claim_number': None,
            'adjuster_name': None,
            'deductible_amount': None
        },
        'steps': {
            'gather_insurance_info': {
                'message': 'I can help you with your insurance claim. We work with all major insurance companies.',
                'questions': [
                    'Which insurance company do you have?',
                    'Do you have a claim number already?',
                    'What\'s your policy number?'
                ],
                'required_vars': ['insurance_company'],
                'transitions': {
                    'has_claim': 'verify_claim_details',
                    'no_claim': 'help_file_claim',
                    'unsure': 'explain_process'
                }
            },
            'verify_claim_details': {
                'message': 'Let me verify your claim details and see what\'s covered.',
                'action': 'check_coverage',
                'transitions': {
                    'approved': 'schedule_work',
                    'pending': 'follow_up_needed',
                    'denied': 'appeal_assistance'
                }
            },
            'help_file_claim': {
                'message': 'I can help you file a claim. We\'ll need photos of the damage and some basic information.',
                'questions': ['Can you describe the incident?', 'Do you have photos?'],
                'transitions': {
                    'ready_to_file': 'file_claim',
                    'need_more_info': 'gather_incident_details'
                }
            }
        },
        'escalation_triggers': [],
        'escalation_action': 'insurance_specialist'
    },

    'emergency_situation': {
        'keywords': ['emergency', 'urgent', 'immediate', 'safety', 'dangerous', 'can\'t drive'],
        'description': 'Urgent safety-related situations',
        'initial_step': 'assess_situation',
        'variables': {
            'location': None,
            'vehicle_driveable': None,
            'safety_risk': None,
            'emergency_type': None
        },
        'steps': {
            'assess_situation': {
                'message': 'I understand this is an emergency. Your safety is our top priority.',
                'questions': [
                    'What is your current location?',
                    'Is your vehicle safe to drive?',
                    'What type of emergency are you facing?'
                ],
                'required_vars': ['location'],
                'transitions': {
                    'driveable': 'dispatch_mobile_unit',
                    'not_driveable': 'arrange_towing',
                    'safety_risk': 'contact_emergency_services'
                }
            },
            'dispatch_mobile_unit': {
                'message': 'I\'m dispatching our emergency mobile unit to your location.',
                'action': 'emergency_dispatch',
                'transitions': {
                    'dispatched': 'provide_eta',
                    'no_units': 'alternative_arrangement'
                }
            },
            'arrange_towing': {
                'message': 'Since your vehicle isn\'t driveable, I\'ll arrange towing to our facility.',
                'transitions': {
                    'towing_arranged': 'schedule_repair',
                    'towing_unavailable': 'alternative_transport'
                }
            }
        },
        'escalation_triggers': ['accident', 'injury', 'hazard'],
        'escalation_action': 'emergency_services'
    }
}

RESPONSE_TEMPLATES = {
    'parts_search': {
        'success': 'I found the following {part_type} parts for your {year} {brand} {model}:\\n{parts_list}',
        'no_results': 'I couldn\'t find {part_type} parts for your {year} {brand} {model}. Let me check if we have alternatives.',
        'multiple_submodels': 'I found multiple versions of your {year} {brand} {model}. Please specify which submodel: {submodels_list}',
        'need_more_info': 'To find the right parts, I need: year, make, and model of your vehicle.'
    },

    'service_explanation': {
        'windshield_repair': 'We offer professional windshield repair and replacement services. Our certified technicians use OEM-quality glass and materials.',
        'mobile_service': 'We provide mobile windshield service - we come to your location for repairs and replacements.',
        'window_regulator': 'We repair and replace window regulators, motors, and switches for all vehicle types.',
        'leak_repair': 'Our leak detection and repair service includes weatherstripping replacement and sealant work.'
    },

    'problem_assessment': {
        'stuck_window': 'Window issues can be caused by regulator failure, motor problems, or switch malfunction. We can diagnose and repair this.',
        'windshield_crack': 'For windshield cracks, we can often repair rather than replace, depending on size and location.',
        'leak_diagnosis': 'Leaks can originate from weatherstripping, windshield seals, or window frames. We\'ll inspect and fix the source.'
    },

    'insurance_process': {
        'claim_guidance': 'We work with all major insurance companies. For claims, we\'ll need your policy information and can help file or process claims.',
        'deductible_info': 'Insurance typically covers the full cost minus your deductible. We\'ll work with your adjuster to minimize your out-of-pocket expense.',
        'adjuster_contact': 'We can contact your insurance adjuster directly, or you can provide us with your claim number to get started.'
    },

    'emergency_protocol': {
        'immediate_response': 'For safety concerns, please pull over to a safe location. We offer emergency mobile service 24/7.',
        'location_request': 'To send immediate assistance, please share your current location or nearest landmark.',
        'safety_first': 'Your safety is our priority. Do not attempt to drive if visibility is compromised.'
    }
}

ESCALATION_PATHS = {
    'schedule_emergency': {
        'action': 'immediate_scheduling',
        'message': 'This sounds urgent. Let me connect you with our emergency scheduling team.',
        'contact': 'emergency_line'
    },

    'schedule_appointment': {
        'action': 'appointment_booking',
        'message': 'Would you like me to help you schedule an appointment?',
        'contact': 'scheduling_system'
    },

    'immediate_assistance': {
        'action': 'emergency_dispatch',
        'message': 'For safety issues, we\'re dispatching immediate assistance.',
        'contact': 'emergency_services'
    },

    'insurance_specialist': {
        'action': 'specialist_transfer',
        'message': 'Let me connect you with our insurance claims specialist.',
        'contact': 'insurance_department'
    },

    'electrical_specialist': {
        'action': 'specialist_transfer',
        'message': 'This may require electrical system expertise. Let me connect you with a specialist.',
        'contact': 'electrical_tech'
    },

    'customer_service': {
        'action': 'general_support',
        'message': 'Let me transfer you to our customer service team for detailed assistance.',
        'contact': 'customer_service'
    },

    'emergency_services': {
        'action': 'emergency_response',
        'message': 'Activating emergency response protocol.',
        'contact': 'emergency_coordinator'
    }
}

def detect_conversation_context(user_message):
    """
    Analyze user message to determine conversation context
    Returns the most likely context based on keyword matching and priority
    """
    user_lower = user_message.lower()

    # Priority order for context detection (most specific to general)
    priority_contexts = [
        'emergency_situation',
        'repair_vs_replacement',
        'competitive_positioning',
        'insurance_guidance',
        'quotation_request',
        'problem_diagnosis',
        'service_inquiry'
    ]

    # Check priority contexts first
    for context_name in priority_contexts:
        if context_name in CONVERSATION_FLOWS:
            context_data = CONVERSATION_FLOWS[context_name]
            keywords = context_data.get('keywords', [])
            if any(keyword in user_lower for keyword in keywords):
                return context_name

    # Check remaining contexts
    for context_name, context_data in CONVERSATION_FLOWS.items():
        if context_name not in priority_contexts:
            keywords = context_data.get('keywords', [])
            if any(keyword in user_lower for keyword in keywords):
                return context_name

    return 'general_inquiry'

def get_context_flow(context):
    """Get the conversation flow for a given context"""
    return CONVERSATION_FLOWS.get(context, CONVERSATION_FLOWS.get('general_inquiry'))

def get_current_step(context, conversation_state):
    """Get the current step in the conversation flow"""
    flow = get_context_flow(context)
    current_step_id = conversation_state.get('current_step', flow.get('initial_step'))
    return flow['steps'].get(current_step_id)

def advance_conversation(context, conversation_state, user_input):
    """
    Process user input and advance the conversation flow
    Returns: (next_step, response_message, updated_variables)
    """
    flow = get_context_flow(context)
    if not flow:
        return None, "I'm not sure how to proceed. Let me connect you with a specialist.", conversation_state

    # Initialize current step if not set
    if not conversation_state.get('current_step'):
        conversation_state['current_step'] = flow.get('initial_step')

    current_step_id = conversation_state['current_step']
    current_step = flow['steps'].get(current_step_id)

    if not current_step:
        return None, "I'm not sure how to proceed. Let me connect you with a specialist.", conversation_state

    # Initialize variables if not exists
    if 'variables' not in conversation_state:
        conversation_state['variables'] = flow.get('variables', {}).copy()

    # Process user input based on step configuration
    variables = conversation_state['variables']

    # Store current step name for logic processing
    variables['current_step_name'] = current_step_id

    # Extract variables from user input
    variables = extract_variables(current_step, user_input, variables)

    # For quotation_request, determine next step based on current state
    if context == 'quotation_request':
        next_step = determine_quotation_next_step(current_step, variables, user_input)
    elif context == 'repair_vs_replacement':
        next_step = determine_repair_replacement_next_step(current_step, variables, user_input)
    else:
        next_step = determine_next_step(current_step, variables, user_input)

    # Get the next step configuration for response generation
    next_step_config = flow['steps'].get(next_step)
    if next_step_config:
        response = generate_step_response(next_step_config, variables)
    else:
        response = "I'm not sure how to proceed. Let me connect you with a specialist."

    conversation_state['current_step'] = next_step
    conversation_state['variables'] = variables

    return next_step, response, conversation_state

def determine_next_step(current_step, variables, user_input):
    """Determine the next step based on current step configuration and user input"""
    transitions = current_step.get('transitions', {})
    context = variables.get('context', '')

    # Special handling for quotation_request context
    if context == 'quotation_request':
        return determine_quotation_next_step(current_step, variables, user_input)

    # Check for action-based transitions
    action = current_step.get('action')
    if action:
        if action == 'query_submodels':
            # Simulate submodel query logic
            submodels = ['sedan', 'hatchback']  # This would be actual database query
            if len(submodels) > 1:
                return transitions.get('multiple', 'end')
            elif len(submodels) == 1:
                return transitions.get('single', 'end')
            else:
                return transitions.get('none', 'end')
        elif action == 'query_parts':
            # Simulate parts query
            parts = ['part1', 'part2']  # This would be actual database query
            if parts:
                return transitions.get('success', 'end')
            else:
                return transitions.get('no_parts', 'end')

    # Check for choice-based transitions
    options = current_step.get('options', [])
    if options:
        choice = identify_choice(user_input, options)
        if choice and choice in transitions:
            return transitions[choice]

    # Check for variable-based transitions
    required_vars = current_step.get('required_vars', [])
    if required_vars and all(variables.get(var) for var in required_vars):
        return transitions.get('complete', 'end')

    # Default transitions
    if 'next_step' in current_step:
        return current_step['next_step']

    return 'end'

def determine_quotation_next_step(current_step, variables, user_input):
    """Determine next step for quotation_request context with business logic"""
    # Get step ID from variables context or assume based on current step
    current_step_name = variables.get('current_step_name', '')

    # If no step name in variables, infer from current step content
    if not current_step_name:
        step_message = current_step.get('message', '').lower()
        if 'initial_greeting' in step_message or 'thanks for reaching out' in step_message:
            current_step_name = 'initial_greeting'
        elif 'assess_primary_intent' in step_message or 'what you\'re looking for' in step_message:
            current_step_name = 'assess_primary_intent'
        elif 'gather_vehicle_basics' in step_message or 'basic information about your vehicle' in step_message:
            current_step_name = 'gather_vehicle_basics'

    transitions = current_step.get('transitions', {})

    # Step-specific logic
    if current_step_name == 'initial_greeting':
        # After greeting, always move to assess intent
        return 'assess_primary_intent'

    elif current_step_name == 'assess_primary_intent':
        intent = variables.get('primary_intent')
        if intent in ['immediate_cash', 'immediate_insurance']:
            return 'gather_vehicle_basics'
        elif intent in ['postponed_cash', 'postponed_insurance']:
            return 'understand_timeline'
        elif intent == 'just_looking':
            return 'provide_general_info'
        elif intent == 'lower_price':
            return 'address_price_concerns'
        elif intent == 'afraid_insurance':
            return 'address_insurance_fears'
        else:
            return 'clarify_intent'

    elif current_step_name == 'check_vehicle_eligibility':
        year_str = variables.get('year')
        year = int(year_str) if year_str and year_str.isdigit() else None

        if year and year < 2003:
            return 'end_conversation'
        elif year and year >= 2018:  # Likely has comprehensive coverage
            return 'explain_insurance_benefits'
        else:
            return 'assess_damage_severity'

    elif current_step_name == 'assess_damage_severity':
        damage_type = variables.get('damage_type', '')
        damage_severity = variables.get('damage_severity', '')

        # Business logic for repair vs replacement
        if damage_type in ['crack', 'chip'] and damage_severity in ['small', 'medium']:
            return 'provide_repair_quote'
        else:
            return 'provide_replacement_quote'

    elif current_step_name == 'assess_insurance_readiness':
        intent = variables.get('primary_intent', '')
        insurance_readiness = variables.get('insurance_readiness')

        if 'insurance' in intent:
            return 'gather_policy_details'
        elif insurance_readiness == 'afraid':
            return 'address_insurance_fears'
        elif insurance_readiness == 'unsure':
            return 'explain_insurance_benefits'
        else:
            return 'discuss_payment_options'

    elif current_step_name in ['provide_repair_quote', 'provide_replacement_quote']:
        # Analyze user response for buying signals
        user_lower = user_input.lower()
        buying_signals = ['yes', 'okay', 'sure', 'that works', 'book it', 'schedule', 'when can you']
        price_concerns = ['expensive', 'too much', 'cheaper', 'lower price', 'discount']

        if any(signal in user_lower for signal in buying_signals):
            payment_form = variables.get('payment_form', 'cash')
            if payment_form == 'insurance':
                return 'schedule_claim_service'
            else:
                return 'schedule_cash_service'
        elif any(concern in user_lower for concern in price_concerns):
            return 'handle_price_objection'
        else:
            return 'provide_takeaway_info'

    elif current_step_name == 'handle_price_objection':
        # Check if customer acknowledges value or still concerned
        user_lower = user_input.lower()
        value_acknowledgment = ['makes sense', 'understand', 'worth it', 'okay', 'book it']
        still_concerned = ['still expensive', 'can you do better', 'cheaper elsewhere']

        if any(ack in user_lower for ack in value_acknowledgment):
            return 'schedule_service'
        elif any(concern in user_lower for concern in still_concerned):
            return 'offer_competitive_alternative'
        else:
            return 'end_positive'

    elif current_step_name == 'address_insurance_fears':
        # Check if fears are addressed
        user_lower = user_input.lower()
        addressed_signals = ['okay', 'makes sense', 'i understand', 'let\'s do insurance', 'file claim']
        still_afraid = ['still worried', 'not sure', 'maybe cash instead']

        if any(signal in user_lower for signal in addressed_signals):
            return 'gather_policy_details'
        elif any(afraid in user_lower for afraid in still_afraid):
            return 'provide_cash_quote'
        else:
            return 'explain_insurance_process'

    elif current_step_name == 'provide_general_info':
        # Check if user shows interest
        user_lower = user_input.lower()
        interest_signals = ['yes', 'tell me more', 'what about', 'interested', 'price', 'quote', 'cost']

        if any(signal in user_lower for signal in interest_signals):
            return 'gather_vehicle_basics'
        else:
            return 'end_conversation'

    elif current_step_name == 'understand_timeline':
        # Check if timeline is provided
        user_lower = user_input.lower()
        timeline_indicators = ['week', 'month', 'next', 'when', 'time', 'schedule']

        if any(indicator in user_lower for indicator in timeline_indicators):
            return 'gather_vehicle_basics'
        else:
            return 'provide_general_info'

    elif current_step_name == 'clarify_intent':
        # Always proceed to gather basics after clarification attempt
        return 'gather_vehicle_basics'

    # Check for required variables completion
    required_vars = current_step.get('required_vars', [])
    if required_vars and all(variables.get(var) for var in required_vars):
        return transitions.get('complete', 'end')

    # Check for choice-based transitions
    options = current_step.get('options', [])
    if options:
        choice = identify_choice(user_input, options)
        if choice and choice in transitions:
            return transitions[choice]

    # Default to next step if defined
    return transitions.get('default', 'end')

def determine_repair_replacement_next_step(current_step, variables, user_input):
    """Determine next step for repair_vs_replacement context using calibrated questions and NEPQ approach"""
    current_step_name = variables.get('current_step_name', '')

    # If no step name in variables, infer from current step content
    if not current_step_name:
        step_message = current_step.get('message', '').lower()
        if 'what kind of damage' in step_message:
            current_step_name = 'assess_damage_and_needs'
        elif 'what\'s most important' in step_message:
            current_step_name = 'explore_concerns_with_questions'

    transitions = current_step.get('transitions', {})
    user_lower = user_input.lower()

    # Step-specific logic for repair vs replacement flow
    if current_step_name == 'assess_damage_and_needs':
        # After assessing damage, move to exploring concerns
        return 'explore_concerns_with_questions'

    elif current_step_name == 'explore_concerns_with_questions':
        # Analyze user response to determine their primary concern
        if any(word in user_lower for word in ['cost', 'price', 'expensive', 'cheap', 'money']):
            return 'address_cost_with_evidence'
        elif any(word in user_lower for word in ['warranty', 'guarantee', 'last', 'long time']):
            return 'highlight_warranty_benefits'
        elif any(word in user_lower for word in ['safe', 'safety', 'structural', 'trust', 'reliable']):
            return 'explain_structural_risks'
        elif any(word in user_lower for word in ['time', 'quick', 'fast', 'schedule', 'soon']):
            return 'discuss_timeline_options'
        elif any(word in user_lower for word in ['insurance', 'claim', 'coverage']):
            return 'explore_insurance_path'
        else:
            # Default to problem awareness questions if unsure
            return 'ask_problem_awareness_questions'

    elif current_step_name in ['address_cost_with_evidence', 'highlight_warranty_benefits',
                              'explain_structural_risks', 'discuss_timeline_options']:
        # After addressing specific concerns, check if they want to explore insurance
        if any(word in user_lower for word in ['insurance', 'claim', 'zero', 'covered', 'pay nothing']):
            return 'explore_insurance_path'
        elif any(word in user_lower for word in ['yes', 'okay', 'makes sense', 'understand']):
            return 'guide_to_solution'
        else:
            return 'ask_problem_awareness_questions'

    elif current_step_name == 'ask_problem_awareness_questions':
        # After problem awareness, guide toward solution
        if any(word in user_lower for word in ['yes', 'had that', 'happened', 'experience']):
            return 'share_similar_stories'
        elif any(word in user_lower for word in ['no', 'never', 'first time']):
            return 'explain_common_issues'
        else:
            return 'guide_to_solution'

    elif current_step_name == 'explore_insurance_path':
        # After exploring insurance, guide to solution
        return 'guide_to_solution'

    elif current_step_name == 'guide_to_solution':
        # Final step - check if they want to explore replacement
        if any(word in user_lower for word in ['yes', 'explore', 'tell me more', 'interested']):
            return 'offer_next_steps'
        elif any(word in user_lower for word in ['question', 'more info', 'know']):
            return 'answer_questions'
        else:
            return 'end'

    # Check for required variables completion
    required_vars = current_step.get('required_vars', [])
    if required_vars and all(variables.get(var) for var in required_vars):
        return transitions.get('complete', 'end')

    # Check for choice-based transitions
    options = current_step.get('options', [])
    if options:
        choice = identify_choice(user_input, options)
        if choice and choice in transitions:
            return transitions[choice]

    # Default to next step if defined
    return transitions.get('default', 'end')

def extract_variables(step_config, user_input, current_vars):
    """Extract variables from user input based on step configuration"""
    variables = current_vars.copy()
    mappings = step_config.get('variable_mapping', {})

    for var_name, pattern in mappings.items():
        if pattern and isinstance(pattern, str):
            import re
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                variables[var_name] = match.group(1) if match.groups() else match.group(0)
        elif pattern is None:
            # For brand/model, use intelligent extraction
            variables[var_name] = extract_vehicle_info(user_input, var_name)

    # Special handling for quotation_request context
    if current_vars.get('context') == 'quotation_request':
        variables = extract_quotation_variables(user_input, variables)

    return variables

def extract_quotation_variables(user_input, variables):
    """Extract variables specific to quotation requests using advanced NLP-like parsing"""
    text = user_input.lower()

    # Extract primary intent
    if variables.get('primary_intent') is None:
        variables['primary_intent'] = detect_customer_intent(text)

    # Extract urgency level
    if 'urgency_level' not in variables or variables['urgency_level'] == 'normal':
        variables['urgency_level'] = detect_urgency(text)

    # Extract price sensitivity
    if 'price_sensitivity' not in variables or variables['price_sensitivity'] == 'medium':
        variables['price_sensitivity'] = detect_price_sensitivity(text)

    # Extract insurance readiness
    if variables.get('insurance_readiness') is None:
        variables['insurance_readiness'] = detect_insurance_readiness(text)

    # Extract service type
    if variables.get('service_type') is None:
        variables['service_type'] = detect_service_type(text)

    # Extract damage information
    if variables.get('damage_type') is None:
        variables['damage_type'] = detect_damage_type(text)

    if variables.get('damage_severity') is None:
        variables['damage_severity'] = detect_damage_severity(text)

    # Extract vehicle information (enhanced)
    if variables.get('year') is None:
        variables['year'] = extract_vehicle_year(text)

    if variables.get('make') is None:
        variables['make'] = extract_vehicle_make(text)

    if variables.get('model') is None:
        variables['model'] = extract_vehicle_model(text)

    # Extract payment preferences
    if variables.get('payment_form') is None:
        variables['payment_form'] = detect_payment_preference(text)

    return variables

def detect_customer_intent(text):
    """Detect customer's primary intent from their message"""
    intents = {
        'immediate_cash': ['need today', 'asap', 'urgent', 'emergency', 'today', 'now', 'immediate', 'cash'],
        'immediate_insurance': ['insurance claim', 'file claim', 'insurance', 'adjuster', 'policy'],
        'postponed_cash': ['next week', 'later', 'schedule', 'appointment', 'cash payment'],
        'postponed_insurance': ['insurance', 'claim', 'later', 'schedule'],
        'just_looking': ['shopping around', 'looking', 'compare prices', 'just checking', 'browsing'],
        'lower_price': ['cheapest', 'lowest price', 'best price', 'discount', 'bargain'],
        'afraid_insurance': ['scared of insurance', 'worried about claim', 'premium increase', 'deductible'],
        'not_matured': ['not ready', 'thinking about it', 'maybe later', 'not sure'],
        'not_interested': ['not interested', 'never mind', 'don\'t need', 'cancel']
    }

    for intent, keywords in intents.items():
        if any(keyword in text for keyword in keywords):
            return intent

    # Default based on context
    if 'quote' in text or 'price' in text:
        return 'just_looking'

    return 'immediate_cash'  # Default assumption

def detect_urgency(text):
    """Detect urgency level from message"""
    high_urgency = ['emergency', 'urgent', 'asap', 'today', 'now', 'immediate', 'dangerous', 'safety']
    low_urgency = ['whenever', 'no rush', 'eventually', 'later', 'sometime']

    if any(word in text for word in high_urgency):
        return 'high'
    elif any(word in text for word in low_urgency):
        return 'low'

    return 'normal'

def detect_price_sensitivity(text):
    """Detect how price-sensitive the customer is"""
    high_sensitivity = ['cheapest', 'lowest', 'best price', 'afford', 'budget', 'expensive', 'cost']
    low_sensitivity = ['quality', 'best service', 'professional', 'warranty']

    if any(word in text for word in high_sensitivity):
        return 'high'
    elif any(word in text for word in low_sensitivity):
        return 'low'

    return 'medium'

def detect_insurance_readiness(text):
    """Detect customer's readiness to use insurance"""
    ready_keywords = ['insurance', 'claim', 'policy', 'adjuster', 'file claim']
    afraid_keywords = ['scared', 'worried', 'afraid', 'premium', 'deductible increase']
    unsure_keywords = ['maybe insurance', 'thinking insurance', 'not sure insurance']

    if any(word in text for word in afraid_keywords):
        return 'afraid'
    elif any(word in text for word in unsure_keywords):
        return 'unsure'
    elif any(word in text for word in ready_keywords):
        return 'ready'

    return None

def detect_service_type(text):
    """Detect type of service requested"""
    if any(word in text for word in ['repair', 'fix', 'chip', 'crack']):
        return 'repair'
    elif any(word in text for word in ['replace', 'new', 'shattered', 'broken']):
        return 'replacement'
    elif any(word in text for word in ['inspect', 'check', 'look at']):
        return 'inspection'

    return 'repair'  # Default

def detect_damage_type(text):
    """Detect type of damage"""
    damage_types = {
        'crack': ['crack', 'cracked'],
        'chip': ['chip', 'chipped', 'stone chip'],
        'shattered': ['shattered', 'broken', 'smashed'],
        'leak': ['leak', 'leaking', 'water leak']
    }

    for damage_type, keywords in damage_types.items():
        if any(keyword in text for keyword in keywords):
            return damage_type

    return None

def detect_damage_severity(text):
    """Detect severity of damage"""
    severe = ['large', 'big', 'huge', 'entire', 'whole', 'shattered', 'smashed']
    moderate = ['medium', 'moderate', 'size of', 'quarter', 'fist']
    minor = ['small', 'tiny', 'little', 'minor', 'chip']

    if any(word in text for word in severe):
        return 'large'
    elif any(word in text for word in moderate):
        return 'medium'
    elif any(word in text for word in minor):
        return 'small'

    return None

def extract_vehicle_year(text):
    """Extract vehicle year from text"""
    import re
    # Look for 4-digit years starting with 19 or 20
    year_match = re.search(r'\b(19|20)\d{2}\b', text)
    if year_match:
        year = int(year_match.group(0))
        return year if 1900 <= year <= 2030 else None

    # Also try to match 2-digit years (assume 2000s)
    short_year_match = re.search(r'\b(\d{2})\b', text)
    if short_year_match:
        year_short = int(short_year_match.group(1))
        if 0 <= year_short <= 30:  # 2000-2030
            return 2000 + year_short
        elif 90 <= year_short <= 99:  # 1990-1999
            return 1900 + year_short

    return None

def extract_vehicle_make(text):
    """Extract vehicle make/brand from text"""
    makes = [
        'toyota', 'honda', 'ford', 'chevrolet', 'chevy', 'bmw', 'mercedes', 'benz',
        'audi', 'nissan', 'hyundai', 'kia', 'subaru', 'mazda', 'lexus', 'acura',
        'infiniti', 'volkswagen', 'vw', 'volvo', 'tesla', 'jeep', 'chrysler',
        'dodge', 'ram', 'gmc', 'cadillac', 'lincoln', 'buick', 'pontiac',
        'saturn', 'mitsubishi', 'porsche', 'ferrari', 'lamborghini', 'jaguar',
        'land rover', 'mini', 'fiat', 'alfa romeo', 'maserati', 'bentley',
        'rolls royce', 'aston martin', 'mclaren', 'bugatti'
    ]

    text_lower = text.lower()
    for make in makes:
        if make in text_lower:
            return make.title()

    return None

def extract_vehicle_model(text):
    """Extract vehicle model from text (simplified - would need database in production)"""
    # Remove common words
    skip_words = {'find', 'windshield', 'for', 'a', 'the', 'my', 'car', 'vehicle',
                  'parts', 'replacement', 'repair', 'quote', 'price', 'need', 'glass'}

    words = text.lower().split()

    # Look for capitalized words or known models
    known_models = ['camry', 'corolla', 'civic', 'accord', 'mustang', 'f150', 'silverado',
                   'wrangler', 'cherokee', 'grand cherokee', 'sonata', 'elantra', 'tucson']

    for word in words:
        if word not in skip_words and len(word) > 2:
            if word in known_models or word[0].isupper():
                return word.title()

    return None

def detect_payment_preference(text):
    """Detect payment preference"""
    if any(word in text for word in ['insurance', 'claim', 'policy']):
        return 'insurance'
    elif any(word in text for word in ['cash', 'pay cash', 'money']):
        return 'cash'
    elif any(word in text for word in ['finance', 'payment plan', 'monthly']):
        return 'financing'

    return None

def extract_vehicle_info(text, info_type):
    """Extract vehicle information from text"""
    text = text.lower()

    if info_type == 'year':
        import re
        year_match = re.search(r'\b(19|20)\d{2}\b', text)
        return year_match.group(0) if year_match else None

    elif info_type == 'brand':
        # Common vehicle brands
        brands = ['toyota', 'honda', 'ford', 'chevrolet', 'bmw', 'mercedes', 'audi', 'nissan', 'hyundai', 'kia', 'subaru', 'mazda', 'lexus', 'acura', 'infiniti', 'volkswagen', 'volvo', 'tesla', 'jeep', 'chrysler', 'dodge', 'ram']
        for brand in brands:
            if brand in text:
                return brand.title()
        return None

    elif info_type == 'model':
        # This is more complex - would need a database lookup or more sophisticated parsing
        # For now, return a placeholder that indicates we need more processing
        return extract_model_from_text(text)

    return None

def extract_model_from_text(text):
    """Extract model name from text (simplified version)"""
    # Remove common words and extract potential model names
    # This is a basic implementation - in production, you'd use a vehicle database
    words = text.split()
    # Skip common words and try to find model-like words
    skip_words = {'find', 'windshield', 'for', 'a', 'the', 'my', 'car', 'vehicle', 'parts', 'replacement', 'repair'}

    for word in words:
        if word not in skip_words and len(word) > 2:
            # Check if it looks like a model name (starts with capital, etc.)
            if word[0].isupper() or word in ['camry', 'corolla', 'civic', 'accord', 'mustang', 'f150']:
                return word.title()

    return None

def identify_choice(user_input, options):
    """Identify which option the user selected"""
    user_lower = user_input.lower()
    for option in options:
        if option.lower() in user_lower:
            return option
    return None

def generate_step_response(step_config, variables):
    """Generate the response message for a step"""
    message = step_config.get('message', '')

    # Substitute variables in message
    for var_name, value in variables.items():
        placeholder = f'{{{var_name}}}'
        if placeholder in message:
            message = message.replace(placeholder, str(value) if value else 'unknown')

    # Add questions if specified
    questions = step_config.get('questions', [])
    if questions:
        message += '\n\n' + '\n'.join(f'• {q}' for q in questions)

    # Add options if specified
    options = step_config.get('options', [])
    if options:
        message += '\n\nPlease choose one:\n' + '\n'.join(f'• {opt.replace("_", " ").title()}' for opt in options)

    return message

def should_escalate(context, user_message):
    """Check if conversation should be escalated"""
    config = CONVERSATION_FLOWS.get(context, {})
    escalation_triggers = config.get('escalation_triggers', [])

    user_lower = user_message.lower()
    return any(trigger in user_lower for trigger in escalation_triggers)

def get_escalation_action(context):
    """Get escalation action for a context"""
    config = CONVERSATION_FLOWS.get(context, {})
    escalation_action = config.get('escalation_action', 'customer_service')
    return ESCALATION_PATHS.get(escalation_action, ESCALATION_PATHS['customer_service'])