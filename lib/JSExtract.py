from termcolor import colored
from traceback import print_exc
from re import search, IGNORECASE
from urllib.parse import urlparse

from lib.Engine import Engine
from lib.PathFunctions import urler, unurler, unender
from lib.Functions import manage_output, shannon_entropy
from lib.Globals import base64char, hexchar, dom_sources_regex, dom_sinks_regex
from lib.Globals import web_services_regex, custom_sensitive, custom_insensitive, Color
from lib.Globals import url_regex, subdomain_regex, path_regex, single_path_regex, library_regex

JSE = Engine()

class JSExtract:
    def __init__(self, argv):
        self.jstext_continuer = 0
        self.argv = argv

    def extract_from_url(self, url: str) -> bool:
        try:
            output_list = []
            jsurl = urler(url)
            parsed_url = urlparse(jsurl)
            print(f"{Color.information} Getting data from {colored(jsurl, color='yellow', attrs=['bold'])}")
            output_list.append((f"URL: {colored(jsurl, color='yellow', attrs=['bold'])}\n\n"))
            (lambda __after: [__after() for self.argv.domain in [(parsed_url.netloc)]][0] if parsed_url.netloc and not self.argv.domain else __after())(lambda: None)
            if parsed_url.path.endswith('.js'):
                jstext = JSE.returnjs_fromjs(jsurl)
                jscomments, js_exlines, js_hidden, js_links, js_imgsrc = (None, None, None, None, None)
            elif not parsed_url.path.endswith('.js'):
                jstext, js_other = JSE.returnjs_fromhtml(jsurl)
                jscomments, js_exlines, js_hidden, js_links, js_imgsrc = js_other
            if js_links or js_imgsrc:
                for js_link in js_links:
                    output_list.append(self.link_extract(js_link))
                for js_src in js_imgsrc:
                    output_list.append(self.link_extract(js_src, is_src=True))
            if jscomments:
                for jscomment in jscomments:
                    jscomment = '"{}"'.format(jscomment.strip(' '))
                    print(f"{Color.good} Comments: {colored(jscomment, color='red', attrs=['bold'])}")
                    output_list.append([manage_output(f"{jscomment} <--- Comments\n"), 'Comments'])
            if js_exlines:
                for exline in js_exlines:
                    output_list.append(self.exline_extract(exline['src']))
            if js_hidden:
                print(f"{Color.good} Hidden input parameters: {colored(js_hidden, color='red', attrs=['bold'])}")
                output_list.append([manage_output(f"{js_hidden} <--- Hidden parameters\n"), 'Hidden'])
            for line in jstext:
                line = line.strip(' ').rstrip('{').rstrip(' ').lstrip('}').lstrip(' ')
                output_list.append(self.domsource_extract(line))
                if self.jstext_continuer: self.jstext_continuer = 0; continue
                output_list.append(self.domsink_extract(line))
                if self.jstext_continuer: self.jstext_continuer = 0; continue
                output_list.append(self.url_extract(line)) 
                if self.jstext_continuer: self.jstext_continuer = 0; continue
                output_list.append(self.path_extract(line))
                if self.jstext_continuer: self.jstext_continuer = 0; continue
                output_list.append(self.subdomain_extract(line))
                if self.jstext_continuer: self.jstext_continuer = 0; continue
                output_list.append(self.custom_extract(line))
                if self.jstext_continuer: self.jstext_continuer = 0; continue
                output_list.append(self.shannon_extract(line))
                if self.jstext_continuer: self.jstext_continuer = 0; continue
            return tuple(filter(None, output_list))
        except Exception:
            print_exc()

    def exline_extract(self, line: str) -> list:
        output_list = []
        #anydigit = lambda x: any(map(str.isdigit, x)) # to be developed later and also, self.jstext_continuer is intentionally removed
        #if self.jstext_continuer: self.jstext_continuer = 0; continue, and self.jstext_continuer = 1 in this function
        for library in library_regex:
            if search(library, line, IGNORECASE):
                print(f"{Color.good} Found {library}: {colored(line, color='red', attrs=['bold'])}")
            else:
                print(f"{Color.good} External script tags: {colored(line, color='red', attrs=['bold'])}")
            output_list = [manage_output(f"{line.rstrip(' ')} <--- External\n"), 'Exline']
            return output_list
        return []

    def domsource_extract(self, line: str) -> list:
        output_list = []
        for dom_source in dom_sources_regex:
            if search(dom_source, line, IGNORECASE):
                print(f"{Color.good} Found Dom XSS Source: {colored(line.strip(' '), color='red', attrs=['bold'])}")
                output_list = [manage_output(f"{line.strip(' ')} <--- DomXSS Source\n"), 'Source']
                self.jstext_continuer = 1
                return output_list
        return []

    def domsink_extract(self, line: str):
        output_list = []
        for dom_source in dom_sinks_regex:
            if search(dom_source, line, IGNORECASE):
                print(f"{Color.good} Found Dom XSS Source: {colored(line.strip(' '), color='red', attrs=['bold'])}")
                output_list = [manage_output(f"{line.strip(' ')} <--- DomXSS Source\n"), 'Sink']
                self.jstext_continuer = 1
                return output_list
        return []

    def subdomain_extract(self, line: str) -> list:
        output_list = []
        if not self.argv.domain:
            return output_list
        subdomain = subdomain_regex(self.argv.domain)
        if search(subdomain, line, IGNORECASE):
            sub = search(subdomain, line, IGNORECASE).group()
            if sub == self.argv.domain:
                return []
            print(f"{Color.good} Found subdomain: {colored(sub, color='red', attrs=['bold'])}")
            output_list = [manage_output(f"{sub} <--- Subdomain\n"), 'Subdomain']
            self.jstext_continuer = 1
            return output_list
        return []
    
    def url_extract(self, line: str) -> list:
        output_list = []
        for web_service in web_services_regex:
            if search(web_service, line):
                line = search(url_regex, line).group()
                print(f"{Color.good} Found web service/storage: {colored(line.strip(' '), color='red', attrs=['bold'])}")
                output_list = [manage_output(f"{line.strip(' ')} <--- Web service\n"), 'Webservice']
                self.jstext_continuer = 1
                return output_list
        if search(url_regex, line):
            line = search(url_regex, line).group()
            if unender(unurler(line), '/') == self.argv.domain:
                return []
            print(f"{Color.good} Found endpoint: {colored(line.strip(' '), color='red', attrs=['bold'])}")
            output_list = [manage_output(f"{line.strip(' ')} <--- Endpoint\n"), "Url"]
            self.jstext_continuer = 1
            return output_list
        return []

    def link_extract(self, line: str, is_src = False) -> list:
        output_list = []
        for web_service in web_services_regex:
            if search(web_service, line):
                line = search(url_regex, line).group()
                print(f"{Color.good} Found web service/storage: {colored(line.strip(' '), color='red', attrs=['bold'])}")
                output_list = [manage_output(f"{line.strip(' ')} <--- Web service\n"), 'Webservice']
                return output_list
        if not line or line.startswith('#'):
            return output_list
        elif search(url_regex, line):
            line = search(url_regex, line).group()
        elif search(path_regex, line):
            line = search(path_regex, line).group()
        elif search(single_path_regex, line):
            line = search(single_path_regex, line).group()
        else:
            return output_list
        if line:
            if not is_src:
                print(f"{Color.good} Found external links/hrefs: {colored(line.strip(' '), color='red', attrs=['bold'])}")
            else:
                print(f"{Color.good} Found image source: {colored(line.strip(' '), color='red', attrs=['bold'])}")
            output_list = [manage_output(f"{line.strip(' ')} <--- External hrefs\n"), "Link"]
        return output_list

    def path_extract(self, line: str) -> list:
        output_list = []
        if search(path_regex, line):
            line = search(path_regex, line).group()
            print(f"{Color.good} Found endpoint: {colored(line.strip(' '), color='red', attrs=['bold'])}")
            output_list = [manage_output(f"{line.strip(' ')} <--- Endpoint\n"), "Endpoint"]
            self.jstext_continuer = 1
        elif search(single_path_regex, line):
            line = self.reduce_string(search(single_path_regex, line).group(), args=['"', "'"])
            print(f"{Color.good} Found endpoint: {colored(line.strip(' '), color='red', attrs=['bold'])}")
            output_list = [manage_output(f"{line.strip(' ')} <--- Endpoint\n"), "Endpoint"]
            self.jstext_continuer = 1
            return output_list
        return []

    def shannon_extract(self, line: str) -> list:
        output_list = []
        if self.argv.enable_entropy:
            for word in line.split(' '):
                if len(word) > 5:
                    if float(shannon_entropy(word, base64char)) > float(3.43) or float(shannon_entropy(word, hexchar)) > float(3.5):
                        word = self.reduce_string(word.rstrip(';'), args=['"', "'"])
                        print(f"{Color.good} Suspicious data: {colored(word, color='red', attrs=['bold'])}")
                        output_list = [manage_output(f"{word} <--- Entropy \n"), "Entropy"]
                        self.jstext_continuer = 1
                        return output_list
        return []
    
    def custom_extract(self, line: str) -> list:
        output_list = []
        for custom in custom_sensitive:
            if search(custom, line):
                print(f"{Color.good} Custom regex match: {colored(line, color='red', attrs=['bold'])}")
                output_list = [manage_output(f"{line} <--- Custom regex \n"), "Custom"]
                self.jstext_continuer = 1
                return output_list
        for custom in custom_insensitive:
            if search(custom, line, IGNORECASE):
                print(f"{Color.good} Custom regex match: {colored(line, color='red', attrs=['bold'])}")
                output_list = [manage_output(f"{line} <--- Custom regex \n"), "Custom"]
                self.jstext_continuer = 1
                return output_list
        return []
    
    def reduce_string(self, line: str, args: list) -> str:
        if not line:
            return ""
        line = line.rstrip('//').rstrip(';')
        for arg in args:
            if arg in line and line[0] == arg and line[-1] == arg:
                return line[1:-1]
            elif arg == "(" or arg == ")":
                if line[0] == "(" and line[-1] == ")":
                    return line[1:-1]
        return line

