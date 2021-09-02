from urlextract import URLExtract

from Nemesis.lib.Color import Color

# General

# Matches url but not direct path
#url_regex = "((http|https)://)[a-zA-Z0-9\./?:@-_=]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"
#url_regex_without_netloc = "((http|https)://)?[a-zA-Z0-9\./?:@-_=]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"

single_path_regex = """('|"|\(|\))(\/){1}[a-zA-Z0-9-_]+(/)?('|"|\(|\))""" #(hi/) or "hi/"
path_regex = "([a-zA-Z0-9]+\.[a-zA-Z0-9]{3,6})?\/(([0-9a-zA-Z+.-]+)([\/&| ])){1,30}([a-zA-Z0-9]+(\.[a-zA-Z0-9]*)?)?(\?|;)?([a-zA-Z\[\]&=]*)?"
experimental_path_regex = "/?\w+(?:/\w+)*\?\w+=\w+(?:&\w+=\w+)*|(?:\w+(?:/\w+){2,}/?|\w+(?:/\w+)+/|/\w+/)(?:&\w+=\w+)*"
experimental_path_regex = "/?\w+(?:/\w+)*\?\w+=\w+(?:&\w+=\w+)*|(?:\w*(?:/\w+){2,}/?|\w+(?:/\w+)+/|/\w+/)(?:&\w+=\w+)*"
subdomain_regex = lambda subdomain: '(.*\.)?{}(\.)?'.format(subdomain)

dom_sources_regex = [
'document.url',
'document.documenturi',
'Document.URLUnencoded',
'Document.baseURI',
'Location.href',
'Location.search',
'Location.hash',
'Location.pathname',
'Document.cookie',
'Document.referrer',
'Window.name',
'History.pushState',
'History.replaceState',
'LocalStorage',
'SessionStorage',
'window.location',
'document.location'
]

dom_sinks_regex = [
'eval',
'setTimeout',
'setInterval',
'setImmediate',
'execScript',
'cyrpto.generateCRMFRequest',
'ScriptElement',
'(\.src)( )?=()?',
'(\.text)( )?=()?',
'(\.textContent)( )?=()?',
'(\.innerText)( )?=()?',
'(\.innerElement)( )?=()?',
'(\.innerHTML)( )?=()?',
'document.write',
'document.writeln',
]
custom_regex_not = [
        ''
]

custom_regex_insensitive = [
'secret',
'admin',
]

custom_regex_sensitive = [
'sourceMappingURL',
]

web_services_regex = [
'([0-9a-zA-Z-.]*s3[a-zA-Z0-9-.]*\.?amazonaws\.com\/?[a-zA-Z-.]*)',
'([0-9a-zA-Z-.]*?storage\.googleapis\.com\/?[a-zA-Z-.]*)',
'([0-9a-zA-Z-.]*?digitaloceanspaces\.com\/?[a-zA-Z-.]*)',
'([0-9a-zA-Z-.]*?blob\.core\.windows\.net\/?[a-zA-Z-.]*)',
]

hexchar = "1234567890abcdefABCDEF"
base64char = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
Color = Color()
extractor = URLExtract()
