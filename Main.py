import sys, os, random, hashlib, re
import time
import datetime
import json

try:
    import requests
except:
    requests = None
    print("heads up: requests is missing, the fun parts need it (pip install requests)")


UA = "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
R    = "\033[0m"
C    = "\033[96m"
G    = "\033[92m"
Y    = "\033[93m"
B    = "\033[94m"
M    = "\033[95m"
D    = "\033[90m"
RD   = "\033[91m"
BOLD = "\033[1m"
HC   = "\033[1;95m"
GB   = "\033[1;92m"
W    = "\033[97m"
HR   = "\033[38;5;98m"
GRAD = ["\033[1;96m", "\033[1;94m", "\033[1;95m", "\033[1;35m"]

CONFIG = {
    "theme": "dark",
    "slow_type": True,
    "timeout": 8,}
THEMES = {
    "dark": {
        "R": "\033[0m", "C": "\033[96m", "G": "\033[92m", "Y": "\033[93m",
        "B": "\033[94m", "M": "\033[95m", "D": "\033[90m", "RD": "\033[91m",
        "BOLD": "\033[1m", "HC": "\033[1;95m", "GB": "\033[1;92m", "W": "\033[97m",
        "HR": "\033[38;5;98m",
        "GRAD": ["\033[1;96m", "\033[1;94m", "\033[1;95m", "\033[1;35m"],
    },
    "light": {
        "R": "\033[0m", "C": "\033[34m", "G": "\033[32m", "Y": "\033[33m",
        "B": "\033[35m", "M": "\033[35m", "D": "\033[90m", "RD": "\033[31m",
        "BOLD": "\033[1m", "HC": "\033[1;34m", "GB": "\033[1;32m", "W": "\033[30m",
        "HR": "\033[38;5;61m",
        "GRAD": ["\033[1;34m", "\033[1;35m", "\033[35m", "\033[34m"],
    },
    "mono": {
        "R": "", "C": "", "G": "", "Y": "", "B": "", "M": "", "D": "", "RD": "",
        "BOLD": "", "HC": "", "GB": "", "W": "", "HR": "",
        "GRAD": ["", "", "", ""],
    },
}

def apply_theme(name):
    t = THEMES.get(name, THEMES["dark"])
    globals().update(t)
    globals()["PROMPT"] = t["HC"] + "»" + t["R"] + " "

TAGLINES = [
    "public data only, relax",
    "your old usernames miss you",
    "no cloud, no keys, no logs",
    "google but with extra steps",
    "reading what got left outside",
    "no logins, no tokens, no drama",
    "everything here was already public anyway",
    "quiet little look behind the username",
    "not stalker grade, just curious",
    "your usernames are snitching",
]

LOGO = r"""
 ██████╗ ███████╗██╗███╗   ██╗████████╗
██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
██║   ██║███████╗██║██╔██╗ ██║   ██║
██║   ██║╚════██║██║██║╚██╗██║   ██║
╚██████╔╝███████║██║██║ ╚████║   ██║
 ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝
██╗      █████╗ ███████╗
██║     ██╔══██╗██╔════╝
██║     ███████║███████╗
██║     ██╔══██║╚════██║
███████╗██║  ██║███████║
╚══════╝╚═╝  ╚═╝╚══════╝
"""

PROMPT = HC + "»" + R + " "

START = time.time()
CMDS_RUN = 0
SWEEPS_DONE = 0
PROFILES_FOUND = 0
WEB_SEARCHES = 0
PHONE_CHECKS = 0
EMAIL_CHECKS = 0
DEEP_RUNS = 0
LAST = {}
VAULT_FILE = "flint_vault.json"
VAULT = {"sweeps": [], "phones": [], "emails": [], "ips": [], "web": [], "dorks": [], "deep": [], "archive": [], "plans": []}

HDRS = {"User-Agent": UA}

NOPE = [
    'no idea what that is',
    'not a command (yet)',
    '??',
    'typo maybe',
    "that's not in here",
    'you made that up',
]

GOODBYES = [
    'later.',
    'stay public.',
    'closing the folder.',
    'gone.',
    'tabs closed.',
]

STATUS = [
    "grab a drink, this takes a sec.",
    "knocking on doors...",
    "asking around, don't rush me.",
    "poking sites one by one.",
    "this is the boring part, hold on.",
]

EMPTY = [
    "nothing. either careful or boring.",
    "ghost mode confirmed.",
    "clean. suspiciously clean.",
    "no hits, this one knows opsec.",
    "the internet has never heard of them.",
]

BIGFP = [
    "same handle on {n} sites, whoever this is, they're findable",
    "one username, {n} places. this person likes consistency",
    "{n} sites, same name. tracking this one would take a day",
]

WEBWAIT = [
    "asking duckduckgo...",
    "searching...",
    "one sec, querying...",
    "typing it into the search box for you...",
]

NUMWAIT = [
    "squinting at the digits...",
    "reading the number back to myself...",
    "counting country codes...",
    "pulling the digits apart...",
]

MAILWAIT = [
    "pulling the address apart...",
    "checking who it's from, sort of...",
    "poking the address...",
]

SITES = [
    ("github",        "https://github.com/{}"),
    ("gitlab",        "https://gitlab.com/{}"),
    ("bitbucket",     "https://bitbucket.org/{}"),
    ("codeberg",      "https://codeberg.org/{}"),
    ("sourceforge",   "https://sourceforge.net/u/{}/profile"),
    ("codepen",       "https://codepen.io/{}"),
    ("dev.to",        "https://dev.to/{}"),
    ("hashnode",      "https://hashnode.com/@{}"),
    ("medium",        "https://medium.com/@{}"),
    ("substack",      "https://{}.substack.com"),
    ("blogger",       "https://{}.blogspot.com"),
    ("wordpress",     "https://{}.wordpress.com"),
    ("replit",        "https://replit.com/@{}"),
    ("codesandbox",   "https://codesandbox.io/u/{}"),
    ("huggingface",   "https://huggingface.co/{}"),
    ("kaggle",        "https://www.kaggle.com/{}"),
    ("hackerrank",    "https://www.hackerrank.com/profile/{}"),
    ("codeforces",    "https://codeforces.com/profile/{}"),
    ("codewars",      "https://www.codewars.com/users/{}"),
    ("exercism",      "https://exercism.org/profiles/{}"),
    ("atcoder",       "https://atcoder.jp/users/{}"),
    ("leetcode",      "https://leetcode.com/{}/"),
    ("dockerhub",     "https://hub.docker.com/u/{}"),
    ("npm",           "https://www.npmjs.com/~{}"),
    ("pypi",          "https://pypi.org/user/{}"),
    ("hackernews",    "https://news.ycombinator.com/user?id={}"),
    ("lobsters",      "https://lobste.rs/u/{}"),
    ("producthunt",   "https://www.producthunt.com/@{}"),
    ("indiehackers",  "https://www.indiehackers.com/{}"),
    ("keybase",       "https://keybase.io/{}"),
    ("hackerone",     "https://hackerone.com/{}"),
    ("bugcrowd",      "https://bugcrowd.com/{}"),
    ("tryhackme",     "https://tryhackme.com/p/{}"),
    ("steam",         "https://steamcommunity.com/id/{}"),
    ("lichess",       "https://lichess.org/@/{}"),
    ("chess",         "https://www.chess.com/member/{}"),
    ("osu",           "https://osu.ppy.sh/users/{}"),
    ("speedrun",      "https://www.speedrun.com/user/{}"),
    ("itch",          "https://{}.itch.io"),
    ("gamejolt",      "https://gamejolt.com/@{}"),
    ("newgrounds",    "https://{}.newgrounds.com"),
    ("twitter",       "https://twitter.com/{}"),
    ("instagram",     "https://www.instagram.com/{}"),
    ("facebook",      "https://www.facebook.com/{}"),
    ("reddit",        "https://www.reddit.com/user/{}"),
    ("tiktok",        "https://www.tiktok.com/@{}"),
    ("youtube",       "https://www.youtube.com/@{}"),
    ("twitch",        "https://www.twitch.tv/{}"),
    ("vimeo",         "https://vimeo.com/{}"),
    ("snapchat",      "https://www.snapchat.com/add/{}"),
    ("telegram",      "https://t.me/{}"),
    ("vk",            "https://vk.com/{}"),
    ("mastodon",      "https://mastodon.social/@{}"),
    ("bluesky",       "https://bsky.app/profile/{}.bsky.social"),
    ("pinterest",     "https://www.pinterest.com/{}"),
    ("tumblr",        "https://{}.tumblr.com"),
    ("imgur",         "https://imgur.com/user/{}"),
    ("9gag",          "https://9gag.com/u/{}"),
    ("quora",         "https://www.quora.com/profile/{}"),
    ("linkedin",      "https://www.linkedin.com/in/{}"),
    ("about.me",      "https://about.me/{}"),
    ("linktree",      "https://linktr.ee/{}"),
    ("biolink",       "https://bio.link/{}"),
    ("allmylinks",    "https://allmylinks.com/{}"),
    ("carrd",         "https://{}.carrd.co"),
    ("flickr",        "https://www.flickr.com/people/{}"),
    ("500px",         "https://500px.com/p/{}"),
    ("deviantart",    "https://www.deviantart.com/{}"),
    ("artstation",    "https://www.artstation.com/{}"),
    ("behance",       "https://www.behance.net/{}"),
    ("dribbble",      "https://dribbble.com/{}"),
    ("unsplash",      "https://unsplash.com/@{}"),
    ("sketchfab",     "https://sketchfab.com/{}"),
    ("soundcloud",    "https://soundcloud.com/{}"),
    ("bandcamp",      "https://bandcamp.com/{}"),
    ("mixcloud",      "https://www.mixcloud.com/{}/"),
    ("lastfm",        "https://www.last.fm/user/{}"),
    ("genius",        "https://genius.com/{}"),
    ("spotify",       "https://open.spotify.com/user/{}"),
    ("trakt",         "https://trakt.tv/users/{}"),
    ("letterboxd",    "https://letterboxd.com/{}"),
    ("myanimelist",   "https://myanimelist.net/profile/{}"),
    ("anilist",       "https://anilist.co/user/{}"),
    ("vndb",          "https://vndb.org/u/{}"),
    ("rateyourmusic", "https://rateyourmusic.com/~{}"),
    ("mydramalist",   "https://mydramalist.com/profile/{}"),
    ("anime-planet",  "https://www.anime-planet.com/users/{}"),
    ("goodreads",     "https://www.goodreads.com/{}"),
    ("boardgamegeek", "https://boardgamegeek.com/user/{}"),
    ("untappd",       "https://untappd.com/user/{}"),
    ("duolingo",      "https://www.duolingo.com/profile/{}"),
    ("patreon",       "https://www.patreon.com/{}"),
    ("kofi",          "https://ko-fi.com/{}"),
    ("buymeacoffee",  "https://www.buymeacoffee.com/{}"),
    ("gumroad",       "https://gumroad.com/{}"),
    ("redbubble",     "https://www.redbubble.com/people/{}/shop"),
    ("etsy",          "https://www.etsy.com/shop/{}"),
    ("ebay",          "https://www.ebay.com/usr/{}"),
    ("depop",         "https://www.depop.com/{}"),
    ("poshmark",      "https://poshmark.com/closet/{}"),
    ("grailed",       "https://www.grailed.com/{}"),
    ("paypal",        "https://paypal.me/{}"),
    ("cashapp",       "https://cash.app/${}"),
    ("onlyfans",      "https://onlyfans.com/{}"),
    ("archive.org",   "https://archive.org/details/@{}"),
    ("wikipedia",     "https://en.wikipedia.org/wiki/User:{}"),
    ("instructables", "https://www.instructables.com/member/{}"),
    ("thingiverse",   "https://www.thingiverse.com/{}/designs"),
    ("hackaday",      "https://hackaday.io/{}"),
]

SITELIST = SITES

CCODES = {
    "1": "usa or canada",
    "7": "russia or kazakhstan",
    "20": "egypt",
    "27": "south africa",
    "30": "greece",
    "31": "netherlands",
    "32": "belgium",
    "33": "france",
    "34": "spain",
    "36": "hungary",
    "39": "italy",
    "40": "romania",
    "41": "switzerland",
    "44": "uk",
    "45": "denmark",
    "46": "sweden",
    "47": "norway",
    "48": "poland",
    "49": "germany",
    "51": "peru",
    "52": "mexico",
    "53": "cuba",
    "54": "argentina",
    "55": "brazil",
    "56": "chile",
    "57": "colombia",
    "58": "venezuela",
    "60": "malaysia",
    "61": "australia",
    "62": "indonesia",
    "63": "philippines",
    "64": "new zealand",
    "65": "singapore",
    "66": "thailand",
    "81": "japan",
    "82": "south korea",
    "84": "vietnam",
    "86": "china",
    "90": "turkey",
    "91": "india",
    "92": "pakistan",
    "93": "afghanistan",
    "94": "sri lanka",
    "95": "myanmar",
    "98": "iran",
    "212": "morocco",
    "213": "algeria",
    "216": "tunisia",
    "218": "libya",
    "221": "senegal",
    "225": "ivory coast",
    "233": "ghana",
    "234": "nigeria",
    "249": "sudan",
    "250": "rwanda",
    "251": "ethiopia",
    "252": "somalia",
    "254": "kenya",
    "255": "tanzania",
    "256": "uganda",
    "260": "zambia",
    "261": "madagascar",
    "263": "zimbabwe",
    "264": "namibia",
    "267": "botswana",
    "351": "portugal",
    "353": "ireland",
    "355": "albania",
    "358": "finland",
    "359": "bulgaria",
    "370": "lithuania",
    "371": "latvia",
    "372": "estonia",
    "375": "belarus",
    "380": "ukraine",
    "381": "serbia",
    "385": "croatia",
    "386": "slovenia",
    "387": "bosnia",
    "389": "north macedonia",
    "420": "czech republic",
    "502": "guatemala",
    "503": "el salvador",
    "504": "honduras",
    "505": "nicaragua",
    "506": "costa rica",
    "507": "panama",
    "509": "haiti",
    "591": "bolivia",
    "593": "ecuador",
    "595": "paraguay",
    "598": "uruguay",
    "675": "papua new guinea",
    "679": "fiji",
    "852": "hong kong",
    "855": "cambodia",
    "856": "laos",
    "880": "bangladesh",
    "886": "taiwan",
    "960": "maldives",
    "961": "lebanon",
    "962": "jordan",
    "963": "syria",
    "964": "iraq",
    "965": "kuwait",
    "966": "saudi arabia",
    "967": "yemen",
    "968": "oman",
    "971": "uae",
    "972": "israel",
    "973": "bahrain",
    "974": "qatar",
    "977": "nepal",
    "994": "azerbaijan",
    "995": "georgia",
    "996": "kyrgyzstan",
    "998": "uzbekistan",
}

NUMLEN = {
    "1": 10,
    "7": 10,
    "44": 10,
    "49": 11,
    "33": 9,
    "34": 9,
    "39": 10,
    "48": 9,
    "55": 11,
    "61": 9,
    "62": 10,
    "63": 10,
    "81": 10,
    "82": 10,
    "86": 11,
    "91": 10,
    "92": 10,
    "971": 9,
    "966": 9,
    "90": 10,
}
MOBILESTART = {
    "44": "7",
    "61": "4",
    "91": "6, 7, 8 or 9",
    "55": "9",
    "49": "15, 16 or 17",
    "33": "6 or 7",
    "34": "6 or 7",
    "27": "6, 7 or 8",
    "971": "5",
    "92": "3",}
NUMLINKS = [
    ("whatsapp", "https://wa.me/{}"),
    ("truecaller", "https://www.truecaller.com/search/global/{}"),
    ("sync.me", "https://sync.me/search/?number={}"),
    ("google it", "https://www.google.com/search?q=%22{}%22"),
    ("bing it", "https://www.bing.com/search?q=%22{}%22"),
]







FREEMAIL = [
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "live.com",
    "proton.me", "protonmail.com", "icloud.com", "me.com", "aol.com",
    "gmx.com", "gmx.de", "mail.com", "yandex.com", "yandex.ru",
    "zoho.com", "tutanota.com", "fastmail.com", "hey.com", "msn.com",
]

DISPOSABLE = [
    "mailinator.com", "10minutemail.com", "guerrillamail.com",
    "tempmail.com", "temp-mail.org", "throwawaymail.com",
    "yopmail.com", "trashmail.com", "getnada.com", "dispostable.com",
    "maildrop.cc", "sharklasers.com", "spam4.me", "grr.la",
]

DORKBITS = [
    ("pastebin",   '{u} site:pastebin.com'),
    ("code",       '{u} (site:github.com OR site:gist.github.com)'),
    ("linkedin",   '{u} site:linkedin.com'),
    ("social",     '{u} (site:twitter.com OR site:reddit.com OR site:instagram.com)'),
    ("docs",       '{u} (filetype:pdf OR filetype:doc OR filetype:xls)'),
    ("forums",     '{u} (inurl:forum OR inurl:thread OR inurl:viewtopic)'),
    ("archived",   '{u} (site:archive.org OR site:web.archive.org)'),
    ("everywhere", '{u} -site:pinterest.com'),
]

DEEPSEP = [".", "_", "-"]
GROUPS = [
    ("code & dev", ["github", "gitlab", "bitbucket", "codeberg", "sourceforge", "codepen", "dev.to", "hashnode", "replit", "codesandbox", "huggingface", "dockerhub", "npm", "pypi", "hackaday", "instructables", "thingiverse"]),
    ("words", ["medium", "substack", "blogger", "wordpress", "goodreads", "wikipedia"]),
    ("social", ["twitter", "instagram", "facebook", "linkedin", "reddit", "tiktok", "youtube", "twitch", "vimeo", "snapchat", "telegram", "vk", "mastodon", "bluesky", "pinterest", "tumblr", "imgur", "9gag", "quora", "about.me", "linktree", "biolink", "allmylinks", "carrd"]),
    ("games", ["steam", "lichess", "chess", "osu", "speedrun", "itch", "gamejolt", "newgrounds", "duolingo"]),
    ("pics & art", ["flickr", "500px", "deviantart", "artstation", "behance", "dribbble", "unsplash", "sketchfab"]),
    ("sound & screen", ["soundcloud", "bandcamp", "mixcloud", "lastfm", "genius", "spotify", "trakt", "letterboxd", "myanimelist", "anilist", "vndb", "rateyourmusic", "mydramalist", "anime-planet", "boardgamegeek", "untappd"]),
    ("money & stuff", ["patreon", "kofi", "buymeacoffee", "gumroad", "redbubble", "etsy", "ebay", "depop", "poshmark", "grailed", "paypal", "cashapp", "onlyfans"]),
    ("the nerdy corners", ["kaggle", "hackerrank", "codeforces", "codewars", "exercism", "atcoder", "leetcode", "hackernews", "lobsters", "producthunt", "indiehackers", "keybase", "hackerone", "bugcrowd", "tryhackme", "archive.org"]),
]


def hr(n=56, ch="─"):
    print(HR + (ch * n) + R)

def sect(t):
    print()
    left = " " + t + " "
    print(HR + "──" + HC + left + HR + ("─" * max(4, 56 - len(left) - 2)) + R)

def kv(k, v, w=12):
    print("  " + D + k.ljust(w) + R + " " + str(v))

def vislen(s):
    return len(re.sub(r"\033\[[0-9;]*m", "", s))

def card(title, rows, w=56):
    kw = 9
    for k, v in rows:
        if len(k) > kw:
            kw = len(k)
    print()
    print(HR + "╭─" + R + HC + " " + title + " " + R + HR + ("─" * max(3, w - 5 - len(title))) + "╮" + R)
    for k, v in rows:
        gap = w - 5 - kw - vislen(str(v))
        if gap >= 0:
            print(HR + "│" + R + "  " + D + k.ljust(kw) + R + " " + str(v) + (" " * gap) + HR + "│" + R)
        else:
            print(HR + "│" + R + "  " + D + k.ljust(kw) + R + " " + str(v) + R)
    print(HR + "╰" + ("─" * (w - 2)) + "╯" + R)

def tag(kind):
    m = {
        "ok":   GB + "[+]" + R,
        "meh":  Y + "[~]" + R,
        "no":   RD + "[-]" + R,
        "info": C + "[i]" + R,
        "warn": Y + "[!]" + R,
        "hmm":  D + "[?]" + R,
    }
    return m[kind]

def bar(n, total, w=24):
    filled = int(round(w * n / total))
    pct = str(int(100 * n / total)).rjust(3)
    return G + "" * filled + D + "*" * (w - filled) + R + D + " " + pct + "% * " + str(n) + "/" + str(total) + R

def pick(items):
    return random.choice(items)

def slow(text, sp=0.008):
    if not CONFIG["slow_type"]:
        print(text)
        return
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(sp)
    sys.stdout.write("\n")

def tstamp():
    try:
        return datetime.datetime.now().strftime("%H:%M:%S")
    except:
        return "??:??"

def geturl(u, t=None):
    if t == None:
        t = CONFIG["timeout"]
    try:
        r = requests.get(u, headers=HDRS, timeout=t)
        return r
    except:
        return None

def strip_tags(s):
    out = ""
    inside = False
    for ch in s:
        if ch == "<":
            inside = True
        elif ch == ">":
            inside = False
        else:
            if inside == False:
                out = out + ch

    out = out.replace("&amp;", "&")
    out = out.replace("&quot;", '"')
    out = out.replace("&#39;", "'")
    out = out.replace("&nbsp;", " ")
    return " ".join(out.split())

def fixlink(u):
    if "uddg=" in u:
        u = u.split("uddg=")[1]
        u = u.split("&")[0]
        u = u.replace("%3A", ":").replace("%2F", "/")
        u = u.replace("%3F", "?").replace("%3D", "=")
        u = u.replace("%26", "&")
    if u.startswith("//"):
        u = "https:" + u
    u = u.replace("&amp;", "&")
    return u

def page_title(htm):
    a = htm.find("<title")
    if a == -1:
        return ""
    a = htm.find(">", a)
    if a == -1:
        return ""
    b = htm.find("</title>", a)
    if b == -1:
        return ""
    t = strip_tags(htm[a + 1:b])
    return t[:90]


def logo():
    lines = LOGO.strip("\n").split("\n")
    n = len(lines)
    for i, ln in enumerate(lines):
        c = GRAD[min(i * len(GRAD) // n, len(GRAD) - 1)]
        print(c + ln + R)

def welcome():
    slow(" oh hi. this is osint lab, it looks at public stuff and nothing else")
    print(" " + D + pick(TAGLINES) + R)


def helpcmd():
    sect("start with these four")
    kv("search", C + "<username>" + R + D + " - find them across " + str(len(SITES)) + " sites" + R)
    kv("phone", C + "<number>" + R + D + " - country, mobile or not" + R)
    kv("email", C + "<address>" + R + D + " - pulled apart, gravatar peek" + R)
    kv("web", C + "<words>" + R + D + " - search the web for you" + R)
    sect("when you need more")
    kv("dork", D + "google dorks * " + C + "dork <q> run" + R + D + " fetches" + R)
    kv("deep", D + "multi step plan for a name * asks one by one * graph at the end" + R)
    kv("sites", D + "the site list, in piles" + R)
    kv("ip", D + "rough geo, no keys" + R)
    kv("wayback", D + "does the archive have it" + R)
    kv("save", D + "last result -> json * " + C + "last" + R + D + " shows it" + R)
    kv("vault", D + "everything grabbed piles up here * " + C + "vault" + R + D + " writes " + C + "flint_vault.json" + R)
    kv("theme", D + "dark * light * mono, recolors everything live" + R)
    print()
    print("  " + D + "tricks: " + C + "search b0b only github,steam" + R + D + " * " + C + "search b0b fast" + R + D + " * " + C + "phone codes" + R)
    print()


def about():
    print()
    print(" " + HC + "osint lab" + R)
    print()
    print(" " + D + "runs local, only looks at public pages. a username gets checked" + R)
    print(" " + D + "on a big pile of sites, words get searched, a number gets read" + R)
    print(" " + D + "apart, an email gets gravatar-checked. no logins, no keys, ever." + R)
    print()
    print(" " + D + "a 200 status is a guess, not proof. treat every hit as a hint." + R)
    print()
    print(" " + D + "built it to find my own old accounts. don't be weird with it." + R)
    print()


def check_site(site, user):
    name = site[0]
    url = site[1].format(user)
    r = geturl(url)
    if r == None:
        return None
    code = r.status_code
    ttl = ""
    if code == 200:
        ttl = page_title(r.text)
    return [name, url, code, ttl]


def sweep(user, only=None, fast=False):

    global SWEEPS_DONE, PROFILES_FOUND
    if requests == None:
        print(" no requests, no hunting. pip install requests first")
        return
    user = user.strip()
    pool = SITES
    if only:
        want = []
        for w in only.split(","):
            want.append(w.strip().lower())
        pool = []
        for s in SITES:
            if s[0] in want:
                pool.append(s)
        if len(pool) == 0:
            print(" none of those are in my list. " + C + "sites" + R + " shows what i got")
            return
    if fast:
        pool = pool[:30]

    total = len(pool)
    print()
    print(" " + D + pick(STATUS) + R + W + user + R + D + " on " + str(total) + " sites" + R)
    print()
    found = []
    odd = []
    miss = 0
    n = 0
    try:
        for site in pool:
            n = n + 1
            res = check_site(site, user)
            sys.stdout.write("\r  " + bar(n, total) + "   ")
            sys.stdout.flush()
            if res == None:
                miss = miss + 1
            elif res[2] == 404:
                miss = miss + 1
            elif res[2] == 200:
                low = res[3].lower()
                if "not found" in low or "content not available" in low or "doesn't exist" in low:
                    miss = miss + 1
                else:
                    found.append(res)
                    print("\r" + " " * 46)
                    print(" " + tag("ok") + " " + HC + res[0] + R + " " + B + res[1] + R)
                    if res[3] != "":
                        print("     " + D + res[3] + R)
            else:
                odd.append(res)
            time.sleep(random.randint(3, 9) / 10)
    except KeyboardInterrupt:
        print()
        print()
        print(" " + Y + "ok ok, stopping there" + R)
        print()
        return

    print()
    print()
    if len(found) == 0:
        print(" " + tag("warn") + " " + pick(EMPTY))
    elif len(found) >= 3:
        tip = pick(BIGFP)
        tip = tip.replace("{n}", str(len(found)))
        print(" " + tag("info") + " " + tip)
    if len(odd) > 0:
        print()
        print(" " + D + "these ones answered something weird, blocked or grumpy:" + R)
        for w in odd:
            print(" " + tag("meh") + " " + C + w[0].ljust(15) + R + " " + D + "status " + str(w[2]) + R)
    rows = [("hits", GB + str(len(found)) + R + D + " of " + str(total) + " checked" + R)]
    if len(odd) > 0:
        rows.append(("odd", str(len(odd)) + D + " blocked or grumpy (the [~] ones)" + R))
    rows.append(("misses", str(miss)))
    card("how it went", rows)
    print(" " + D + C + "save" + R + " " + D + "writes it out, " + C + "last" + R + " " + D + "reminds you what this was" + R)

    oddlist = []
    for w in odd:
        oddlist.append([w[0], w[2]])
    when = str(datetime.datetime.now())[:16]
    LAST["sweep"] = {"user": user, "total": total, "found": found, "odd": oddlist, "when": when}
    vault_add("sweeps", LAST["sweep"])
    SWEEPS_DONE += 1
    PROFILES_FOUND = PROFILES_FOUND + len(found)


def cmd_search(rest):
    if rest == "":
        print(" usage: search <username> [fast] [only site1,site2]")
        print(" like: " + C + "search b0bthegoldfish only github,steam" + R)
        return
    bits = rest.split()
    user = bits[0]
    if user.startswith("@"):
        user = user[1:]
    fast = False
    only = None
    i = 1
    while i < len(bits):
        if bits[i] == "fast" or bits[i] == "-f":
            fast = True
        if bits[i] == "only":
            if i + 1 < len(bits):
                only = bits[i + 1]
        i = i + 1
    if "@" in user and "." in user:
        print(" that looks like an email, i only do usernames right now")
        return
    sweep(user, only, fast)


def sites_list():
    print()
    print(" " + str(len(SITELIST)) + " sites in the list, search runs all of them, sorted into piles")
    done = []
    leftout = []
    for gname, glist in GROUPS:
        rows = []
        for s in SITELIST:
            if s[0] in glist and s[0] not in done:
                rows.append(s[0])
        if len(rows) == 0:
            continue
        done = done + rows
        print("  " + HC + gname + R)
        line = "    "
        i = 0
        for name in rows:
            line = line + C + name.ljust(16) + R
            i = i + 1
            if i == 4:
                print(line)
                line = "    "
                i = 0
        if i > 0:
            print(line)
        print()
    for s in SITELIST:
        if s[0] not in done:
            leftout.append(s[0])
    if len(leftout) > 0:
        print("  " + D + "everything else" + R)
        line = "    "
        i = 0
        for name in leftout:
            line = line + C + name.ljust(16) + R
            i = i + 1
            if i == 4:
                print(line)
                line = "    "
                i = 0
        if i > 0:
            print(line)
        print()
    print(" " + D + "tip: " + C + "search <user> only github,reddit" + R + " " + D + "picks just those" + R)
    print()


def ddg_snips(htm):
    snips = []
    parts = htm.split('class="result__snippet"')
    for p in parts[1:]:
        c = p.find(">")
        d = p.find("</a>")
        if d == -1:
            d = p.find("</td>")
        if c == -1 or d == -1:
            continue
        t = strip_tags(p[c + 1:d])
        snips.append(t[:260])
    return snips


def ddg_lookup(q):
    got = []
    u = "https://html.duckduckgo.com/html/?q=" + q.replace(" ", "+")
    r = geturl(u, 12)
    if r == None:
        return got
    if r.status_code != 200:
        return got
    snips = ddg_snips(r.text)
    parts = r.text.split('class="result__a"')

    i = 0
    for p in parts[1:]:
        a = p.find('href="')
        if a == -1:
            continue
        b = p.find('"', a + 6)
        if b == -1:
            continue
        c = p.find(">", b)
        d = p.find("</a>", c)
        if c == -1 or d == -1:
            continue
        title = strip_tags(p[c + 1:d])
        if title == "":
            continue
        link = fixlink(p[a + 6:b])
        desc = ""
        if i < len(snips):
            desc = snips[i]
        got.append([title[:120], link, desc])
        i = i + 1
        if len(got) == 12:
            break
    return got


def bing_lookup(q):
    got = []
    u = "https://www.bing.com/search?q=" + q.replace(" ", "+") + "&count=18"
    r = geturl(u, 15)
    if r == None:
        return got
    if r.status_code != 200:
        return got
    parts = r.text.split("<h2")
    for p in parts[1:]:
        a = p.find('href="http')
        if a == -1:
            continue
        b = p.find('"', a + 6)
        if b == -1:
            continue
        c = p.find(">", b)
        d = p.find("</a>", c)
        if c == -1 or d == -1:
            continue
        title = strip_tags(p[c + 1:d])
        if title == "":
            continue
        link = p[a + 6:b]
        if "bing.com" in link:
            continue
        got.append([title[:120], link, ""])
        if len(got) == 12:
            break
    return got


def show_web(got, q):
    print()
    if len(got) == 0:
        print(" " + tag("warn") + " nothing came back. try different words maybe")
        print()
        return
    print(" " + D + str(len(got)) + " results for" + R + " " + BOLD + q + R)
    print()
    n = 1
    for r in got:
        print(" " + GB + str(n) + "." + R + " " + W + r[0] + R)
        print("    " + B + r[1] + R)
        if r[2] != "":
            print("    " + D + r[2][:170] + R)
        n = n + 1
    print()


def cmd_web(rest):
    global WEB_SEARCHES
    if requests == None:
        print(" no requests lib, no web either. pip install requests")
        return
    if rest == "":
        print(" usage: web <query>")
        print(" like: " + C + "web old bandmate from leeds, drums" + R)
        return
    engine = ""
    if rest.endswith(" bing"):
        engine = "bing"
        rest = rest[:-5].strip()
    if rest.endswith(" ddg"):
        engine = "ddg"
        rest = rest[:-4].strip()
    if rest == "":
        print(" that's just an engine name, gimme actual words")
        return
    print(" " + D + pick(WEBWAIT) + R)
    got = []
    if engine != "bing":
        got = ddg_lookup(rest)
    if len(got) == 0 and engine != "ddg":
        if engine == "":
            print(" " + D + "ddg's being difficult. bing then..." + R)
        got = bing_lookup(rest)
    show_web(got, rest)
    WEB_SEARCHES = WEB_SEARCHES + 1
    when = str(datetime.date.today()) + " " + tstamp()
    LAST["web"] = {"q": rest, "got": got, "when": when}
    vault_add("web", LAST["web"])


def digitsonly(s):
    out = ""
    for ch in s:
        if ch.isdigit():
            out = out + ch
    return out


def qurl(q):
    q = q.replace("%", "%25")
    q = q.replace('"', "%22")
    q = q.replace(":", "%3A")
    q = q.replace("(", "%28")
    q = q.replace(")", "%29")
    q = q.replace(" ", "+")
    return q


def codes_table():
    print()
    print(" " + str(len(CCODES)) + " country codes in the table, the ones i know anyway")
    print()
    keys = sorted(CCODES, key=lambda x: int(x))
    line = "  "
    i = 0
    for k in keys:
        entry = D + ("+" + k).ljust(6) + CCODES[k][:13].ljust(14) + R
        line = line + entry
        i = i + 1
        if i == 3:
            print(line)
            line = "  "
            i = 0
    if i > 0:
        print(line)
    print()
    print(" " + D + "not every country on earth, just the common ones. " + C + "phone +XX..." + R + " " + D + "to use one" + R)
    print()


def cmd_phone(rest):
    global PHONE_CHECKS
    if rest.strip() == "codes":
        codes_table()
        return
    raw = rest.strip()
    if raw == "":
        print(" usage: phone <number>")
        print(" like: " + C + "phone +254 712 345 678" + R + " " + D + "or phone +4478..., spaces and dashes are fine")
        print(" the code table itself: " + C + "phone codes" + R)
        return
    for junk in (" ", "-", "(", ")", ".", "/"):
        raw = raw.replace(junk, "")
    num = digitsonly(raw)
    if len(num) < 7:
        print(" that's too short to be anybody's number. count it again?")
        return
    if len(num) > 15:
        print(" " + str(len(num)) + " digits is more than the planet allows (15 max). something's off")
        return
    print(" " + D + pick(NUMWAIT) + R)
    print()

    cc = None
    for ln in (3, 2, 1):
        if num[:ln] in CCODES:
            cc = num[:ln]
            break

    if cc == None:
        print(" " + tag("hmm") + " i don't recognize " + BOLD + num[:3] + R + " as a country code i know.")
        print("   still reading the rest of it, but take the country with salt.")
        print("   what i do have: " + C + "phone codes" + R)
        print()
        cc = ""
        country = "no idea"
        restn = num
    else:
        country = CCODES[cc]
        restn = num[len(cc):]
                                        
    pretty = "+" + cc if cc else ""
    i = 0
    while i < len(restn):
        take = 3 if (len(restn) - i) > 3 else (len(restn) - i)
        pretty = pretty + " " + restn[i:i + take]
        i = i + take

    rows = [
        ("country", BOLD + country + (R + " " + D + "(+" + cc + ")" + R if cc else R)),
        ("looks like", B + pretty.strip() + R),
        ("digits", str(len(num)) + " total" + (D + " (" + str(len(restn)) + " after the code)" + R if cc else "")),
    ]
    if cc != "" and cc in NUMLEN:
        want = NUMLEN[cc]
        got = len(restn)
        if got == want:
            rows.append(("length", G + str(got) + R + D + " - matches the " + str(want) + " expected for +" + cc + R))
        else:
            rows.append(("length", Y + str(got) + R + D + " - expected " + str(want) + " for +" + cc + ", typo?" + R))
    if cc != "" and cc in MOBILESTART:
        starts = []
        for chx in MOBILESTART[cc]:
            if chx.isdigit():
                starts.append(chx)
        if restn[:1] in starts:
            rows.append(("type", G + "starts like a mobile" + R))
        else:
            rows.append(("type", D + "not a usual mobile opener for +" + cc + R))
    elif cc != "":
        rows.append(("type", D + "no mobile-pattern note for +" + cc + R))
    card("what the digits say", rows)

    full = "+" + num
    print()
    print(" " + D + "no lookups, no logins - just doors:" + R)
    for label, tpl in NUMLINKS:
        if label == "whatsapp":
            link = tpl.format(num)
        else:
            link = tpl.format("%2B" + num)
        print("  " + C + label.ljust(12) + R + " " + B + link + R)
    print()
    print(" " + D + "tip: google the digits in groups too, people write them every which way" + R)
    print()

    PHONE_CHECKS = PHONE_CHECKS + 1
    LAST["phone"] = {"number": full, "country": country, "digits": len(num), "when": str(datetime.datetime.now())[:16]}
    vault_add("phones", LAST["phone"])


def cmd_email(rest):
    global EMAIL_CHECKS
    a = rest.strip().lower()
    if a == "":
        print(" usage: email <address>")
        print(" like: " + C + "email some.old.name@gmail.com" + R)
        return
    if a.count("@") != 1:
        print(" that's not exactly one email. zero or two @ signs, can't work with that")
        return
    local, dom = a.split("@")
    print(" " + D + pick(MAILWAIT) + R)
    print()
    if local == "" or dom == "":
        print(" empty on one side of the @. that goes nowhere")
        return
    if "." not in dom:
        print(" " + tag("hmm") + " domain " + BOLD + dom + R + " has no dot, so no mail server would answer it. typo?")
        print()
        kind = "broken looking"
    else:
        tld = dom.rsplit(".", 1)[1]
        rows = [
            ("address", B + a + R),
            ("local part", local + "  " + D + "(" + str(len(local)) + " chars" + (" + dots" if "." in local else "") + (" + plus-tag" if "+" in local else "") + ")" + R),
            ("domain", dom + "  " + D + "(tld ." + tld + ")" + R),
        ]
        if dom in FREEMAIL:
            kind = "free mail"
            rows.append(("kind", C + kind + R + D + " - big provider, tells you nothing alone" + R))
        elif dom in DISPOSABLE:
            kind = "throwaway"
            rows.append(("kind", Y + kind + R + D + " - burner mail" + R))
        else:
            kind = "own domain"
            rows.append(("kind", D + "company, school or personal domain" + R))
        card("the address", rows)
        if "+" in local:
            print("  " + D + "the +" + local.split("+", 1)[1] + " part is a gmail tag - strip it, it's the same mailbox: " + C + local.split("+", 1)[0] + "@" + dom + R)
        if "." in local and dom in FREEMAIL:
            print("  " + D + "gmail ignores dots - " + C + local.replace(".", "") + "@" + dom + R + D + " is the same inbox" + R)

    print()
    print(" " + D + "gravatar check..." + R)
    h = hashlib.md5(a.encode("utf-8")).hexdigest()
    r = geturl("https://www.gravatar.com/avatar/" + h + "?d=404&s=80", 8)
    if r == None:
        print(" " + tag("hmm") + " couldn't reach gravatar at all. skip it")
    elif r.status_code == 200:
        print(" " + tag("ok") + " there's a gravatar on this address. " + B + "https://gravatar.com/" + h + R)
        prof = geturl("https://gravatar.com/" + h, 8)
        if prof != None and prof.status_code == 200:
            t = page_title(prof.text)
            if t != "":
                print("    " + D + t + R)
    else:
        print(" " + D + "no gravatar. that's most addresses, means nothing either way" + R)

    print()
    print(" " + D + "and the usual doors:" + R)
    for label, tpl in [("google", "https://www.google.com/search?q=%22{}%22"),
                       ("bing", "https://www.bing.com/search?q=%22{}%22"),
                       ("ddg", "https://html.duckduckgo.com/html/?q={}"),
                       ("pastebin dork", "https://www.google.com/search?q=%22{}%22+site%3Apastebin.com")]:
        link = tpl.replace("{}", qurl(a).replace("+", "%20"))
        print("  " + C + label.ljust(12) + R + " " + B + link + R)
    print()

    EMAIL_CHECKS = EMAIL_CHECKS + 1
    LAST["email"] = {"addr": a, "domkind": kind, "gravatar": h, "when": str(datetime.datetime.now())[:16]}
    vault_add("emails", LAST["email"])


def cmd_dork(rest):
    if requests == None:
        print(" no requests lib, the run part won't work. the links will though")
    if rest == "":
        print(" usage: dork <name or words> [run]")
        print(" like: " + C + "dork b0bthegoldfish" + R)
        print("       " + C + "dork \"john smith\" leeds run" + R + D + "   ← actually fetches the first few" + R)
        return
    runmode = False
    q = rest
    if q.endswith(" run"):
        runmode = True
        q = q[:-4].strip()
    if q == "":
        print(" that's just 'run', gimme something to search")
        return
    quoted = '"' + q + '"'
    sect("dorks for " + q)
    print(" " + D + "click them or let me run a few" + R)
    print()
    for label, tpl in DORKBITS:
        query = tpl.replace("{u}", quoted)
        link = "https://www.google.com/search?q=" + qurl(query)
        print("  " + C + label.ljust(12) + R + " " + B + link + R)
    print()

    if not runmode:
        print(" " + D + "want me to fetch the first few? " + C + "dork " + q + " run" + R)
        print()
        return

    if requests == None:
        print(" " + RD + "no requests lib after all. links above still work in a browser" + R)
        print()
        return

    print(" " + D + "running the first four through ddg..." + R)
    got = []
    seen = []
    for label, tpl in DORKBITS[:4]:
        query = tpl.replace("{u}", quoted)
        print(" " + D + "* " + label + R)
        res = ddg_lookup(query)
        for r in res:
            if r[1] in seen:
                continue
            seen.append(r[1])
            r.append(label)
            got.append(r)
        time.sleep(random.randint(3, 8) / 10)
    print()
    if len(got) == 0:
        print(" " + tag("warn") + " nothing came back. ddg mood, probably. try the google links above")
    else:
        print(" " + GB + str(len(got)) + " unique results" + R)
        print()
        n = 1
        for r in got[:12]:
            print(" " + GB + str(n) + "." + R + " " + W + r[0] + R + " " + D + "[" + r[3] + "]" + R)
            print("    " + B + r[1] + R)
            if r[2] != "":
                print("    " + D + r[2][:170] + R)
            n = n + 1
    print()
    LAST["web"] = {"q": "dorks: " + q, "got": [[r[0], r[1], r[2]] for r in got], "when": str(datetime.date.today()) + " " + tstamp()}
    vault_add("dorks", LAST["web"])




                
DEEPTAGS = [
    "the slow way. more steps, more stuff",
    "building the plan out of whatever you gave me",
    "we go digging properly this time",
    "one step at a time, no rushing",
    "same drill as always: plan, poke, write it down",
]

DEEPEDGE = ["~", "=", "*", "+", "#", ":", "<", ""]
DEEPPALETTE = ["\033[38;5;39m", "\033[38;5;41m", "\033[38;5;45m", "\033[38;5;51m",
               "\033[38;5;87m", "\033[38;5;99m", "\033[38;5;111m", "\033[38;5;147m",
               "\033[38;5;170m", "\033[38;5;176m", "\033[38;5;183m", "\033[38;5;205m",
               "\033[38;5;212m", "\033[38;5;219m", "\033[38;5;198m"]               

BIGSITES = ["github", "twitter", "instagram", "reddit", "youtube", "tiktok",
            "telegram", "steam", "medium", "linktree", "pinterest", "soundcloud"]


def deep_styler(state):
    state["edge"] = random.choice(DEEPEDGE)
    state["c1"] = random.choice(DEEPPALETTE)
    state["c2"] = random.choice(DEEPPALETTE)
    state["c3"] = random.choice(DEEPPALETTE)
    while state["c2"] == state["c1"]:
        state["c2"] = random.choice(DEEPPALETTE)
    while state["c3"] == state["c1"] or state["c3"] == state["c2"]:
        state["c3"] = random.choice(DEEPPALETTE)


def deep_head(state, text):
    e = state["edge"]
    print()
    print(state["c1"] + (e * 3) + " " + text.upper() + " " + (e * 3) + R)
    print(state["c1"] + (e * (len(text) + 8)) + R)


def deep_ask(state, text):
    try:
        a = input(state["c2"] + " " + state["edge"] + R + " " + text + " ").strip().lower()
    except EOFError:
        print()
        return "n"
    except KeyboardInterrupt:
        print()
        return "q"
    if a == "":
        return "y"
    if a.startswith("n"):
        return "n"
    if a.startswith("q"):
        return "q"
    return "y"


def step_read(state):
    deep_head(state, "step * reading the name")
    w = state["words"]
    name = state["name"]
    if len(w) == 1:
        state["notes"].append("one word, probably a handle not a real name")
        print("  one word -> handle style, less likely a real name")
    else:
        state["notes"].append(str(len(w)) + " words, could be a real name")
        print("  " + str(len(w)) + " words -> could be a real name, shapes will matter")
    hasdig = False
    for chx in name:
        if chx.isdigit():
            hasdig = True
    if hasdig:
        state["notes"].append("has digits, old handle smell, maybe a birthyear")
        print("  has digits -> old handle smell, maybe a birthyear in there")
    else:
        state["notes"].append("no digits, maybe a newer account")
        print("  no digits -> cleaner handle, maybe a newer account")
    if "_" in name or "-" in name or "." in name:
        state["notes"].append("separator in the name, common pattern")
        print("  has a separator -> common style, worth keeping as-is too")
    short = name.replace(" ", "")
    if len(short) <= 3:
        state["notes"].append("very short handle, rare")
        print("  very short -> rare, good for searching")
    if len(short) > 15:
        state["notes"].append("long handle, fewer false hits expected")
        print("  long handle -> fewer false hits expected")
    if name.lower() != name:
        state["notes"].append("mixed caps, most sites fold it to lowercase anyway")
        print("  mixed caps -> sites lowercase it anyway, search the lower form")
    print("  notes so far: " + str(len(state["notes"])))


def step_shapes(state):
    deep_head(state, "step * username shapes")
    w = state["words"]
    shapes = []
    if len(w) >= 2:
        f = w[0]
        l = w[-1]
        shapes = [f + l, f + "." + l, f + "_" + l, f + "-" + l, l + f, f[0] + l, f + "." + l[:1], f + l[:1]]
        print("  two words, so mixing them the usual ways")
    else:
        u = w[0]
        shapes = [u, u + "_", "_" + u, u + "-", "the" + u, u + u[-1:]]
        print("  one word, so poking it with decoration")
    uniq = []
    for s in shapes:
        if s not in uniq:
            uniq.append(s)
    state["shapes"] = uniq
    line = "   "
    for s in uniq:
        line = line + state["c3"] + s + R + "  "
        if len(line) > 70:
            print(line)
            line = "   "
    if line.strip() != "":
        print(line)
    print("  " + D + "asking ddg about the first few shapes..." + R)
    gotn = 0
    for s in uniq[:3]:
        res = ddg_lookup('"' + s + '" profile')
        for r in res:
            state["links"].append([r[0], r[1], r[2], s])
            gotn = gotn + 1
        time.sleep(random.randint(3, 8) / 10)
    state["counts"]["shapes"] = gotn
    print("  shapes made: " + str(len(uniq)) + " * links back: " + str(gotn))


def step_sites(state):
    deep_head(state, "step * poking the big sites")
    if requests == None:
        print("  " + Y + "no requests lib, this step can't run. pip install requests" + R)
        state["counts"]["sites"] = 0
        return
    u = state["words"][0].lstrip("@")
    if len(state["words"]) >= 2:
        u = state["words"][0] + state["words"][1]
    pool = []
    for s in SITES:
        if s[0] in BIGSITES:
            pool.append(s)
    print("  " + D + "checking " + W + u + R + D + " on " + str(len(pool)) + " busy sites..." + R)
    hits = 0
    for site in pool:
        res = check_site(site, u)
        if res == None:
            continue
        if res[2] == 200:
            low = res[3].lower()
            if "not found" in low or "doesn't exist" in low or "page not found" in low:
                pass
            else:
                state["hits"].append(res)
                hits = hits + 1
                print("  " + tag("ok") + " " + HC + res[0] + R + " " + B + res[1] + R)
        time.sleep(random.randint(2, 6) / 10)
    state["counts"]["sites"] = hits
    print("  site hits: " + str(hits))


def step_dorks(state):
    deep_head(state, "step * the dork pile")
    q = state["name"]
    gotn = 0
    seen = []
    for label, tpl in DORKBITS[:3]:
        query = tpl.replace("{u}", '"' + q + '"')
        print("  " + D + "* " + label + R)
        res = ddg_lookup(query)
        for r in res:
            if r[1] in seen:
                continue
            seen.append(r[1])
            state["links"].append([r[0], r[1], r[2], label])
            gotn = gotn + 1
        time.sleep(random.randint(3, 8) / 10)
    state["counts"]["dorks"] = gotn
    print("  fresh links: " + str(gotn))


def step_web(state):
    deep_head(state, "step * plain web pile")
    q = '"' + state["name"] + '"'
    if len(state["words"]) >= 2:
        q = q + ' OR "' + state["words"][0] + " " + state["words"][1] + '" profile'
    print("  " + D + "searching: " + q + R)
    res = ddg_lookup(q)
    gotn = 0
    for r in res[:8]:
        state["links"].append([r[0], r[1], r[2], "web"])
        gotn = gotn + 1
    state["counts"]["web"] = gotn
    print("  links: " + str(gotn))


STEPFUNC = {"read": step_read, "shapes": step_shapes, "sites": step_sites,
            "dorks": step_dorks, "web": step_web}


def build_plan(state):
    plan = []
    plan.append(["read", "read the name first, see what we're even dealing with"])
    plan.append(["shapes", "build username shapes and search them"])
    if requests != None:
        plan.append(["sites", "poke the big sites with the main handle"])
        plan.append(["dorks", "run the dork pile, pastebin code and docs"])
        plan.append(["web", "plain web search around the plain name"])
    else:
        state["notes"].append("no requests lib, so every net step is off")
    return plan


def deep_chart(state):
    e = state["edge"]
    print()
    print(state["c1"] + (e * 58) + R)
    print(state["c1"] + "   THE PICTURE SO FAR" + R)
    print(state["c1"] + (e * 58) + R)
    counts = state["counts"]
    if len(counts) == 0:
        print()
        print("  " + D + "no counting steps ran, so no graph. run it again and answer y to the net steps" + R)
    biggest = 1
    for k in counts:
        if counts[k] > biggest:
            biggest = counts[k]
    print()
    print("  " + D + "what each step pulled in (bar graph)" + R)
    print()
    for k in counts:
        n = counts[k]
        fill = int(round(24 * n / biggest))
        col = random.choice(DEEPPALETTE)
        print("  " + col + k.ljust(8) + R + " " + col + ("" * fill) + R + D + ("*" * (24 - fill)) + R + " " + str(n))
    total = 0
    for k in counts:
        total = total + counts[k]
    print()
    print("  " + D + "how the pile grew while the steps ran (each row is one step)" + R)
    print()
    run = 0
    i = 1
    for k in counts:
        run = run + counts[k]
        fill = 0
        if total > 0:
            fill = int(round(40 * run / total))
        print("  " + D + str(i).rjust(2) + R + " " + state["c3"] + ("" * fill) + R + D + ("*" * (40 - fill)) + R + " " + str(run))
        i = i + 1
    print()
    print("  links in the bag: " + BOLD + str(len(state["links"])) + R)
    print("  notes made: " + str(len(state["notes"])))
    print("  site hits: " + str(len(state["hits"])))
    print()
    if len(state["links"]) > 0:
        print("  " + D + "top of the link pile:" + R)
        shown = 0
        for r in state["links"]:
            if shown == 8:
                break
            print("   " + state["c3"] + str(shown + 1) + "." + R + " " + W + r[0][:70] + R)
            print("      " + B + r[1][:90] + R)
            shown = shown + 1
        print()
    if total == 0 and len(state["links"]) == 0:
        print("  " + tag("warn") + " nothing stuck. rare name, or a quiet day on the internet")
    elif len(state["links"]) >= 10:
        print("  " + tag("ok") + " " + pick(BIGFP).replace("{n}", str(len(state["links"]))))
    else:
        print("  " + tag("info") + " " + pick(DEEPTAGS))
    print()


def cmd_deep(rest):
    global DEEP_RUNS
    bits = rest.split()
    if len(bits) == 0:
        print(" usage: deep <name or username>")
        print(" like: " + C + "deep john smith" + R + " " + D + "or a handle: " + C + "deep b0bthegoldfish" + R)
        print(" " + D + "it builds a plan, runs it step by step, asks before each one, saves it all" + R)
        return
    state = {}
    state["name"] = rest.strip().lstrip("@")
    state["words"] = rest.split()
    state["notes"] = []
    state["shapes"] = []
    state["links"] = []
    state["hits"] = []
    state["counts"] = {}
    state["steps_done"] = []
    deep_styler(state)
    print()
    print(" " + D + pick(DEEPTAGS) + R)
    plan = build_plan(state)
    e = state["edge"]
    print()
    print(state["c2"] + (e * 4) + " THE PLAN " + (e * 4) + R)
    n = 1
    for step in plan:
        print("  " + state["c2"] + str(n) + "." + R + " " + W + step[0] + R + D + " - " + step[1] + R)
        n = n + 1
    print("  " + D + "i ask before every step. enter = go, n = skip, q = stop and keep what we got" + R)
    print()
    i = 0
    for step in plan:
        i = i + 1
        a = deep_ask(state, "run step " + str(i) + "/" + str(len(plan)) + " (" + step[0] + ")? [enter = yes / n = skip / q = stop]")
        if a == "n":
            print(" " + D + "skipping " + step[0] + R)
            continue
        if a == "q":
            print(" " + Y + "ok, stopping the plan, keeping everything we got so far" + R)
            break
        try:
            STEPFUNC[step[0]](state)
        except KeyboardInterrupt:
            print()
            print(" " + Y + "cut that step short, moving on" + R)
        state["steps_done"].append(step[0])
        print()
    deep_chart(state)
    DEEP_RUNS = DEEP_RUNS + 1
    linkout = []
    for r in state["links"]:
        linkout.append([r[0], r[1], r[2], r[3]])
    hitout = []
    for h in state["hits"]:
        hitout.append([h[0], h[1]])
    LAST["deep"] = {"name": state["name"], "steps": state["steps_done"], "notes": state["notes"],
                    "shapes": state["shapes"], "links": linkout, "site_hits": hitout,
                    "when": str(datetime.datetime.now())[:16]}
    vault_add("plans", LAST["deep"])
    print(" " + D + "all of it went into the vault. " + C + "vault" + R + " " + D + "writes the json, " + C + "last" + R + " " + D + "reminds you" + R)
    print()


def cmd_ip(rest):
    ip = rest.strip()
    if ip == "":
        print(" usage: ip <address or host>")
        print(" like: " + C + "ip 8.8.8.8" + R + " " + D + "or a hostname, both work" + R)
        return
    if requests == None:
        print(" no requests lib, no geo. pip install requests")
        return
    has_letters = False
    for ch in ip:
        if ch.isalpha():
            has_letters = True
    if not has_letters and ":" not in ip:
        bits = ip.split(".")
        if len(bits) != 4:
            print(" that doesn't look like an ipv4 (four numbers, dots between). hostnames work too")
            return
        for bx in bits:
            if bx == "" or not bx.isdigit() or int(bx) > 255:
                print(" " + bx + " isn't a number between 0 and 255. that's not an ip")
                return
    print(" " + D + "asking a public registry, no keys involved..." + R)
    data = {}
    r = geturl("https://ipinfo.io/" + ip + "/json", 8)
    if r != None and r.status_code == 200:
        try:
            data = json.loads(r.text)
        except:
            data = {}
        if "error" in data:
            data = {}
    if data == {} or ("ip" not in data and "hostname" not in data):
        r = geturl("http://ip-api.com/json/" + ip, 8)
        if r != None and r.status_code == 200:
            try:
                raw = json.loads(r.text)
                if raw.get("status") == "success":
                    data = {"ip": raw.get("query", ip), "country": raw.get("country"),
                            "region": raw.get("regionName"), "city": raw.get("city"),
                            "org": (raw.get("isp") or "") + (", " + raw.get("org") if raw.get("org") and raw.get("org") != raw.get("isp") else ""),
                            "loc": ",".join([str(raw.get("lat", "")), str(raw.get("lon", ""))]).strip(",")}
            except:
                data = {}
    print()
    if data == {}:
        print(" " + tag("warn") + " both registries shrugged. private range? typo? or they just don't like me today")
        print()
        return
    rows = []
    where = ""
    if data.get("country"):
        where = data.get("city", "") + ", " + data["country"] if data.get("city") else data["country"]
        rows.append(("country", BOLD + data["country"] + R))
    if data.get("region"):
        rows.append(("region", data["region"]))
    if data.get("city"):
        rows.append(("city", data["city"]))
    if data.get("org"):
        rows.append(("network", C + str(data["org"]) + R))
    if data.get("hostname"):
        rows.append(("hostname", data["hostname"]))
    if data.get("loc") and "," in str(data.get("loc")):
        lat, lon = str(data["loc"]).split(",", 1)
        if lat and lon:
            rows.append(("pin", B + "https://www.google.com/maps?q=" + lat + "," + lon + R))
    card("where it lives", rows)
    if where != "":
        print(" " + D + "city is a guess from the registry. the network name is the real signal" + R)
    print()
    LAST["ip"] = {"q": ip, "where": where, "when": str(datetime.datetime.now())[:16]}
    vault_add("ips", LAST["ip"])


def cmd_way(rest):
    u = rest.strip()
    if u == "":
        print(" usage: wayback <url>")
        print(" like: " + C + "wayback oldforum.example.com/user/b0b" + R)
        return
    if requests == None:
        print(" no requests lib, no archive. pip install requests")
        return
    if "://" not in u:
        u = "https://" + u
    print(" " + D + "checking the archive's shelf..." + R)
    r = geturl("https://archive.org/wayback/available?url=" + u, 12)
    snap = None
    if r != None and r.status_code == 200:
        try:
            j = json.loads(r.text)
            snap = j.get("archived_snapshots", {}).get("closest")
        except:
            snap = None
    print()
    if snap:
        when = snap.get("timestamp", "?")
        nice = when[:4] + "-" + when[4:6] + "-" + when[6:8] if len(when) >= 8 else when
        print(" " + tag("ok") + " yep, it has a copy from " + BOLD + nice + R)
        print("    " + B + snap.get("url", "") + R)
    else:
        print(" " + tag("warn") + " nothing saved that i can see. doesn't mean never, just means not that url")
    print()
    print(" " + D + "everything they kept:" + R)
    print("    " + B + "https://web.archive.org/web/*/" + u + R)
    print()
    vault_add("archive", {"url": u, "snap": (snap.get("url", "") if snap else ""), "when": str(datetime.datetime.now())[:16]})

def vault_add(kind, data):
    entry = dict(data)
    entry["kind"] = kind
    VAULT[kind].append(entry)


def vault_line(e):
    k = e.get("kind", "")
    if k == "sweeps":
        return B + e.get("user", "?") + R + D + " * " + str(len(e.get("found", []))) + " hits of " + str(e.get("total", 0)) + R
    if k == "phones":
        return B + e.get("number", "?") + R + D + " * " + e.get("country", "?") + R
    if k == "emails":
        return B + e.get("addr", "?") + R + D + " * " + e.get("domkind", "?") + R
    if k == "ips":
        return B + e.get("q", "?") + R + D + " * " + (e.get("where") or "no luck") + R
    if k == "archive":
        return B + e.get("url", "?") + R + D + " * " + ("snapshot kept" if e.get("snap") else "nothing kept") + R
    if k == "plans":
        return B + e.get("name", "?") + R + D + " * " + str(len(e.get("links", []))) + " links * " + str(len(e.get("steps", []))) + " steps ran" + R
    return B + e.get("q", "?") + R + D + " * " + str(len(e.get("got", []))) + " results" + R


def vault_cmd(rest):
    rest = rest.strip().lower()
    total = 0
    for k in VAULT:
        total = total + len(VAULT[k])

    old = {}
    try:
        f = open(VAULT_FILE, "r", encoding="utf-8")
        old = json.load(f)
        f.close()
    except:
        old = {}
    olditems = {}
    if type(old) == dict:
        olditems = old.get("items", {})

    if rest == "wipe":
        for k in VAULT:
            VAULT[k] = []
        print(" " + tag("ok") + " vault emptied in memory. the file on disk stays until the next write")
        print()
        return

    if rest == "show":
        sect("what the vault holds")
        if total == 0:
            print("  nothing in it yet. run a search, phone, email, ip, web, anything")
            print()
            return
        for k in VAULT:
            if len(VAULT[k]) == 0:
                continue
            print("  " + HC + k + R + D + " (" + str(len(VAULT[k])) + ")" + R)
            for e in VAULT[k][-5:]:
                print("    " + D + "*" + R + " " + vault_line(e))
            if len(VAULT[k]) > 5:
                print("    " + D + "  and " + str(len(VAULT[k]) - 5) + " older ones" + R)
        print()
        print("  " + D + "vault writes the whole pile to " + C + VAULT_FILE + R)
        print()
        return

    if total == 0:
        got = 0
        for k in olditems:
            got = got + len(olditems[k])
        if got == 0:
            print(" nothing collected yet, and " + C + VAULT_FILE + R + " is empty or missing too")
            print(" go run a " + C + "search" + R + " or a " + C + "phone" + R + " first, then vault picks it up")
            print()
            return
        print(" nothing new this session, but the file already holds " + BOLD + str(got) + R + " things")
        print(" " + D + "it'll get merged in proper the next time you collect something" + R)
        print()
        return

    print(" " + D + "piling everything the tool has gotten into one json..." + R)
    merged = {}
    brought = 0
    for k in VAULT:
        merged[k] = list(VAULT[k])
        for e in olditems.get(k, []):
            if e not in merged[k]:
                merged[k].append(e)
                brought = brought + 1
    try:
        f = open(VAULT_FILE, "w", encoding="utf-8")
        json.dump({"updated": str(datetime.datetime.now())[:19], "items": merged}, f, indent=2, ensure_ascii=False)
        f.close()
        rows = []
        for k in sorted(merged):
            if len(merged[k]) == 0:
                continue
            extra = ""
            if brought > 0 and len(olditems.get(k, [])) > 0:
                extra = D + " (+" + str(len(olditems[k])) + " from before)" + R
            rows.append((k, GB + str(len(merged[k])) + R + D + " entries" + extra + R))
        grand = 0
        for k in merged:
            grand = grand + len(merged[k])
        rows.append(("total", BOLD + str(grand) + R + D + " things remembered" + R))
        card("vault", rows)
        print(" " + G + VAULT_FILE + R + " " + D + "written. plain json, opens with anything. the proper reader comes later" + R)
        print()
    except:
        print(" " + RD + "couldn't write " + VAULT_FILE + ". folder read only? name taken? no idea" + R)
        print()


def save_results(rest):
    data = None
    for k in ("sweep", "phone", "email", "ip", "web", "deep"):
        if k in LAST:
            data = LAST[k]
            break
    if data == None:
        print(" nothing to save yet, go run a search first")
        return
    if rest != "":
        fname = rest
    elif "user" in data:
        fname = "sweep_" + data["user"] + ".json"
    elif "number" in data:
        fname = "phone_" + data["number"].strip("+") + ".json"
    elif "addr" in data:
        fname = "email_" + data["addr"].split("@")[0] + ".json"
    elif "name" in data:
        fname = "deep_" + data["name"].replace(" ", "_") + ".json"
    elif "q" in data:
        fname = "web_" + tstamp().replace(":", "") + ".json"
    else:
        fname = "osint_" + tstamp().replace(":", "") + ".json"
    try:
        f = open(fname, "w", encoding="utf-8")
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.close()
        print(" saved it all to " + G + fname + R)
    except:
        print(" " + RD + "couldn't save that. folder read only? weird name? no idea" + R)


def last_what():
    sect("in memory right now")
    if len(LAST) == 0:
        print(" memory's empty, run a search or a web thing first")
        print()
        return
    if "sweep" in LAST:
        sw = LAST["sweep"]
        print("  sweep   " + B + sw["user"] + R + " * " + str(len(sw["found"])) + " hits of " + str(sw["total"]) + " * " + sw["when"])
    if "phone" in LAST:
        ph = LAST["phone"]
        print("  phone   " + B + ph["number"] + R + " * " + ph["country"] + " * " + ph["when"])
    if "email" in LAST:
        em = LAST["email"]
        print("  email   " + B + em["addr"] + R + " * " + em["domkind"] + " * " + em["when"])
    if "ip" in LAST:
        ipr = LAST["ip"]
        print("  ip      " + B + ipr["q"] + R + " * " + (ipr["where"] if ipr["where"] else "no luck") + " * " + ipr["when"])
    if "deep" in LAST:
        dp = LAST["deep"]
        print("  deep    " + B + dp["name"] + R + " * " + str(len(dp["links"])) + " links * " + str(len(dp["steps"])) + " steps ran * " + dp["when"])
    if "web" in LAST:
        wb = LAST["web"]
        print("  web     \"" + wb["q"] + "\" * " + str(len(wb["got"])) + " results * " + wb["when"])
    print()
    print(" " + D + "the " + C + "save" + R + " " + D + "command writes it to a json file" + R)
    print()


def tagline():
    print(" " + Y + pick(TAGLINES) + R)

def theme_cmd(rest):
    t = rest.strip().lower()
    if t == "":
        names = " * ".join(sorted(THEMES))
        print(" themes: " + C + names + R)
        print(" " + D + "now on " + HC + CONFIG["theme"] + R + D + ". try " + C + "theme light" + R + D + ", or " + C + "theme mono" + R + D + " for no colors at all" + R)
        return
    if t not in THEMES:
        print(" " + tag("meh") + " don't have that one. " + C + "theme" + R + D + " alone lists them" + R)
        return
    apply_theme(t)
    CONFIG["theme"] = t
    print(" " + tag("ok") + " switched to " + HC + t + R + D + " - logo redrawn so you can see the difference" + R)
    logo()

def nowcmd():
    print(" " + G + str(datetime.datetime.now())[:19] + R)

def wipe():
    try:
        os.system("clear" if os.name != "nt" else "cls")
    except:
        pass

def stats():
    up = time.time() - START
    try:
        h = int(up // 3600)
        m = int((up % 3600) // 60)
        s = int(up % 60)
    except:
        h = m = s = 0
    print()
    hr()
    kv("uptime", W + str(h) + "h " + str(m) + "m " + str(s) + "s", 14)
    kv("commands", W + str(CMDS_RUN), 14)
    kv("sweeps", W + str(SWEEPS_DONE), 14)
    kv("profiles hit", W + str(PROFILES_FOUND), 14)
    kv("web searches", W + str(WEB_SEARCHES), 14)
    kv("phone checks", W + str(PHONE_CHECKS), 14)
    kv("email checks", W + str(EMAIL_CHECKS), 14)
    kv("deep runs", W + str(DEEP_RUNS), 14)
    vaultn = 0
    for k in VAULT:
        vaultn = vaultn + len(VAULT[k])
    kv("vault items", W + str(vaultn), 14)
    kv("site list", W + str(len(SITES)) + R + D + " sites", 14)
    kv("code table", W + str(len(CCODES)) + R + D + " country codes", 14)
    kv("requests", W + ("loaded" if requests else "not installed"), 14)
    hr()
    print(" " + D + "counting the boring things since you said hi" + R)
    print()


def unknown(cmd):
    if cmd == "sudo":
        print(" " + Y + "nice try" + R)
        return
    if cmd == "google":
        print(" " + Y + "not google. close enough though:" + R + " " + C + "web <query>" + R)
        return
    if cmd in ("rm", "format", "del"):
        print(" " + RD + "absolutely not" + R)
        return
    if cmd == "hack":
        print(" " + Y + "wrong movie. this thing only reads what's already outside" + R)
        return
    if cmd in ("phone", "number", "num"):
        print(" " + Y + "it's there, needs an argument:" + R + " " + C + "phone +254712345678" + R)
        return
    if cmd == "breach":
        print(" " + Y + "no breach lists in here, those all want keys or logins" + R)
        return
    print(" " + D + pick(NOPE) + R + "   (" + C + "help" + R + " lists what works)")


def bye():
    print()
    print(" " + D + pick(GOODBYES) + R)


def boot():
    if os.name == "nt":
        os.system("")
    apply_theme(CONFIG["theme"])
    logo()
    hr()
    welcome()
    sect("start with these four")
    kv("search", C + "<username>" + R + D + "  - find them across " + str(len(SITES)) + " sites" + R)
    kv("phone", C + "<number>" + R + D + "  - country, mobile or not, lookup links" + R)
    kv("email", C + "<address>" + R + D + "  - pulled apart, gravatar peek" + R)
    kv("web", C + "<words>" + R + D + "  - search the web for you" + R)
    print()
    print(" " + D + "everything else lives in " + C + "help" + R + D + ". leave with " + C + "exit" + R)
    print()


def run():
    global CMDS_RUN
    while True:
        try:
            userin = input(PROMPT).strip()
        except KeyboardInterrupt:
            print()
            bye()
            break
        except EOFError:
            print()
            bye()
            break

        if not userin:
            continue

        CMDS_RUN = CMDS_RUN + 1

        parts = userin.split()
        cmd = parts[0].lower()
        rest = userin[len(parts[0]):].strip()

        try:
            if cmd in ("exit", "quit", "q", ":q"):
                bye()
                break

            elif cmd in ("help", "menu"):
                helpcmd()

            elif cmd in ("search", "find", "hunt", "sweep"):
                cmd_search(rest)

            elif cmd in ("web", "g", "ddg"):
                cmd_web(rest)

            elif cmd in ("phone", "num", "number"):
                cmd_phone(rest)

            elif cmd in ("email", "mail"):
                cmd_email(rest)

            elif cmd in ("dork", "dorks"):
                cmd_dork(rest)

            elif cmd == "deep":
                cmd_deep(rest)

            elif cmd in ("ip", "geo"):
                cmd_ip(rest)

            elif cmd in ("wayback", "wb"):
                cmd_way(rest)

            elif cmd == "sites": sites_list()

            elif cmd == "save": save_results(rest)

            elif cmd in ("vault", "store"): vault_cmd(rest)

            elif cmd == "last": last_what()

            elif cmd == "tag": tagline()

            elif cmd == "about": about()

            elif cmd == "stats": stats()

            elif cmd in ("now", "time"): nowcmd()

            elif cmd in ("clear", "cls"): wipe()

            elif cmd == "theme": theme_cmd(rest)

            else:
                unknown(cmd)

        except Exception as e:
            print(" " + RD + "something broke:" + R + " " + str(e))
            print(" " + D + "moving on like nothing happened" + R)


if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
    helpcmd()
else:
    boot()
    run()
