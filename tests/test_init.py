import unittest
from Nemesis import Nemesis
from Nemesis.lib.Functions import reduce_string, dom_source_extract, dom_sink_extract
from Nemesis.lib.Functions import subdomain_extract, url_extract, path_extract, shannon_extract
from Nemesis.lib.Functions import custom_extract, link_extract

class NemesisTest(unittest.TestCase):
    def test_test(self):
        self.assertEqual(Nemesis, Nemesis, "Should be equal")

    def test_reduce_string(self):
        self.assertEqual(reduce_string(""), "", "Should be empty")
        self.assertEqual(reduce_string("'test_string'", ["'"]), "test_string", "Should be equal")
        self.assertEqual(reduce_string('"test_string"', ['"']), "test_string", "Should be equal")
        self.assertEqual(reduce_string('["test_string"]', ['"', '[', ']']), "test_string", "Should be equal")
        self.assertEqual(reduce_string('(test_string)//', ['(', ')']), "test_string", "Should be equal")

    def test_dom_source_extract(self):
        dse = dom_source_extract
        self.assertEqual(dse(''), (), "Should be empty")
        self.assertEqual(dse('var a = 1'), (), "Should be empty")
        self.assertEqual(dse('var has = location.hash'), ('location.hash', 'dom_source_match'), "Should be equal")
        self.assertEqual(dse('console.log(Location.Hash)'), ('Location.Hash', 'dom_source_match'), "Should be equal")

    def test_dom_sink_extract(self):
        dse = dom_sink_extract
        self.assertEqual(dse(''), (), "Should be empty")
        self.assertEqual(dse('randomText'), (), "Should be empty")
        self.assertEqual(dse('setSomething(a, b, c)'), (), "Should be equal")
        self.assertEqual(dse('document.write("Hello World")'), ('document.write', 'dom_sink_match'), "Should be equal")
        self.assertEqual(dse('e.innerHTML = "Hello World")'), ('.innerHTML =', 'dom_sink_match'), "Should be equal")
        self.assertEqual(dse('var x.innerText=`pwn`'), ('.innerText=', 'dom_sink_match'), "Should be equal")

    def test_subdomain_extract(self):
        self.assertEqual(subdomain_extract('', 'nemesis.com'), (), "Should be empty")
        self.assertEqual(subdomain_extract('randomText', 'bit.ly'), (), "Should be empty")
        self.assertEqual(subdomain_extract('test.bit.lee', 'bit.ly'), (), "Should be equal")
        self.assertEqual(subdomain_extract('test.bit.ly', 'bit.ly'), ("test.bit.ly", "subdomain_match"), "Should be equal")
        self.assertEqual(subdomain_extract('a.b.c', 'b.c'), ('a.b.c', 'subdomain_match'), "Should be equal")

    def test_url_extract(self):
        self.assertEqual(url_extract(''), (), "Should be empty")
        self.assertEqual(url_extract('random_path/'), (), "Should be empty")
        self.assertEqual(url_extract('/random_path/'), (), "Should be empty")
        self.assertEqual(url_extract('a/b/c'), (), "Should be empty")
        self.assertEqual(url_extract('/a/b/c'), (), "Should be empty")
        self.assertEqual(url_extract('/a/b/c?d=e&f=g'), (), "Should be empty")
        self.assertEqual(url_extract('https://google.com'), ("https://google.com", "url_match"), "Should be equal")
        self.assertEqual(url_extract('https://google.com/a/b/c'), ("https://google.com/a/b/c", "url_match"), "Should be equal")
        self.assertEqual(url_extract('https://google.com/a/b/c?d=e&f=g'), ("https://google.com/a/b/c?d=e&f=g", "url_match"), "Should be equal")
        self.assertEqual(url_extract('google.com/a/b/c'), ("google.com/a/b/c", "url_match"), "Should be equal")
        self.assertEqual(url_extract('s3.us-west-2.amazonaws.com'), ("s3.us-west-2.amazonaws.com", "url_match"), "Should be equal")
        self.assertEqual(url_extract('https://s3.amazonaws.com/examplebucket'), ("https://s3.amazonaws.com/examplebucket", "url_match"), "Should be equal")

    def test_path_extract(self):
        self.assertEqual(path_extract(''), (), "Should be empty")
        self.assertEqual(path_extract('random_path/'), (), "Should be empty")
        self.assertEqual(path_extract('random_path/random_path'), (), "Should be empty")
        self.assertEqual(path_extract('/random_path'), (), "Should be empty")
        self.assertEqual(path_extract('/a?d=e&f=g'), ("/a?d=e&f=g", "experimental_path_match"), "Should be equal")
        self.assertEqual(path_extract('/random_path/'), ("/random_path/", "experimental_path_match"), "Should be equal")
        self.assertEqual(path_extract('a/b/c'), ("a/b/c", "experimental_path_match"), "Should be equal")
        self.assertEqual(path_extract('/a/b/c'), ("/a/b/c", "experimental_path_match"), "Should be equal")
        self.assertEqual(path_extract('/a/b/c?d=e&f=g'), ("/a/b/c?d=e&f=g", "experimental_path_match"), "Should be equal")

    def test_shannon_extract(self):
        self.assertEqual(shannon_extract(''), (), "Should be empty")
        self.assertEqual(shannon_extract('hi whatsup'), (), "Should be empty")
        self.assertEqual(shannon_extract('e48f39e2b23136a22596efcc0a59f742 whatsup'), ("e48f39e2b23136a22596efcc0a59f742", "shannon_entropy_match"), "Should be equal")

    def custom_extract(self):
        self.assertEqual(custom_extract(''), (), "Should be empty")
        self.assertEqual(custom_extract('sourceMappingURL: {}'), ("sourceMappingURL", "custom_match"), "Should be equal")
        self.assertEqual(custom_extract('secret'), ("secret", "custom_match"), "Should be equal")
        self.assertEqual(custom_extract('adMin'), ("adMin", "custom_match"), "Should be equal")

    def link_extract(self):
        self.assertEqual(link_extract(''), (), "Should be empty")
        self.assertEqual(link_extract('random_path/'), (), "Should be empty")
        self.assertEqual(link_extract('/random_path/'), ("/random_path/", "path_match"), "Should be empty")
        self.assertEqual(link_extract('a/b/c'), ("a/b/c", "path_match"), "Should be empty")
        self.assertEqual(link_extract('/a/b/c'), ("/a/b/c", "path_match"), "Should be empty")
        self.assertEqual(link_extract('/a/b/c?d=e&f=g'), ("/a/b/c?d=e&f=g", "path_match"), "Should be empty")
        self.assertEqual(link_extract('https://google.com'), ("https://google.com", "url_match"), "Should be equal")
        self.assertEqual(link_extract('https://google.com/a/b/c'), ("https://google.com/a/b/c", "url_match"), "Should be equal")
        self.assertEqual(link_extract('https://google.com/a/b/c?d=e&f=g'), ("https://google.com/a/b/c?d=e&f=g", "url_match"), "Should be equal")
        self.assertEqual(link_extract('google.com/a/b/c'), ("google.com/a/b/c", "url_match"), "Should be equal")
        self.assertEqual(link_extract('s3.us-west-2.amazonaws.com'), ("s3.us-west-2.amazonaws.com", "web_service_match"), "Should be equal")
        self.assertEqual(link_extract('https://s3.amazonaws.com/examplebucket'), ("https://s3.amazonaws.com/examplebucket", "web_service_match"), "Should be equal")
        self.assertEqual(link_extract('randomText',  domain = 'bit.ly'), (), "Should be empty")
        self.assertEqual(link_extract('test.bit.ly', domain =  'bit.ly'), (), "Should be empty")
        self.assertEqual(link_extract('test.bit.lee', domain = 'bit.ly'), ('test.bit.lee', 'subdomain_match'), "Should be equal")
        self.assertEqual(link_extract('a.b.c', domain = 'b.c'), ('a.b.c', 'subdomain_match'), "Should be equal")
        self.assertEqual(link_extract('/a', domain = '', already = True), ('/a', 'link_match'))
        self.assertEqual(link_extract('/a/b/c', domain = '', already = True), ('/a/b/c', 'link_match'))
        self.assertEqual(link_extract('/a?b=c', domain = '', already = True), ('/a?b=c', 'link_match'))
