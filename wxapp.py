import sublime
import sublime_plugin
import os
import copy


# ----------------------------------------------------------
# Config
# ----------------------------------------------------------
def get_st_version():
    return 2 if sys.version_info < (3,) else 3

_join = os.path.join
def get_wxapp_path():
    return _join(sublime.packages_path(), 'wxapp')

def get_doc_path():
    return _join(get_wxapp_path(), 'doc')

def get_api_path():
    return _join(get_doc_path(), 'api')

def get_framework_path():
    return _join(get_doc_path(), 'framework')


# ----------------------------------------------------------
# Controller
# ----------------------------------------------------------
def make_doc_list():
    return os.listdir(get_api_path())

def parse_doc_file(path):
    with open(path, 'r', encoding='utf8') as fp:
        content = fp.readlines()
        url = content[0]
        desc = content[1]
        info = {
            'url': url,
            'desc': desc
        }
        return info

def open_url(url):
    command = ''
    if sublime.platform() == 'osx':
        command = 'open'
    elif sublime.platform() == 'windows':
        command = 'start'
    elif sublime.platform() == 'linux':
        command = 'lynx'
    command += ' ' + str(url)
    os.system(command)

def open_api_url(url):
    prefix = 'https://mp.weixin.qq.com/debug/wxadoc/dev/api/'
    url = prefix + url
    open_url(url)

# ----------------------------------------------------------
# Commands
# ----------------------------------------------------------
class OpenDocumentCommand(sublime_plugin.WindowCommand):
    def run(self):
        doc_list = make_doc_list()
        doc_bak = copy.copy(doc_list)

        for i in range(len(doc_bak)):
            prefix = get_api_path()
            path = _join(prefix, doc_bak[i])
            info = parse_doc_file(path)
            doc_bak[i] = 'wx.%s  (%s)' % (doc_bak[i], info['desc'])

        def on_done(index):
            if index == -1: return
            prefix = get_api_path()
            path = _join(prefix, doc_list[index])
            info = parse_doc_file(path)
            open_api_url(info['url'])

        self.window.show_quick_panel(doc_bak, on_done)
