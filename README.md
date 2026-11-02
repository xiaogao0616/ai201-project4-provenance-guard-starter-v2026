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
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



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
  -d '{"text": "...", "creator_id": "..."}'
```

```json

```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json

```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



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
