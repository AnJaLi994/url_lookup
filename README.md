# Url_lookup
Detection of phishing website
url_lookup is an HTTP webservice that is scanning traffic looking for malware URL's. Before allowing HTTP connections to be made, this proxy asks a service(main_model) that maintains several databases of malware URL's if the resource being requested is known to contain malware.

The GET requests would look like this:

  GET /urlinfo/1/{url}/
FLOWCHART:
![alt tag](https://github.com/AnJaLi994/url_lookup/blob/master/Untitled%20Diagram.jpg  "FLOWCHART")
 
1.User initiates request by sending url

2.Proxy intercepts request, and forwards to Loadbalancer(nginx)

3.Loadbalancer distributes traffic to web-services

4.Web service looks for URL in malware database(redis-cache)

5. If not found ,Web service predicts it using bayes algorithm.

6. In parallel,malwareinfo() function will be called to update db with phishing urls
in regular interval.
--------------------------------------------------------------------------------------------------------------------------------------
Getting Started:
  1.Use python flask_api.py to start the service:
  2.Use curl command to test the service 
    curl should be in format of  curl -i -X POST -H "Content-Type: application/json" -d "{\"url\":\"https://slack.com\"}"http://localhost:80/GET/URLINFO/1
  
  3. Superviser is responsible for starting, managing and re-starting programs using a configuration file.
  4. As soon as we send curl command,nginx which is listening on default port,redirects the request to 9000 and 9001,algorithm used is least connection.
  5.Default redis port on which it is listening is 6379
  5.Simultaneously,randominfo() is running in background,it's main function is to update db with new urls in every one hour.The source used is "Phishtank"details here:(https://www.phishtank.com/)
FUTURE SCOPE:
  Sharding can be used to ensure seamless read/write .

