import json, csv, sys

if len(sys.argv) < 2:
    sys.exit("Need filename")

infile = open(sys.argv[1])
outfile = open(sys.argv[1].replace(".json", ".csv"), "w")
outcsv = csv.writer(outfile)

outcsv.writerow(["id", "date", "text"])

for tweet in infile:
    t = json.loads(tweet)
    outcsv.writerow([
        t["id"], t["created_at"], t["text"].encode('utf-8')
    ])

infile.close()
outfile.close()
