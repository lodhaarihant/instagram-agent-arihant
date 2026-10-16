#!/usr/bin/env python3
"""
Week 1 content for @thoughts4us.official, as data.

Run it to write schedule/week1.json, which render.py turns into images and
autopost.py publishes. Every famous quote here is one with a known source
(book, letter, translation). Misattributed internet quotes (the Gandhi "be the
change", the Aristotle "we are what we repeatedly do") are left out on purpose:
a quote page that gets attributions wrong loses the people who know.

Daily shape (IST): 20 items, one an hour, 05:00 to 00:00. See SLOTS.
  reels     07 thought, 11 quote, 15 original line, 19 quote, 22 poem
  feed      08 quote card, 13 list carousel, 18 quote/poem carousel
  stories   the other 12 hours
More content lives in content_extra.py.
"""
import datetime as dt
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = json.load(open(os.path.join(HERE, "config.json")))
WEEK_START = dt.date.fromisoformat(CONFIG["week_start"])
TZ = CONFIG["utc_offset"]          # "+05:30"


# One palette per day, so the grid alternates instead of blurring together.
# bg, ink, accent, and the dot colours from the Thoughts4us logo.
PALETTES = [
    {"bg": "#211814", "ink": "#F5EBDD", "accent": "#F2A541", "dots": ["#F2A541", "#E85D75", "#4FB3BF", "#F6D55C"]},
    {"bg": "#F4EDE2", "ink": "#2B211C", "accent": "#C8553D", "dots": ["#C8553D", "#F2A541", "#588B8B", "#E85D75"]},
    {"bg": "#1B2A33", "ink": "#EEF2F0", "accent": "#F6D55C", "dots": ["#F6D55C", "#4FB3BF", "#E85D75", "#F2A541"]},
    {"bg": "#2E1F2B", "ink": "#F7E9EE", "accent": "#E85D75", "dots": ["#E85D75", "#F2A541", "#F6D55C", "#4FB3BF"]},
    {"bg": "#EDE6D6", "ink": "#22302B", "accent": "#3C7A63", "dots": ["#3C7A63", "#F2A541", "#C8553D", "#4FB3BF"]},
    {"bg": "#14212B", "ink": "#F1EADF", "accent": "#4FB3BF", "dots": ["#4FB3BF", "#F6D55C", "#E85D75", "#F2A541"]},
    {"bg": "#2A2118", "ink": "#F6EEDF", "accent": "#F6D55C", "dots": ["#F6D55C", "#E85D75", "#4FB3BF", "#C8553D"]},
]

T_QUOTES = "#motivationalquotes #lifequotes #wordsofwisdom"
T_POETRY = "#poetry #poetrycommunity #shortpoems"
T_LIFE = "#lifequotes #inspiration #selfgrowth"

# ---------------------------------------------------------------------------
# 08:00  quote card, famous person, sourced
# ---------------------------------------------------------------------------
QUOTE_CARDS = [
    {
        "quote": "All that we are is the result of what we have thought.",
        "author": "The Dhammapada",
        "source": "verse 1, tr. Max Muller, 1881",
        "hook": "This line is over 2,000 years old and it's the reason this page is called Thought's.",
        "body": [
            "The full verse goes on: it is founded on our thoughts, it is made up of our thoughts.",
            "We named the page after that idea back in 2021. Same idea, new home. Daily quotes, short poems and life lines from people who said it first and said it best.",
        ],
        "ask": "Follow along this week. Four posts a day, all of them short.",
        "tags": "#buddha #motivationalquotes #dailyquotes",
    },
    {
        "quote": "We suffer more often in imagination than in reality.",
        "author": "Seneca",
        "source": "Letters to Lucilius, XIII",
        "hook": "Seneca wrote this to a friend who was scared of things that hadn't happened yet.",
        "body": [
            "The full line: there are more things likely to frighten us than there are to crush us.",
            "Think of the last thing you dreaded for a week. How long did the actual thing take? Ten minutes? An hour?",
        ],
        "ask": "Share this with the friend who overthinks. They'll know why.",
        "tags": "#stoicism #seneca #overthinking",
    },
    {
        "quote": "Optimism is the faith that leads to achievement. Nothing can be done without hope and confidence.",
        "author": "Helen Keller",
        "source": "Optimism, 1903",
        "hook": "Helen Keller wrote an entire essay on optimism at 23, after losing sight and hearing at 19 months old.",
        "body": [
            "It's not the cheerful kind of optimism. It's the stubborn kind, the one that does the work anyway.",
            "Quotes about hope usually come from people who had it easy. This one didn't.",
        ],
        "ask": "Save it for a week when hope feels expensive.",
        "tags": "#helenkeller #hope #motivationalquotes",
    },
    {
        "quote": "Life is like riding a bicycle. To keep your balance you must keep moving.",
        "author": "Albert Einstein",
        "source": "letter to his son Eduard, 1930",
        "hook": "Einstein wrote this in a letter to his 19-year-old son, who was going through a hard time.",
        "body": [
            "No equations. Just a dad telling his kid to keep pedalling.",
            "Moving doesn't mean fast. It means not stopping completely. Small counts.",
        ],
        "ask": "Which part of your life needs one small push this week? Tell me below.",
        "tags": "#einstein #lifequotes #keepgoing",
    },
    {
        "quote": "Everything can be taken from a man but one thing: the last of the human freedoms, to choose one's attitude in any given set of circumstances.",
        "author": "Viktor Frankl",
        "source": "Man's Search for Meaning, 1946",
        "hook": "Viktor Frankl wrote this after surviving four concentration camps.",
        "body": [
            "He lost his parents, his brother and his wife. He came out and wrote a book about meaning.",
            "When people say attitude is a choice, it can sound cheap. From him, it isn't.",
        ],
        "ask": "Share it with someone who's carrying a lot right now.",
        "tags": "#viktorfrankl #mansearchformeaning #wordsofwisdom",
    },
    {
        "quote": "Work is love made visible.",
        "author": "Kahlil Gibran",
        "source": "The Prophet, 1923",
        "hook": "Five words from Kahlil Gibran about every meal your mother ever cooked.",
        "body": [
            "And every report someone stayed late to fix, every shirt ironed before school, every song practised a hundred times.",
            "The Prophet has sold over ten million copies. This might be its shortest line.",
        ],
        "ask": "Tag the person whose work you see as love.",
        "tags": "#kahlilgibran #theprophet #poetryquotes",
    },
    {
        "quote": "I am the master of my fate,\nI am the captain of my soul.",
        "author": "William Ernest Henley",
        "source": "Invictus, 1888",
        "hook": "Henley wrote Invictus from a hospital bed after doctors took one of his legs.",
        "body": [
            "Nelson Mandela recited it to other prisoners on Robben Island.",
            "Two lines, 1888, still the thing people say to themselves before the hard day.",
        ],
        "ask": "Save it for Monday.",
        "tags": "#invictus #poetry #motivationalquotes",
    },
]

# ---------------------------------------------------------------------------
# 13:00  original thought
# ---------------------------------------------------------------------------
THOUGHTS = [
    {
        "text": "You don't need a new life.\nYou need ten quiet minutes\nwith the one you have.",
        "hook": "Before you change everything, try ten quiet minutes.",
        "body": [
            "No phone, no plan, no podcast in your ears. Tea, a window, whatever's around.",
            "Most of us are not unhappy with our life. We're just never in it long enough to notice.",
        ],
        "ask": "Try it today and tell me how it went.",
        "tags": T_LIFE,
    },
    {
        "text": "Some days the win\nis that you showed up.\nCount it.",
        "hook": "Showing up on a bad day is a win. Count it.",
        "body": [
            "Not every day is a good day. Some days you just get out of bed, do the minimum and go back.",
            "That still counts. The streak is what matters, not the score.",
        ],
        "ask": "Share this with someone who showed up today.",
        "tags": "#motivationalquotes #keepgoing #selfcare",
    },
    {
        "text": "Keep the people\nwho stayed\nwhen you were boring.",
        "hook": "The friends who stayed when you had nothing exciting going on? Keep them.",
        "body": [
            "Everyone shows up for the wedding, the promotion, the trip photos.",
            "Fewer people show up for the Tuesday when you have nothing to say. Those are the ones.",
        ],
        "ask": "Tag one of yours.",
        "tags": "#friendshipquotes #lifequotes #truefriends",
    },
    {
        "text": "Rest is not a reward\nfor finishing.\nIt's part of how you finish.",
        "hook": "If you only rest after the work is done, you'll never rest.",
        "body": [
            "The work is never done. There's always one more email.",
            "Athletes plan rest days. Farmers let fields sit. You're allowed to stop before you're empty.",
        ],
        "ask": "Save it for the next time you feel guilty about a nap.",
        "tags": "#rest #selfcare #inspiration",
    },
    {
        "text": "Nobody remembers your bad haircut.\nThey remember\nhow you made the room feel.",
        "hook": "Nobody remembers your bad haircut. Promise.",
        "body": [
            "Think of your favourite teacher. You probably can't remember what they wore. You remember how they spoke to you.",
            "That's what people keep of us.",
        ],
        "ask": "Who made a room feel good for you? Tell me about them below.",
        "tags": T_LIFE,
    },
    {
        "text": "You can be gentle with yourself\nand still keep going.\nBoth fit in one day.",
        "hook": "Being kind to yourself and working hard aren't opposites.",
        "body": [
            "We think we have to be harsh to get things done. Most of us have been harsh for years and it hasn't helped much.",
            "Try gentle and steady for a week. See what happens.",
        ],
        "ask": "Share it with someone who's too hard on themselves.",
        "tags": "#selflove #motivationalquotes #mentalhealth",
    },
    {
        "text": "Start before you feel ready.\nReady is a feeling\nthat shows up halfway.",
        "hook": "If you're waiting to feel ready, read this.",
        "body": [
            "Nobody felt ready for their first job, first child, first stage, first anything.",
            "The feeling of ready comes after you start, usually somewhere in the middle, usually when you're too busy to notice.",
        ],
        "ask": "What are you starting this week? Tell me below.",
        "tags": "#motivation #startnow #inspiration",
    },
]

# ---------------------------------------------------------------------------
# 18:30  carousels
# ---------------------------------------------------------------------------
CAROUSELS = [
    {
        "cover": "5 old lines for a loud week",
        "sub": "Written up to 2,500 years ago. Still true on a Monday.",
        "stake": "Five people who never had a phone said the most useful things about having one.",
        "slides": [
            ("Men are disturbed not by things, but by the views which they take of things.", "Epictetus, Enchiridion", "The news isn't the stress. The story we add to it is."),
            ("Do not act as if thou wert going to live ten thousand years.", "Marcus Aurelius, Meditations", "Written by an emperor, to himself, while away at war."),
            ("Nothing can bring you peace but yourself.", "Ralph Waldo Emerson, Self-Reliance", "Not a holiday, not a person, not a purchase."),
            ("A man's ability to remain in one place and linger in his own company.", "Seneca, Letters", "His sign of a well-ordered mind. Try ten minutes."),
            ("A journey of a thousand miles begins with a single step.", "Lao Tzu, Tao Te Ching", "One step. Not a plan for all thousand miles."),
        ],
        "recap": ["Your view is the stress", "You don't have forever", "Peace is an inside job", "Sit with yourself", "Take one step"],
        "cta": "Save this. Come back to slide 3 on Thursday.",
        "hook": "5 old lines for a loud week. Swipe slowly.",
        "body": [
            "Epictetus, Marcus Aurelius, Emerson, Seneca and Lao Tzu. Philosophy and life quotes from people who lived through plagues, wars and empires falling, and still wrote calmly.",
            "My favourite is the Seneca one. Which is yours?",
        ],
        "ask": "Save it for the week you need it.",
        "tags": "#stoicism #philosophy #wordsofwisdom #motivationalquotes",
    },
    {
        "kind": "poem",
        "cover": "Emily Dickinson wrote hope as a bird",
        "sub": "Four lines. Read them slowly.",
        "stake": "She wrote around 1,800 poems and published fewer than a dozen while she was alive.",
        "slides": [
            ("\"Hope\" is the thing with feathers -", "", "Not a feeling. A small, light thing that lands on you."),
            ("That perches in the soul -", "", "It doesn't move in. It perches. Ready to fly, but staying."),
            ("And sings the tune without the words -", "", "Hope rarely explains itself. It just hums."),
            ("And never stops - at all -", "", "Even on the bad days. Listen for it."),
        ],
        "recap_poem": "\"Hope\" is the thing with feathers -\nThat perches in the soul -\nAnd sings the tune without the words -\nAnd never stops - at all -",
        "recap_credit": "Emily Dickinson, c. 1861",
        "cta": "Share it with someone who needs a little bird today.",
        "hook": "Emily Dickinson wrote hope as a bird. Read it one line at a time.",
        "body": [
            "One of the best known poems about hope in English, and it's only the first stanza.",
            "She didn't title it. She almost never titled anything. The world just started calling it by its first line.",
        ],
        "ask": "Share it with someone who needs a little bird today.",
        "tags": "#emilydickinson #poetry #quotesabouthope #classicpoetry",
    },
    {
        "cover": "4 tiny poems from Tagore",
        "sub": "Some barely a sentence. All of them enough.",
        "stake": "Stray Birds came out in 1916, Fireflies in 1928. Some of the poems are a single line.",
        "slides": [
            ("If you shed tears when you miss the sun, you also miss the stars.", "Stray Birds, 6", "Grief for what's gone can hide what's here."),
            ("Let life be beautiful like summer flowers and death like autumn leaves.", "Stray Birds, 82", "Bright while it lasts. Gentle when it goes."),
            ("The butterfly counts not months but moments, and has time enough.", "Fireflies, 1928", "You have more time than you think. Look at the moments."),
            ("Faith is the bird that feels the light and sings when the dawn is still dark.", "Fireflies, 1928", "You don't wait for the sun to start singing."),
        ],
        "recap": ["Don't miss the stars", "Live like summer flowers", "Count moments, not months", "Sing before the dawn"],
        "cta": "Which one is yours? Comment its number.",
        "hook": "Tagore could fit a whole life into one sentence. Here are four.",
        "body": [
            "Rabindranath Tagore, the first non-European to win the Nobel Prize in Literature, in 1913.",
            "Stray Birds and Fireflies are his shortest poems and maybe his most quoted.",
        ],
        "ask": "Comment the number of the one that stays with you.",
        "tags": "#tagore #rabindranathtagore #poetry #indianpoetry",
    },
    {
        "cover": "6 things I wish I knew at 25",
        "sub": "Nobody handed me this list. So here it is.",
        "stake": "Most of these took me years. You can have them in a minute.",
        "slides": [
            ("You don't owe anyone a five-year plan.", "", "Most people with one change it by year two."),
            ("Some friendships end quietly. That's allowed.", "", "No fight, no reason. Just different roads."),
            ("Your parents were figuring it out too.", "", "They were your age once, with less help."),
            ("Being liked by everyone costs you yourself.", "", "Pick being known by a few instead."),
            ("Walk more. Problems shrink outside.", "", "Twenty minutes. Works more often than it should."),
            ("The hard conversation is shorter than the dread.", "", "Weeks of worry. Ten minutes of talking."),
        ],
        "recap": ["No five-year plan needed", "Quiet endings are okay", "Parents are people", "Be known, not liked", "Walk it off", "Have the talk"],
        "cta": "What would you add? Number 7 goes in the comments.",
        "hook": "6 things I wish someone told me at 25. Number 6 took me the longest.",
        "body": [
            "Life lessons don't come with a manual. They come late, usually after the mistake.",
            "If you're 25 now, screenshot the last slide. If you're past it, you know.",
        ],
        "ask": "Add your number 7 in the comments.",
        "tags": "#lifelessons #lifequotes #adulting #selfgrowth",
    },
    {
        "kind": "poem",
        "cover": "The most misread poem in English",
        "sub": "Robert Frost, The Road Not Taken, 1916",
        "stake": "Everyone quotes the last line as a pep talk. Frost was being sly.",
        "slides": [
            ("Two roads diverged in a wood, and I -\nI took the one less traveled by,\nAnd that has made all the difference.", "", "The famous part. Sounds like: be brave, be different."),
            ("Though as for that the passing there\nHad worn them really about the same,", "", "Earlier in the poem. Both roads were the same."),
            ("I shall be telling this with a sigh\nSomewhere ages and ages hence:", "", "The sigh is the point. He'll tell the story later, and make it sound bigger."),
            ("Choose a road. Then be kind about the story you tell.", "", "Frost wrote it as a gentle joke for his friend Edward Thomas, who could never pick a path."),
        ],
        "recap": ["Both roads were about the same", "We decide what it meant later", "So just choose", "Then own the story"],
        "cta": "Did you know this? Yes or no in the comments.",
        "hook": "The Road Not Taken doesn't say what most people think it says.",
        "body": [
            "Robert Frost's most famous poem is quoted at graduations as advice to be different. Read the middle stanza and the roads were 'really about the same'.",
            "It's about how we tell our life story afterwards. Which might be a better lesson.",
        ],
        "ask": "Did you know this? Tell me yes or no below.",
        "tags": "#robertfrost #poetry #theroadnottaken #classicpoetry",
    },
    {
        "cover": "6 lines from old books worth keeping",
        "sub": "Read one a day. Or all six now.",
        "stake": "Each of these has outlived the person who wrote it by a century or more.",
        "slides": [
            ("If one advances confidently in the direction of his dreams, he will meet with a success unexpected in common hours.", "Henry David Thoreau, Walden", "The real line behind every 'follow your dreams' poster."),
            ("Trust thyself: every heart vibrates to that iron string.", "Ralph Waldo Emerson, Self-Reliance", "You already know more than you're giving yourself credit for."),
            ("The unexamined life is not worth living.", "Socrates, in Plato's Apology", "Said at his own trial. He didn't take it back."),
            ("We know what we are, but know not what we may be.", "William Shakespeare, Hamlet", "You're not finished. Nobody is."),
            ("How wonderful it is that nobody need wait a single moment before starting to improve the world.", "Anne Frank", "Written at 14, in hiding."),
            ("Arise, awake, and stop not till the goal is reached.", "Swami Vivekananda", "From the Katha Upanishad, made famous by him."),
        ],
        "recap": ["Walk toward your dreams", "Trust yourself", "Look at your life", "You're still becoming", "Start now", "Don't stop"],
        "cta": "Save it. Read one each morning this week.",
        "hook": "Six lines from old books that are worth more than most new ones.",
        "body": [
            "Thoreau, Emerson, Socrates, Shakespeare, Anne Frank and Swami Vivekananda. Famous quotes with the sources, so you can go read the rest.",
            "The Anne Frank line gets me every time.",
        ],
        "ask": "Save it and read one each morning.",
        "tags": "#bookquotes #wordsofwisdom #inspiration #famousquotes",
    },
    {
        "cover": "A small guide to bad days",
        "sub": "No fixing. Just getting through.",
        "stake": "You don't need to solve the day. You need to land it.",
        "slides": [
            ("Drink water before you decide anything.", "", "Half of bad moods are just thirst and no lunch."),
            ("Lower the bar to one task.", "", "One. Do it. The day now has a win in it."),
            ("Text one person. Not everyone.", "", "Pick the one who doesn't need an explanation."),
            ("Go outside for ten minutes.", "", "Phone in your pocket. Look at something far away."),
            ("Don't read old messages tonight.", "", "Bad days rewrite the past. Leave it alone."),
            ("Sleep early. It's the reset button.", "", "Tomorrow-you will thank you."),
        ],
        "recap": ["Water first", "One task", "One person", "Ten minutes outside", "No old messages", "Sleep early"],
        "cta": "Share this with someone having a bad day.",
        "hook": "A small guide to bad days. Screenshot the last slide.",
        "body": [
            "It's Sunday. Some of you are dreading tomorrow. This is for you.",
            "Simple self care, nothing that costs money, nothing that needs motivation you don't have.",
        ],
        "ask": "Share it with someone having a bad day.",
        "tags": "#selfcare #mentalhealth #baddays #inspiration",
    },
]

# ---------------------------------------------------------------------------
# 21:30  reels: original four-line poems, one line at a time
# ---------------------------------------------------------------------------
REELS = [
    {
        "lines": ["I left a light on", "for the person I was becoming.", "It took years.", "Tonight, they walked in."],
        "hook": "A four-line poem for anyone who finally feels like themselves.",
        "body": ["Short poems, every night at 9:30. This one is for the slow growers."],
        "ask": "Share it with someone who's becoming.",
        "tags": T_POETRY,
    },
    {
        "lines": ["The tea went cold", "while I worried about Thursday.", "Thursday came. I was fine.", "The tea wasn't."],
        "hook": "A short poem about overthinking, and cold tea.",
        "body": ["Most of what we worry about turns out fine. The tea is the only real loss."],
        "ask": "Tag the friend whose tea is always cold.",
        "tags": "#shortpoems #overthinking #poetry",
    },
    {
        "lines": ["Not every season blooms.", "Some just hold the roots", "and wait,", "and that is also growing."],
        "hook": "If you feel stuck, this poem is for you.",
        "body": ["Winter isn't failure. The roots are busy. So are you."],
        "ask": "Save it for the slow season.",
        "tags": "#poetry #growth #shortpoems",
    },
    {
        "lines": ["My mother never said \"I love you.\"", "She said \"have you eaten?\"", "Every single day.", "Same thing."],
        "hook": "Our mothers said I love you in their own language.",
        "body": ["Have you eaten. Did you reach home. Take a jacket. Call when you get there.", "It was always the same sentence."],
        "ask": "What did yours say instead? Tell me below.",
        "tags": "#motherslove #poetry #indianmoms",
    },
    {
        "lines": ["You are allowed to outgrow", "the room you prayed for.", "Say thank you.", "Open the door."],
        "hook": "A poem for when the dream you got doesn't fit any more.",
        "body": ["The job, the city, the relationship. You wanted it, you got it, and now you want something else. That's not ungrateful. That's growing."],
        "ask": "Share it with someone standing at a door.",
        "tags": "#poetry #lettinggo #selfgrowth",
    },
    {
        "lines": ["The river doesn't argue with the rock.", "It goes around", "and keeps its song.", "Be the river today."],
        "hook": "Four lines for a day full of rocks.",
        "body": ["You don't have to win every argument. Some things you just go around."],
        "ask": "Save it for the next difficult person.",
        "tags": "#poetry #peace #shortpoems",
    },
    {
        "lines": ["Sunday says:", "nothing is due,", "nothing is late,", "you are not behind."],
        "hook": "A Sunday poem. Read it twice.",
        "body": ["Whatever the week was, it's over. Tomorrow can wait until tomorrow."],
        "ask": "Share it with someone who works too much.",
        "tags": "#sundayvibes #poetry #rest",
    },
]

# ---------------------------------------------------------------------------
# stories: eight frames a day. The API can't add stickers, so the asks are
# "reply here", which goes straight to DMs and works without one.
# ---------------------------------------------------------------------------
S_MORNING = [
    "Good morning.\nOne thing at a time today.",
    "Morning.\nThe day hasn't decided anything yet.\nNeither have you.",
    "Good morning.\nWater first. Then the world.",
    "Morning.\nBe a little kinder than yesterday.\nThat's the whole plan.",
    "Good morning.\nYou slept. You woke up.\nThat's two things done.",
    "Morning.\nOpen a window.\nLet the day in slowly.",
    "Good morning.\nNo alarms in your head today, okay?",
]
S_QUOTE = [
    ("If you can keep your head when all about you\nare losing theirs and blaming it on you...", "Rudyard Kipling, If, 1910"),
    ("That you are here, that life exists and identity,\nthat the powerful play goes on,\nand you may contribute a verse.", "Walt Whitman, O Me! O Life!"),
    ("Let right deeds be thy motive,\nnot the fruit which comes from them.", "Bhagavad Gita 2.47, tr. Edwin Arnold"),
    ("Your children are not your children.\nThey are the sons and daughters\nof Life's longing for itself.", "Kahlil Gibran, The Prophet"),
    ("The mass of men lead lives\nof quiet desperation.", "Henry David Thoreau, Walden"),
    ("This above all:\nto thine own self be true.", "William Shakespeare, Hamlet"),
    ("Hatred does not cease by hatred at any time:\nhatred ceases by love.", "The Dhammapada, verse 5"),
]
S_THIS_OR_THAT = [
    ("Sunrise", "Sunset"), ("Old letters", "Voice notes"), ("Mountains", "Sea"),
    ("Books", "Long walks"), ("Early bird", "Night owl"), ("Chai", "Coffee"),
    ("Rain on the window", "Sun on your face"),
]
S_ONE_WORD = [
    "Describe today\nin one word.",
    "One word for\nhow your heart is doing?",
    "One word you needed\nto hear this week?",
    "One small thing\nthat made you smile today?",
    "One word for the person\nyou're becoming.",
    "A word your grandmother\nused to say?",
    "One word\nfor next week.",
]
S_FRAGMENT = [
    "Some people are home\nwithout having a door.",
    "I counted my worries tonight.\nMost of them were tomorrow's.",
    "The moon doesn't hurry,\nand it still gets everywhere.",
    "Be soft.\nEven rivers carve stone that way.",
    "You are not late.\nYou are on your own clock.",
    "Old songs know us\nbetter than we remember.",
    "Light gets in\nwhen you stop holding the curtain shut.",
]
S_FILL_IN = [
    "Finish this:\nI'm proud of myself for ___",
    "Finish this:\nThe best advice I ever got was ___",
    "Finish this:\nThis year taught me ___",
    "Finish this:\nI feel most like me when ___",
    "Finish this:\nA song that saved me was ___",
    "Finish this:\nI'm learning to let go of ___",
    "Finish this:\nNext week I'll try ___",
]
S_NIGHT = [
    "Goodnight.\nWhat didn't get done\ncan wait for the sun.",
    "Goodnight.\nYou did more than you think.",
    "Rest now.\nThe worrying can clock out too.",
    "Goodnight.\nPut the phone down after this one.",
    "Sleep well.\nTomorrow is a clean page.",
    "Goodnight.\nBe proud of the small stuff.",
    "Goodnight.\nNext week, same us,\na little braver.",
]


def caption(p):
    parts = [p["hook"], *p["body"], p["ask"], p["tags"]]
    return "\n\n".join(parts)


def stamp(day, hhmm):
    return f"{day.isoformat()}T{hhmm}:00{TZ}"


# Twenty slots a day, hourly, 05:00 to 00:00 IST. 5 reels, 3 feed posts,
# 12 stories. Reels sit at the peak hours because they are what reaches
# people who don't follow the page yet.
SLOTS = [
    ("05:00", "story", "morning"), ("06:00", "story", "affirm"), ("07:00", "reel", "thought"),
    ("08:00", "quote", None), ("09:00", "story", "quote"), ("10:00", "story", "choice"),
    ("11:00", "reel", "quote_am"), ("12:00", "story", "pointer"), ("13:00", "carousel", "noon"),
    ("14:00", "story", "prompt"), ("15:00", "reel", "line"), ("16:00", "story", "reminder"),
    ("17:00", "story", "choice2"), ("18:00", "carousel", "main"), ("19:00", "reel", "quote_pm"),
    ("20:00", "story", "pointer2"), ("21:00", "story", "fragment"), ("22:00", "reel", "poem"),
    ("23:00", "story", "fill"), ("00:00", "story", "night"),
]


def build():
    from content_extra import (CAROUSELS_NOON, LINE_REELS, QUOTE_REELS_AM, QUOTE_REELS_PM,
                               S_AFFIRM, S_CHOICE2, S_REMINDER)
    posts = []
    for i in range(7):
        day = WEEK_START + dt.timedelta(days=i)
        d = f"d{i + 1}"
        # Content is written per weekday (index 0 = Monday) because some of it
        # says "Sunday" or "Monday". The week can start on any day.
        w = day.weekday()
        # The Dhammapada card explains the page name, so it always goes first;
        # whatever card it displaces takes its weekday slot.
        qi = 0 if i == 0 else (WEEK_START.weekday() if w == 0 else w)
        t = THOUGHTS[w]

        reels = {
            "thought": {"lines": t["text"].split("\n"), **t},
            "quote_am": QUOTE_REELS_AM[w], "line": LINE_REELS[w],
            "quote_pm": QUOTE_REELS_PM[w], "poem": REELS[w],
        }
        decks = {"noon": CAROUSELS_NOON[w], "main": CAROUSELS[w]}
        stories = {
            "morning": ("morning", {"text": S_MORNING[w]}),
            "affirm": ("morning", {"text": S_AFFIRM[w]}),
            "quote": ("quote", {"quote": S_QUOTE[w][0], "author": S_QUOTE[w][1]}),
            "choice": ("choice", {"a": S_THIS_OR_THAT[w][0], "b": S_THIS_OR_THAT[w][1]}),
            "pointer": ("pointer", {"text": "This morning's reel:\n" + t["text"].replace("\n", " "), "note": "Watch it on the page"}),
            "prompt": ("prompt", {"text": S_ONE_WORD[w], "note": "Reply here. I read every one."}),
            "reminder": ("morning", {"text": S_REMINDER[w]}),
            "choice2": ("choice", {"a": S_CHOICE2[w][0], "b": S_CHOICE2[w][1]}),
            "pointer2": ("pointer", {"text": "Tonight's carousel:\n" + CAROUSELS[w]["cover"], "note": "Swipe through it on the page"}),
            "fragment": ("fragment", {"text": S_FRAGMENT[w]}),
            "fill": ("prompt", {"text": S_FILL_IN[w], "note": "Reply and tell me."}),
            "night": ("night", {"text": S_NIGHT[w]}),
        }

        for hhmm, kind, which in SLOTS:
            when = day + dt.timedelta(days=1) if hhmm == "00:00" else day
            base = {"id": f"{d}-{hhmm.replace(':', '')}-{which or kind}", "at": stamp(when, hhmm),
                    "day": day.isoformat(), "palette": w}
            if kind == "quote":
                q = QUOTE_CARDS[qi]
                posts.append({**base, "kind": "quote", "media": "IMAGE", "quote": q["quote"],
                              "author": q["author"], "source": q["source"], "caption": caption(q)})
            elif kind == "reel":
                r = reels[which]
                posts.append({**base, "kind": "reel", "media": "REELS", "lines": r["lines"],
                              "credit": r.get("credit", ""), "caption": caption(r)})
            elif kind == "carousel":
                c = decks[which]
                posts.append({**base, "kind": "carousel", "media": "CAROUSEL",
                              "deck": {k: v for k, v in c.items() if k not in ("hook", "body", "ask", "tags")},
                              "caption": caption(c)})
            else:
                sk, data = stories[which]
                posts.append({**base, "kind": "story", "story": sk, "media": "STORIES", **data})

    posts.sort(key=lambda p: p["at"])
    return posts


if __name__ == "__main__":
    posts = build()
    out = os.path.join(HERE, "schedule", "week1.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({"handle": CONFIG["handle"], "palettes": PALETTES, "posts": posts}, open(out, "w"), indent=1, ensure_ascii=False)
    import shutil
    shutil.rmtree(os.path.join(HERE, "captions"), ignore_errors=True)
    os.makedirs(os.path.join(HERE, "captions"), exist_ok=True)
    for p in posts:
        if "caption" in p:
            open(os.path.join(HERE, "captions", p["id"] + ".txt"), "w").write(p["caption"] + "\n")
    feed = sum(1 for p in posts if p["media"] != "STORIES")
    print(f"wrote {out}: {feed} feed posts, {len(posts) - feed} stories")
