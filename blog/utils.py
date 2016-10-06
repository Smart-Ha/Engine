# encoding=utf-8
import re
from flask import request
from flask import url_for


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


def extract_tags(tags):
    whitespace = re.compile('\s')
    nowhite = whitespace.sub("", tags)
    tags_array = nowhite.split(',')

    cleaned = []
    for tag in tags_array:
        if tag not in cleaned and tag != "":
            cleaned.append(tag)
    return cleaned
