import sys, os, random
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
    print(" " + BOLD + "web" + R)
    print("  " + C + "web" + R + " <query>     duckduckgo, bing if it sulks. no api keys")
    print("  " + C + "g" + R + " <query>      same thing, less typing")
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


def save_results(rest):
    data = None
    if "sweep" in LAST:
        data = LAST["sweep"]
    elif "web" in LAST:
        data = LAST["web"]
    if data == None:
        print(" nothing to save yet, go run a search first")
        return
    if rest != "":
        fname = rest
    elif "user" in data:
        fname = "sweep_" + data["user"] + ".json"
    else:
        fname = "web_" + tstamp().replace(":", "") + ".json"
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
    print(f"  site list     {len(SITES)} sites")
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
