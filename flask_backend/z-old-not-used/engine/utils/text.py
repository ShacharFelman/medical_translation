import re

def is_text_contains_words_from_list(text, word_list):
    for separator in ('|', '@', '#', '$', '%', '^', '&', '*'):
        if separator not in text:
            break
    else:
        return False

    pattern = r'\b(?:{})\b'.format(separator.join(map(re.escape, word_list)))
    return bool(re.search(pattern, text, re.IGNORECASE))


def get_matching_words_in_text(text, word_list):
    matching_words = []
    for separator in ('|', '@', '#', '$', '%', '^', '&', '*'):
        if separator not in text:
            break
    else:
        return matching_words

    pattern = r'\b(?:{})\b'.format(separator.join(map(re.escape, word_list)))
    matches = re.findall(pattern, text, re.IGNORECASE)
    matching_words.extend(matches)
    return matching_words