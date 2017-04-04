#!/usr/bin/env python
#coding=utf-8

from lxml import etree # pip install lxml
import urllib2
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# ----------------------------------------------------------
# config
# ----------------------------------------------------------
API_URL = r'https://mp.weixin.qq.com/debug/wxadoc/dev/api/'
COMPONENT_URL = r'https://mp.weixin.qq.com/debug/wxadoc/dev/component/'


# ----------------------------------------------------------
# json
# ----------------------------------------------------------
def write_json(data, path):
    in_json = json.dumps(
        data,
        sort_keys=True,
        indent=4,
        separators=(',', ': '),
        encoding="utf-8",
        ensure_ascii=False)

    with open(path, 'w') as fp:
        fp.write(in_json)

    print('-> %s' % path)


def write_api_json(data):
    write_json(data, 'wxapp_api.json')


def write_component_json(data):
    write_json(data, 'wxapp_component.json')


# ----------------------------------------------------------
# wget
# ----------------------------------------------------------
def wget(url):
    response = urllib2.urlopen(url)
    return response.read()


# ----------------------------------------------------------
# doc
# ----------------------------------------------------------
def parse_html(html):
    selector = etree.HTML(html)
    content = selector.xpath('//table/tbody/tr')
    wxapp_json = {}

    for item in content:
        td = item.xpath('td')
        api = td[0].xpath('a/text()')
        href = td[0].xpath('a/@href')
        desc = td[1].text

        if len(api) <> 1: continue
        api = api[0]
        href = href[0]
        wxapp_json[api] = {
            'desc': desc,
            'href': href,
        }
    return wxapp_json


def api_doc():
    html = wget(API_URL)
    wxapp_json = parse_html(html)
    write_api_json(wxapp_json)


def component_doc():
    html = wget(COMPONENT_URL)
    wxapp_json = parse_html(html)
    write_component_json(wxapp_json)


# ----------------------------------------------------------
# main
# ----------------------------------------------------------
if __name__ == '__main__':
    api_doc()
    component_doc()
