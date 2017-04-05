import sublime
import sublime_plugin
import os
import copy
import json


# ----------------------------------------------------------
# Config
# ----------------------------------------------------------
def get_api_url():
    return r'https://mp.weixin.qq.com/debug/wxadoc/dev/api/'


def get_component_url():
    return r'https://mp.weixin.qq.com/debug/wxadoc/dev/component/'


def get_api_json_path():
    return "/".join(["Packages", "wxapp", "wxapp_api.json"])


def get_component_json_path():
    return "/".join(["Packages", "wxapp", "wxapp_component.json"])


# ----------------------------------------------------------
# Utils
# ----------------------------------------------------------
def open_url(url):
    if sublime.platform() == 'osx':
        command = 'open'
    elif sublime.platform() == 'windows':
        command = 'start'
    elif sublime.platform() == 'linux':
        command = 'lynx'
    command += ' ' + str(url)
    os.system(command)


# ----------------------------------------------------------
# Manager
# ----------------------------------------------------------
class WxappManager():
    def open_doc(self, json_path, prefix_url):
        doc_dict = json.loads(sublime.load_resource(json_path))

        doc_list = list(doc_dict.keys())
        doc_list = sorted(doc_list)

        show_list = copy.copy(doc_list)

        for i in range(len(show_list)):
            api = doc_list[i]
            info = doc_dict[api]
            show_list[i] = '%s  (%s)' % (api, info['desc'])

        def on_done(index):
            if index == -1: return
            api = doc_list[index]
            info = doc_dict[api]
            url = prefix_url + info['href']
            open_url(url)

        window = sublime.active_window()
        window.show_quick_panel(show_list, on_done)


# ----------------------------------------------------------
# Commands
# ----------------------------------------------------------
class OpenApiDocument(sublime_plugin.WindowCommand):
    def run(self):
        json_path = get_api_json_path()
        prefix_url = get_api_url()
        wmanager = WxappManager()
        wmanager.open_doc(json_path, prefix_url)


class OpenComponentDocument(sublime_plugin.WindowCommand):
    def run(self):
        json_path = get_component_json_path()
        prefix_url = get_component_url()
        wmanager = WxappManager()
        wmanager.open_doc(json_path, prefix_url)
