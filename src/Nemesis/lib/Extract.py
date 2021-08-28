from termcolor import colored
from traceback import print_exc
from re import search, IGNORECASE
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from Nemesis.lib.Engine import Engine
from Nemesis.lib.Globals import Color
from Nemesis.lib.PathFunctions import urler
from Nemesis.lib.Functions import link_extract
from Nemesis.lib.Functions import dom_source_extract, dom_sink_extract, path_extract
from Nemesis.lib.Functions import subdomain_extract, custom_extract, shannon_extract
from Nemesis.lib.Functions import pretty_print

engine = Engine()
def extract_url(url):
    unparsed_url = urler(url)
    parsed_url = urlparse(unparsed_url)
    domain, path = parsed_url.netloc, parsed_url.path
    is_js_url = path.endswith('.js')
    output_list = []
    if is_js_url:
        js_code = engine.js_source_return(unparsed_url)
    else:
        s = BeautifulSoup(engine.html_source_return(unparsed_url), 'html.parser')
        js_scripts = engine.find_script_code(s)

    for js_code in js_scripts:
        for js_line in js_code:
            line = js_line.strip(' ').rstrip('{').rstrip(' ').lstrip('}').lstrip(' ')
            l = dom_source_extract(line)
            if l:
                output_list.append(l)
                pretty_print(line, l)
                continue
            l = dom_sink_extract(line)
            if l:
                output_list.append(l)
                pretty_print(line, l)
                continue
            l = link_extract(line, domain = domain)
            if l:
                output_list.append(l)
                pretty_print(line, l)
                continue
            #l = path_extract(line)
            #if l:
            #    output_list.append(l)
            #    continue
            #l = subdomain_extract(line)
            #if l:
            #    output_list.append(l)
            #    continue
            l = custom_extract(line)
            if l:
                output_list.append(l)
                pretty_print(line, l)
                continue
            l = shannon_extract(line)
            if l:
                output_list.append(l)
                pretty_print(line, l)
                continue
    if not path or not is_js_url:
        print(url)
        html_dict = {
            'url': unparsed_url,
            'links': engine.find_href(s),
            'img_links': engine.find_img_src(s),
            'script_links': engine.find_script_src(s),
            'comments': engine.find_comment(s),
            'hidden_parameters': engine.find_hidden_input(s),
            }

        if html_dict['links']:
            print(f"{Color.information} General links:")
            for link in html_dict['links']:
                l = link_extract(link)
                pretty_print(link, l)
        if html_dict['img_links']:
            print(f"{Color.information} Image links:")
            for link in html_dict['img_links']:
                l = link_extract(link)
                pretty_print(link, l)
        if html_dict['script_links']:
            print(f"{Color.information} Exline scripts sources:")
            for link in html_dict['script_links']:
                l = link_extract(link)
                pretty_print(link, l)
        if html_dict['comments']:
            print(f"{Color.information} Comments:")
            for comment in html_dict['comments']:
                print(f"{Color.good} Found: {comment}")
        if html_dict['hidden_parameters']:
            print(f"{Color.information} Hidden parameters:")
            h = "&".join([hp.replace(":", "=") for hp in html_dict['hidden_parameters']])
            #h = hidden_parameter.replace(":", "=")
            print(f"{Color.good} Found: {colored(h, color='red', attrs=['bold'])}")
