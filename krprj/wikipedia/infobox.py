# -*- coding: utf-8 -*-

def parse_infobox(page):
    ibox = {}
    text = ''.join(page)
    current = ''
    start = text.lower().find('{{infobox')
    if start > -1:
        count = 0
        for pos, letter in enumerate(text[start::]):
            if letter == '{':
                count += 1
            elif letter == '}':
                count -= 1
            if count == 0:
                end = start + pos + 1
                break
        infobox = text[start:end].split('\n')
        for line in infobox:
            if line.strip().startswith('|') and '=' in line:
                key = ''
                value = ''
                elems = line.strip('|').split('=')
                if len(elems) > 0:
                    key = elems[0].strip()
                    if len(elems) > 1:
                        value = elems[1].strip()
                    ibox[key] = value
    return ibox

