from requests import get
from jsbeautifier import beautify
from bs4 import BeautifulSoup, Comment

class Engine:
    def __init__(self):
        pass

    def find_href(self, s):
        l =  [t['href'] for t in s.find_all(href = True) if t]
        return l

    def find_img_src(self, s):
        l = [i['src'] for i in s.find_all('image', {'src': True})]
        return l

    def find_comment(self, s) -> set:
        c = set(s.find_all(string=lambda text: isinstance(text, Comment)))
        return c

    def find_hidden_input(self, s):
        p = []
        l = s.find_all('input', {'type': 'hidden', 'name': True})
        for i in l:
            if i.has_attr('value'):
                p.append(i['name'] + ':' + i['value'])
            else:
                p.append(i['name'] + ":"))
        return p

    def find_script_src(self, s):
        l = [st['src'] for st in s.find_all('script', {'src': True })]
        return l

    def find_script_code(self, s):
        e = [beautify(st.string).split('\n') for st in s.find_all('script', {'src': False })]
        return e

    def html_return(self, u):
        data = []
        try:
            data = get(u).text
        except Exception as E:
            print(E, E.__class__)
        return data

    def js_return(self, u):
        data = []
        try:
            data = beautify(get(u).text).split('\n')
        except Exception as E:
            print(E, E.__class__)
        return data
