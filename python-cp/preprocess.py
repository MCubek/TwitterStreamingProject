import string
import re

english_punctuations = string.punctuation
punctuations_list = english_punctuations

def separate_hashtags(s, tokenizer, segmenter):
    '''Removes the hashtag sign and segments the hashtag text.'''
    hashtags = []
    l = []
    for i, s_i in enumerate(s):
        if s_i.startswith('#'):
            tmp = tokenizer.tokenize(segmenter.segment(s_i.replace('#', '')))
            l.extend(tmp)
        else:
            l.append(s_i)
    return l



def preprocess_words(s):
    '''
    Removes tags, links, smiley faces, | signs, stopwords and changes the case to lower.
    '''
    ret_list = []

    smiley_regex = r'([\:\;\=][()PDO\/\]\[p|]+)+'
    
    is_tag = lambda w: w.startswith('@')
    is_vertical_line = lambda w: w.startswith('|')
    is_link = lambda w: w.startswith("http") or w.startswith("https")
    is_hashtag = lambda w: w.startswith("#")
    is_smiley = lambda w: re.match(smiley_regex, w)

    w2 = []
    for i, w in enumerate(s):
        if is_tag(w) or is_link(w) or is_vertical_line(w):
            continue

        elif is_hashtag(w):
            w_tmp = w.replace('#', '')
            if w_tmp != '':
                lower_append(w_tmp, w2)

        elif is_smiley(w):
            w_tmp = re.sub(smiley_regex, '', w)
            if w_tmp != '':
                lower_append(w_tmp, w2)

        else:
            w_tmp = w.replace('#', '')
            w_tmp = w_tmp.replace('|', '')
            w_tmp = w_tmp.replace('_', '')
            w_tmp = w_tmp.replace('...', '')
            if w_tmp != '':
                lower_append(w_tmp, w2)

    return ' '.join([i for i in w2 if len(i) > 2])

def lower_append(w, l):
    l.append(w.lower())

def cleaning_punctuations(text):
    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)

def remove_tuple_characters(s):
    return [re.sub(r'(.)\1{2,}', r'\1', w) for w in s.split()]

def lemmatize(s, lemmatizer):
    ret = ' '.join([lemmatizer.lemmatize(word) for word in s])
    return ret

def preprocess_tweet(tweet_text, tokenizer, segmenter, lemmatizer):
    tokenized = tokenizer.tokenize(tweet_text)
    text = preprocess_words(separate_hashtags(tokenized, tokenizer, segmenter))
    text = cleaning_punctuations(text)
    text = remove_tuple_characters(text)
    return lemmatize(text, lemmatizer)import string
import re

english_punctuations = string.punctuation
punctuations_list = english_punctuations

def separate_hashtags(s, tokenizer, segmenter):
    '''Removes the hashtag sign and segments the hashtag text.'''
    hashtags = []
    l = []
    for i, s_i in enumerate(s):
        if s_i.startswith('#'):
            tmp = tokenizer.tokenize(segmenter.segment(s_i.replace('#', '')))
            l.extend(tmp)
        else:
            l.append(s_i)
    return l



def preprocess_words(s):
    '''
    Removes tags, links, smiley faces, | signs, stopwords and changes the case to lower.
    '''
    ret_list = []

    smiley_regex = r'([\:\;\=][()PDO\/\]\[p|]+)+'
    
    is_tag = lambda w: w.startswith('@')
    is_vertical_line = lambda w: w.startswith('|')
    is_link = lambda w: w.startswith("http") or w.startswith("https")
    is_hashtag = lambda w: w.startswith("#")
    is_smiley = lambda w: re.match(smiley_regex, w)

    w2 = []
    for i, w in enumerate(s):
        if is_tag(w) or is_link(w) or is_vertical_line(w):
            continue

        elif is_hashtag(w):
            w_tmp = w.replace('#', '')
            if w_tmp != '':
                lower_append(w_tmp, w2)

        elif is_smiley(w):
            w_tmp = re.sub(smiley_regex, '', w)
            if w_tmp != '':
                lower_append(w_tmp, w2)

        else:
            w_tmp = w.replace('#', '')
            w_tmp = w_tmp.replace('|', '')
            w_tmp = w_tmp.replace('_', '')
            w_tmp = w_tmp.replace('...', '')
            if w_tmp != '':
                lower_append(w_tmp, w2)

    return ' '.join([i for i in w2 if len(i) > 2])

def lower_append(w, l):
    l.append(w.lower())

def cleaning_punctuations(text):
    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)

def remove_tuple_characters(s):
    return [re.sub(r'(.)\1{2,}', r'\1', w) for w in s.split()]

def lemmatize(s, lemmatizer):
    ret = ' '.join([lemmatizer.lemmatize(word) for word in s])
    return ret

def preprocess_tweet(tweet_text, tokenizer, segmenter, lemmatizer):
    tokenized = tokenizer.tokenize(tweet_text)
    text = preprocess_words(separate_hashtags(tokenized, tokenizer, segmenter))
    text = cleaning_punctuations(text)
    text = remove_tuple_characters(text)
    return lemmatize(text, lemmatizer)