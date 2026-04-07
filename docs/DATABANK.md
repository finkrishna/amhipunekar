# AmhiPunekar — DataBank Contribution Guide

## The Standard

Every entry must pass this test:

> A real Punekar from the old Peths (Sadashiv, Narayan, Kasba) reads this and says: **"Haan. Exactly. This is us."**

Not: "Haha funny Punekar thing."
Not: "This could be from any sharp Indian city."

**Specifically Pune. Specifically Peth. Specifically this register.**

---

## Entry Schema

```json
{
  "id": "DB-TYPE-NNN",
  "type": "patya | proverb | pula | journalism | contemporary | institution | vocabulary",
  "text_original": "The actual text in original language/script",
  "text_transliterated": "Roman script if original is Devanagari, else null",
  "text_translation": "English translation if needed, else null",
  "source": "Source work, publication, or context",
  "source_url": "URL if available, else null",
  "topics": ["keyword1", "keyword2"],
  "tone": "sardonic | dry | warm | demolition | philosophical | nostalgic | resigned",
  "signal": "One sentence: what makes this specifically Puneri",
  "score": 0
}
```

---

## Entry Types

### patya
Puneri Patya — the legendary hand-painted signboards of Pune. Shop notices, housing society boards, house door signs, restaurant notices.

**The gold standard:** The sign assumes you are probably wrong before you have done anything. It pre-empts, prohibits, and instructs with complete authority and zero warmth.

**High value sub-genres:**
- Housing society notice boards (highest signal)
- Old Peth area shop signs
- Door/nameplate signs from Sadashiv/Narayan Peth
- Restaurant and tapri notices

### proverb
Marathi Mhani (proverbs) — especially those with sardonic, deflationary, or philosophically sharp quality.

**Requirements:**
- Must include deployment context: when would a Punekar use this?
- Prefer proverbs that deflate pomposity, name incompetence, or describe asymmetric transactions
- Note if specifically Pune/Desh region vs general Marathi

### pula
P.L. Deshpande quotes and observations.

**CRITICAL RULE:** Every PuLa entry must have a verifiable source — specific work title (e.g., "Asa Mi Asami", "Vyakti ani Valli"). No unverified attributions. A fabricated PuLa quote is worse than no entry at all.

**Best sources:**
- Wikiquote: en.wikiquote.org/wiki/P._L._Deshpande
- Specific book attributions from verified Marathi literary sites

### journalism
Tilak, Agarkar, Gokhale — the intellectual-political backbone of Pune.

**What to look for:**
- Argumentative structure — how Pune intellectuals build a case
- The rhetorical move of using history to demolish a current argument
- The Agarkar/Tilak tension: social reform vs political freedom

### contemporary
Reddit r/pune, Twitter/X, YouTube comments — the living Puneri voice.

**Requirements:**
- Must be authentically Puneri, not generic Indian internet humour
- Historically grounded + currently annoyed = high signal
- Anonymise all usernames

### institution
Cultural lore around specific Pune institutions — Chitale Bandhu, Balgandharva, ABC bookshop, Fergusson College, Irani cafes.

**Focus:** How Punekars talk about these places, not just what they are.

### vocabulary
Single words or short phrases encoding the Puneri register.

**Already in DataBank (do not resubmit):**
खोचक, टोमणा, अगाऊ, TTMM, Aawraa, Ghanta, Lai Bhaari, मखलाशी, उफराटा, पाल्हाळ, झोंबणारे, निरुत्तर, निष्प्रश्न, खापर फोडणे, कोडगेपणा, काय हो

---

## Rejection Criteria

Reject before submitting if:

- [ ] It could come from Mumbai, Nagpur, or anywhere else equally
- [ ] It requires explanation to land (Puneri wit never explains itself)
- [ ] It is generic "funny Indian" content
- [ ] For PuLa: no verifiable source work cited
- [ ] It punches at specific communities harmfully
- [ ] It feels performed rather than observed
- [ ] The signal is "sharp/funny" rather than "specifically Puneri"

---

## How to Submit

**Via GitHub PR:**
1. Fork the repo
2. Add your entries to the appropriate JSON file in `databank/`
3. Run the validation script: `python scripts/validate_databank.py`
4. Submit a PR with a brief note on your sources

**Via web form (Phase 3):**
The web app will have a submission form with community rating before entries are accepted.

---

## Scoring Guide

Scores are assigned by maintainers after community review:

| Score | Meaning |
|-------|---------|
| 9-10 | Unmistakably Pune. High signal across multiple dimensions. |
| 7-8 | Clearly Puneri. Strong signal. Minor gaps in specificity. |
| 5-6 | Authentically Marathi but not specifically Pune. |
| 3-4 | Generic. Weak signal. Needs work. |
| 1-2 | Caricature or incorrect. Will be rejected. |
| 0 | Actively harmful. Rejected immediately. |

---

## The Question to Ask Yourself

Before submitting any entry, ask:

**Would Tatya deploy this? Would it sound natural in his voice? Or would it sound like an AI doing an impression of Tatya?**

If the latter — don't submit it.
