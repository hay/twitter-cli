#!/usr/bin/env python3
import json, sys
from dataknead import Knead
from pathlib import Path

if len(sys.argv) < 2:
    sys.exit("Need filename")

infile = open(sys.argv[1])
outfile = Path(Path(sys.argv[1]).stem).with_suffix(".csv")
tweets = []

for tweet in infile:
    try:
        t = json.loads(tweet)
    except:
        print("Could not convert this tweet")
        continue

    try:
        loc = t["coordinates"]["coordinates"]
        loc.reverse()
        loc = ",".join([str(l) for l in loc])
    except:
        loc = ""

    tid =  t["id"]
    user = t["user"]["screen_name"]

    if "full_text" in t:
        # Full 280 character tweets
        text = t["full_text"]
    else:
        text = t["text"]

    tweets.append({
        "id"   : tid,
        "date" : t["created_at"],
        "user" : user,
        "user_link" : f"https://twitter.com/{user}",
        "text" : text,
        "tweet_link" : f"https://twitter.com/{user}/status/{tid}",
        "location" : loc,
        "is_retweet" : bool(t.get("retweeted_status", False)),
        "is_reply" : bool(t["in_reply_to_user_id"]),
        "lang" : t["lang"]
    })

Knead(tweets).write(outfile)