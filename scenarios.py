"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # Ten passages I wrote myself. The first three are in a plain,
        # non-native style (criteria.md #1: none of those may be labeled AI).
        # 4-10 are chunks 1-7 of my essay on "I Have a Dream".
        "texts": [
            "I usually eat breakfast in my room. I make two eggs and have a piece of bread. Sometimes I also eat a banana. My first class starts at nine, so I have enough time to sit down and eat. On weekends, I get up late and have breakfast with my roommate.",
            "Yesterday it rained after class. I had no umbrella, so I waited by the door. My friend saw me and asked me to walk with her. Her umbrella was small, and my bag got a little wet. We went to a café near our school and had some hot tea.",
            "I like to play a computer game with my brother. In this game, we build small cities. I like to build houses near a river because they look nice there. My brother always builds roads first. He lives far from me now, but we still play together on Friday nights.",
            "I have a Dream, a speech delivered by Dr. Martin Luther King, was significantly influential to American society, resulting in growing affirmative action movement in followed decades.",
            "During his speech, Dr. King combined plenty of rhetorical devices, such as metaphor, allusion and repetition, which facilitate the artistic value of the context, the appeal of the slogan, the credibility of the Dr. King's opinion and the justice of his position and plays a considerable role in making the speech so spread all around the world and become the example of the struggle for national liberation. To begin with, the speech mentions the the signing of the Emancipation Proclamation and affirms its importance for slaves.",
            "This is a typical allusion, which forms cooperation with the place, Lincoln's statue, where the speech was given and emphasizes the equivalent identity between African American and Caucasian.",
            "Emancipation Proclamation offers the declaration of equal rights legal support, which is what the whole context based on, and it is also a contract that should have fulfilled but many people choose to ignore and even violate at that era, resulting listeners' self-recognition and furious emotion related to the contradictory reality, which is listed in the following part of the speech in repetition: Dr. King uses a series of \"shameful condition\" to evoke the anger of his audience and make his speech with a tremendous momentum.",
            "Furthermore, Dr. King extended his illustration through a metaphor: the American government and society didn't cash their check. In other words, the promise of American government made had not been achieved. Now the African-American was not only protect their inherent right, but regain the rights that had been violates. They became victims.",
            "Dr. King reinforced the his position mentioned in the former part, clarifying the necessity and urgency of the struggle. This encouraged people to take actions to change the inequality and discrimination right away, resulting in lasting influence and extensive impact on society. Then, Dr. King highlighted the potential results of ignoring the sound of African-American.",
            "This is important because it demonstrates that the speech is not only for those who are experiencing unfair treatment, but it also asks traditional American society to realize their fault and change their attitudes towards African-American. Next, Dr. King emphasized the principle of non-violation.",
        ],
    },
    {
        "name": "gap AI set",
        "criterion": 2,
        # Ten unedited ChatGPT outputs (one prompt, ten paragraphs; only the
        # numbering and markdown bold were stripped).
        "texts": [
            "Learning to cook. The first meal I cooked in my apartment was tomato soup from a can. By October, I could make it from scratch, mostly because my roommate showed me how to tell when an onion was ready. Now, whenever I cook for someone else, I pass along her advice: keep the heat low enough that you can finish your story.",
            "An unexpected elective. I signed up for astronomy because it fit my schedule. During our first evening lab, I looked through a telescope and saw Saturn’s rings. I had seen clearer pictures in textbooks, but this time I could step away, look up at an ordinary patch of sky, and find the little dot where I had just seen them.",
            "Working through college. Every Thursday, I leave chemistry lab, change shirts in the library bathroom, and catch the bus to my shift at a grocery store. The schedule gets tiring around exams, but I like working the register on Thursdays. One regular always buys flowers, and every week he asks me to help pick a different color for his wife.",
            "Finding a study method. My biology notes looked impressive until a friend asked me to explain how a nerve signal travels. I got halfway through a sentence and reached for my notebook. Since then, we’ve ended each study session by taking turns at the whiteboard. A blank space in the middle of a diagram tells me exactly what to review.",
            "Calling home. My dad and I used to run out of things to say five minutes into our Sunday phone calls. One afternoon, I called while walking across campus and described a squirrel dragging an entire bagel up a tree. Now he takes his phone outside, too. Last Sunday, I got a fifteen-minute tour of the tomatoes in his garden.",
            "Starting a campus club. Four people showed up to our first chess meeting, including me and the friend who had helped tape up the flyers. We pushed two tables together and played until the custodian needed the room. The following week, one member brought his grandfather’s battered chess clock. That was the first time I believed the club might last.",
            "Living with a roommate. My roommate likes to wash dishes the next morning. I like to wake up to an empty sink. For three weeks, I scrubbed her pans and quietly got angrier. When I finally mentioned it, she said she thought I enjoyed doing dishes. We laughed at that, bought a second dishpan, and reclaimed most of our counter space.",
            "Losing an election. I lost the election for residence hall representative by three votes. The next morning, the winner knocked on my door carrying one of my flyers. She had circled my proposal for a shelf where residents could leave things they no longer needed. We installed it together that Saturday. By dinner, someone had already claimed the first item, a rice cooker.",
            "Taking the city bus. Riding the bus to my internship changed how I give people directions. I used to say a place was ten minutes away because that was how long the drive took. Now I know which transfer takes half an hour and which stop leaves you across six lanes of traffic from the building you can already see.",
            "Changing majors. I realized I wanted to switch from accounting to history while helping my grandmother label photographs. One picture showed her standing outside a factory I had passed my whole life without noticing. We spent an hour discussing a single shift she worked there in 1974. The next morning, I went to office hours to ask my history professor about oral history projects.",
        ],
    },
    {
        "name": "gap human set",
        "criterion": 2,
        # My past essay on "I Have a Dream", written before I used AI tools,
        # split at sentence boundaries into ten chunks.
        "texts": [
            "I have a Dream, a speech delivered by Dr. Martin Luther King, was significantly influential to American society, resulting in growing affirmative action movement in followed decades.",
            "During his speech, Dr. King combined plenty of rhetorical devices, such as metaphor, allusion and repetition, which facilitate the artistic value of the context, the appeal of the slogan, the credibility of the Dr. King's opinion and the justice of his position and plays a considerable role in making the speech so spread all around the world and become the example of the struggle for national liberation. To begin with, the speech mentions the the signing of the Emancipation Proclamation and affirms its importance for slaves.",
            "This is a typical allusion, which forms cooperation with the place, Lincoln's statue, where the speech was given and emphasizes the equivalent identity between African American and Caucasian.",
            "Emancipation Proclamation offers the declaration of equal rights legal support, which is what the whole context based on, and it is also a contract that should have fulfilled but many people choose to ignore and even violate at that era, resulting listeners' self-recognition and furious emotion related to the contradictory reality, which is listed in the following part of the speech in repetition: Dr. King uses a series of \"shameful condition\" to evoke the anger of his audience and make his speech with a tremendous momentum.",
            "Furthermore, Dr. King extended his illustration through a metaphor: the American government and society didn't cash their check. In other words, the promise of American government made had not been achieved. Now the African-American was not only protect their inherent right, but regain the rights that had been violates. They became victims.",
            "Dr. King reinforced the his position mentioned in the former part, clarifying the necessity and urgency of the struggle. This encouraged people to take actions to change the inequality and discrimination right away, resulting in lasting influence and extensive impact on society. Then, Dr. King highlighted the potential results of ignoring the sound of African-American.",
            "This is important because it demonstrates that the speech is not only for those who are experiencing unfair treatment, but it also asks traditional American society to realize their fault and change their attitudes towards African-American. Next, Dr. King emphasized the principle of non-violation.",
            "Those things were combined and made people recognize that Dr. King was a leader who devoted himself to the conflict between the society and knew what was acceptable method to strive. He was a courageous and level-headed pioneer. In the next part, Dr. King illustrated his ambition and determination through parallelism: as long as one compatriot can't get what they deserve, his fighting wouldn't stop.",
            "He restated the insulted circumstances of African-American to evoke the excitement of crowds and encourage them rise up. Finally, the speech turned into its most famous section: parallelism beginning with \"I have a dream\". The anger were transformed into the motivation to continuously struggle. Also, Dr. King expressed his expectation, which conceived listeners that their effort was not useless and would consequently lead to their better future.",
            "This slogan was not only based on the rights of African-American, but it also came from the wish of a stronger and more desirable America, elevating national contradictions to the perspective of national development and coinciding with the core of American social construction: fairness and freedom.",
        ],
    },
    {
        "name": "label coverage",
        "criterion": 3,
        # Two inputs aimed at each label, from my unit 7 calibration:
        # 1-2 human, 3-4 unsure, 5-6 AI.
        "texts": [
            "I missed the bus again. Third time this week, and honestly? I'd stopped caring by Wednesday. The driver, a guy with a moustache like a push broom, saw me running and just kept going. So I walked. Forty minutes in the rain, past the laundromat that always smells like burnt sugar.",
            "My grandmother kept her buttons in a rusted Danish cookie tin. Every Sunday I would tip them out across the rug and sort them by some private logic of color and smell. She never asked what the system was. I'm not sure I knew either.",
            "I like my school. My teacher is very kind. Every day I study English and math. After school I go home and help my mother cook dinner.",
            "In today's fast-paced world, technology plays an important role in our daily lives. It helps us communicate, work, and learn more efficiently. However, it is important to use technology responsibly. By doing so, we can enjoy its many benefits while avoiding its potential drawbacks.",
            "Social media has become an important part of modern society. It allows people to connect with friends and family. It also provides a platform for sharing information and ideas. However, it is important to be aware of the potential risks associated with social media use.",
            "Regular exercise is important for maintaining good health. It helps to strengthen the heart and improve overall fitness. In addition, exercise can help to reduce stress and improve mental health. It is important to find an activity that you enjoy so that you can stay motivated.",
        ],
    },
    {
        "name": "bad input",
        "criterion": 5,
        # The four cases criteria.md #5 names. Each must come back 400 with a
        # non-empty message, and leave no decision entry in the log.
        "bodies": [
            {"creator_id": "eval_bad_missing"},
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "   \n\t  ", "creator_id": "eval_bad_whitespace"},
            {"text": "a" * 5001, "creator_id": "eval_bad_toolong"},
        ],
    },
    # Criterion 4 (appeals) needs a submission and then an appeal against the
    # content_id that came back, so it lives in appeal_eval.py instead.
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
