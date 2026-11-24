import sys, os, random, hashlib
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
D    = "\033[2m"
RD   = "\033[91m"
BOLD = "\033[1m"

CONFIG = {
    "theme": "dark",
    "slow_type": True,
    "timeout": 8,
}

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

PROMPT = C + "[?]" + R + " "

START = time.time()
CMDS_RUN = 0
SWEEPS_DONE = 0
PROFILES_FOUND = 0
WEB_SEARCHES = 0
PHONE_CHECKS = 0
EMAIL_CHECKS = 0
DEEP_RUNS = 0
LAST = {}

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
    "92": "3",
}

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


def hr(n=56, ch="─"):
    print(D + (ch * n) + R)

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
    print(C + LOGO + R)

def welcome():
    slow(" oh hi. this is osint lab, it looks at public stuff and nothing else")
    print(" " + D + pick(TAGLINES) + R)
    print(" " + D + "type " + C + "help" + R + D + " if you're lost" + R)


def helpcmd():
    print()
    print(" " + BOLD + "hunting" + R)
    print("  " + C + "search" + R + " <user>       check a username on every site in the list")
    print("  " + C + "search" + R + " <user> fast      first 30 sites only, quick peek")
    print("  " + C + "search" + R + " <user> only github,steam     just those ones")
    print("  " + C + "sites" + R + "           the whole list (" + str(len(SITES)) + " of them)")
    print("  " + C + "save" + R + " [name]      last results out to a json file")
    print("  " + C + "last" + R + "           what's sitting in memory right now")
    print()
    print(" " + BOLD + "numbers & mail" + R)
    print("  " + C + "phone" + R + " <number>   country code, mobile or not, links to look it up")
    print("  " + C + "phone" + R + " codes       the country code table (" + str(len(CCODES)) + " of them)")
    print("  " + C + "email" + R + " <addr>     pull the address apart, gravatar peek, search links")
    print()
    print(" " + BOLD + "web" + R)
    print("  " + C + "web" + R + " <query>     duckduckgo, bing if it sulks. no api keys")
    print("  " + C + "g" + R + " <query>      same thing, less typing")
    print("  " + C + "dork" + R + " <user>     google dorks ready to click, " + C + "dork <u> run" + R + " runs a few")
    print("  " + C + "deep" + R + " <name>     same name, other shapes + web results")
    print("  " + C + "ip" + R + " <addr>       rough geo off public registries, no keys")
    print("  " + C + "wayback" + R + " <url>   does the archive have a copy of this page")
    print()
    print(" " + BOLD + "small stuff" + R)
    print("  " + C + "tag" + R + "     random tagline      " + C + "about" + R + "     what this even is")
    print("  " + C + "stats" + R + "   session numbers     " + C + "now" + R + "       date and time")
    print("  " + C + "clear" + R + "   wipe the screen     " + C + "exit" + R + "      leave")
    print()


def about():
    print()
    print(" " + BOLD + "osint lab" + R)
    print()
    print(" small thing, runs local, only looks at public pages.")
    print(" give it a username and it checks if that name exists on a")
    print(" big pile of sites. give it words and it asks duckduckgo")
    print(" for pages, bing if duckduckgo sulks.")
    print()
    print(" give it a phone number and it reads the country code, the")
    print(" length, whether it starts like a mobile, and hands you the")
    print(" links. give it an email and it pulls the address apart and")
    print(" checks gravatar. no lookups behind any login, ever.")
    print()
    print(" a 200 status is a good guess, not proof. some sites lie")
    print(" about it. treat every hit as a hint.")
    print()
    print(" built it to find my own old accounts. don't be weird with it.")
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
    print(" " + D + pick(STATUS) + R + " checking " + str(total) + " sites for " + BOLD + user + R)
    print()
    found = []
    odd = []
    miss = 0
    n = 0
    try:
        for site in pool:
            n = n + 1
            res = check_site(site, user)
            sys.stdout.write("\r " + D + str(n) + "/" + str(total) + R + "        ")
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
                    print()
                    print(" " + G + "+" + R + " " + C + res[0] + R + " " + B + res[1] + R)
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
        print(" " + Y + "[!]" + R + " " + pick(EMPTY))
    else:
        print(" " + G + "found on " + str(len(found)) + " out of " + str(total) + R)
        if len(found) >= 3:
            tip = pick(BIGFP)
            tip = tip.replace("{n}", str(len(found)))
            print(" " + M + "[i]" + R + " " + tip)
    if len(odd) > 0:
        print()
        print(" " + D + "these ones answered something weird, blocked or grumpy:" + R)
        for w in odd:
            print(" " + Y + "?" + R + " " + C + w[0].ljust(15) + R + " " + D + "status " + str(w[2]) + R)
    print()
    print(" " + D + str(total) + " checked, " + str(len(found)) + " hits, " + str(len(odd)) + " odd ones, " + str(miss) + " misses. " + C + "save" + R + " " + D + "writes it out" + R)

    oddlist = []
    for w in odd:
        oddlist.append([w[0], w[2]])
    when = str(datetime.datetime.now())[:16]
    LAST["sweep"] = {"user": user, "total": total, "found": found, "odd": oddlist, "when": when}
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
    print(" " + D + str(len(SITELIST)) + " sites in the list, search runs all of them" + R)
    print()
    line = "  "
    i = 0
    for s in SITELIST:
        line = line + C + s[0].ljust(17) + R
        i = i + 1
        if i == 4:
            print(line)
            line = "  "
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
        print(" " + Y + "[!]" + R + " nothing came back. try different words maybe")
        print()
        return
    print(" " + D + str(len(got)) + " results for" + R + " " + BOLD + q + R)
    print()
    n = 1
    for r in got:
        print(" " + G + str(n) + "." + R + " " + BOLD + r[0] + R)
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
        print(" " + Y + "?" + R + " i don't recognize " + BOLD + num[:3] + R + " as a country code i know.")
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

    print("  country     " + BOLD + country + (R + " " + D + "(+" + cc + ")" + R if cc else R))
    print("  looks like  " + B + pretty.strip() + R)
    print("  digits      " + str(len(num)) + " total" + (D + " (" + str(len(restn)) + " after the code)" + R if cc else ""))

    if cc != "" and cc in NUMLEN:
        want = NUMLEN[cc]
        got = len(restn)
        if got == want:
            print("  length      " + G + str(got) + R + " after the code, that matches the " + str(want) + " i expected for +" + cc)
        else:
            print("  length      " + Y + str(got) + R + " after the code, i expected " + str(want) + " for +" + cc + ". typo or a weird plan, who knows")

    if cc != "" and cc in MOBILESTART:
        starts = []
        for chx in MOBILESTART[cc]:
            if chx.isdigit():
                starts.append(chx)
        if restn[:1] in starts:
            print("  type        " + G + "starts like a mobile" + R + " " + D + "(" + MOBILESTART[cc] + " are the usual openers for +" + cc + ")" + R)
        else:
            print("  type        " + D + "doesn't start like the usual mobile for +" + cc + ". landline, voip or virtual, probably" + R)
    elif cc != "":
        print("  type        " + D + "no mobile-pattern note for +" + cc + " in my table, sorry" + R)

    if cc != "" and cc not in NUMLEN and cc not in MOBILESTART:
        print("  " + D + "(i only keep length/mobile notes for the big countries)" + R)

    full = "+" + num
    print()
    print(" " + D + "no lookups here, no logins. these are just doors to knock on:" + R)
    for label, tpl in NUMLINKS:
        if label == "whatsapp":
            link = tpl.format(num)
        else:
            link = tpl.format("%2B" + num)
        print("  " + C + label.ljust(12) + R + " " + B + link + R)
    print()
    print(" " + D + "tip: also google the digits in groups, like " + C + '"0712 345"' + R + D + ". people write them all sorts of ways" + R)
    print()

    PHONE_CHECKS = PHONE_CHECKS + 1
    LAST["phone"] = {"number": full, "country": country, "digits": len(num), "when": str(datetime.datetime.now())[:16]}


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
        print(" " + Y + "?" + R + " domain " + BOLD + dom + R + " has no dot, so no mail server would answer it. typo?")
        print()
        kind = "broken looking"
    else:
        tld = dom.rsplit(".", 1)[1]
        print("  address     " + B + a + R)
        print("  local part  " + local + "  " + D + "(" + str(len(local)) + " chars" + (" + dots" if "." in local else "") + (" + plus-tag" if "+" in local else "") + ")" + R)
        print("  domain      " + dom + "  " + D + "(tld ." + tld + ")" + R)
        if dom in FREEMAIL:
            kind = "free mail"
            print("  kind        " + C + kind + R + D + " — big provider, millions of these, tells you almost nothing by itself" + R)
        elif dom in DISPOSABLE:
            kind = "throwaway"
            print("  kind        " + Y + kind + R + D + " — burner mail. whoever made it didn't plan on being found" + R)
        else:
            kind = "own domain"
            print("  kind        kind of its own thing. company, school or a personal domain")
            print("  " + D + "worth a look at " + C + "http://" + dom + R + D + " and their mx records somewhere like mxtoolbox" + R)
        if "+" in local:
            print("  " + D + "the +" + local.split("+", 1)[1] + " part is a gmail tag — strip it, it's the same mailbox: " + C + local.split("+", 1)[0] + "@" + dom + R)
        if "." in local and dom in FREEMAIL:
            print("  " + D + "gmail ignores dots — " + C + local.replace(".", "") + "@" + dom + R + D + " is the same inbox" + R)

    print()
    print(" " + D + "gravatar check..." + R)
    h = hashlib.md5(a.encode("utf-8")).hexdigest()
    r = geturl("https://www.gravatar.com/avatar/" + h + "?d=404&s=80", 8)
    if r == None:
        print(" " + Y + "?" + R + " couldn't reach gravatar at all. skip it")
    elif r.status_code == 200:
        print(" " + G + "+" + R + " there's a gravatar on this address. " + B + "https://gravatar.com/" + h + R)
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
    print(" " + D + "no breach lists here — those need keys or logins and this thing doesn't do that" + R)
    print()

    EMAIL_CHECKS = EMAIL_CHECKS + 1
    LAST["email"] = {"addr": a, "domkind": kind, "gravatar": h, "when": str(datetime.datetime.now())[:16]}


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
    print()
    print(" " + D + "dorks for" + R + " " + BOLD + q + R + D + ", click them or let me run a few" + R)
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
        print(" " + D + "· " + label + R)
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
        print(" " + Y + "[!]" + R + " nothing came back. ddg mood, probably. try the google links above")
    else:
        print(" " + G + str(len(got)) + " unique results" + R)
        print()
        n = 1
        for r in got[:12]:
            print(" " + G + str(n) + "." + R + " " + BOLD + r[0] + R + " " + D + "[" + r[3] + "]" + R)
            print("    " + B + r[1] + R)
            if r[2] != "":
                print("    " + D + r[2][:170] + R)
            n = n + 1
    print()
    LAST["web"] = {"q": "dorks: " + q, "got": [[r[0], r[1], r[2]] for r in got], "when": str(datetime.date.today()) + " " + tstamp()}


def cmd_deep(rest):
    global DEEP_RUNS
    if requests == None:
        print(" no requests, no deep. pip install requests first")
        return
    bits = rest.split()
    if len(bits) == 0:
        print(" usage: deep <name>   (one word or 'first last')")
        print(" like: " + C + "deep john smith" + R + " " + D + "builds the shapes and searches them" + R)
        return
    if len(bits) >= 2:
        f = bits[0].lstrip("@")
        l = bits[-1]
        shapes = [f + l, f + "." + l, f + "_" + l, f + "-" + l, l + f, f[0] + l, f + "." + l[:1], f + l[:1]]
        print(" " + D + "two words, so making the usual combinations" + R)
    else:
        u = bits[0].lstrip("@")
        shapes = [u, u + "_", "_" + u, u + "-", "the" + u, u + u[-1:]]
        print(" " + D + "one word, so poking at it with decoration. half of these will be garbage" + R)
    seen = []
    uniq = []
    for s in shapes:
        if s not in uniq:
            uniq.append(s)
    print()
    print(" " + D + "shapes to try (guesses, not findings):" + R)
    line = "  "
    for s in uniq:
        chunk = C + s.ljust(20) + R
        if len(line) + len(s) > 74:
            print(line)
            line = "  "
        line = line + chunk + "  "
    print(line)
    print()
    print(" " + D + "tip: run any of them through " + C + "search <shape>" + R + D + " for the full site sweep" + R)
    print()
    print(" " + D + "asking ddg about the first few..." + R)
    got = []
    seenlinks = []
    for s in uniq[:4]:
        print(" " + D + "· " + s + R)
        for res in ddg_lookup('"' + s + '" profile'):
            if res[1] in seenlinks:
                continue
            seenlinks.append(res[1])
            res.append(s)
            got.append(res)
        time.sleep(random.randint(3, 8) / 10)
    print()
    if len(got) == 0:
        print(" " + Y + "[!]" + R + " quiet out there. maybe the name's too generic or too rare, both go badly")
    else:
        print(" " + G + str(len(got)) + " unique hits" + R)
        print()
        n = 1
        for r in got[:12]:
            print(" " + G + str(n) + "." + R + " " + BOLD + r[0] + R + " " + D + "[shape: " + r[3] + "]" + R)
            print("    " + B + r[1] + R)
            if r[2] != "":
                print("    " + D + r[2][:170] + R)
            n = n + 1
    print()
    DEEP_RUNS = DEEP_RUNS + 1
    LAST["web"] = {"q": "deep: " + rest, "got": [[r[0], r[1], r[2]] for r in got], "when": str(datetime.date.today()) + " " + tstamp()}


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
        print(" " + Y + "[!]" + R + " both registries shrugged. private range? typo? or they just don't like me today")
        print()
        return
    where = ""
    if data.get("country"):
        where = data.get("city", "") + ", " + data["country"] if data.get("city") else data["country"]
        print("  country     " + BOLD + data["country"] + R)
    if data.get("region"):
        print("  region      " + data["region"])
    if data.get("city"):
        print("  city        " + data["city"])
    if data.get("org"):
        print("  network     " + C + str(data["org"]) + R)
    if data.get("hostname"):
        print("  hostname    " + data["hostname"])
    if data.get("loc") and "," in str(data.get("loc")):
        lat, lon = str(data["loc"]).split(",", 1)
        if lat and lon:
            print("  pin         " + B + "https://www.google.com/maps?q=" + lat + "," + lon + R)
    if where != "":
        print("  " + D + "city is a guess from the registry. the network name is the real signal" + R)
    print()
    LAST["ip"] = {"q": ip, "where": where, "when": str(datetime.datetime.now())[:16]}


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
        print(" " + G + "+" + R + " yep, it has a copy from " + BOLD + nice + R)
        print("    " + B + snap.get("url", "") + R)
    else:
        print(" " + Y + "[!]" + R + " nothing saved that i can see. doesn't mean never, just means not that url")
    print()
    print(" " + D + "wanna browse everything they kept:" + R)
    print("    " + B + "https://web.archive.org/web/*/" + u + R)
    print(" " + D + "and the cdx index if you like lists:" + R)
    print("    " + B + "https://web.archive.org/cdx/search/cdx?url=" + u.replace("://", "://") + "&output=text&limit=40" + R)
    print()


def save_results(rest):
    data = None
    for k in ("sweep", "phone", "email", "ip", "web"):
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
    print()
    if len(LAST) == 0:
        print(" memory's empty, run a search or a web thing first")
        print()
        return
    if "sweep" in LAST:
        sw = LAST["sweep"]
        print("  sweep   " + B + sw["user"] + R + " · " + str(len(sw["found"])) + " hits of " + str(sw["total"]) + " · " + sw["when"])
    if "phone" in LAST:
        ph = LAST["phone"]
        print("  phone   " + B + ph["number"] + R + " · " + ph["country"] + " · " + ph["when"])
    if "email" in LAST:
        em = LAST["email"]
        print("  email   " + B + em["addr"] + R + " · " + em["domkind"] + " · " + em["when"])
    if "ip" in LAST:
        ipr = LAST["ip"]
        print("  ip      " + B + ipr["q"] + R + " · " + (ipr["where"] if ipr["where"] else "no luck") + " · " + ipr["when"])
    if "web" in LAST:
        wb = LAST["web"]
        print("  web     \"" + wb["q"] + "\" · " + str(len(wb["got"])) + " results · " + wb["when"])
    print()
    print(" " + D + "the " + C + "save" + R + " " + D + "command writes it to a json file" + R)
    print()


def tagline():
    print(" " + Y + pick(TAGLINES) + R)

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
    print(f"  uptime        {h}h {m}m {s}s")
    print(f"  commands run  {CMDS_RUN}")
    print(f"  sweeps done   {SWEEPS_DONE}")
    print(f"  profiles hit  {PROFILES_FOUND}")
    print(f"  web searches  {WEB_SEARCHES}")
    print(f"  phone checks  {PHONE_CHECKS}")
    print(f"  email checks  {EMAIL_CHECKS}")
    print(f"  deep runs     {DEEP_RUNS}")
    print(f"  site list     {len(SITES)} sites")
    print(f"  code table    {len(CCODES)} country codes")
    print(f"  requests lib  {'loaded' if requests else 'not installed'}")
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
    logo()
    hr()
    welcome()
    hr()
    print()
    print(" " + D + "try " + C + "search <username>" + R + " " + D + "or " + C + "web <query>" + R + D + ", " + C + "help" + R + D + " for the rest" + R)
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

            elif cmd == "help":
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

            elif cmd == "last": last_what()

            elif cmd == "tag": tagline()

            elif cmd == "about": about()

            elif cmd == "stats": stats()

            elif cmd in ("now", "time"): nowcmd()

            elif cmd in ("clear", "cls"): wipe()

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
