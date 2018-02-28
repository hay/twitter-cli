#!/usr/bin/env python
import json, sys
import unicodecsv as csv

if len(sys.argv) < 2:
    sys.exit("Need filename")

infile = open(sys.argv[1])
outfile = open(sys.argv[1].replace(".json", ".csv"), "w")
outcsv = csv.writer(outfile)

outcsv.writerow(["id", "date", "user", "text", "location"])

for tweet in infile:
    try:
        t = json.loads(tweet)
    except:
        print "Could not convert this tweet"
        continue

    try:
        loc = t["coordinates"]["coordinates"]
        loc.reverse()
        loc = ",".join([str(l) for l in loc])
    except:
        loc = ""

    outcsv.writerow([
        t["id"],
        t["created_at"],
        t["user"]["screen_name"].encode('utf-8'),
        t["text"].encode('utf-8'),
        loc
    ])

infile.close()
outfile.close()