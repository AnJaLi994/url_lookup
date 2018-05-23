# url_lookup
Detection of phishing website
url_lookup is an HTTP webservice that is scanning traffic looking for malware URL's. Before allowing HTTP connections to be made, this proxy asks a service(main_model) that maintains several databases of malware URL's if the resource being requested is known to contain malware.

The GET requests would look like this:

  GET /urlinfo/1/{url}/
FLOWCHART:

 
User initiates request by sending url
Proxy intercepts request, and forwards to Loadbalancer(nginx)
loadbalancer distributes traffic to web-services
Web service looks for URL in malware database(redis-cache)
if not found ,Web service predicts it using bayes algorithm.
Web service provides response to proxy
in parallel,Also stores into db if it is a malware.
Based on response, proxy can pass or block website
