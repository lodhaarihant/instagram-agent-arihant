"""
Extra week 1 content for the 20-a-day schedule: quote reels, original line
reels, a second daily carousel and four more story frames a day.

Same rule as content.py: every famous quote has a known source. Each list has
seven entries, indexed by weekday (0 = Monday).
"""

# ---------------------------------------------------------------------------
# 11:00 and 19:00  quote reels, one line at a time, credit at the end
# ---------------------------------------------------------------------------
QUOTE_REELS_AM = [
    {
        "lines": ["Nothing is ours,", "except time."],
        "credit": "Seneca, Letters to Lucilius, I",
        "hook": "Seneca wrote this 2,000 years ago. Your screen time report agrees.",
        "body": ["The first of his letters to a friend opens with time, and how quietly it gets taken from us."],
        "ask": "Share this with someone who keeps saying they're too busy.",
        "tags": "#seneca #stoicism #timequotes",
    },
    {
        "lines": ["You cannot cross the sea", "merely by standing", "and staring at the water."],
        "credit": "Rabindranath Tagore, Stray Birds",
        "hook": "Tagore on the thing you keep planning and not starting.",
        "body": ["One line from Stray Birds, 1916. Still the shortest push you'll get today."],
        "ask": "Save this for the morning you need it.",
        "tags": "#tagore #motivationalquotes #startnow",
    },
    {
        "lines": ["To be great", "is to be misunderstood."],
        "credit": "Ralph Waldo Emerson, Self-Reliance",
        "hook": "Emerson, for anyone whose family doesn't get their plan yet.",
        "body": ["Right before it he names Socrates, Galileo and Newton as people who were misunderstood. Good company."],
        "ask": "Share it with someone who's being doubted right now.",
        "tags": "#emerson #selfreliance #motivationalquotes",
    },
    {
        "lines": ["Things do not change;", "we change."],
        "credit": "Henry David Thoreau, Walden",
        "hook": "Five words from Walden for anyone waiting for life to change.",
        "body": ["Thoreau spent two years in a cabin he built himself. This is one of the things he came back with."],
        "ask": "Save it and read it again on Sunday.",
        "tags": "#thoreau #walden #lifequotes",
    },
    {
        "lines": ["Although the world", "is full of suffering,", "it is full also", "of the overcoming of it."],
        "credit": "Helen Keller, Optimism, 1903",
        "hook": "Helen Keller on the part of the news nobody reports.",
        "body": ["For every hard story, there's someone who got through it. Usually quietly."],
        "ask": "Share it with someone who's getting through something.",
        "tags": "#helenkeller #hope #inspiration",
    },
    {
        "lines": ["Your pain is the breaking", "of the shell", "that encloses", "your understanding."],
        "credit": "Kahlil Gibran, The Prophet",
        "hook": "Gibran on why the hard year taught you the most.",
        "body": ["From the chapter On Pain. It doesn't say pain is good. It says something opens."],
        "ask": "Save this for a hard day.",
        "tags": "#kahlilgibran #theprophet #healing",
    },
    {
        "lines": ["There is nothing", "either good or bad,", "but thinking makes it so."],
        "credit": "William Shakespeare, Hamlet",
        "hook": "Shakespeare said this 400 years before anyone called it mindset.",
        "body": ["Hamlet says it to his friends Rosencrantz and Guildenstern, about Denmark feeling like a prison."],
        "ask": "Share it with your overthinking friend.",
        "tags": "#shakespeare #hamlet #mindset",
    },
]

QUOTE_REELS_PM = [
    {
        "lines": ["It is not that we have", "a short space of time,", "but that we waste", "much of it."],
        "credit": "Seneca, On the Shortness of Life",
        "hook": "Seneca, before the evening scroll starts.",
        "body": ["He wrote a whole essay on this, around the year 49. The point still lands at 7pm."],
        "ask": "Save it, then put the phone down for an hour.",
        "tags": "#seneca #shortnessoflife #stoicism",
    },
    {
        "lines": ["Clouds come floating into my life,", "no longer to carry rain", "or usher storm,", "but to add colour", "to my sunset sky."],
        "credit": "Rabindranath Tagore, Stray Birds",
        "hook": "Tagore on what the hard years look like from far away.",
        "body": ["What felt like a storm at the time, later just looks like colour."],
        "ask": "Share it with someone who's past their storm.",
        "tags": "#tagore #poetry #sunset",
    },
    {
        "lines": ["No man is free", "who is not master", "of himself."],
        "credit": "Epictetus, Fragments",
        "hook": "Epictetus was born a slave. This is what he said about freedom.",
        "body": ["He later taught philosophy in Rome and in Greece. Freedom, for him, started inside."],
        "ask": "Save it for the next time your phone is running your evening.",
        "tags": "#epictetus #stoicism #selfcontrol",
    },
    {
        "lines": ["Forever", "is composed", "of nows."],
        "credit": "Emily Dickinson",
        "hook": "Emily Dickinson's shortest answer to the future.",
        "body": ["Four words, from a poem she wrote around 1862. Tonight is one of the nows."],
        "ask": "Share it with someone you want to spend more nows with.",
        "tags": "#emilydickinson #poetry #presentmoment",
    },
    {
        "lines": ["Darkness cannot drive out darkness;", "only light can do that.", "Hate cannot drive out hate;", "only love can do that."],
        "credit": "Martin Luther King Jr., Strength to Love",
        "hook": "Martin Luther King Jr. on the only thing that has ever worked.",
        "body": ["From his 1963 book of sermons, Strength to Love."],
        "ask": "Share it. Somebody needs it tonight.",
        "tags": "#martinlutherking #love #wordsofwisdom",
    },
    {
        "lines": ["The world breaks every one,", "and afterward", "many are strong", "at the broken places."],
        "credit": "Ernest Hemingway, A Farewell to Arms",
        "hook": "Hemingway on the places you were hurt.",
        "body": ["A Farewell to Arms, 1929. He'd been badly wounded in the war he was writing about."],
        "ask": "Save it for someone who's rebuilding.",
        "tags": "#hemingway #bookquotes #strength",
    },
    {
        "lines": ["All we have to decide", "is what to do", "with the time", "that is given us."],
        "credit": "J.R.R. Tolkien, The Fellowship of the Ring",
        "hook": "Gandalf's answer to every Sunday-night worry.",
        "body": ["Frodo wishes none of it had happened in his time. Gandalf says this."],
        "ask": "Share it with someone dreading Monday.",
        "tags": "#tolkien #lordoftherings #bookquotes",
    },
]

# ---------------------------------------------------------------------------
# 15:00  original line reels
# ---------------------------------------------------------------------------
LINE_REELS = [
    {
        "lines": ["Not everyone who leaves", "was meant to stay.", "Some came", "to show you the door."],
        "hook": "For the person who keeps replaying why they left.",
        "body": ["Some people are a chapter, not the book. That's allowed."],
        "ask": "Share it with someone who needs to let go.",
        "tags": "#lettinggo #poetry #healing",
    },
    {
        "lines": ["Your pace", "is not wrong.", "It's yours."],
        "hook": "A reminder for anyone comparing timelines today.",
        "body": ["Someone got engaged, someone got promoted, someone bought a flat. You're still on your own clock."],
        "ask": "Share it with a friend who feels behind.",
        "tags": "#selfgrowth #comparison #motivationalquotes",
    },
    {
        "lines": ["Small steps, every day,", "look like nothing", "until they look", "like everything."],
        "hook": "If your progress feels invisible, read this.",
        "body": ["Ten pages a day is a book a month. Ten minutes a day is sixty hours a year."],
        "ask": "Save this and come back in 30 days.",
        "tags": "#consistency #motivation #smallsteps",
    },
    {
        "lines": ["Some chapters", "close quietly.", "You're still allowed", "to turn the page."],
        "hook": "Not every ending gets a goodbye.",
        "body": ["Friendships fade, jobs end, cities change. No closure needed to move on."],
        "ask": "Share it with someone turning a page.",
        "tags": "#newbeginnings #poetry #lifequotes",
    },
    {
        "lines": ["Peace is not a place.", "It's the moment you stop", "arguing", "with what is."],
        "hook": "Looking for peace? It's not in the next holiday.",
        "body": ["Most of the noise is the fight with what already happened."],
        "ask": "Save it for the next argument in your head.",
        "tags": "#innerpeace #mindfulness #inspiration",
    },
    {
        "lines": ["Talk to yourself", "the way you'd talk", "to someone", "you love."],
        "hook": "You'd never speak to a friend the way you speak to yourself.",
        "body": ["Try it for one day. Same words, same patience."],
        "ask": "Share it with someone who's hard on themselves.",
        "tags": "#selflove #mentalhealth #kindness",
    },
    {
        "lines": ["Every bad day so far,", "you got through.", "Keep", "the streak."],
        "hook": "Your record on bad days is better than you think.",
        "body": ["Every single one of them, you're still here. That counts."],
        "ask": "Share it with someone having a rough week.",
        "tags": "#keepgoing #mentalhealth #motivation",
    },
]

# ---------------------------------------------------------------------------
# 13:00  second daily carousel, original lists
# ---------------------------------------------------------------------------
CAROUSELS_NOON = [
    {
        "cover": "5 small habits for a calmer mind",
        "sub": "None of them take more than ten minutes.",
        "stake": "A calm mind isn't a personality. It's a few small habits, repeated.",
        "slides": [
            ("Tea before messages.", "", "The first ten minutes of the day set the next ten hours."),
            ("One walk without earphones.", "", "Let your own thoughts finish a sentence."),
            ("Three lines before sleep.", "", "What happened, what you felt, what you're grateful for."),
            ("Say no once this week.", "", "Kindly. Without a long reason."),
            ("Phone sleeps outside the bedroom.", "", "An old alarm clock costs 200 rupees."),
        ],
        "recap": ["Tea before messages", "Walk without earphones", "Three lines at night", "One kind no", "Phone out of the bedroom"],
        "cta": "Save this. Try one habit tomorrow.",
        "hook": "5 small habits for a calmer mind. Number 5 is the hardest.",
        "body": ["Simple mental health habits that cost nothing and take ten minutes or less."],
        "ask": "Save it and try one tomorrow.",
        "tags": "#selfcare #mentalhealth #calm #habits",
    },
    {
        "cover": "Free things that are still priceless",
        "sub": "A short list. Add yours.",
        "stake": "The best things in your week probably didn't cost anything.",
        "slides": [
            ("A long call with an old friend.", "", "The kind where you lose track of time."),
            ("Sunrise, on purpose.", "", "Not on the way to work. Just to watch it."),
            ("A library card.", "", "Thousands of lives, for free."),
            ("Saying sorry first.", "", "Costs pride. Saves years."),
            ("Your mother's voice note.", "", "Keep them. All of them."),
        ],
        "recap": ["Old friends", "Sunrise", "Libraries", "Sorry, first", "Mum's voice notes"],
        "cta": "What's on your list? Tell me in the comments.",
        "hook": "Free things that are still priceless. The last one got me.",
        "body": ["Gratitude lists don't need to be big. These are small and free."],
        "ask": "Tell me what's on your list in the comments.",
        "tags": "#gratitude #simplelife #lifequotes #happiness",
    },
    {
        "cover": "How to be a good friend, quietly",
        "sub": "Nothing dramatic. All of it matters.",
        "stake": "The best friends don't make big speeches. They do small things.",
        "slides": [
            ("Remember the small things.", "", "Their exam date. Their mum's name. How they take their chai."),
            ("Text back when it matters.", "", "Not always fast. But never when they need you."),
            ("Show up without being asked.", "", "Hospital, house move, bad day."),
            ("Listen without fixing.", "", "Sometimes they just want you to hear it."),
            ("Celebrate them loudly.", "", "Their wins are not your losses."),
        ],
        "recap": ["Remember small things", "Text back when it counts", "Show up", "Listen, don't fix", "Celebrate them"],
        "cta": "Share this with the friend who does all five.",
        "hook": "How to be a good friend, quietly. Five things.",
        "body": ["Friendship quotes are everywhere. This is the practical version."],
        "ask": "Share it with the friend who does all five.",
        "tags": "#friendship #friendshipquotes #truefriends #lifelessons",
    },
    {
        "cover": "6 sentences to say more often",
        "sub": "Short. Free. Hard to say.",
        "stake": "Most relationships are repaired with six or seven words.",
        "slides": [
            ("\"I'm proud of you.\"", "", "Parents, kids, friends, colleagues. Everyone needs it."),
            ("\"Take your time.\"", "", "The kindest thing you can give someone in a hurry."),
            ("\"I was wrong.\"", "", "Three words that end a lot of fights."),
            ("\"Tell me more.\"", "", "Makes anyone feel interesting."),
            ("\"You did enough today.\"", "", "Say it to yourself too."),
            ("\"I'm here.\"", "", "No advice needed after it."),
        ],
        "recap": ["I'm proud of you", "Take your time", "I was wrong", "Tell me more", "You did enough today", "I'm here"],
        "cta": "Which one will you say today? Comment its number.",
        "hook": "6 sentences to say more often. Number 3 is the hardest.",
        "body": ["Kind words cost nothing and fix more than long conversations."],
        "ask": "Comment the number you'll say today.",
        "tags": "#kindwords #relationships #lifequotes #kindness",
    },
    {
        "cover": "Signs you're healing that nobody posts about",
        "sub": "Quiet ones. Real ones.",
        "stake": "Healing doesn't look like a glow-up. It looks like this.",
        "slides": [
            ("You sleep through the night.", "", "The 3am replay stopped without you noticing."),
            ("Old songs don't hurt the same.", "", "You can listen and stay."),
            ("You say no without a speech.", "", "No guilt essay needed."),
            ("You enjoy being alone.", "", "Lonely turned into peaceful."),
            ("You stopped checking.", "", "Their profile, their status, their story."),
        ],
        "recap": ["You sleep", "Songs are just songs", "No without a speech", "Alone is peaceful", "You stopped checking"],
        "cta": "Share it with someone who's healing.",
        "hook": "Signs you're healing that nobody posts about.",
        "body": ["Healing quotes usually talk about big moments. Most of it is small and quiet."],
        "ask": "Share it with someone who's healing.",
        "tags": "#healing #selfgrowth #mentalhealth #movingon",
    },
    {
        "cover": "A reminder for your 20s",
        "sub": "From someone a bit further down the road.",
        "stake": "Nobody has it figured out. The ones who look like they do are just quieter.",
        "slides": [
            ("Slow is fine.", "", "Most good lives were built slowly."),
            ("Their timeline isn't your deadline.", "", "Weddings, jobs, flats. Not a race."),
            ("Savings and sleep are self care.", "", "Boring. True."),
            ("Call your grandparents.", "", "Ask them about their 20s. You'll be surprised."),
            ("You can change your mind.", "", "About a degree, a city, a person."),
        ],
        "recap": ["Slow is fine", "Not a race", "Save and sleep", "Call your grandparents", "Change your mind"],
        "cta": "Share it with someone in their 20s.",
        "hook": "A reminder for your 20s. Screenshot slide 8.",
        "body": ["Life advice for your 20s from people who survived theirs."],
        "ask": "Share it with someone in their 20s.",
        "tags": "#20s #lifeadvice #adulting #selfgrowth",
    },
    {
        "cover": "Before you give up, read this",
        "sub": "Five slides. Then decide.",
        "stake": "Quitting is allowed. Just not on the worst day.",
        "slides": [
            ("You've been here before.", "", "And you got through it. Every time."),
            ("Tired isn't the same as finished.", "", "Rest first. Decide later."),
            ("Rest. Don't quit.", "", "A break is not a failure."),
            ("Ask for help.", "", "One message. One person."),
            ("Look how far you've come.", "", "Scroll back a year. Look properly."),
        ],
        "recap": ["You've done this before", "Tired, not finished", "Rest, don't quit", "Ask for help", "Look back"],
        "cta": "Save it. Read it on the hard day.",
        "hook": "Before you give up, read this. Five slides.",
        "body": ["Motivation for the days you want to stop. No yelling, no hustle."],
        "ask": "Save it for the hard day.",
        "tags": "#dontgiveup #motivation #keepgoing #inspiration",
    },
]

# ---------------------------------------------------------------------------
# extra stories: affirmation, reminder, second choice
# ---------------------------------------------------------------------------
S_AFFIRM = [
    "Today I'll do\nwhat I can,\nand that will be enough.",
    "I'm allowed to\ntake up space.",
    "I don't have to\nhave it all figured out\nby tonight.",
    "I'm getting better,\neven when\nit doesn't feel like it.",
    "I can be proud\nand still be growing.",
    "Rest is allowed.\nJoy is allowed.",
    "I'm exactly\nwhere I need to start.",
]
S_REMINDER = [
    "Reminder:\ndrink some water,\nunclench your jaw.",
    "Reminder:\nstand up,\nstretch for a minute.",
    "Reminder:\nyou haven't eaten properly.\nGo.",
    "Reminder:\nlook at something\nfar away for 20 seconds.",
    "Reminder:\nreply to the message\nyou've been avoiding.",
    "Reminder:\nopen a window,\ntake three slow breaths.",
    "Reminder:\ncall someone\nyou miss.",
]
S_CHOICE2 = [
    ("Handwritten letters", "Long phone calls"), ("Rainy evenings", "Winter mornings"),
    ("Poetry", "Novels"), ("Old songs", "New songs"), ("Mountains at dawn", "Beach at sunset"),
    ("Silence", "Soft music"), ("Plans", "Spontaneous"),
]
