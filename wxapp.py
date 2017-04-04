import sublime
import sublime_plugin
import os
import copy
import json


# ----------------------------------------------------------
# Config
# ----------------------------------------------------------
def get_api_url():
    return 'https://mp.weixin.qq.com/debug/wxadoc/dev/api/'


def get_api_json_path():
    return "/".join(["Packages", "wxapp", "wxapp_api.json"])


# ----------------------------------------------------------
# Controller
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


def open_api_url(url):
    prefix = get_api_url()
    url = prefix + url
    open_url(url)


# ----------------------------------------------------------
# Commands
# ----------------------------------------------------------
class OpenApiDocument(sublime_plugin.WindowCommand):
    def run(self):
        api_dict = json.loads(sublime.load_resource(get_api_json_path()))
        api_list = list(api_dict.keys())
        api_list = sorted(api_list)
        show_list = copy.copy(api_list)

        for i in range(len(show_list)):
            api = api_list[i]
            info = api_dict[api]
            show_list[i] = '%s  (%s)' % (api, info['desc'])

        def on_done(index):
            if index == -1: return

            api = api_list[index]
            info = api_dict[api]
            open_api_url(info['href'])

        self.window.show_quick_panel(show_list, on_done)
