var e = (window.location.hash);						// Dom Source
document.write(e);							// Dom Sink
var web_service = "http://data.s3-website-us-east-1.amazonaws.com/"; 	// Web service
var subdomain = "a.b.c.d.e.f.localhost.com";				// Subdomain
var endpoint = "getcodexecution.com/a/?cmd=ls";				// Endpoint detection 1
set(atoz(atob(btoa(atoi(itoa("/a/b/c"))))));				// Endpoint detection 2
set(ztoa(atob(btoa(atoi(itoa("/a/b/c?d=e&f=g"))))));			// Endpoint detection 3
set(ztoz(atob(btoa(atoi(itoa("/a/b/c;d=e&f=g"))))));			// Endpoint detection 4
set(atob("/a/b/c?d[]=e&f[]=g"));					// Endpoint detection 5
var admin = "/secret_admin_dashboard";					// Endpoint detection 6
var administrator = "/secret_admin_dashboard/a/b";			// Endpoint detection 7
hash = "810a5bdaafc6dd30b1d9979215935871";				// Entropy
