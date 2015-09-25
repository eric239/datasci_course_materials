import json
import re
import sys

states = { 
        'ak': 'alaska',
        'al': 'alabama',
        'ar': 'arkansas',
        'as': 'american samoa',
        'az': 'arizona',
        'ca': 'california',
        'co': 'colorado',
        'ct': 'connecticut',
        'dc': 'district of columbia',
        'de': 'delaware',
        'fl': 'florida',
        'ga': 'georgia',
        'gu': 'guam',
        'hi': 'hawaii',
        'ia': 'iowa',
        'id': 'idaho',
        'il': 'illinois',
        'in': 'indiana',
        'ks': 'kansas',
        'ky': 'kentucky',
        'la': 'louisiana',
        'ma': 'massachusetts',
        'md': 'maryland',
        'me': 'maine',
        'mi': 'michigan',
        'mn': 'minnesota',
        'mo': 'missouri',
        'mp': 'northern mariana islands',
        'ms': 'mississippi',
        'mt': 'montana',
        'nc': 'north carolina',
        'nd': 'north dakota',
        'ne': 'nebraska',
        'nh': 'new hampshire',
        'nj': 'new jersey',
        'nm': 'new mexico',
        'nv': 'nevada',
        'ny': 'new york',
        'oh': 'ohio',
        'ok': 'oklahoma',
        'or': 'oregon',
        'pa': 'pennsylvania',
        'pr': 'puerto rico',
        'ri': 'rhode island',
        'sc': 'south carolina',
        'sd': 'south dakota',
        'tn': 'tennessee',
        'tx': 'texas',
        'ut': 'utah',
        'va': 'virginia',
        'vi': 'virgin islands',
        'vt': 'vermont',
        'wa': 'washington',
        'wi': 'wisconsin',
        'wv': 'west virginia',
        'wy': 'wyoming'
}


def load_sent(fname):
    with open(fname) as sent_file:
        return { term: int(score) for term, score in [ line.split('\t') for line in sent_file ] }


def get_text_and_loc(line):
    tweet = json.loads(line)
    text = tweet.get('text', '')# if tweet.get('lang', '') == 'en' else ''
    loc = tweet.get('user', {}).get('location', '') if text else ''
    return text, loc


def process_term(term):
    return re.sub(r'(?u)\W*', '', term) if term and not term.startswith('http') and (term[0].isalpha() or term[0] == '#') else ''

def tokenize(text):
    return filter(len, map(process_term, re.split(r'\s+', text.lower())))


def get_state(loc):
    if not loc:
        return ''
    lloc = loc.lower().strip()
    for code, name in states.viewitems():
        if name in lloc:
            return code
    if len(lloc) > 1 and (len(lloc) == 2 or lloc[-3] in ' ,;') and lloc[-2:] in states:
        return lloc[-2:]
    return ''


def main():
    sent_dict = load_sent(sys.argv[1])
    state_sent = {}
    state_occ = {}

    with open(sys.argv[2]) as tweets_file:
        for line in tweets_file:
            text, loc = get_text_and_loc(line)
            if text:
                state = get_state(loc)
                if state:
                    state_sent[state] = state_sent.get(state, 0.0) + sum(map(lambda token: sent_dict.get(token, 0), tokenize(text)))
                    state_occ[state] = state_occ.get(state, 0) + 1

    max_sent = -0xFFFFFFFF
    max_state = ''
    for state, occ in state_occ.viewitems():
        sent = state_sent[state] / occ
        if sent > max_sent:
            max_sent = sent
            max_state = state

    print max_state.upper()


if __name__ == '__main__':
    main()
