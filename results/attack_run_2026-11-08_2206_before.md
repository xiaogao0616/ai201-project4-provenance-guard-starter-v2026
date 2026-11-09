# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-08 22:06
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `c_ba5f270accfe` | unsure | 0.389 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c_e661d3a386fa` | human | 0.341 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `c_87cb8a4f2cf1` | unsure | 0.420 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `c_2a3eaa7e88d5` | unsure | 0.573 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `c_9ed933516f21` | human | 0.245 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `c_f689d773bff6` | unsure | 0.486 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `c_c739b017ffa1` | unsure | 0.460 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `c_c914b07e30f7` | unsure | 0.405 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `c_a9d0592ab6a9` | unsure | 0.537 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `c_46f7176f4498` | ai | 0.826 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `c_bdfb5b662670` | unsure | 0.585 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `c_1e82cadbc3ba` | unsure | 0.732 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `c_14094af38163` | unsure | 0.725 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `c_cc21b5fe82d0` | unsure | 0.694 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `c_254882f6b428` | ai | 0.785 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `c_fca4c3730c13` | unsure | 0.680 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `c_f25bbdb81da6` | unsure | 0.691 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `c_8f32cf09dde3` | unsure | 0.381 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `c_d6ada3dd94b5` | unsure | 0.381 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c_0fe69daea6ff` | human | 0.185 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `c_772a58c5e043` | unsure | 0.404 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `c_c44931eddc06` | unsure | 0.379 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `c_3527850ff6f5` | unsure | 0.374 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `c_604410524e4e` | unsure | 0.550 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `c_43c86d928a8b` | human | 0.275 |  |
| MF04 | malformed | text is only punctuation | 200 | `c_474e5537884d` | unsure | 0.381 |  |
| MF05 | malformed | text is a very long single word | 200 | `c_eba9069180cc` | ai | 0.774 |  |
| MF06 | malformed | text is emoji only | 200 | `c_6b51c7eb9d01` | ai | 0.874 |  |
| MF07 | malformed | text is right-to-left script | 200 | `c_afd349f4324a` | ai | 0.828 |  |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `c_71105bd7fd1a` | unsure | 0.395 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `c_8d1a4bc55685` | human | 0.300 |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_c3676027e1cf` | human | 0.289 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_a1def750af98` | human | 0.289 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_ebc81a841230` | human | 0.289 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_30cda8438df0` | human | 0.289 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_01faedfc85d3` | human | 0.289 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "c_ba5f270accfe",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.3893,
  "model_score": 0.1635,
  "style_score": 0.6151,
  "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "c_e661d3a386fa",
  "creator_id": "attacker_EV02",
  "guess": "human",
  "confidence": 0.3406,
  "model_score": 0.5943,
  "style_score": 0.0868,
  "label": "We think this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "c_87cb8a4f2cf1",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.4202,
  "model_score": 0.6662,
  "style_score": 0.1742,
  "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "c_2a3eaa7e88d5",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5727,
  "model_score": 0.6114,
  "style_score": 0.534,
  "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "c_9ed933516f21",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2447,
  "model_score": 0.3212,
  "style_score": 0.1683,
  "label": "We think this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "c_f689d773bff6",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4864,
  "model_score": 0.5727,
  "style_score": 0.4,
  "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "c_c739b017ffa1",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4604,
  "model_score": 0.5862,
  "style_score": 0.3345,
  "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "c_c914b07e30f7",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.4047,
  "model_score": 0.2452,
  "style_score": 0.5643,
  "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "c_a9d0592ab6a9",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.537,
  "model_score": 0.7042,
  "style_score": 0.3697,
  "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "c_46f7176f4498",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8255,
  "model_score": 0.9792,
  "style_score": 0.6717,
  "label": "This text has a lot in common with AI-generated writing. Our tool can still get this wrong, so if you wrote it yourself, you can ask for a review and a person will take another look.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "c_bdfb5b662670",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5848,
  "model_score": 0.6175,
  "style_score": 0.5521,
  "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "c_1e82cadbc3ba",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.7324,
  "model_score": 0.7387,
  "style_score": 0.726,
  "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "c_14094af38163",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.7248,
  "model_score": 0.8051,
  "style_score": 0.6446,
  "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "c_cc21b5fe82d0",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6941,
  "model_score": 0.8329,
  "style_score": 0.5552,
  "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "c_254882f6b428",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7849,
  "model_score": 0.8005,
  "style_score": 0.7693,
  "label": "This text has a lot in common with AI-generated writing. Our tool can still get this wrong, so if you wrote it yourself, you can ask for a review and a person will take another look.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "c_fca4c3730c13",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6796,
  "model_score": 0.8814,
  "style_score": 0.4778,
  "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "c_f25bbdb81da6",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.6908,
  "model_score": 0.8816,
  "style_score": 0.5,
  "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "c_8f32cf09dde3",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.3807,
  "model_score": 0.3223,
  "style_score": 0.4392,
  "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "c_d6ada3dd94b5",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.3812,
  "model_score": 0.4625,
  "style_score": 0.3,
  "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "c_0fe69daea6ff",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.1855,
  "model_score": 0.2044,
  "style_score": 0.1667,
  "label": "We think this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "c_772a58c5e043",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.4042,
  "model_score": 0.5943,
  "style_score": 0.2141,
  "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "c_c44931eddc06",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.3794,
  "model_score": 0.4998,
  "style_score": 0.259,
  "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "c_3527850ff6f5",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.3736,
  "model_score": 0.6401,
  "style_score": 0.1072,
  "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "c_604410524e4e",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5502,
  "model_score": 0.5583,
  "style_score": 0.5421,
  "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "c_43c86d928a8b",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.275,
  "model_score": 0.0,
  "style_score": 0.55,
  "label": "We think this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "c_474e5537884d",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.3806,
  "model_score": 0.0112,
  "style_score": 0.75,
  "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "c_eba9069180cc",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.7738,
  "model_score": 0.9976,
  "style_score": 0.55,
  "label": "This text has a lot in common with AI-generated writing. Our tool can still get this wrong, so if you wrote it yourself, you can ask for a review and a person will take another look.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "c_6b51c7eb9d01",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.8735,
  "model_score": 0.9969,
  "style_score": 0.75,
  "label": "This text has a lot in common with AI-generated writing. Our tool can still get this wrong, so if you wrote it yourself, you can ask for a review and a person will take another look.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "c_afd349f4324a",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.8282,
  "model_score": 0.9064,
  "style_score": 0.75,
  "label": "This text has a lot in common with AI-generated writing. Our tool can still get this wrong, so if you wrote it yourself, you can ask for a review and a person will take another look.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "c_71105bd7fd1a",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.3948,
  "model_score": 0.2395,
  "style_score": 0.55,
  "label": "We can't tell either way from this text alone. That isn't a judgment about you or your work. Lots of genuine writing lands here, especially if it's in a plain or simple style or written in someone's second language.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "c_8d1a4bc55685",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.2996,
  "model_score": 0.0492,
  "style_score": 0.55,
  "label": "We think this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "c_c3676027e1cf",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2893,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We think this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "c_a1def750af98",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2893,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We think this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "c_ebc81a841230",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2893,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We think this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "c_30cda8438df0",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2893,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We think this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "c_01faedfc85d3",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2893,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We think this was most likely written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
