import requests
import sys
# import pprint

FILE_ROMANTABLE = "./romantable.txt"
FILE_ROMANTABLE_EMOJI = "./romantable_emoji.txt"

URL = 'https://raw.githubusercontent.com/joypixels/emoji-toolkit/master/emoji.json'
r = requests.get(URL)

if (r.status_code != requests.codes.ok):
    sys.exit(f"Error! HTTP Status Code: {r.status_code}")


pre_dic = {}  # { code: emoji }
for code, v in r.json().items():
    shortname = v["shortname"].rstrip(':')
    shortname_alternates = v["shortname_alternates"]
    code_points = v["code_points"]["fully_qualified"]

    if ('-' in code_points):
        splited_code_points = code_points.split('-')
        unicode = ''.join([chr(int(c, 16)) for c in splited_code_points])
        emoji = unicode.encode('utf-16', 'surrogatepass').decode('utf-16')
    else:
        emoji = chr(int(code_points, 16))

    pre_dic[shortname] = emoji

    for i in shortname_alternates:
        if not i.startswith(shortname):
            pre_dic[i.rstrip(':')] = emoji

dic = {}
for k, v in pre_dic.items():
    is_match = False
    for key in pre_dic.keys():
        if k == key:
            continue
        if key.startswith(k):
            is_match = True
            break

    if is_match:
        dic[k + ':'] = v
    else:
        dic[k] = v

# pprint.pprint(dic)
# print(len(dic))
rt = ""
with open(FILE_ROMANTABLE, 'r') as f:
    rt = f.read()
with open(FILE_ROMANTABLE_EMOJI, 'w') as f:
    f.write(rt)
    for t in sorted(dic.items()):
        f.write(f"{t[0]} {t[1]}\n")
