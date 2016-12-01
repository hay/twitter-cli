from TwitterAPI import TwitterAPI
import time, urllib.request, urllib.parse, urllib.error, json

class Twitter:
    def __init__(self, config):
        self.api = TwitterAPI(
            config["consumer_key"],
            config["consumer_secret"],
            config["access_token_key"],
            config["access_token_secret"]
        )

    def get_time(self, complete = True):
        if complete:
            return time.strftime("%Y-%m-%dT%H%M", time.localtime())
        else:
            return time.strftime('%Y-%m-%d', time.localtime())

    def search(self, q):
        f = open("search-" + q + ".json", "a")

        max_id = "inf"
        params = { "q" : urllib.parse.quote_plus(q) }

        while max_id:
            if max_id is not "inf":
                params["max_id"] = max_id

            print("MAX: " + str(max_id))

            req = self.api.request("search/tweets", params)

            count = 0

            for msg in req.get_iterator():
                if msg["id"] < max_id:
                    max_id = msg["id"]

                f.write( json.dumps(msg) + "\n" )

                count += 1

            if count == 1:
                print("Okay, that's all folks!")
                break
            else:
                print("Okay, got %s tweets" % count)

            time.sleep(1)

        f.close()

    def query(self, q):
        timestamp = get_time(complete = True)
        filename = "stream-" + q + "-" + timestamp + ".json"
        f = open(filename, "a")

        r = self.api.request('statuses/filter', { 'track' : q })

        for msg in r.get_iterator():
            f.write( json.dumps(msg) )
            f.write( "\n" )

    def user_timeline(self):
        timestamp = get_time(complete = False)
        f = open("timeline_%s-%s.json" % (args.user, timestamp), "w")

        max_id = "inf"
        params = {
            "screen_name" : args.user,
            "count" : 200
        }

        while max_id:
            if max_id is not "inf":
                params["max_id"] = max_id

            print("MAX: " + str(max_id))

            req = self.api.request("statuses/user_timeline", params)

            count = 0

            for msg in req.get_iterator():
                if msg["id"] < max_id:
                    max_id = msg["id"]

                f.write( json.dumps(msg) + "\n" )

                count += 1

            if count == 1:
                print("Okay, that's all folks!")
                break
            else:
                print("Okay, got %s tweets" % count)

            time.sleep(1)

        f.close()

    def timeline(self):
        """Saves the authenticated users tweets to a datestamped json file"""
        print("Saving the timeline")

        timestamp = get_time(complete = False)
        f = open("timeline_%s.json" % timestamp, "a")

        if args.user:
            req = self.api.request("statuses/user_timeline", {
                "screen_name" : args.user,
                "count" : 200
            })
        else:
            req = self.api.request('user')

        for msg in req.get_iterator():
            # Check if we need a new logfile
            timestamp_now = get_time(complete = False)

            if timestamp_now != timestamp:
                print(timestamp_now, timestamp)
                print("New day, opening a new logfile")
                f.close()
                timestamp = get_time(complete = False)
                f = open("timeline_%s.json" % timestamp, "a")

            f.write( json.dumps(msg) )
            f.write( "\n" )

    def run_timeline(self):
        try:
            timeline()
        except Exception as e:
            print("Got some kind of error, waiting a minute, then trying again")
            print(e)
            time.sleep(60)
            run_timeline();