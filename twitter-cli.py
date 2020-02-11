from TwitterAPI import TwitterAPI
import json, argparse, sys, time, urllib

try:
    jsondata = open("./config.json").read()
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

args = {}

def get_time(complete = True):
    if complete:
        return time.strftime("%Y-%m-%dT%H%M", time.localtime())
    else:
        return time.strftime('%Y-%m-%d', time.localtime())

def get_filename(filename):
    if args.out:
        return args.out
    else:
        return filename

def search(q):
    f = open(get_filename("search-" + q + ".json"), "a")

    max_id = "inf"
    ids = []

    params = {
        "q" : urllib.quote_plus(q),
        "count" : 100,
        "lang" : "nl"
    }

    print "Going to search for " + params["q"]

    while max_id:
        if max_id is not "inf":
            params["max_id"] = max_id

        print "MAX: " + str(max_id)

        req = api.request("search/tweets", params)

        count = 0

        for msg in req.get_iterator():
            id_ = msg["id"]

            # Check if this ID not written already, and if so,
            # skip
            if id_ in ids:
                continue

            ids.append(id_)

            if id_ < max_id:
                max_id = msg["id"]

            f.write( json.dumps(msg) + "\n" )

            count += 1

        if count <= 1:
            print "Okay, that's all folks!"
            break
        else:
            print "Okay, got %s tweets" % count

        time.sleep(1)

    f.close()

def query(q):
    timestamp = get_time(complete = True)
    filename = get_filename("stream-" + q + "-" + timestamp + ".json")
    f = open(filename, "a")

    r = api.request('statuses/filter', { 'track' : q })

    for msg in r.get_iterator():
        f.write( json.dumps(msg) )
        f.write( "\n" )

def location(loc):
    timestamp = get_time(complete = True)
    filename = get_filename("stream-location-%s.json" % timestamp)
    f = open(filename, "a")

    r = api.request('statuses/filter', { 'locations' : loc })

    for msg in r.get_iterator():
        f.write( json.dumps(msg) )
        f.write( "\n" )

def user_timeline():
    timestamp = get_time(complete = False)
    f = open(get_filename("timeline_%s-%s.json" % (args.user, timestamp)), "w")

    max_id = "inf"
    params = {
        "screen_name" : args.user,
        "count" : 200
    }

    while max_id:
        if max_id is not "inf":
            params["max_id"] = max_id

        print "MAX: " + str(max_id)

        req = api.request("statuses/user_timeline", params)

        count = 0

        for msg in req.get_iterator():
            if msg["id"] < max_id:
                max_id = msg["id"]

            f.write( json.dumps(msg) + "\n" )

            count += 1

        if count == 1:
            print "Okay, that's all folks!"
            break
        else:
            print "Okay, got %s tweets" % count

        time.sleep(1)

    f.close()

def timeline():
    """Saves the authenticated users tweets to a datestamped json file"""
    print "Saving the timeline"

    timestamp = get_time(complete = False)
    f = open(get_filename("timeline_%s.json" % timestamp), "a")

    if args.user:
        req = api.request("statuses/user_timeline", {
            "screen_name" : args.user,
            "count" : 200
        })
    else:
        req = api.request('user')

    for msg in req.get_iterator():
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
    global args

    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--query', type = str, help = "Gets all tweets and retweets for a specifc search query (realtime)")
    parser.add_argument('-t', '--timeline', action = "store_true", help = "Gets all tweets for the authenticated user")
    parser.add_argument('-u', '--user', type = str, help = "Get a timeline with a username")
    parser.add_argument('-s', '--search', type = str, help = "Get results for a search query (not realtime)")
    parser.add_argument('-o', '--out', type = str, help = "Specifies a custom filename for the export")
    parser.add_argument('-l', '--location', type = str, help = "Get all tweets in a geolocation-bounded box (realtime)")

    args = parser.parse_args()

    if args.query:
        query(args.query)
    elif args.location:
        location(args.location)
    elif args.timeline:
        run_timeline()
    elif args.user:
        user_timeline()
    elif args.search:
        search(args.search)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()