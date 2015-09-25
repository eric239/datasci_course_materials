import json
import re
import sys

def get_text(line):
    return json.loads(line).get('text', '')

def process_term(term):
    return re.sub(r'(?u)\W*', '', term) if term and not term.startswith('http') and (term[0].isalpha() or term[0] == '#') else ''

def tokenize(text):
    return filter(len, map(process_term, re.split(r'\s+', text.lower())))

def main():
    terms_occ = {}
    with open(sys.argv[1]) as tweets_file:
        for line in tweets_file:
            for term in tokenize(get_text(line)):
                terms_occ[term] = terms_occ.get(term, 0.0) + 1
    total_occ = sum(terms_occ.viewvalues())
    for term, occ in terms_occ.viewitems():
        print term.encode('utf-8'), occ / total_occ



if __name__ == '__main__':
    main()
