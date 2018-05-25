# Url_lookup
Detection of phishing website
url_lookup is an HTTP webservice that is scanning traffic looking for malware URL's. Before allowing HTTP connections to be made, this proxy asks a service(main_model) that maintains several databases of malware URL's if the resource being requested is known to contain malware.

The POST requests would look like this:

GET /urlinfo/1/
FLOWCHART:
---------
![alt tag](https://github.com/AnJaLi994/url_lookup/blob/master/Untitled%20Diagram.jpg  "FLOWCHART")
 
1.User initiates request by sending url.

2.Proxy intercepts request, and forwards to Loadbalancer(nginx).

3.Loadbalancer distributes traffic to web-services.

4.Web service looks for URL in malware database(redis-cache)

5.If not found ,Web service predicts it using bayes algorithm.In parallel,malwareinfo() function will be called to update db with phishing urls.

Getting Started:
---------------

  1.Add supervisor.conf file under /etc/supervisor/conf.d and run sudo supervisorctl update
to start services.Supervisor is responsible for starting, managing and re-starting programs using a configuration file.
  
  
  2.Use curl command to test the service .
    curl should be in format of  curl -i -X POST -H "Content-Type: application/json" -d "{\"url\":\"https://slack.com\"}" http://localhost:80/GET/URLINFO/1
  
  
  3. As soon as we send curl command,nginx which is listening on default port,redirects the request to 9000 and 9001 Port,algorithm used is least connection.
  
  
  4.Default redis port on which it is listening is 6379.
  
  5.Simultaneously,malwareinfo() is running in background,it's main function is to update db with new urls in every one hour.The source used is "Phishtank"details here:(https://www.phishtank.com/).
  6. Response will look like :
        i) If Malware Found:
                 {'ok': True, 'Malware': 'Yes'}
        ii)If Malware not Found:
                 {'ok': True, 'Malware': 'No'}
                 
                 
FUTURE SCOPE:
--------------
  1.Sharding can be used to ensure seamless read/write .
  2.Currently the ports 9000 and 9001 is running on the same system,Later on this can be scaled up by Horizontal Scaling ,Adding Multiple systems and Configuring Nginx with required update.

