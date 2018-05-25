# url_lookup
Detection of phishing website
url_lookup is an HTTP webservice that is scanning traffic looking for malware URL's. Before allowing HTTP connections to be made, this proxy asks a service(main_model) that maintains several databases of malware URL's if the resource being requested is known to contain malware.

The GET requests would look like this:

  GET /urlinfo/1/{url}/
FLOWCHART:
![alt tag](https://github.com/AnJaLi994/url_lookup/blob/master/Untitled%20Diagram.jpg  "FLOWCHART")
 
1.User initiates request by sending url
2.Proxy intercepts request, and forwards to Loadbalancer(nginx)
3.loadbalancer distributes traffic to web-services
4.Web service looks for URL in malware database(redis-cache)
5. if not found ,Web service predicts it using bayes algorithm.
6. Web service provides response to proxy
in parallel,Also stores into db if it is a malware.
7.Based on response, proxy can pass or block website
