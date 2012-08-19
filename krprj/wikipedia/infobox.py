# -*- coding: utf-8 -*-


def parse_infobox(page):
    ibox = {}
    text = ''.join(page)
    current = ''
    infobox = []
    inside = False
    for line in page:
        if line.lower().strip().strip('|') == '}}':
            break
        if inside:
            infobox.append(line)
        if line.lower().strip().startswith('{{infobox'):
            inside = True

    # WIKIPEDIA MARKUP SUCKS
    # start = text.lower().find('{{infobox')
    # if start > -1:
    #     count = 0
    #     for pos, letter in enumerate(text[start::]):
    #         if letter == '{':
    #             count += 1
    #         elif letter == '}':
    #             count -= 1
    #         if count == 0:
    #             end = start + pos + 1
    #             break
    #     infobox = text[start:end].split('\n')

    # box = ''.join(infobox)
    # print "Box:", box
    # kv = box.split('|')[1:-1]
    # for pair in kv:
    #     elems = pair.split('=', 1)
    #     if len(elems) > 0:
    #         key = elems[0].strip()
    #         if len(elems) > 1:
    #             value = elems[1].strip()
    #         ibox[key] = value

    key = ''
    value = ''
    for line in infobox:
        if line.strip().startswith('|') and '=' in line:
            ibox[key] = value
            key = ''
            value = ''
            elems = line.strip('|').split('=', 1)
            if len(elems) > 0:
                key = elems[0].strip()
                if len(elems) > 1:
                    value = elems[1].strip()
        else:
            value = value + line
    return ibox
