import json
import requests
import sys
import thread
from zlib import crc32


thread_count = 0


def check_link(url, name, level):
    global thread_count
    thread_count += 1
    try:
        req = requests.head(url, allow_redirects=True)
        if req.status_code != 200:
            print("Dead link (%s) - %s: %s" % (req.status_code, level, name))
        thread_count -= 1
    except Exception as e:
        print "%s: %s" % (e, url)
        thread_count -= 1


def iterate_items(node, level):
    for item in node:
        if item['type'] == 'folder':
            iterate_items(item['children'], "%s -> %s" % (level, item['name']))
        elif item['type'] == 'url':
            # check for duplicate
            crc = crc32(item['url'])
            if crc in hashes:
                print("Duplicate - %s: %s" % (level, item['name']))
            else:
                hashes.append(crc)

            # check for dead link
            thread.start_new_thread(check_link, (item['url'], item['name'], level,))
            #check_link(item['url'], item['name'], level)


if __name__ == '__main__':

    # load file contents
    content = json.load(open(sys.argv[1]))

    #import pdb
    #pdb.set_trace()

    hashes = []

    # iterate over bookmark bar
    iterate_items(content['roots']['bookmark_bar']['children'], 'Bookmark Bar')
    iterate_items(content['roots']['other']['children'], 'Other')

    while thread_count > 0:
        pass
