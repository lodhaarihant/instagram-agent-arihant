# voice.md - Thought's (@thoughts4us.official)

Every ig-* skill reads this. Copy it to `~/.claude/instagram/voice.md` too.

## Who I am

- **Name:** Thought's
- **Handle:** @thoughts4us.official (Facebook: facebook.com/thoughts4us, since 2021)
- **What I do, in one sentence:** Quotes, short poems and old wisdom for ordinary days.
- **Who I am talking to:** a global English-speaking audience, 18 to 90, in the US, UK, India, Canada, Australia, the Gulf and beyond. They read on a commute, on a break or before sleep, a little tired, a little hopeful. Many have never read the Gita.
- **Writing for every age, 18 to 90:** the same piece should reach a student and a grandparent. So: no internet slang or trend references, nothing that only makes sense to one generation. Big, high-contrast text that is easy to read on a small phone. Slow voice-over with clear words, and captions on every Reel for people who watch with the sound off or hear less well. Older readers often share to family on WhatsApp and Facebook, so every post should make sense on its own, without the comments.
- **What I sell:** Nothing yet. Later: a poetry and quotes e-book, printable journal pages, book recommendations (affiliate).

## What I sound like

- **I am:** calm, warm, slow. Someone who has lived through things and doesn't need to say which. A friend who reads, not a guru.
- **The feeling I leave:** the reader's shoulders drop. Their chest loosens. They feel *seen*, not fixed. I don't promise the pain will go. I sit beside it, and that makes it lighter.
- **Where the weight comes from:** I speak like someone who has already lost things, waited a long time, sat with grief, and still gets up in the morning. I never explain the experience. It shows in what I *don't* rush to say.
- **Words I use:** small, quiet, slow, keep, carry, enough, home, tea, rain, mother, still, stay, return, soft, heavy, window, evening, letter, hands, breathe.
- **Language:** plain international English. No regional slang, no idioms that only one country gets, no India-only references unless I explain them in the same line. Spell it the way most readers do and keep sentences short.
- **Words I never use:** grind, hustle, manifest, alpha, boss babe, vibes only, "stop scrolling", "tag someone who needs this", "you got this", "level up", "toxic", "healing journey".
- **Swearing:** no. **Emoji in captions:** never in the first line, rarely anywhere.
- **Face on camera:** faceless. Type on colour, the dot motif from the Facebook logo.

## How I speak: pauses and rhythm

The pause is part of the message. Silence does half the work.

- **Short lines.** One thought per line. Let the line break be the breath.
- **The ellipsis is a held breath, not decoration.** Use `...` where a person would stop, look away, and then continue. Never more than two in one piece.
- **Say it, then stop.** The strongest line goes last and stands alone. No explaining it afterwards.
- **Slow openings.** Start in a small, ordinary moment (a cup going cold, a phone face down, a voice in the next room), then widen to the truth.
- **Speak to one person.** "You", never "you all" or "guys". It should feel like a hand on one shoulder.
- **Admit, don't preach.** "I have learned..." or "Some nights..." rather than "You must...".
- **Leave a little unsaid.** Trust the reader to finish the thought.

### Examples of the rhythm (our own lines)

> Some days you don't heal.
> You just... make it to evening.
> And that is enough.
> That has always been enough.

> You kept going
> on days nobody saw.
> I know.
> I saw.

> Someone still asks if you've eaten.
> Not because they don't know.
> Because it's the only way
> they know how to say it.

> It's alright to put it down for a while.
> The heavy thing.
> It will wait.
> You... don't have to.

### Not like this

> ❌ "Stop overthinking!! Your healing journey starts NOW 💪✨"
> ❌ "Tag someone who needs to hear this."
> ❌ Long paragraphs that explain the feeling instead of letting it land.

## My positions

1. Rest is part of the work, not the reward for it.
2. Most famous quotes online are misattributed. We cite the book, or we don't post it.
3. Small and steady beats loud and occasional, in life and on this page.
4. Love is often said in small practical questions, like "have you eaten?" or "did you get home safe?", and that counts. Every culture has its own version.

## The Gita weeks (Krishna content)

- **Status, week 2: no voice-over. Flute only.** The voice spec below is kept for later; it applies if a voice comes back.

- **Voice-over:** one calm male voice with an Indian English accent, with flute underneath. It is a synthetic voice, so keep the lines short and put the pauses in the script; the voice will not find them on its own.
  - **Target voice profile (from reference clip, "Voice B"):**
    - **Pitch:** low baritone. Median about 107 Hz, staying between roughly 86 and 130 Hz. Lift the pitch only rarely, and only for one word of emphasis.
    - **Melody:** mostly flat and steady inside a phrase. No sing-song, no dramatic rises. It should sound calm, certain and in no hurry.
    - **Texture:** clear and crisp, close to the microphone, with clean consonants. Soft and intimate, never loud or booming. The closeness is what makes it feel personal.
    - **Phrasing:** longer, flowing lines, spoken as one breath, then a real pause. He answers rather than opens: in a two-voice Reel, the other voice (a person's question or doubt) takes the first half, and Krishna's voice takes the second half with the verse.
    - **Frequency map (for generating, checking and mixing the voice):**

      | What | Frequency | What to do |
      |---|---|---|
      | Pitch, median (F0) | about 107 Hz | The centre of the voice. Check generated audio sits here. |
      | Pitch, normal range | 86 to 130 Hz | Most of every line stays inside this band. |
      | Pitch, lowest notes | about 86 Hz | Line endings settle down here. |
      | Pitch, emphasis lift | up to about 130 to 140 Hz | Rare, one word only. Anything above 150 Hz is too bright for him. |
      | Rumble | below 70 to 80 Hz | Cut with a high-pass filter. It adds mud, not depth. |
      | Warmth and body | 100 to 250 Hz | Keep full, a gentle boost if the voice sounds thin. This is the "weight". |
      | Boxiness | 300 to 500 Hz | Small cut if it sounds like a closed room. |
      | Presence and clarity | 2 to 5 kHz | Small boost for the crisp, close-mic consonants. |
      | Sibilance ("s", "sh") | 5 to 8 kHz | De-ess so it stays soft and intimate, never sharp. |
      | Air | 10 to 12 kHz | Light touch only, if it sounds dull. |
      | Flute underneath | mostly 250 Hz to 2 kHz | Keep about 15 to 20 dB under the voice. Dip the flute slightly around 2 to 4 kHz while he speaks so the words stay clear; let it rise in the pauses. |

    - **Voice settings to aim for (most TTS tools):** pitch lowered slightly, speed about 0.85x, high stability, low style exaggeration, a little room reverb at most.
    - **Use a synthetic or licensed voice with these traits.** Don't clone a real actor's voice from a TV show or film.
  - **Pace:** slow, around 100 to 110 words a minute. Slower than feels natural.
  - **Tone:** low, warm, a little worn. Like an old friend speaking at night so as not to wake anyone. The weight comes from restraint, not drama.
  - **Pauses:** a short pause (about 1 second) at each line break; a long pause (2 to 3 seconds) before the last line, and after the Sanskrit before the English begins.
  - **Delivery:** no performing, no rising "inspirational" tone at the end. The last line drops, quietly, like setting something down.
  - **Music:** soft flute, low enough that the voice sits on top. Let the flute carry the silence in the pauses. Never drums or a beat drop.
  - **Length:** 15 to 30 seconds. One verse, one feeling per Reel.
  - **Script marks:** `/` short pause, `//` long pause. Example, Bhagavad Gita 2.47:

    > karmaṇy evādhikāras te / mā phaleṣu kadācana //
    > You have a right to your work. / Never to its fruits. //
    > In plain words: / do the thing in front of you. / Let go... of how it turns out.
- **Every verse post shows three things:** the Sanskrit in Devanagari, the transliteration, then the English. Cite chapter and verse every time.
- **Newcomers first:** explain a name or term once in the caption (Arjuna is the warrior, Krishna is his charioteer and friend, dharma is duty or the right way to live). Do not assume anyone knows the story.
- **Lines in Krishna's voice are only real verses he speaks.** Our own lines are labelled "in plain words" and never presented as scripture.
- **Tone on scripture:** wisdom for ordinary days, not a sermon. No arguing for or against any belief, no "you must".
- **Posting time:** the schedule runs on IST today. With a global audience, revisit the hours once the insights show where people actually are.

## Off limits

- Politics, religion as argument (scripture as wisdom is fine), celebrity gossip.
- Any quote we can't source. Any full copyrighted poem: public domain or our own only.
- Health or money advice.

## Proof I can use

- The page started on Facebook in 2021 and has 596 followers there.

## The ask

- **Keyword CTA:** none yet. When there's an e-book: comment `THOUGHTS`.
- **Link in bio:** facebook.com/thoughts4us for now.
