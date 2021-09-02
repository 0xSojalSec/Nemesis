from termcolor import colored
from re import search, IGNORECASE
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from Nemesis.lib.Engine import Engine
from Nemesis.lib.Globals import Color
from Nemesis.lib.PathFunctions import urler
from Nemesis.lib.Functions import path_extract, subdomain_extract, custom_extract, shannon_extract
from Nemesis.lib.Functions import link_extract, dom_source_extract, dom_sink_extract, pretty_print

class NemesisScan:
    def __init__(self, options):
        self.options = options
        self.engine = Engine()

    def scan_url(self, url):
        print(f"{Color.other} Scanning {url} ...")
        unparsed_url = urler(url)
        parsed_url = urlparse(unparsed_url)
        domain, path = parsed_url.netloc, parsed_url.path
        is_javascript = path.endswith('.js')
        output_list = []
        if is_javascript:
            js_code = self.engine.js_source_return(unparsed_url)
            output_list.extend(self.extract_from_javascript(js_code))

        s = BeautifulSoup(self.engine.html_source_return(unparsed_url), 'html.parser')
        js_code = "\n".join(self.engine.find_script_code(s))
        output_list.extend(self.extract_from_javascript(js_code))
        html_dict = {
            'url': unparsed_url,
            'links': self.engine.find_href(s),
            'img_links': self.engine.find_img_src(s),
            'script_links': self.engine.find_script_src(s),
            'comments': self.engine.find_comment(s),
            'hidden_parameters': self.engine.find_hidden_input(s),
        }
        output_list.extend(self.extract_from_html(html_dict))
        return output_list

    def extract_from_javascript(self, js_code):
        results = []
        for line in js_code.split('\n'):
            js_line = line.strip(' ')
            match = dom_source_extract(js_line)
            if match:
                results.append((match, js_line))
                continue
            match = dom_sink_extract(js_line)
            if match:
                results.append((match, js_line))
                continue
            match = link_extract(js_line, domain = self.options['domain'])
            if match:
                results.append((match, js_line))
                continue
            match = custom_extract(js_line)
            if match:
                results.append((match, js_line))
                continue
            match = () if self.options['enable_entropy'] else shannon_extract(js_line)
            if match:
                results.append((match, js_line))
        #l = path_extract(line) ... subdomain_extract(line) ...
        output_list = []
        print(f"{Color.information} Javascript Extraction:")
        for match, js_line in results:
            output_list.append(match)
            pretty_print(js_line, *match)
        return output_list

    def extract_from_html(self, html_dict):
        results = []
        if html_dict['links']:
            print(f"{Color.information} General links:")
            for link in html_dict['links']:
                match = link_extract(link)
                if match:
                    results.append((match, link))
        if html_dict['img_links']:
            print(f"{Color.information} Image links:")
            for link in html_dict['img_links']:
                match = link_extract(link)
                if match:
                    results.append((match, link))
        if html_dict['script_links']:
            print(f"{Color.information} Exline scripts sources:")
            for link in html_dict['script_links']:
                match = link_extract(link)
                if match:
                    results.append((match, link))
        if html_dict['comments']:
            print(f"{Color.information} Comments:")
            for comment in html_dict['comments']:
                results.append(((comment,"Comment"), comment))
        if html_dict['hidden_parameters']:
            print(f"{Color.information} Hidden parameters:")
            h = "&".join([hp.replace(":", "=") for hp in html_dict['hidden_parameters']])
            results.append(((h,"Hidden parameter"), h))
        output_list = []
        for match, link in results:
            output_list.append(match)
            pretty_print(link, *match)
        return output_list
