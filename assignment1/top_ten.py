import json
import re
import sys

def get_hashtags(line):
    return map(lambda x: x['text'], json.loads(line).get('entities', {}).get('hashtags', []))

def main():
    hashtags = {}
    with open(sys.argv[1]) as tweets_file:
        for line in tweets_file:
            for hashtag in get_hashtags(line):
                hashtags[hashtag] = hashtags.get(hashtag, 0) + 1

    total = sum(hashtags.viewvalues())
    for hashtag, occ in sorted(hashtags.viewitems(), key=lambda x: x[1], reverse=True)[0:10]:
        print hashtag, occ# / total



if __name__ == '__main__':
    main()
