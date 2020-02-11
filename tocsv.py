#!/usr/bin/env python3
import json, sys
from dataknead import Knead

TWITTER_LINK = "https://twitter.com/%s/status/%s"

if len(sys.argv) < 2:
    sys.exit("Need filename")

infile = open(sys.argv[1])
outfile = sys.argv[1].replace(".json", ".csv")
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

    tweets.append({
        "id"   : tid,
        "date" : t["created_at"],
        "user" : user,
        "user_link" : "https://twitter.com/%s" % user,
        "text" : t["text"],
        "tweet_link" : TWITTER_LINK % (user, tid),
        "location" : loc,
        "is_retweet" : bool(t.get("retweeted_status", False))
    })

Knead(tweets).write("tweets-amalia.csv")