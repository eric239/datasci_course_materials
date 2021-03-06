import json
import re
import sys

def load_sent(fname):
    with open(fname) as sent_file:
        return { term: int(score) for term, score in [ line.split('\t') for line in sent_file ] }

def get_text(line):
    return json.loads(line).get('text', '')

def process_term(term):
    return re.sub(r'(?u)\W*', '', term) if term and not term.startswith('http') and (term[0].isalpha() or term[0] == '#') else ''

def tokenize(text):
    return filter(len, map(process_term, re.split(r'\s+', text.lower())))

def main():
    sent_dict = load_sent(sys.argv[1])
    with open(sys.argv[2]) as tweets_file:
        for line in tweets_file:
            print sum(map(lambda token: sent_dict.get(token, 0), tokenize(get_text(line))))


if __name__ == '__main__':
    main()
