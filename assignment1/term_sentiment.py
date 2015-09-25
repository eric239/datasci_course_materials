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
    pos_dict = {}
    neg_dict = {}
    with open(sys.argv[2]) as tweets_file:
        for line in tweets_file:
            pos = 0
            neg = 0
            terms = tokenize(get_text(line))
            for term in terms:
                sent = sent_dict.get(term, 0)
                if sent > 0:
                    pos += 1
                elif sent < 0:
                    neg += 1
            for term in terms:
                if not term in sent_dict:
                    pos_dict[term] = pos_dict.get(term, 1.0) + pos
                    neg_dict[term] = neg_dict.get(term, 1.0) + neg

    for term, pos in pos_dict.viewitems():
        neg = neg_dict[term]
        print term.encode('utf-8'), pos / neg


if __name__ == '__main__':
    main()
