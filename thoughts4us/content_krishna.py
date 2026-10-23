#!/usr/bin/env python3
"""
Week 2 for @thoughts4us.official: the Bhagavad Gita, one theme a day.

Same shape as week 1 (20 posts a day, one an hour, 05:00 to 00:00 IST), written to
schedule/week2.json. Run it, then render_krishna.py.

  Sat  Karma          Sun  The mind and rest   Mon  Staying steady   Tue  The soul
  Wed  Devotion       Thu  Knowledge           Fri  Peace

Rules, same as week 1:
- Every verse is cited by chapter and verse. The wording is ours: a short, plain
  rendering that stays close to the Sanskrit, not a quote of any one translation.
  Check it against the translation you prefer before posting.
- Lines in Krishna's voice are real verses he speaks in the Gita, nothing invented.
  The 07:00 and 19:00 reels, plus the 05:00 and 00:00 stories, are read aloud.
- Our own lines (15:00, 22:00, the poems, the stories) are marked "in plain words" or
  carry no credit, so they never read as scripture.
"""
import datetime as dt
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = json.load(open(os.path.join(HERE, "config.json")))
TZ = CONFIG["utc_offset"]
START = dt.date(2026, 10, 24)           # Saturday

VOICE_OVER = False       # True reads the English aloud on the 07:00 and 19:00 reels and the 05:00 and 00:00 stories. Off: flute only.

G = "#bhagavadgita #krishna #gitaquotes"
GK = "#bhagavadgita #krishna #karmayoga"

DAYS = []


def verse(lines, credit, hook, body, ask, tags=G, voice=False):
    return {"lines": lines, "credit": credit, "hook": hook, "body": body, "ask": ask, "tags": tags, "voice": voice}


def plain(lines, hook, body, ask, tags="#gitawisdom #krishna #dailywisdom"):
    return {"lines": lines, "credit": "in plain words", "hook": hook, "body": body, "ask": ask, "tags": tags, "voice": False}


def poem(lines, hook, body, ask, tags="#poetry #shortpoems #krishna"):
    return {"lines": lines, "credit": "", "hook": hook, "body": body, "ask": ask, "tags": tags, "voice": False}


def deck(cover, sub, stake, slides, recap, cta, hook, body, ask, tags):
    return {"cover": cover, "sub": sub, "stake": stake, "slides": slides, "recap": recap, "cta": cta,
            "hook": hook, "body": body, "ask": ask, "tags": tags}


# ============================================================ DAY 1  Saturday  KARMA
DAYS.append({
    "theme": "Karma",
    "reel_am7": verse(
        ["You have a right to your work,", "but never to its fruits.", "Do not let the reward be your reason,", "and do not cling to doing nothing."],
        "Bhagavad Gita 2.47",
        "Krishna's most quoted line, and the one most of us only read half of.",
        ["New here? The Gita is a conversation between Arjuna, a warrior, and Krishna, his charioteer and friend, on the eve of a war. This is the line people quote most.", "It says the effort is yours and the result never was. Then it adds the second half: do not hide in doing nothing."],
        "Which half did you need today? Tell me below.", GK, voice=True),
    "card": {"quote": "Do the work that is yours to do. Action is better than doing nothing.", "author": "Krishna to Arjuna", "source": "Bhagavad Gita 3.8", "sa": [0],
             "hook": "Arjuna sat down in the middle of the battlefield and said he couldn't do it. This is part of Krishna's answer.",
             "body": ["Not a pep talk. A reason to take one small step, even when the whole thing feels too big.", "The verse goes on: even keeping the body going takes some work."],
             "ask": "What is one small step you've been putting off? Tell me below.", "tags": GK},
    "story_quote": ("Stay steady, do your work,\nand let go of attachment\nto success or failure.", "Bhagavad Gita 2.48"),
    "reel_am11": verse(
        ["Better to do your own work", "imperfectly,", "than someone else's", "perfectly."],
        "Bhagavad Gita 3.35",
        "Krishna on comparison, in four short lines.",
        ["Verse 3.35. Your path has your name on it, even when it looks messier than the one next to you."],
        "Share this with someone who keeps comparing.", GK) | {"sa": [0]},
    "line": plain(
        ["Do the thing.", "Let go of the applause.", "Come back tomorrow", "and do it again."],
        "The Gita on work, in plain words.",
        ["Not a translation. The verses behind it are 2.47 and 3.8."],
        "Save it for Monday.", "#karmayoga #gitawisdom #dailywisdom"),
    "reel_pm19": verse(
        ["Whatever a great person does,", "others follow.", "Whatever standard they set,", "the world walks behind it."],
        "Bhagavad Gita 3.21",
        "Gita 3.21: what you do matters more than what you say.",
        ["Your family, your team and your little cousins are watching what you do, not what you tell them."],
        "Who learned something from watching you? Tell me below.", G, voice=True),
    "poem": poem(
        ["I stopped counting what I would get.", "The work grew quiet, and light.", "The days were no easier.", "I just stopped asking them for more."],
        "A short poem about doing the work and letting go of the result.",
        ["Our own words, inspired by Bhagavad Gita 2.47."],
        "Save it for the week you start something."),
    "noon": deck(
        "5 small ways to use the Gita at work", "No incense needed. Just a Saturday and a to-do list.",
        "The verses are 2,000 years old. The to-do list is yours.",
        [("Do the next task, not the whole list.", "", "2.47: you own the effort of this one thing."),
         ("Say what you did, not what you hoped.", "", "2.48: success and failure are the same weather."),
         ("Do the boring task before the shiny one.", "", "3.8: action beats thinking about action."),
         ("Stop checking how others are doing.", "", "3.35: their path is not your homework."),
         ("Be the person you want your team to copy.", "", "3.21: they watch you more than they listen.")],
        ["One task", "Honest report", "Boring first", "Eyes on your own", "Be the example"],
        "Save this. Use number 1 on Monday.",
        "5 small ways to use the Gita at work. Number 4 helps most.",
        ["Plain words, not translations, with the verse behind each one. Take what helps, ignore what doesn't."],
        "Which one will you try first? Tell me the number.", "#bhagavadgita #karmayoga #workwisdom"),
    "main": deck(
        "Gita 2.47, one phrase at a time", "The verse everyone quotes and few read slowly.",
        "Four phrases. Each one says something different.",
        [("You have a right to your work.", "2.47, part 1", "The effort is yours. Nobody can take it."),
         ("But not to its fruits.", "2.47, part 2", "The result depends on a hundred things you don't control."),
         ("Do not let the reward be your reason.", "2.47, part 3", "Work because it's worth doing. Anything extra is a bonus."),
         ("And do not cling to doing nothing.", "2.47, part 4", "The verse is not permission to quit. It says the opposite.")],
        ["Effort is yours", "Results are not", "Work for the work", "Don't quit"],
        "Share it with someone who is waiting for results.",
        "Gita 2.47 in four phrases. Most people only quote the second one.",
        ["Chapter 2, verse 47. Krishna says it to Arjuna on the battlefield, and it has been quoted ever since."],
        "Which phrase hits hardest? Comment its number.", GK),
    "morning": (["Get up, Arjuna.", "Be ready."], "Bhagavad Gita 2.37", [1]),
    "affirm": "Today I do my part\nand let go of the rest.",
    "choice": ("Effort", "Outcome"), "prompt": "One task you'll do today\nwithout needing applause?",
    "reminder": "Drink some water.\nThe work can wait two minutes.",
    "choice2": ("Start small", "Start big"),
    "fragment": "The seed doesn't watch the tree.\nIt just does its part.",
    "fill": "Finish this:\nToday I did my part by ___",
    "night": (["Yoga is", "skill in action."], "Bhagavad Gita 2.50", [1]),
})

# ============================================================ DAY 2  Sunday  THE MIND AND REST
DAYS.append({
    "theme": "The mind and rest",
    "reel_am7": verse(
        ["Lift yourself by your own mind.", "Do not let it pull you down.", "The mind can be your friend,", "or your enemy."],
        "Bhagavad Gita 6.5",
        "Krishna on the voice in your head.",
        ["Sunday is when it gets loudest. The verse says you hold more of the volume knob than you think."],
        "Is your mind a friend or a critic today? Tell me below.", G, voice=True),
    "card": {"quote": "For one who has won over the mind, the mind is a friend. For one who hasn't, it acts like an enemy.", "author": "Krishna to Arjuna", "source": "Bhagavad Gita 6.6",
             "hook": "Your mind is on a side. This verse says the side depends on you.",
             "body": ["Winning over it doesn't mean silencing it. It means not letting every thought drive.", "Start with one: the next time it shouts, answer calmly."],
             "ask": "Share it with someone who is hard on themselves.", "tags": G},
    "story_quote": ("The mind is restless\nand hard to hold.\nPractice and letting go\ncan train it.", "Bhagavad Gita 6.35"),
    "reel_am11": verse(
        ["Wherever the restless mind wanders,", "bring it back,", "and settle it in the Self."],
        "Bhagavad Gita 6.26",
        "Krishna's instruction for a wandering mind. It is the whole practice.",
        ["No scolding in the verse. Just: bring it back. Then bring it back again."],
        "Save this for the next time you can't focus.", G),
    "line": plain(
        ["A wandering mind", "is not a broken one.", "Bring it back.", "That is the practice."],
        "The Gita on attention, in plain words.",
        ["Not a translation. The verses behind it are 6.26 and 6.35."],
        "Share it with someone who can't sit still.", "#mindfulness #gitawisdom #krishna"),
    "reel_pm19": verse(
        ["For one who is moderate", "in eating and in rest,", "in work, in sleep and in waking,", "yoga ends all sorrow."],
        "Bhagavad Gita 6.17",
        "Krishna on balance: eat, work, sleep, rest. None of it in extremes.",
        ["Written long before anyone said burnout. Rest is part of the practice, and it always has been."],
        "What is one thing you will do slower this week? Tell me below.", "#bhagavadgita #krishna #rest", voice=True),
    "poem": poem(
        ["My mind is a lake in the wind.", "I stopped throwing stones.", "By evening the water", "showed the sky again."],
        "A short poem for a restless Sunday night.",
        ["Our own words, inspired by Bhagavad Gita 6.19."],
        "Save it for when your mind is loud."),
    "noon": deck(
        "5 ways to bring a wandering mind back", "Gentle ones. No sitting cross-legged for an hour.",
        "The Gita doesn't say stop the mind from wandering. It says bring it back.",
        [("Name it. \"Thinking about Monday.\"", "", "Naming a thought is the first step back."),
         ("Look at one thing for ten breaths.", "", "A cup, a leaf, a window. Anything."),
         ("Walk slowly, on purpose.", "", "Feel each foot land. Takes two minutes."),
         ("Do one thing at a time today.", "", "Eat without the phone. Cook without a podcast."),
         ("Forgive the drift and begin again.", "", "6.26: bring it back. That is all of it.")],
        ["Name it", "One object", "Slow walk", "One thing at a time", "Begin again"],
        "Save this. Try number 2 on Monday.",
        "5 ways to bring a wandering mind back. None of them need a mat.",
        ["Plain words, with the verse behind each idea. The Gita's answer to a busy mind is practice, not punishment."],
        "Which one will you try? Tell me the number.", "#mindfulness #bhagavadgita #krishna"),
    "main": deck(
        "Gita 6.6, the mind as friend or enemy", "One verse, four ways to read it.",
        "Krishna says it plainly: your mind can work for you or against you.",
        [("The mind can be your friend.", "6.6, part 1", "When it's trained, it helps. It reminds you what matters."),
         ("The mind can be your enemy.", "6.6, part 2", "When it isn't, it argues with everything you try."),
         ("Which one it is depends on you.", "6.5", "\"Lift yourself by your own mind.\" You have a hand in it."),
         ("Start with one small habit.", "6.17", "Moderate food, work, sleep and rest. A steady body helps a steady mind.")],
        ["Mind as friend", "Mind as enemy", "It depends on you", "Small habits first"],
        "Share it with someone whose mind is loud.",
        "Gita 6.6: your mind is either a friend or an enemy. Which one is it today?",
        ["Chapter 6 is the Gita's chapter on the mind. These are its clearest lines."],
        "Friend or enemy today? Tell me below.", G),
    "morning": (["Like a lamp", "in a windless place,", "the steady mind", "does not flicker."], "Bhagavad Gita 6.19"),
    "affirm": "My mind is allowed\nto rest today.",
    "choice": ("Silence", "Soft music"), "prompt": "What is your mind\nchasing today?",
    "reminder": "Close your eyes for one minute.\nBreathe out slowly.",
    "choice2": ("Walk alone", "Walk with someone"),
    "fragment": "A still lake\nshows the whole sky.",
    "fill": "Finish this:\nMy mind feels calmest when ___",
    "night": (["Even a little of this practice", "protects you from great fear."], "Bhagavad Gita 2.40", [1]),
})

# ============================================================ DAY 3  Monday  STAYING STEADY
DAYS.append({
    "theme": "Staying steady",
    "reel_am7": verse(
        ["Heat and cold, pleasure and pain,", "they come and they go.", "They do not stay.", "Bear them, Arjuna."],
        "Bhagavad Gita 2.14",
        "Krishna on every Monday that feels like it will last forever.",
        ["Verse 2.14. Everything the senses bring in, good or bad, arrives and leaves. You are not stuck with it."],
        "Share this with someone having a heavy Monday.", G, voice=True),
    "card": {"quote": "Treat pleasure and pain, gain and loss, victory and defeat alike. Then prepare for the battle.", "author": "Krishna to Arjuna", "source": "Bhagavad Gita 2.38",
             "hook": "Gita 2.38: Krishna's advice before a war was not to feel nothing. It was to stop letting the swings decide.",
             "body": ["Win or lose, the next step is the same: prepare, then act.", "Easier said than done. Start with one swing today."],
             "ask": "Save it for the day you need to stay level.", "tags": G},
    "story_quote": ("One who is not shaken by sorrow\nand does not chase joy\nis steady in wisdom.", "Bhagavad Gita 2.56"),
    "reel_am11": verse(
        ["Rivers flow into the ocean,", "and the ocean does not move.", "Desires flow into the steady mind,", "and it stays at peace."],
        "Bhagavad Gita 2.70",
        "Krishna's picture of a steady mind is an ocean, not a rock.",
        ["Things still arrive. Wants, worries, news. The ocean takes all of it and stays the ocean."],
        "Save this for the next wave.", G),
    "line": plain(
        ["Not every wave", "needs your reaction.", "Let it reach the shore", "and leave."],
        "The Gita on staying calm, in plain words.",
        ["Not a translation. The verses behind it are 2.14 and 2.70."],
        "Share it with someone who reacts to everything.", "#calm #gitawisdom #krishna"),
    "reel_pm19": verse(
        ["Do not give in to weakness, Arjuna.", "It does not suit you.", "Shake off this small-heartedness,", "and stand up."],
        "Bhagavad Gita 2.3",
        "The first thing Krishna says to Arjuna is not comfort.",
        ["Verse 2.3. Arjuna had just put his bow down. Krishna's reply is short and kind in the way a friend is kind: he says you are capable of more."],
        "Who told you that you could, when you didn't think so? Tell me below.", G, voice=True),
    "poem": poem(
        ["Monday is only a door.", "I have walked through worse.", "Whatever waits on the other side,", "I will meet it standing."],
        "A short poem for the hardest day of the week.",
        ["Our own words, inspired by Bhagavad Gita 2.3."],
        "Share it with someone starting a hard week."),
    "noon": deck(
        "5 things Krishna tells Arjuna on his worst day", "He didn't tell him to feel better. He told him what is true.",
        "Arjuna put his bow down on the first page. This is what he heard next.",
        [("It will pass.", "2.14", "Heat and cold, pleasure and pain. Nothing stays."),
         ("Do not shrink.", "2.3", "\"It does not suit you.\" A friend's push."),
         ("Treat the swings alike.", "2.38", "Win, lose, gain, lose. Then act."),
         ("Do not be shaken by sorrow.", "2.56", "Steady, not numb."),
         ("Be the ocean.", "2.70", "Let the rivers in. Stay the ocean.")],
        ["It will pass", "Don't shrink", "Treat swings alike", "Stay steady", "Be the ocean"],
        "Save this for the next bad day.",
        "5 things Krishna tells Arjuna on his worst day. Number 1 is the one I forget.",
        ["From chapter 2 of the Gita. Short lines for a day when long advice won't stick."],
        "Comment the number of the one you need.", G),
    "main": deck(
        "Arjuna's bad day", "The Gita starts with someone falling apart.",
        "The world's most famous teaching begins with a man who couldn't go on.",
        [("A great archer put down his bow.", "Gita 1.47", "He wasn't lazy. He was overwhelmed."),
         ("He told Krishna: I will not fight.", "Gita 2.9", "Said out loud, to a friend."),
         ("Krishna didn't scold him. He explained.", "", "Seventeen more chapters of explaining."),
         ("The war went on. Arjuna got up.", "", "The first step was listening.")],
        ["He fell apart", "He said so", "Krishna explained", "He got up"],
        "Share it with someone who needs to hear it's okay to fall apart.",
        "The Gita begins with a man who put down his weapons. Sound familiar?",
        ["Arjuna doesn't start as a hero. He starts as someone who can't do it, and says so. That is why it still works."],
        "Have you been Arjuna lately? Tell me below.", G),
    "morning": (["No one who does good", "ever comes to a bad end."], "Bhagavad Gita 6.40", [1]),
    "affirm": "I can handle\nwhat today brings.",
    "choice": ("Hot tea", "Cold water"), "prompt": "One thing that felt\nbigger than it was?",
    "reminder": "Stand up.\nRoll your shoulders.\nBack to it.",
    "choice2": ("Monday", "Friday"),
    "fragment": "Storms are loud.\nThey are not long.",
    "fill": "Finish this:\nI got through ___ and I can do it again",
    "night": (["The one who stays steady", "in pain and in pleasure", "is fit for immortality."], "Bhagavad Gita 2.15"),
})

# ============================================================ DAY 4  Tuesday  THE SOUL
DAYS.append({
    "theme": "The soul",
    "reel_am7": verse(
        ["The soul is never born,", "and it never dies.", "It did not begin,", "and it will not end."],
        "Bhagavad Gita 2.20",
        "Krishna on what you are underneath everything that happens to you.",
        ["Verse 2.20 is read at funerals. It is also a good one for a Tuesday when everything feels final."],
        "Share this with someone who is grieving.", G, voice=True) | {"sa": [0, 1, 2]},
    "card": {"quote": "The soul cannot be cut by any weapon, burned by fire, wet by water or dried by wind.", "author": "Krishna to Arjuna", "source": "Bhagavad Gita 2.23",
             "hook": "Four elements, none of them can touch it. Krishna lists them one by one.",
             "body": ["The verse isn't about being tough. It's about what in you cannot be hurt.", "That is a gentle thing to know on a hard day."],
             "ask": "Save it for a day you feel small.", "tags": G},
    "story_quote": ("As a person puts on new clothes\nand leaves the old,\nthe soul takes new bodies.", "Bhagavad Gita 2.22"),
    "reel_am11": verse(
        ["The Lord lives", "in the heart", "of every being."],
        "Bhagavad Gita 18.61",
        "Seven words. Krishna says you are never alone in there.",
        ["From the last chapter, when Krishna is nearly done teaching. Even the quietest person has company."],
        "Share it with someone who feels alone.", G) | {"sa": [0]},
    "line": plain(
        ["You are more", "than your worst year.", "Underneath it,", "something stays."],
        "The Gita on who you are, in plain words.",
        ["Not a translation. The verses behind it are 2.20 and 2.23."],
        "Save it for a hard day.", "#soul #gitawisdom #krishna"),
    "reel_pm19": verse(
        ["I am the Self,", "seated in the heart of every being.", "I am the beginning,", "the middle and the end."],
        "Bhagavad Gita 10.20",
        "Krishna describes himself, and starts with the heart.",
        ["Verse 10.20. Before the grand descriptions, the first thing he says is: I am in you."],
        "Where do you feel most like yourself? Tell me below.", G, voice=True),
    "poem": poem(
        ["Clothes wear thin and we replace them.", "Houses age and we move on.", "Something in me has never worn out.", "I am learning to trust it."],
        "A short poem about what doesn't wear out.",
        ["Our own words, inspired by Bhagavad Gita 2.22."],
        "Share it with someone who has lost something."),
    "noon": deck(
        "5 lines from the Gita for a grieving day", "Not to fix it. Just to sit with it.",
        "Krishna talks about loss early in the Gita, because Arjuna was in the middle of it.",
        [("As the soul passes through childhood, youth and old age, so it passes on.", "Gita 2.13", "The wise are not shaken by it."),
         ("The soul is never born and never dies.", "Gita 2.20", "It did not begin and will not end."),
         ("As old clothes are given up, so are old bodies.", "Gita 2.22", "A change, not an ending."),
         ("No weapon can cut it, no fire burn it.", "Gita 2.23", "Something in us cannot be touched."),
         ("For one born, death is certain. For one who has died, birth is certain.", "Gita 2.27", "So do not grieve over what cannot be avoided.")],
        ["The soul moves on", "It never dies", "A change of clothes", "It can't be hurt", "Do not grieve alone"],
        "Share this with someone grieving. No words needed.",
        "5 lines from the Gita for a day when you're grieving.",
        ["If you've lost someone, these verses are for you. There is no right way to feel today."],
        "Tell me who you are thinking of today.", G),
    "main": deck(
        "Gita 2.20, one phrase at a time", "The verse read at funerals, read slowly.",
        "Four phrases about the one thing in you that doesn't change.",
        [("The soul is never born.", "2.20, part 1", "It didn't start when your body did."),
         ("And it never dies.", "2.20, part 2", "It doesn't end when the body does."),
         ("It did not begin and will not end.", "2.20, part 3", "Time doesn't reach it."),
         ("The body is only its home.", "2.20, part 4", "It isn't killed when the body is struck.")],
        ["Never born", "Never dies", "No beginning or end", "The body is a home"],
        "Share it with someone who is missing someone.",
        "Gita 2.20: what Krishna says about the part of you that doesn't end.",
        ["Chapter 2, verse 20. The verse is always read slowly, and it should be."],
        "Who are you carrying in your heart today? Tell me below.", G),
    "morning": (["What is unreal never is,", "and what is real never ceases."], "Bhagavad Gita 2.16", [0]),
    "affirm": "I am more than\nthis one day.",
    "choice": ("Memory", "Dream"), "prompt": "Who in your life\nfelt like home?",
    "reminder": "Call someone\nyou haven't called in a while.",
    "choice2": ("Old photos", "New plans"),
    "fragment": "Something in you\nhas never been afraid.",
    "fill": "Finish this:\nSomething in me that never changes is ___",
    "night": (["As the soul passes through", "childhood, youth and old age,", "so it passes to another body.", "The wise are not shaken."], "Bhagavad Gita 2.13"),
})

# ============================================================ DAY 5  Wednesday  DEVOTION
DAYS.append({
    "theme": "Devotion",
    "reel_am7": verse(
        ["A leaf, a flower,", "a fruit, some water,", "offered to Me with love:", "I accept it."],
        "Bhagavad Gita 9.26",
        "The most generous verse in the Gita. Krishna asks for a leaf.",
        ["No gold, no big ritual, no grand gesture. Something small, given with love."],
        "What small thing did you give with love lately? Tell me below.", "#bhagavadgita #krishna #bhakti", voice=True),
    "card": {"quote": "Keep your mind on Me, love Me, worship Me and bow to Me. You will come to Me. This I promise, for you are dear to Me.", "author": "Krishna to Arjuna", "source": "Bhagavad Gita 18.65",
             "hook": "Near the end of the Gita, Krishna stops explaining and makes a promise.",
             "body": ["After seventeen chapters of philosophy he says it simply: you are dear to me.", "Read it as a friend talking, not as a rule."],
             "ask": "Share it with someone who needs to hear they are dear.", "tags": "#bhagavadgita #krishna #bhakti"},
    "story_quote": ("To those who think of Me alone,\nI bring what they lack\nand protect what they have.", "Bhagavad Gita 9.22"),
    "reel_am11": verse(
        ["As people come to Me,", "so I receive them.", "Whatever path they take,", "it is My path they follow."],
        "Bhagavad Gita 4.11",
        "Krishna on every road leading to the same place.",
        ["Verse 4.11. However you come, you are received the same way."],
        "Share it with someone on a different path from yours.", "#bhagavadgita #krishna #bhakti"),
    "line": plain(
        ["Love that asks for nothing", "is the lightest thing", "you will ever carry.", "Try it today."],
        "The Gita on love, in plain words.",
        ["Not a translation. The verses behind it are 9.26 and 18.65."],
        "Share it with someone you love.", "#bhakti #gitawisdom #krishna"),
    "reel_pm19": verse(
        ["I am equal to all beings.", "No one is hateful to Me, no one is dear.", "But those who love Me are in Me,", "and I am in them."],
        "Bhagavad Gita 9.29",
        "Krishna says he has no favourites. Then says who is close.",
        ["Verse 9.29. Equal to everyone, and still, love makes the difference."],
        "Who would you call right now if you could? Tell me below.", "#bhagavadgita #krishna #bhakti", voice=True),
    "poem": poem(
        ["I brought a small flower", "to a very large sky.", "The sky did not laugh.", "It made room."],
        "A short poem about small offerings.",
        ["Our own words, inspired by Bhagavad Gita 9.26."],
        "Save it for the day you feel your offering is too small."),
    "noon": deck(
        "5 small ways to offer your day", "A leaf, a flower, a fruit, some water.",
        "Krishna asks for something small, so we made a list of small things.",
        [("Say thank you before you eat.", "", "A few seconds. Out loud or not."),
         ("Do one chore with full attention.", "", "The cup, the floor, the fold. Do it with care."),
         ("Call one person just to ask how they are.", "", "No agenda. Just ask."),
         ("Give something away today.", "", "A seat, a snack, a minute."),
         ("End the day with a quiet word of gratitude.", "", "9.26: it's not the size. It's the love.")],
        ["Thank before eating", "Chores with care", "Call someone", "Give a little", "End with thanks"],
        "Save this. Pick one for tomorrow.",
        "5 small ways to offer your day. Gita 9.26 style.",
        ["The verse asks for a leaf, a flower, a fruit and some water. Our list is as small."],
        "Which one will you do today?", "#bhakti #bhagavadgita #krishna"),
    "main": deck(
        "Gita 9.26: what Krishna asks for", "He lists four things. None of them cost much.",
        "In a whole book of big ideas, this verse asks for almost nothing.",
        [("A leaf.", "9.26, part 1", "Something that grows by the road."),
         ("A flower.", "9.26, part 2", "Something that lasts a day."),
         ("A fruit and some water.", "9.26, part 3", "Something to eat and drink."),
         ("Offered with love, and he accepts.", "9.26, part 4", "The love is the offering. The rest is wrapping.")],
        ["A leaf", "A flower", "Fruit and water", "Love is the gift"],
        "Share it with someone who gives quietly.",
        "Gita 9.26: Krishna asks for a leaf. That's the verse.",
        ["Chapter 9, verse 26. A small verse with a very big idea."],
        "What would you offer? Tell me below.", "#bhagavadgita #krishna #bhakti"),
    "morning": (["Declare it boldly, Arjuna:", "My devotee never perishes."], "Bhagavad Gita 9.31", [1]),
    "affirm": "I give today\nmy best attention.",
    "choice": ("Prayer", "Music"), "prompt": "What did you give\nwith love lately?",
    "reminder": "Say thank you\nto someone\nright now.",
    "choice2": ("Temple bells", "River sounds"),
    "fragment": "A flower asks for nothing.\nIt opens anyway.",
    "fill": "Finish this:\nI offer today to ___",
    "night": (["Come to Me alone.", "I will free you.", "Do not grieve."], "Bhagavad Gita 18.66"),
})

# ============================================================ DAY 6  Thursday  KNOWLEDGE
DAYS.append({
    "theme": "Knowledge",
    "reel_am7": verse(
        ["In this world,", "there is nothing", "as purifying", "as knowledge."],
        "Bhagavad Gita 4.38",
        "Krishna on why understanding beats everything else.",
        ["Verse 4.38. It's not about degrees. It's about seeing clearly."],
        "What did you understand this week that you didn't last week? Tell me below.", "#bhagavadgita #krishna #gyan", voice=True) | {"sa": [0]},
    "card": {"quote": "Reflect on this fully. Then do as you wish.", "author": "Krishna to Arjuna", "source": "Bhagavad Gita 18.63", "sa": [1],
             "hook": "At the end of eighteen chapters, Krishna says: now you decide.",
             "body": ["No commands. After teaching everything, he hands the choice back to Arjuna.", "A rare thing for a teacher to do."],
             "ask": "Save it for the next big decision.", "tags": "#bhagavadgita #krishna #wisdom"},
    "story_quote": ("As a blazing fire turns wood to ash,\nthe fire of knowledge turns\nall results of action to ash.", "Bhagavad Gita 4.37"),
    "reel_am11": verse(
        ["Hating no one,", "friendly and kind,", "free of \"mine\" and \"I\",", "the same in pain and pleasure,", "and forgiving."],
        "Bhagavad Gita 12.13",
        "Krishna's description of a person he loves. Read it slowly.",
        ["Verse 12.13. It starts with not hating anyone. That's the whole first test."],
        "Share it with someone who fits this.", "#bhagavadgita #krishna #wisdom"),
    "line": plain(
        ["Knowing is not enough.", "Understand it, reflect on it,", "then live it", "on an ordinary Thursday."],
        "The Gita on learning, in plain words.",
        ["Not a translation. The verses behind it are 4.38 and 18.63."],
        "Save it for your next study session.", "#wisdom #gitawisdom #krishna"),
    "reel_pm19": verse(
        ["Peace of mind, gentleness,", "silence, self-control,", "a clean heart.", "This is the discipline of the mind."],
        "Bhagavad Gita 17.16",
        "Krishna on what discipline of the mind looks like. It is quieter than you expect.",
        ["Verse 17.16. No fasting, no performance. Just gentleness and a clear mind."],
        "Which one is hardest for you? Tell me below.", "#bhagavadgita #krishna #wisdom", voice=True),
    "poem": poem(
        ["I read a hundred wise lines.", "Then I forgave one person.", "That was the one", "that taught me anything."],
        "A short poem about knowing and doing.",
        ["Our own words, inspired by Bhagavad Gita 4.38."],
        "Share it with someone who is still learning."),
    "noon": deck(
        "5 questions the Gita asks you to reflect on", "Not for answering fast. For sitting with.",
        "Krishna ends with \"reflect on this fully.\" These are the things worth reflecting on.",
        [("Am I doing the work, or only wanting the result?", "", "2.47: effort is yours."),
         ("Is my mind helping me or fighting me today?", "", "6.6: friend or enemy."),
         ("What in me stays steady when everything changes?", "", "2.20: the part that doesn't change."),
         ("Who did I show kindness to this week?", "", "12.13: hating no one, friendly and kind."),
         ("What have I finally understood?", "", "4.38: understanding purifies.")],
        ["Effort or result", "Mind friend or enemy", "What stays steady", "Who got kindness", "What I understand"],
        "Save this. Answer one on Sunday.",
        "5 questions from the Gita to sit with this week.",
        ["One for each theme of the week so far. No right answers."],
        "Which question will you take with you? Comment its number.", "#bhagavadgita #krishna #reflection"),
    "main": deck(
        "Gita 4.34, how to learn", "Three things Krishna says a learner does.",
        "Krishna doesn't say study harder. He says how to learn.",
        [("Approach with humility.", "4.34, part 1", "Come to a teacher without already knowing."),
         ("Ask questions.", "4.34, part 2", "The Gita itself is Arjuna's questions answered."),
         ("Serve.", "4.34, part 3", "Learning goes both ways. Give something back."),
         ("Then those who know can teach you.", "4.34, part 4", "Knowledge is passed to people who are ready.")],
        ["Be humble", "Ask", "Serve", "Be taught"],
        "Share it with your favourite teacher.",
        "Gita 4.34: Krishna's three steps for learning.",
        ["Chapter 4, verse 34. It might be the only verse in any scripture that says: ask questions."],
        "Who taught you something that stuck? Tell me below.", "#bhagavadgita #krishna #wisdom"),
    "morning": (["Learn by asking,", "with humility,", "and by serving."], "Bhagavad Gita 4.34", [0]),
    "affirm": "I am allowed\nto not know yet.",
    "choice": ("Read", "Listen"), "prompt": "One thing you finally\nunderstood this year?",
    "reminder": "Read one page\nbefore you scroll.",
    "choice2": ("Teacher", "Student"),
    "fragment": "A good question\nis half the answer.",
    "fill": "Finish this:\nSomething I understand now is ___",
    "night": (["One who does not disturb the world,", "and is not disturbed by it,", "free from fear and anxiety,", "is dear to Me."], "Bhagavad Gita 12.15"),
})

# ============================================================ DAY 7  Friday  PEACE
DAYS.append({
    "theme": "Peace",
    "reel_am7": verse(
        ["There is no wisdom for the restless,", "no peace without it,", "and without peace,", "where is happiness?"],
        "Bhagavad Gita 2.66",
        "Krishna asks a question and doesn't answer it. You already know.",
        ["Verse 2.66. A chain: a calm mind, then peace, then happiness. Skip the first link and the rest don't come."],
        "What is one thing that calms you? Tell me below.", G, voice=True),
    "card": {"quote": "Give up craving, move through life without \"mine\" and \"I\", and you will find peace.", "author": "Krishna to Arjuna", "source": "Bhagavad Gita 2.71",
             "hook": "Gita 2.71: Krishna's recipe for peace has two ingredients, and both are things to let go of.",
             "body": ["Craving, and the ownership of everything. That's it.", "Try letting go of one \"mine\" today. A grudge counts."],
             "ask": "Save it for a Friday evening.", "tags": G},
    "story_quote": ("The one who keeps the mind steady\nattains the peace\nthat lives in Me.", "Bhagavad Gita 6.15"),
    "reel_am11": verse(
        ["Whenever goodness declines", "and wrong rises,", "at that time, Arjuna,", "I appear."],
        "Bhagavad Gita 4.7",
        "Krishna's promise to show up when things fall apart.",
        ["Verse 4.7, one of the most quoted in the Gita. It is a promise, said out loud."],
        "Share it with someone who is losing hope.", G),
    "line": plain(
        ["Peace is not", "the end of problems.", "It is a quiet place", "you keep returning to."],
        "The Gita on peace, in plain words.",
        ["Not a translation. The verses behind it are 2.66 and 6.15."],
        "Share it with someone who needs a quiet place.", "#peace #gitawisdom #krishna"),
    "reel_pm19": verse(
        ["Keep your mind on Me,", "and by My grace", "you will cross every obstacle."],
        "Bhagavad Gita 18.58",
        "Krishna's promise for the end of the week.",
        ["Verse 18.58. A week of Gita verses in, this is the thread: keep the mind steady, and obstacles get crossed one at a time."],
        "What obstacle are you carrying into the weekend? Tell me below.", G, voice=True) | {"sa": [0]},
    "poem": poem(
        ["The week was loud.", "I sat by the window.", "Everything I carried", "was lighter than it looked."],
        "A short poem for Friday night.",
        ["Our own words, inspired by Bhagavad Gita 6.15."],
        "Share it with someone who made it to the weekend."),
    "noon": deck(
        "7 days, 7 lines from the Gita", "One for each day of this week.",
        "A week ago we started with a verse about work. Here is the whole week in seven lines.",
        [("Saturday: you own the effort, not the result.", "Gita 2.47", "Karma."),
         ("Sunday: lift yourself by your own mind.", "Gita 6.5", "The mind."),
         ("Monday: pleasure and pain pass.", "Gita 2.14", "Staying steady."),
         ("Tuesday: the soul is never born and never dies.", "Gita 2.20", "The soul."),
         ("Wednesday: a leaf, offered with love.", "Gita 9.26", "Devotion."),
         ("Thursday: reflect fully, then decide.", "Gita 18.63", "Knowledge."),
         ("Friday: keep your mind steady, and you cross every obstacle.", "Gita 18.58", "Peace.")],
        ["Karma", "Mind", "Steadiness", "Soul", "Devotion", "Knowledge", "Peace"],
        "Save it. Read one a day next week.",
        "7 days, 7 lines from the Gita, one for each day of this week.",
        ["A summary of the week for anyone who joined late, and a reminder for anyone who didn't."],
        "Which day was yours? Tell me below.", "#bhagavadgita #krishna #gitaquotes"),
    "main": deck(
        "How the Gita ends", "The last two things anyone says in it.",
        "After eighteen chapters, the book closes with two short lines.",
        [("Arjuna says: my doubt is gone.", "Gita 18.73", "\"I will act on your word.\" The man who put his bow down picks it up."),
         ("Sanjaya says: where Krishna and Arjuna are,", "Gita 18.78", "wisdom and action together."),
         ("There will be fortune, victory and good judgment.", "Gita 18.78", "Sanjaya, the narrator, gives his view."),
         ("It starts with a man who can't. It ends with one who will.", "", "That is the whole book.")],
        ["Doubt is gone", "Wisdom and action", "Fortune follows", "He will"],
        "Share it with someone starting something.",
        "The Gita begins with a man who can't. It ends with one who will.",
        ["Chapter 18, the last. If you've followed this week, you've read the arc of the whole book."],
        "What is your \"I will\" for next week? Tell me below.", G),
    "morning": (["At all times, remember Me,", "and fight."], "Bhagavad Gita 8.7", [0]),
    "affirm": "I end the week lighter\nthan I began it.",
    "choice": ("Quiet evening", "Evening out"), "prompt": "One thing you're letting go of\nbefore the weekend?",
    "reminder": "Unclench your jaw.\nDrop your shoulders.",
    "choice2": ("Sunrise walk", "Late sleep"),
    "fragment": "A week is just\nseven small doors.",
    "fill": "Finish this:\nThis week taught me ___",
    "night": (["One who sees Me everywhere,", "and sees everything in Me,", "is never lost to Me,", "and I am never lost to them."], "Bhagavad Gita 6.30"),
})


# ------------------------------------------------------------------ build
import sys
sys.path.insert(0, HERE)
from bg import for_day  # noqa: E402
import re  # noqa: E402
import sanskrit as S  # noqa: E402


def verse_of(text, sel=None):
    """Sanskrit and transliteration for the verse cited in text. sel picks lines (0 = first half)
    when our English covers only part of the verse."""
    ref = S.ref_in(text)
    if ref not in S._DATA:
        return None
    v = S.get(ref)
    if sel is not None:
        v = {"ref": ref, "deva": [v["deva"][i] for i in sel if i < len(v["deva"])], "tr": [v["tr"][i] for i in sel if i < len(v["tr"])]}
    return v


def slide_verses(c):
    out = []
    for main, credit, note in c["slides"]:
        ref = S.ref_in(credit) or (S.ref_in(note) if re.match(r"^\d+\.\d+:", note) else None)
        if ref not in S._DATA:
            out.append(None)
            continue
        m = re.search(r"part (\d)", credit)
        out.append(S.part(ref, int(m[1])) if m else S.get(ref))
    return out

SLOTS = [
    ("05:00", "story_video", "morning"), ("06:00", "story", "affirm"), ("07:00", "reel", "reel_am7"),
    ("08:00", "quote", "card"), ("09:00", "story", "quote"), ("10:00", "story", "choice"),
    ("11:00", "reel", "reel_am11"), ("12:00", "story", "pointer"), ("13:00", "carousel", "noon"),
    ("14:00", "story", "prompt"), ("15:00", "reel", "line"), ("16:00", "story", "reminder"),
    ("17:00", "story", "choice2"), ("18:00", "carousel", "main"), ("19:00", "reel", "reel_pm19"),
    ("20:00", "story", "pointer2"), ("21:00", "story", "fragment"), ("22:00", "reel", "poem"),
    ("23:00", "story", "fill"), ("00:00", "story_video", "night"),
]


def caption(p, theme, ref=None):
    """Hook, body, a plain search line (Instagram search reads caption text), the ask, then tags."""
    body = list(p["body"])
    text = " ".join([p["hook"], *body])
    if "Bhagavad Gita" not in text or theme.lower().split()[0] not in text.lower():
        body.append(f"Bhagavad Gita {ref}, on {theme.lower()}." if ref else f"Bhagavad Gita, on {theme.lower()}.")
    return "\n\n".join([p["hook"], *body, p["ask"], p["tags"]])


def stamp(day, hhmm):
    return f"{day.isoformat()}T{hhmm}:00{TZ}"


def build():
    posts = []
    for i, dd in enumerate(DAYS):
        day = START + dt.timedelta(days=i)
        n = i + 1
        d = f"d{n}"
        for slot, (hhmm, kind, which) in enumerate(SLOTS):
            when = day + dt.timedelta(days=1) if hhmm == "00:00" else day
            bgk = for_day(n, slot)
            base = {"id": f"{d}-{hhmm.replace(':', '')}-{which}", "at": stamp(when, hhmm), "day": day.isoformat(),
                    "bg": bgk, "palette": i, "theme": dd["theme"]}
            if kind == "reel":
                r = dd[which]
                posts.append({**base, "kind": "reel", "media": "REELS", "lines": r["lines"], "credit": r["credit"],
                              "voice": r["voice"] and VOICE_OVER, "verse": verse_of(r["credit"], r.get("sa")) if r["credit"].startswith("Bhagavad") else None,
                              "caption": caption(r, dd["theme"], S.ref_in(r["credit"]) if r["credit"].startswith("Bhagavad") else None)})
            elif kind == "quote":
                q = dd["card"]
                posts.append({**base, "kind": "quote", "media": "IMAGE", "quote": q["quote"], "author": q["author"],
                              "source": q["source"], "verse": verse_of(q["source"], q.get("sa")), "caption": caption(q, dd["theme"], S.ref_in(q["source"]))})
            elif kind == "carousel":
                c = dd[which]
                posts.append({**base, "kind": "carousel", "media": "CAROUSEL",
                              "deck": {**{k: v for k, v in c.items() if k not in ("hook", "body", "ask", "tags")}, "verses": slide_verses(c)},
                              "caption": caption(c, dd["theme"])})
            elif kind == "story_video":
                lines, credit, *sel = dd[which]
                posts.append({**base, "kind": "story_video", "media": "STORIES", "lines": lines, "credit": credit, "voice": VOICE_OVER,
                              "verse": verse_of(credit, sel[0] if sel else None)})
            else:
                data = {
                    "affirm": ("text", {"text": dd["affirm"]}),
                    "quote": ("quote", {"quote": dd["story_quote"][0], "author": dd["story_quote"][1], "verse": verse_of(dd["story_quote"][1])}),
                    "choice": ("choice", {"a": dd["choice"][0], "b": dd["choice"][1]}),
                    "pointer": ("pointer", {"text": "This morning's reel:\n" + " ".join(dd["reel_am7"]["lines"][:2]), "note": "Watch it on the page"}),
                    "prompt": ("prompt", {"text": dd["prompt"], "note": "Reply here. I read every one."}),
                    "reminder": ("text", {"text": dd["reminder"]}),
                    "choice2": ("choice", {"a": dd["choice2"][0], "b": dd["choice2"][1]}),
                    "pointer2": ("pointer", {"text": "Tonight's carousel:\n" + dd["main"]["cover"], "note": "Swipe through it on the page"}),
                    "fragment": ("text", {"text": dd["fragment"]}),
                    "fill": ("prompt", {"text": dd["fill"], "note": "Reply and tell me."}),
                }[which]
                posts.append({**base, "kind": "story", "story": data[0], "media": "STORIES", **data[1]})
    posts.sort(key=lambda p: p["at"])
    return posts


if __name__ == "__main__":
    posts = build()
    out = os.path.join(HERE, "schedule", "week2.json")
    json.dump({"handle": CONFIG["handle"], "posts": posts}, open(out, "w"), indent=1, ensure_ascii=False)
    cap = os.path.join(HERE, "captions")
    for p in posts:
        if "caption" in p:
            open(os.path.join(cap, p["id"] + ".txt"), "w").write(p["caption"] + "\n")
    feed = sum(1 for p in posts if p["media"] != "STORIES")
    print(f"wrote {out}: {len(posts)} posts ({feed} feed, {len(posts) - feed} stories)")
