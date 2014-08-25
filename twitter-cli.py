from TwitterAPI import TwitterAPI
import json, argparse, sys, time

try:
    jsondata = file("./config.json").read()
except:
    sys.exit("Could not find config.json file")

try:
    config = json.loads(jsondata)
except:
    sys.exit("Could not parse the config.json file")

api = TwitterAPI(
    config["consumer_key"],
    config["consumer_secret"],
    config["access_token_key"],
    config["access_token_secret"]
)

def get_time(complete = True):
    if complete:
        return time.strftime("%Y-%m-%dT%H%M", time.localtime())
    else:
        return time.strftime('%Y-%m-%d', time.localtime())

def search(q):
    timestamp = get_time(complete = True)
    filename = "stream-" + q + "-" + timestamp + ".json"
    f = open(filename, "a")

    r = api.request('statuses/filter', { 'track' : q })

    for msg in r.get_iterator():
        f.write( json.dumps(msg) )
        f.write( "\n" )

def timeline():
    """Saves the authenticated users tweets to a datestamped json file"""
    print "Saving the timeline"

    timestamp = get_time(complete = False)
    f = open("timeline_%s.json" % timestamp, "a")
    r = api.request('user')

    for msg in r.get_iterator():
        # Check if we need a new logfile
        timestamp_now = get_time(complete = False)

        if timestamp_now != timestamp:
            print timestamp_now, timestamp
            print "New day, opening a new logfile"
            f.close()
            timestamp = get_time(complete = False)
            f = open("timeline_%s.json" % timestamp, "a")

        f.write( json.dumps(msg) )
        f.write( "\n" )

def run_timeline():
    try:
        timeline()
    except Exception as e:
        print "Got some kind of error, waiting a minute, then trying again"
        print e
        time.sleep(60)
        run_timeline();

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--query', type = str, help = "Gets all tweets and retweets for a specifc search query")
    parser.add_argument('-t', '--timeline', action = "store_true", help = "Gets all tweets for the authenticated user")

    args = parser.parse_args()

    if args.query:
        search(args.query)
    elif args.timeline:
        run_timeline()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()