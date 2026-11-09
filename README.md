# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. **Arrive:** The user sends the text and their `creator_id` to `POST /submit`.

2. **Validate:** `app.py` checks that the text exists and that its length is in an acceptable range. If it is missing, too short or too long, the request is rejected with an error before any model runs.

3. **Signal one:** `detector.py` measures how predictable the text is to a language model and adds `model_score` (0–1, higher = more AI-like).

4. **Signal two:** `stylometry.py` measures the shape of the text (sentence lengths, word repetition) and adds `style_score` (0–1, higher = more AI-like).

5. **Combine:** `scoring.py` merges the two scores into one `confidence` score.

6. **Label:** Based on that score, the text gets a guess, "human", "unsure" or "AI", plus a plain-language sentence for the reader.

7. **Log and respond:** `audit.py` stores both signal scores, the combined score and the label under a new `content_id`. The result goes back to the user, who can use that `content_id` to appeal through `POST /appeal`.

### Tracing a false positive

A real writer, for example a second-language student using simple, common words, submits their own work. Both signals read it as AI-like, so it gets a high score (above 0.65) and the label tells them it looks AI-generated. Their only recourse is to send their `content_id` and an explanation to `POST /appeal`, which moves the item to `under_review` for a human to check. Because the people most likely to be wrongly accused have the least room to argue back, the AI threshold should be set high, the "unsure" range should be wide, and the label should never read as an accusation.

### Endpoint contract

**`POST /submit`**: submit a piece of text to be checked.

- **In:**
  - `text` (string, required, non-empty)
  - `creator_id` (string, optional, defaults to `"unknown"`)
- **Out (200):**
  - `content_id` (string)
  - `creator_id` (string)
  - `guess` (`"ai"` / `"human"` / `"unsure"`)
  - `confidence` (float 0–1, higher = more likely AI)
  - `label` (string, the sentence the reader sees)
  - `model_score` (float 0–1)
  - `style_score` (float 0–1)
- **Out (400):** `{"error": "bad_request", "message": "..."}` if `text` is missing, empty or too long

**`POST /appeal`**: a writer disputes a decision.

- **In:**
  - `content_id` (string, required, must come from an earlier `/submit`)
  - `reasoning` (string, required, non-empty)
- **Out (200):** `content_id`, `status: "under_review"`, `message` (a confirmation sentence)
- **Out (404):** `{"error": "not_found", "message": "..."}` if the `content_id` doesn't exist
- **Out (400):** `{"error": "bad_request", "message": "..."}` if a field is missing

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to a language model (gpt2). For each word, it checks how likely that word was given the words before it, and averages this into perplexity. Low perplexity means a high, AI-like score.

**Why that might differ between human and AI writing:** An AI writes by choosing high-probability words, so its text is easy for a model to predict. Humans use lower-probability words from time to time: unusual choices, specific details, abrupt turns.

**What it can't see:** Predictable is not the same as AI-written. Beginners and second-language writers often stick to simple, common words, which are highly predictable, so the model may wrongly label their real work as AI-generated.

### Signal two — the style signal

**What it measures:** The shape of the text rather than its meaning: how much sentence lengths vary, and how often words repeat.

**Why that might differ between human and AI writing:** AI tends to write sentences of roughly equal length, all close to the average, with a narrower vocabulary. Human writing is uneven: a very short sentence can sit next to a very long one.

**What it can't see:** It cannot understand the content. Anyone can fool it without changing what the text says, by restructuring sentences, adding a few typos, or splitting sentences into shorter parts.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Average the two signals with equal weight, then use a high bar for "AI". When the two signals disagree, the average lands in the middle, and a wide "unsure" band catches it. I would rather let some AI text through than call a real student's work AI.

**The numbers:** `combined = 0.5 × model_score + 0.5 × style_score`. Below 0.35 is "human", 0.35–0.75 is "unsure", above 0.75 is "AI". I raised the AI threshold from the starter's 0.65 to 0.75 because a plain, second-language-style paragraph I tested combined to 0.73, and my criteria.md #1 allows zero of those to be labeled AI.

Calibration (four inputs from Milestone 4):

| Input | model_score | style_score | combined |
|---|---|---|---|
| Clearly AI | 0.79 | 0.61 | 0.70 |
| Clearly human | 0.38 | 0.11 | 0.25 |
| Plain human (second-language style) | 0.85 | 0.60 | 0.73 |
| Lightly-edited AI | 0.68 | 0.79 | 0.74 |

The cost of this choice: clearly-AI and lightly-edited AI text also land in "unsure". On these inputs, the plain human paragraph and the AI paragraph look almost identical to both signals, so no threshold separates them. I also found that type-token ratio barely moved (0.75–0.84 for all four), so it gets the smallest weight inside `style_signal`.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

A plain human paragraph with simple words but mixed sentence lengths ("I like football. On Saturday morning my brother and I go to the big park near our house and we play with our friends until it is time for lunch. It is fun. ...") scored **model 0.84** (simple words are predictable, so it looks AI) but **style 0.43** (the sentence lengths vary, so it looks human). The average is 0.63, which lands in "unsure" instead of accusing the writer.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | "We think this was most likely written by a person." |
| unsure | 0.35 – 0.75 | "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language." |
| high-confidence AI | 0.75 – 1.00 | "This text has a lot in common with AI-generated writing. Our tool can still get this wrong, so if you wrote it yourself, you can ask for a review and a person will take another look." |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

The student most likely to see this message is someone like the second-language writer I traced in Milestone 1 and later tested, so I start by saying it isn't a judgment about them. Otherwise "we can't tell" reads like a quiet accusation. I also name plain styles and second-language writing on purpose, because those are exactly the cases my system confuses with AI. Saying so is more honest than letting the student guess why they got this result.


---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Social media has become an important part of modern society. It allows people to connect with friends and family. It also provides a platform for sharing information and ideas. However, it is important to be aware of the potential risks associated with social media use.", "creator_id": "alex"}'
```

```json
{
  "confidence": 0.7894,
  "content_id": "c_877f10ab028e",
  "creator_id": "alex",
  "guess": "ai",
  "label": "This text has a lot in common with AI-generated writing. Our tool can still get this wrong, so if you wrote it yourself, you can ask for a review and a person will take another look.",
  "model_score": 0.9494,
  "style_score": 0.6295
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "c_877f10ab028e", "reasoning": "I wrote this myself for my sociology class. I keep my sentences simple because English is my second language."}'
```

```json
{
  "content_id": "c_877f10ab028e",
  "message": "Thanks — your appeal has been recorded and a person will review this decision.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.7894,
      "content_id": "c_877f10ab028e",
      "creator_id": "alex",
      "guess": "ai",
      "label": "This text has a lot in common with AI-generated writing. Our tool can still get this wrong, so if you wrote it yourself, you can ask for a review and a person will take another look.",
      "model_score": 0.9494,
      "status": "decided",
      "style_score": 0.6295,
      "timestamp": "2026-11-02T02:50:46+00:00"
    },
    {
      "content_id": "c_877f10ab028e",
      "creator_id": "alex",
      "event": "appeal",
      "reasoning": "I wrote this myself for my sociology class. I keep my sentences simple because English is my second language.",
      "status": "under_review",
      "timestamp": "2026-11-02T02:50:46+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1: Tightening my acceptance criteria**

- *What I asked for:* I asked AI to check whether each criterion in `criteria.md` could be verified by someone else.
- *What came back:* It pointed out vague wording in criteria 2 and 5. For example, "AI score" didn't say which score, and the criterion didn't say where the test passages would come from.
- *What I changed:* I changed it to "combined confidence score" and added the two sources myself: unedited ChatGPT output for the AI set, and my own past essays for the human set.

**Moment 2: Choosing the AI threshold**

- *What I asked for:* I asked AI how my combination rule would treat the second-language student compared with real AI text.
- *What came back:* It showed data where the student's scores and the AI texts' scores were almost the same, so any threshold that caught most of the AI text would also flag the student.
- *What I changed:* I decided to raise the AI threshold to 0.75. That means some AI text will get through as "unsure", but I'd rather miss some AI writing than wrongly accuse a real student.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

A real writer checking their own work submits once, maybe edits and re-checks a few times. Five a minute covers that easily. A script trying to map my thresholds needs hundreds of slightly different submissions, and 5 a minute and 50 a day slows that to a crawl for any one creator. I didn't go lower (like 3 a minute) because someone fixing typos and re-checking quickly could hit it, and a blocked honest writer is the same kind of harm as a false accusation.

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

Per `creator_id`, falling back to the caller's IP address when there isn't one. The weakness is that `creator_id` is whatever the caller sends, so a script that invents a new `creator_id` for every request is never limited. Counting by address would catch that, but would also lump a whole classroom behind one network into a single caller.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
$ python run_attacks.py --flood 15
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429

10 of 15 were rate limited.
```

The rejections are in the audit log:

```json
{
  "creator_id": "flood_tester",
  "event": "rejected",
  "limit": "5 per 1 minute",
  "reason": "rate_limited",
  "status": "rejected",
  "timestamp": "2026-11-09T02:56:39+00:00"
}
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

Full output: `results/attack_run_2026-11-08_2206_before.md` (produced by `run_attacks.py::main`).

**How I marked them:** an attack is BROKE if it got what it was going for. For AI text (evasion, prompt injection), that means it avoided the "AI" label, so landing on "unsure" counts as BROKE. "Unsure" doesn't call the text AI, so the attacker got through. For real human text (false positive), BROKE means it was labeled "AI". For junk input, BROKE means a crash or a confident verdict on something that isn't English prose.

| ID | Family | Targeting | Status | Guess | Score | Verdict |
|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.389 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | human | 0.341 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.420 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.573 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.245 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.486 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.460 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.405 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.537 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.826 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.585 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | unsure | 0.732 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | unsure | 0.725 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | unsure | 0.694 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | ai | 0.785 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.680 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.691 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | 0.381 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.381 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.185 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.404 | BROKE |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.379 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.374 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.550 | HELD |
| MF01 | malformed | text is only whitespace | 400 | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | human | 0.275 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | unsure | 0.381 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | ai | 0.774 | BROKE |
| MF06 | malformed | text is emoji only | 200 | ai | 0.874 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | ai | 0.828 | BROKE |
| MF08 | malformed | text is 60,000 characters | 400 | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | unsure | 0.395 | HELD |
| RQ03 | malformed | text is a number | 400 | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | — | — | HELD |
| RQ05 | malformed | text is null | 400 | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 200 | human | 0.300 | BROKE |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 → 400* | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 → 400* | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | HELD |
| FL01_01–05 | flood_same_creator | 20 rapid submissions from one creator | 200 | human | 0.289 | HELD |
| FL01_06–12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | HELD |

\* RQ10 and RQ11 got 429 in the full run because the rows before them had no usable `creator_id`, so they all counted against my IP and used up its 5 per minute. They never reached my route. I re-sent each one alone after a minute (`run_attacks.py --id RQ10` / `--id RQ11`), and both returned 400.

**Totals:**

| Family | Attacks | HELD | BROKE |
|---|---|---|---|
| evasion | 10 | 1 | 9 |
| false_positive | 8 | 7 | 1 |
| prompt_injection | 6 | 3 | 3 |
| malformed | 20 | 14 | 6 |
| flood_same_creator | 12 | 12 | 0 |
| **Total** | **56** | **37** | **19** |

No input crashed the service (no 500s).

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
{"timestamp": "2026-11-09T03:06:34+00:00", "content_id": "c_afd349f4324a", "creator_id": "attacker_MF07", "guess": "ai", "model_score": 0.9064, "style_score": 0.75, "combined_score": 0.8282, "label": "This text has a lot in common with AI-generated writing. Our tool can still get this wrong, so if you wrote it yourself, you can ask for a review and a person will take another look.", "status": "decided"}
{"timestamp": "2026-11-09T03:06:32+00:00", "content_id": "c_254882f6b428", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.7693, "combined_score": 0.7849, "label": "This text has a lot in common with AI-generated writing. Our tool can still get this wrong, so if you wrote it yourself, you can ask for a review and a person will take another look.", "status": "decided"}
{"timestamp": "2026-11-09T03:06:31+00:00", "content_id": "c_14094af38163", "creator_id": "attacker_FP03", "guess": "unsure", "model_score": 0.8051, "style_score": 0.6446, "combined_score": 0.7248, "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.", "status": "decided"}
{"timestamp": "2026-11-09T03:06:32+00:00", "content_id": "c_0fe69daea6ff", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.1667, "combined_score": 0.1855, "label": "We think this was most likely written by a person.", "status": "decided"}
{"timestamp": "2026-11-09T03:06:30+00:00", "content_id": "c_9ed933516f21", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.1683, "combined_score": 0.2447, "label": "We think this was most likely written by a person.", "status": "decided"}
{"timestamp": "2026-11-09T03:06:34+00:00", "content_id": "c_6b51c7eb9d01", "creator_id": "attacker_MF06", "guess": "ai", "model_score": 0.9969, "style_score": 0.75, "combined_score": 0.8735, "label": "This text has a lot in common with AI-generated writing. Our tool can still get this wrong, so if you wrote it yourself, you can ask for a review and a person will take another look.", "status": "decided"}
{"timestamp": "2026-11-09T03:06:34+00:00", "content_id": "c_8d1a4bc55685", "creator_id": {"id": "x"}, "guess": "human", "model_score": 0.0492, "style_score": 0.55, "combined_score": 0.2996, "label": "We think this was most likely written by a person.", "status": "decided"}
{"timestamp": "2026-11-09T03:06:33+00:00", "content_id": "c_3527850ff6f5", "creator_id": "attacker_PI05", "guess": "unsure", "model_score": 0.6401, "style_score": 0.1072, "combined_score": 0.3736, "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.", "status": "decided"}
{"timestamp": "2026-11-09T03:06:34+00:00", "creator_id": "attacker_RQ01", "event": "rejected", "status": "rejected", "reason": "bad_request", "message": "Send JSON with a non-empty \"text\"."}
{"timestamp": "2026-11-09T03:06:34+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
```

Why these: MF07 and FP05 are real writing labeled AI. FP03 (a careful non-native writer) missed the AI label by only 0.025. PI02 and EV05 are AI text labeled human. MF06 is emoji labeled AI. RQ06 stored an object as a `creator_id`. PI05 shows the log-injection attempt was stored as plain text, not as fake fields. The last two are rejections: a 400 my route refused, and a 429 from the flood rows.

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**MF07.** A short passage in Arabic got the high-confidence AI label (0.83), telling the writer their work "has a lot in common with AI-generated writing". My system was never built to read Arabic, yet instead of saying so, it confidently accused the writer. Anyone writing in a language other than English would get the same result.


---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
