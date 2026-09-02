"""Scenario bank for TalkMate's English conversation practice."""

LEVELS = {
    "everyday": {
        "id": "everyday",
        "order": 1,
        "name": "Everyday confidence",
        "eyebrow": "REAL LIFE",
        "desc": "Short, useful conversations for travel and daily life.",
        "goal": "Speak clearly, politely, and keep the conversation moving.",
        "color": "sun",
        "scenarios": [
            {
                "title": "Coffee, please",
                "icon": "cup",
                "duration": "6 min",
                "context": "You have just walked into a busy neighborhood cafe. Order a drink and ask one friendly question.",
                "persona": "Maya, a warm barista who speaks naturally but not too fast.",
                "opening": "Hi there! Welcome in. What can I get started for you today?",
                "starter": "I'd like a ... , please.",
                "vocabulary": ["still or sparkling", "for here", "to go", "receipt"],
                "offline_replies": [
                    "Nice choice. Would you like that hot or iced?",
                    "Sure. Is that for here or to go?",
                    "Perfect. That will be four fifty. Would you like a receipt?",
                ],
            },
            {
                "title": "Find the station",
                "icon": "map",
                "duration": "7 min",
                "context": "You are visiting a new city and need directions to the train station before your train leaves.",
                "persona": "Noah, a helpful local on his way home.",
                "opening": "You look a little lost. Can I help you find something?",
                "starter": "Excuse me, could you tell me ...?",
                "vocabulary": ["turn left", "straight ahead", "on the corner", "how long"],
                "offline_replies": [
                    "Of course. The station is about a ten-minute walk from here.",
                    "Walk straight ahead, then turn left at the traffic lights.",
                    "You cannot miss it - it is the big glass building on the corner. Safe travels!",
                ],
            },
            {
                "title": "Meet the neighbor",
                "icon": "home",
                "duration": "5 min",
                "context": "You meet a neighbor in the elevator. Make a little small talk without sounding rehearsed.",
                "persona": "Liam, a friendly neighbor who has lived in the building for a year.",
                "opening": "Hey! I do not think we have met. I am Liam from apartment 8B.",
                "starter": "Nice to meet you. I'm ...",
                "vocabulary": ["just moved in", "settling in", "around here", "recommend"],
                "offline_replies": [
                    "Nice to meet you too! Did you just move into the building?",
                    "There are some great places around here. What kind of food do you like?",
                    "You should try the little noodle shop across the street. Welcome to the neighborhood!",
                ],
            },
            {
                "title": "Make a phone call",
                "icon": "phone",
                "duration": "6 min",
                "context": "You are calling a hotel to change a reservation. Explain the issue, ask for options, and confirm the new details.",
                "persona": "Grace, a calm hotel receptionist who needs the details one step at a time.",
                "opening": "Good afternoon, Riverside Hotel. This is Grace speaking. How may I help you?",
                "starter": "Hi, I'm calling about my reservation ...",
                "vocabulary": ["reservation", "check-in date", "available", "could you confirm"],
                "offline_replies": [
                    "Of course. Could I have the name on the reservation, please?",
                    "I can see your booking. Which date would you like to change it to?",
                    "Great. I have updated it for you. Is there anything else I can help with?",
                ],
            },
            {
                "title": "At the doctor's office",
                "icon": "doctor",
                "duration": "7 min",
                "context": "You have a mild sore throat and need to explain your symptoms clearly, then ask what you should do next.",
                "persona": "Dr. Patel, a patient and reassuring doctor who asks clear questions.",
                "opening": "Hi, I'm Dr. Patel. What brings you in today?",
                "starter": "I've had a sore throat since ...",
                "vocabulary": ["symptoms", "since yesterday", "allergic", "prescription"],
                "offline_replies": [
                    "I see. Do you have a fever or any trouble swallowing?",
                    "Have you taken anything for the pain so far?",
                    "It sounds mild. Please rest, drink plenty of water, and come back if it gets worse.",
                ],
            },
            {
                "title": "Rent an apartment",
                "icon": "key",
                "duration": "8 min",
                "context": "You are viewing an apartment and want to ask practical questions before deciding whether to rent it.",
                "persona": "Morgan, a straightforward property agent who knows the building well.",
                "opening": "Welcome! This is the one-bedroom apartment you asked about. What do you think so far?",
                "starter": "It looks great. Could I ask about ...?",
                "vocabulary": ["monthly rent", "utilities", "deposit", "move in"],
                "offline_replies": [
                    "The monthly rent is twelve hundred, and water is included.",
                    "The deposit is one month's rent. Are you planning to move in soon?",
                    "Pets are allowed with a small extra fee. Would you like to see the kitchen next?",
                ],
            },
            {
                "title": "Order at a restaurant",
                "icon": "plate",
                "duration": "6 min",
                "context": "You are at a restaurant with a food allergy. Order politely, ask about ingredients, and request a small change.",
                "persona": "Elliot, an attentive server who wants to make sure your meal is safe and enjoyable.",
                "opening": "Good evening! Are you ready to order, or would you like a few more minutes?",
                "starter": "I think I'm ready. Could you tell me if ...?",
                "vocabulary": ["allergic to", "ingredients", "without", "on the side"],
                "offline_replies": [
                    "Absolutely. Do you have any allergies I should let the kitchen know about?",
                    "That dish does contain peanuts, but we can recommend a safe alternative.",
                    "Perfect. I will put the sauce on the side for you. Can I get you anything to drink?",
                ],
            },
            {
                "title": "Meet a traveler",
                "icon": "globe",
                "duration": "6 min",
                "context": "You meet a foreign traveler at a local cafe. Start a genuine conversation and offer one helpful recommendation.",
                "persona": "Sam, a curious visitor who has just arrived and wants to learn about the city.",
                "opening": "Hi! Sorry to bother you - do you know any good places to visit around here?",
                "starter": "Sure! If you like ..., you should ...",
                "vocabulary": ["local favorite", "worth visiting", "get around", "what brings you here"],
                "offline_replies": [
                    "That sounds perfect. Is it easy to get there by public transport?",
                    "Thanks for the tip! Have you lived here for a long time?",
                    "I really appreciate your help. Maybe I will see you around the city!",
                ],
            },
        ],
    },
    "work": {
        "id": "work",
        "order": 2,
        "name": "Work & ambition",
        "eyebrow": "CAREER MODE",
        "desc": "Sound composed in meetings, interviews, and professional introductions.",
        "goal": "Explain your ideas with confidence and respond naturally under light pressure.",
        "color": "blue",
        "scenarios": [
            {
                "title": "The first interview",
                "icon": "briefcase",
                "duration": "8 min",
                "context": "You are interviewing for a junior product role. Introduce yourself and connect your experience to the job.",
                "persona": "Sofia, an encouraging recruiter who asks concise follow-up questions.",
                "opening": "Thanks for joining us today. Could you tell me a little about yourself?",
                "starter": "Sure. I'm currently ... and I'm interested in ...",
                "vocabulary": ["responsible for", "strength", "challenge", "opportunity"],
                "offline_replies": [
                    "That sounds interesting. What made you apply for this particular role?",
                    "Could you give me an example of a project you are proud of?",
                    "Great, thank you. Do you have any questions for me about the team?",
                ],
            },
            {
                "title": "Speak up in a meeting",
                "icon": "spark",
                "duration": "7 min",
                "context": "Your team is choosing a launch plan. Share a practical idea and respond to a colleague's concern.",
                "persona": "Alex, a thoughtful teammate who wants evidence before agreeing.",
                "opening": "We have two weeks before launch. Does anyone have an idea for reaching more early users?",
                "starter": "I think we could ... because ...",
                "vocabulary": ["I suggest", "timeline", "trade-off", "measure results"],
                "offline_replies": [
                    "I like the direction, but do we have enough time to do that well?",
                    "What would be the smallest version we could test this week?",
                    "That feels realistic. Let us bring it to the team lead this afternoon.",
                ],
            },
            {
                "title": "Make a new connection",
                "icon": "handshake",
                "duration": "6 min",
                "context": "You are at a professional event. Introduce yourself, ask about the other person's work, and find common ground.",
                "persona": "Jamie, a designer attending the event for the first time.",
                "opening": "Hi! I am Jamie. This is my first time at one of these events. How about you?",
                "starter": "Hi Jamie, I'm ... I work/study ...",
                "vocabulary": ["I work in", "currently", "curious about", "keep in touch"],
                "offline_replies": [
                    "That is cool. What kind of projects do you usually work on?",
                    "I have been curious about that area too. How did you get into it?",
                    "I have really enjoyed talking with you. Would you like to connect on LinkedIn?",
                ],
            },
            {
                "title": "Present your idea",
                "icon": "presentation",
                "duration": "8 min",
                "context": "You have two minutes to introduce an idea to your team. Explain the problem, the proposed solution, and why it matters.",
                "persona": "Riley, a team lead who is open-minded but asks direct questions about impact and feasibility.",
                "opening": "We have a few minutes left. Would you like to walk us through your idea?",
                "starter": "Thanks. The problem I noticed is ...",
                "vocabulary": ["the problem is", "propose", "expected impact", "next step"],
                "offline_replies": [
                    "That is a clear problem. What is the simplest version of your solution?",
                    "How would we know whether it is working after the first month?",
                    "I like the focus. Put together a short outline and we can review it on Friday.",
                ],
            },
        ],
    },
}


# Each flow stays local and transparent: a learner progresses through a few
# concrete conversational moves rather than a fixed list of partner replies.
OFFLINE_FLOWS = {
    "cup": {
        "goals": [
            {"id": "order", "label": "Place your order", "terms": "like want order coffee latte tea drink espresso cappuccino", "reply": "Great choice. Would you like that hot or iced?", "nudge": "Tell me what you would like to drink."},
            {"id": "detail", "label": "Add one drink detail", "terms": "hot iced ice milk sugar small medium large", "reply": "Got it. Is that for here or to go?", "nudge": "Add one detail, such as hot, iced, or milk."},
            {"id": "confirm", "label": "Confirm how you will take it", "terms": "here go takeaway take away", "reply": "Perfect. Would you like a receipt?", "nudge": "Say whether it is for here or to go."},
            {"id": "close", "label": "Close politely", "terms": "thanks thank all good thats all that's all", "reply": "You are all set. Enjoy your drink!", "nudge": "Close the order politely with thanks."},
        ],
    },
    "map": {
        "goals": [
            {"id": "ask", "label": "Ask for the station", "terms": "station train directions where find get", "reply": "Of course. The station is about a ten-minute walk from here.", "nudge": "Ask where the station is or how to get there."},
            {"id": "clarify", "label": "Ask one follow-up question", "terms": "how long which way left right straight bus walk turn", "reply": "Walk straight ahead, then turn left at the traffic lights.", "nudge": "Ask a follow-up about the route or how long it takes."},
            {"id": "confirm", "label": "Confirm the route", "terms": "so go got it corner lights building", "reply": "Yes, that is right. You cannot miss the big glass building on the corner.", "nudge": "Repeat one route detail to confirm you understand."},
            {"id": "close", "label": "Thank the local", "terms": "thanks thank helpful appreciate", "reply": "You are welcome. Safe travels!", "nudge": "Thank them before you go."},
        ],
    },
    "home": {
        "goals": [
            {"id": "introduce", "label": "Introduce yourself", "terms": "nice meet im i'm name moved live apartment", "reply": "Nice to meet you too! Did you just move into the building?", "nudge": "Introduce yourself and say hello."},
            {"id": "share", "label": "Share one personal detail", "terms": "moved new work study live food like", "reply": "That sounds nice. What kind of food do you like?", "nudge": "Share one detail about moving in, work, or what you like."},
            {"id": "ask", "label": "Ask for a local recommendation", "terms": "recommend recommendation around restaurant cafe food place", "reply": "You should try the little noodle shop across the street.", "nudge": "Ask for one place or recommendation nearby."},
            {"id": "close", "label": "End warmly", "terms": "thanks thank see welcome", "reply": "Any time. Welcome to the neighborhood!", "nudge": "Close the small talk warmly."},
        ],
    },
    "phone": {
        "goals": [
            {"id": "identify", "label": "Explain the reservation issue", "terms": "reservation booking hotel change date check in", "reply": "Of course. Could I have the name on the reservation, please?", "nudge": "Say that you are calling about a reservation."},
            {"id": "request", "label": "Request a new date or option", "terms": "would like need move new date available change to", "reply": "I can see your booking. Which date would you like to change it to?", "nudge": "Ask to change the date or ask what is available."},
            {"id": "confirm", "label": "Confirm the new details", "terms": "confirm correct yes date night nights", "reply": "Great. I have updated it for you. Is there anything else I can help with?", "nudge": "Confirm the new date or number of nights."},
            {"id": "close", "label": "End the call politely", "terms": "thanks thank all thats all that's all", "reply": "You are very welcome. Have a lovely stay!", "nudge": "Thank the receptionist and close the call."},
        ],
    },
    "doctor": {
        "goals": [
            {"id": "symptom", "label": "Describe your main symptom", "terms": "sore throat fever pain sick cough headache symptom", "reply": "I see. Do you have a fever or any trouble swallowing?", "nudge": "Describe your main symptom and when it started."},
            {"id": "detail", "label": "Answer a follow-up question", "terms": "since yesterday no yes fever swallow medicine took allergy", "reply": "Thanks for explaining that. Have you taken anything for the pain so far?", "nudge": "Give one clear detail about timing, fever, or medicine."},
            {"id": "ask", "label": "Ask what to do next", "terms": "should what do medicine prescription treatment recommend", "reply": "It sounds mild. Please rest, drink plenty of water, and come back if it gets worse.", "nudge": "Ask what you should do next."},
            {"id": "close", "label": "Close the visit politely", "terms": "thanks thank appreciate", "reply": "You are welcome. I hope you feel better soon.", "nudge": "Thank the doctor before you leave."},
        ],
    },
    "key": {
        "goals": [
            {"id": "interest", "label": "React to the apartment", "terms": "looks like apartment interested great nice", "reply": "I am glad you like it. What would you like to know?", "nudge": "Say what you think about the apartment."},
            {"id": "ask", "label": "Ask a practical question", "terms": "rent utilities deposit lease pets furnished kitchen", "reply": "The monthly rent is twelve hundred, and water is included.", "nudge": "Ask about rent, utilities, deposit, or another practical detail."},
            {"id": "decision", "label": "Discuss your move-in plan", "terms": "move move in soon date available decide", "reply": "The deposit is one month's rent. Are you planning to move in soon?", "nudge": "Say when you might move in or ask about availability."},
            {"id": "close", "label": "Close the viewing", "terms": "thanks thank think contact", "reply": "Of course. Let me know if you would like another viewing.", "nudge": "Thank the agent and say what you will do next."},
        ],
    },
    "plate": {
        "goals": [
            {"id": "allergy", "label": "Explain your allergy", "terms": "allergy allergic peanuts ingredients safe", "reply": "Thank you for telling me. That dish contains peanuts, but I can suggest a safe alternative.", "nudge": "Tell the server about your allergy first."},
            {"id": "order", "label": "Choose or ask about a safe dish", "terms": "order dish menu alternative vegetarian chicken salad", "reply": "That is a good choice. Would you like any changes to it?", "nudge": "Choose a safe dish or ask about an alternative."},
            {"id": "change", "label": "Request one small change", "terms": "without on side no sauce change", "reply": "Absolutely. I will put the sauce on the side for you.", "nudge": "Request one small change, such as without sauce."},
            {"id": "close", "label": "Finish the order politely", "terms": "thanks thank thats all that's all", "reply": "Perfect. I will get that started for you.", "nudge": "Thank the server and finish your order."},
        ],
    },
    "globe": {
        "goals": [
            {"id": "recommend", "label": "Give one recommendation", "terms": "should recommend visit museum beach market local", "reply": "That sounds perfect. Is it easy to get there by public transport?", "nudge": "Recommend one place to visit."},
            {"id": "detail", "label": "Add a useful detail", "terms": "bus train walk minutes near easy", "reply": "Great, that sounds easy enough. Have you lived here for a long time?", "nudge": "Add a direction, transport tip, or reason it is worth visiting."},
            {"id": "ask", "label": "Ask about the traveler", "terms": "where from brings how long trip travel", "reply": "I just arrived yesterday, so your advice really helps.", "nudge": "Ask the traveler one friendly question."},
            {"id": "close", "label": "End the chat warmly", "terms": "thanks thank enjoy welcome", "reply": "I really appreciate your help. Maybe I will see you around the city!", "nudge": "Close the chat warmly."},
        ],
    },
    "briefcase": {
        "goals": [
            {"id": "intro", "label": "Introduce your experience", "terms": "currently experience work studied responsible project", "reply": "That sounds interesting. What made you apply for this particular role?", "nudge": "Introduce your current experience or background."},
            {"id": "motive", "label": "Connect yourself to the role", "terms": "apply role interested opportunity because", "reply": "That makes sense. Could you give me an example of a project you are proud of?", "nudge": "Say why this role interests you."},
            {"id": "example", "label": "Give one concrete example", "terms": "project led built improved challenge result", "reply": "Great example. Do you have any questions for me about the team?", "nudge": "Give one short example from a project or challenge."},
            {"id": "close", "label": "Ask a final question or close", "terms": "question team culture thanks thank", "reply": "Thank you for your thoughtful questions. We will be in touch soon.", "nudge": "Ask one question about the team or thank the interviewer."},
        ],
    },
    "spark": {
        "goals": [
            {"id": "idea", "label": "Share a practical idea", "terms": "suggest idea could launch users plan", "reply": "I like the direction, but do we have enough time to do that well?", "nudge": "Share one practical idea for the launch."},
            {"id": "tradeoff", "label": "Address a concern", "terms": "time timeline risk trade off because", "reply": "What would be the smallest version we could test this week?", "nudge": "Address the time, risk, or trade-off."},
            {"id": "test", "label": "Suggest a small test", "terms": "test smaller version measure results week", "reply": "That feels realistic. Let us bring it to the team lead this afternoon.", "nudge": "Suggest a small test or a way to measure results."},
            {"id": "close", "label": "Agree on the next step", "terms": "agree next step team lead thanks", "reply": "Great. I will add it to the meeting notes.", "nudge": "Agree on the next step."},
        ],
    },
    "handshake": {
        "goals": [
            {"id": "intro", "label": "Introduce yourself", "terms": "im i'm work study name", "reply": "That is cool. What kind of projects do you usually work on?", "nudge": "Introduce yourself and say what you do."},
            {"id": "ask", "label": "Ask about their work", "terms": "what kind projects work do you how", "reply": "I have been curious about that area too. How did you get into it?", "nudge": "Ask one open question about their work."},
            {"id": "common", "label": "Find common ground", "terms": "also too interested curious similar", "reply": "It sounds like we have a lot in common. Would you like to connect on LinkedIn?", "nudge": "Share one interest or point of common ground."},
            {"id": "close", "label": "Suggest staying in touch", "terms": "linkedin connect keep touch thanks", "reply": "I have really enjoyed talking with you. Let us keep in touch.", "nudge": "Suggest staying in touch or close the conversation."},
        ],
    },
    "presentation": {
        "goals": [
            {"id": "problem", "label": "Explain the problem", "terms": "problem users customer issue noticed", "reply": "That is a clear problem. What is the simplest version of your solution?", "nudge": "State the problem you noticed."},
            {"id": "solution", "label": "Propose a solution", "terms": "propose solution build create simpler", "reply": "How would we know whether it is working after the first month?", "nudge": "Propose one simple solution."},
            {"id": "impact", "label": "Explain the expected impact", "terms": "impact measure results users improve month", "reply": "I like the focus. What is the next step to make this real?", "nudge": "Explain how you would measure the impact."},
            {"id": "close", "label": "Confirm the next step", "terms": "next step outline review friday thanks", "reply": "Put together a short outline and we can review it on Friday.", "nudge": "Confirm one concrete next step."},
        ],
    },
}


SENTENCE_BUILDERS = {
    "cup": {
        "label": "POLITE ORDER",
        "frame": "I'd like [item] [detail], please.",
        "hint": "Name what you want, then add one useful detail.",
        "slots": [
            {"key": "item", "label": "item", "placeholder": "an iced latte"},
            {"key": "detail", "label": "detail", "placeholder": "to go"},
        ],
        "examples": ["I'd like an iced latte to go, please.", "Could I have a coffee for here, please?"],
    },
    "map": {
        "label": "ASK FOR DIRECTIONS",
        "frame": "Could you tell me [question], please?",
        "hint": "Use a polite opener before your exact question.",
        "slots": [{"key": "question", "label": "question", "placeholder": "where the station is"}],
        "examples": ["Could you tell me where the station is, please?", "How long does it take to walk there?"],
    },
    "home": {
        "label": "SMALL TALK",
        "frame": "I [situation], so I'm looking for [thing].",
        "hint": "Give one small detail, then invite a useful response.",
        "slots": [
            {"key": "situation", "label": "situation", "placeholder": "just moved in"},
            {"key": "thing", "label": "thing", "placeholder": "good food nearby"},
        ],
        "examples": ["I just moved in, so I'm looking for good food nearby.", "Do you have any recommendations around here?"],
    },
    "phone": {
        "label": "MAKE A REQUEST",
        "frame": "I'm calling about [topic]. Could I [request]?",
        "hint": "State the reason first, then make one clear request.",
        "slots": [
            {"key": "topic", "label": "topic", "placeholder": "my reservation"},
            {"key": "request", "label": "request", "placeholder": "change the date"},
        ],
        "examples": ["I'm calling about my reservation. Could I change the date?", "Could you confirm the new check-in date?"],
    },
    "doctor": {
        "label": "EXPLAIN A SYMPTOM",
        "frame": "I've had [symptom] for [time].",
        "hint": "Use have had + a time period for symptoms that continue now.",
        "slots": [
            {"key": "symptom", "label": "symptom", "placeholder": "a sore throat"},
            {"key": "time", "label": "time", "placeholder": "two days"},
        ],
        "examples": ["I've had a sore throat for two days.", "Should I take anything for the pain?"],
    },
    "key": {
        "label": "ASK A PRACTICAL QUESTION",
        "frame": "Could I ask whether [question]?",
        "hint": "Whether makes apartment questions sound clear and professional.",
        "slots": [{"key": "question", "label": "question", "placeholder": "utilities are included"}],
        "examples": ["Could I ask whether utilities are included?", "When would the apartment be available?"],
    },
    "plate": {
        "label": "ORDER SAFELY",
        "frame": "I'm allergic to [food]. Could I have [dish] without it?",
        "hint": "State the allergy first so the server can help safely.",
        "slots": [
            {"key": "food", "label": "food", "placeholder": "peanuts"},
            {"key": "dish", "label": "dish", "placeholder": "this dish"},
        ],
        "examples": ["I'm allergic to peanuts. Could I have this dish without them?", "Could you put the sauce on the side?"],
    },
    "globe": {
        "label": "GIVE A RECOMMENDATION",
        "frame": "If you like [interest], you should [recommendation].",
        "hint": "Use this to make a personal, useful recommendation.",
        "slots": [
            {"key": "interest", "label": "interest", "placeholder": "local food"},
            {"key": "recommendation", "label": "recommendation", "placeholder": "try the night market"},
        ],
        "examples": ["If you like local food, you should try the night market.", "It's worth visiting in the evening."],
    },
    "briefcase": {
        "label": "INTRODUCE YOURSELF",
        "frame": "I'm currently [role], and I'm interested in [field] because [reason].",
        "hint": "Connect what you do now to the direction you want next.",
        "slots": [
            {"key": "role", "label": "role", "placeholder": "a junior designer"},
            {"key": "field", "label": "field", "placeholder": "product design"},
            {"key": "reason", "label": "reason", "placeholder": "I enjoy solving user problems"},
        ],
        "examples": ["I'm currently a junior designer, and I'm interested in product design because I enjoy solving user problems.", "One project I'm proud of is ..."],
    },
    "spark": {
        "label": "SHARE AN IDEA",
        "frame": "I suggest we [action] because [reason].",
        "hint": "A clear suggestion needs one practical reason.",
        "slots": [
            {"key": "action", "label": "action", "placeholder": "test a smaller version first"},
            {"key": "reason", "label": "reason", "placeholder": "we only have two weeks"},
        ],
        "examples": ["I suggest we test a smaller version first because we only have two weeks.", "The trade-off is ..., but ..."],
    },
    "handshake": {
        "label": "MAKE A CONNECTION",
        "frame": "I work in [field]. What kind of [thing] do you work on?",
        "hint": "Share one fact about yourself, then ask an open question.",
        "slots": [
            {"key": "field", "label": "field", "placeholder": "marketing"},
            {"key": "thing", "label": "thing", "placeholder": "projects"},
        ],
        "examples": ["I work in marketing. What kind of projects do you work on?", "How did you get into that field?"],
    },
    "presentation": {
        "label": "PRESENT AN IDEA",
        "frame": "The problem is [problem], so I propose [solution].",
        "hint": "Lead with the problem, then make your solution concrete.",
        "slots": [
            {"key": "problem", "label": "problem", "placeholder": "new users leave too early"},
            {"key": "solution", "label": "solution", "placeholder": "a simpler onboarding flow"},
        ],
        "examples": ["The problem is new users leave too early, so I propose a simpler onboarding flow.", "The expected impact is ..."],
    },
}


def sentence_builder_for(scenario: dict):
    """Return a reusable sentence frame for the selected real-life situation."""
    return SENTENCE_BUILDERS.get(scenario.get("icon"), SENTENCE_BUILDERS["home"])


def conversation_flow_for(scenario: dict):
    """Return safe public goal metadata for the offline conversation flow."""
    flow = OFFLINE_FLOWS.get(scenario.get("icon"), {})
    return [
        {"id": goal["id"], "label": goal["label"]}
        for goal in flow.get("goals", [])
    ]


def level_list():
    """Return concise level metadata for the home screen."""
    return sorted(
        (
            {
                "id": level["id"],
                "order": level["order"],
                "name": level["name"],
                "eyebrow": level["eyebrow"],
                "desc": level["desc"],
                "goal": level["goal"],
                "color": level["color"],
                "count": len(level["scenarios"]),
                "scenarios": [
                    {
                        "title": scenario["title"],
                        "icon": scenario["icon"],
                        "duration": scenario["duration"],
                        "description": scenario["context"],
                    }
                    for scenario in level["scenarios"]
                ],
            }
            for level in LEVELS.values()
        ),
        key=lambda item: item["order"],
    )


def get_level(level_id: str):
    return LEVELS.get(level_id)


def get_scenario(level_id: str, index: int):
    level = LEVELS.get(level_id)
    if not level or not level["scenarios"]:
        return None
    options = level["scenarios"]
    return options[index % len(options)]
