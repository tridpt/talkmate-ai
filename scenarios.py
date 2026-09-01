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
