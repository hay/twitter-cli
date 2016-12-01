import json, argparse, sys
from twitter import Twitter


def get_conf():
    try:
        jsondata = open("./config.json").read()
        config = json.loads(jsondata)
    except:
        sys.exit("Could not read or find config.json file")
    else:
        return config

def main():
    conf = get_conf()
    twitter = Twitter(conf)

    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--query', type = str,
        help = "Gets all tweets and retweets for a specifc search query (realtime)")
    parser.add_argument('-t', '--timeline', action = "store_true",
        help = "Gets all tweets for the authenticated user")
    parser.add_argument('-u', '--user', type = str,
        help = "Get a timeline with a username")
    parser.add_argument('-s', '--search', type = str,
        help = "Get results for a search query (not realtime)")

    args = parser.parse_args()

    if args.query:
        twitter.query(args.query)
    elif args.timeline:
        twitter.run_timeline()
    elif args.user:
        twitter.user_timeline()
    elif args.search:
        twitter.search(args.search)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()