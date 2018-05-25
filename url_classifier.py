import pandas as pd
import redis
redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import urlparse
import urllib2
import urllib
import urlparse
import requests
import ssl, socket
import csv
import datetime
import whois
from bs4 import BeautifulSoup
import warnings
import timeit
import base64
import json
import re
from xml.dom import minidom
'''fExtractor's function is to return 1,0,-1 based on number of factors which is important to determine whether a
website has malware or not
'''
class fExtractor(object):
    def __init__(self, url):
        self.url = url
        self.content = None
        self.tokens_words=re.split('\W+',self.url)
        self.hostname = urlparse.urlparse(self.url).hostname
        try:
            self.response = requests.get(self.url, verify=True)
            data = self.response.text
            self.content = BeautifulSoup(data)
            self.scripts = self.content.find_all('script')
        except requests.exceptions.SSLError:
            self.response = requests.get(self.url, verify=False)
            data = self.response.text
            self.content = BeautifulSoup(data)
            self.scripts = self.content.find_all('script')
        except:
            self.response = ""
            self.content = BeautifulSoup("")
            self.scripts=[]
            pass
        try:
            self.whois = whois.whois(self.url)
            self.dns=True
        except:
            self.dns=False
            pass
    def isAbnormalUrl(self):
        '''
        determines whether website has some dns value or not
        '''

        if self.dns:
            return 1
        return -1


    def hasManyRedirects(self):
        '''
        determines whether website is redirecting to other urls
        '''

        r = self.response
        try:
            if len(r.history)<= 1:
                return -1
        except Exception as e:
            return -1
        return 1

    def isStandardPort(self):
        '''
        determines whether port is in whitelist list
        '''

        whitelist =[21,22,23,80,443,445,1433,1521,3306,3389]
        try:
            uparse = urlparse.urlparse(self.url)
            if uparse.port not in whitelist:
                return 1
            return -1
        except:
            return 0

    def hasHttpsToken(self):
        '''
        determines whether domain has http in it
        '''

        hostname = urlparse.urlparse(self.url).hostname
        if 'http' in hostname:
            return 1
        return -1

    def has_IPAdress(self):
        '''
        determines whether  tokenwords has any numeric value

        '''


        cnt=0
        for ele in self.tokens_words:
            if unicode(ele).isnumeric():
                cnt+=1

        if cnt>0:
            return -1
        return 0
    def isRedirectingUrl(self):
        '''
        determines whether url has more than one" //"
        '''

        if self.url.count('//')>1:
            return 1
        return -1
    def isLongUrl(self):
        '''
        determines whether website's length is too long
        '''

        length = len(self.url)
        if length<54:
            return -1
        elif length>=54 and length<=75:
            return 0
        else:
            return 1
    def isTinyUrl(self):
        '''
        determines whether websit's length is too small
        '''


        try:
            shHostName = urlparse.urlparse(self.url).hostname
            res = urllib2.urlopen(self.url)
            otHostName = urlparse.urlparse(res.geturl()).hostname
            self.hostname = otHostName
            if len(shHostName)<len(otHostName):
                shHostName = re.split('\W+',shHostName)
                otHostName = re.split('\W+',otHostName)
                intersect = list(set(shHostName).intersection(otHostName))
                if len(intersect) is 0:
                    return 1
            return -1
        except:
            return 0
    def domainExpiry(self):
        '''
        determines whether website is experied for more than a year
        '''

        try:
            lookup = self.whois
            expDate = lookup.expiration_date
            now = datetime.datetime.now()
            diff = expDate - now
            if diff.days>=365:
                return -1
            return 1
        except:
            return 0
    def isSFHSuspicious(self):
        '''
        determines whether about of website has nothing
        '''

        scripts = self.scripts

        res = -1
        for script in scripts:
            if 'window.open(""' in script:
                res = 1
                break
        return res


    def extract(self,argument):
        '''
        Creates list of all values
        '''

        result =[self.has_IPAdress(), self.isLongUrl(), self.isTinyUrl(),\
        self.isRedirectingUrl(), self.domainExpiry(),\
         self.isStandardPort(), self.hasHttpsToken(), \
        self.isSFHSuspicious(), \
        self.isAbnormalUrl(), self.hasManyRedirects(),argument]

        return result


    def inputtomodel(self):
        '''
        Creates list to be used by model
        '''

        im =[self.has_IPAdress(), self.isLongUrl(), self.isTinyUrl(),\
        self.isRedirectingUrl(), self.domainExpiry(),\
         self.isStandardPort(), self.hasHttpsToken(), \
        self.isSFHSuspicious(), \
        self.isAbnormalUrl(), self.hasManyRedirects()]
        return im


def dummy_set():
        '''
        Using bayes algorithm,a model isbeing made to predict values of label after pushing some predefined data set
        '''


        result = []

        data_url = pd.read_csv("dataset.csv")
        data_url.head()
        featureSet = pd.DataFrame(columns=('ipadress','longurl','tinyurl','redirectingurl',\
        'domainexpiry','standardport','httpstoken','sfhsuspicious','abnormalurl','manyredirects',\
        'Label'))

        for ind in range(1,len(data_url)):
                print 'feature extractor done {} {} {}'.format(ind, data_url["URL"].loc[ind], data_url["Label"].loc[ind])
                featureSet.loc[ind]= fExtractor(data_url["URL"].loc[ind]).extract(data_url["Label"].loc[ind])
                redis_db.set(data_url["URL"].loc[ind],data_url["Label"].loc[ind])


        LE = LabelEncoder()

        featureSet['ipadress'] = LE.fit_transform(featureSet['ipadress'])
        featureSet['longurl'] = LE.fit_transform(featureSet['longurl'])
        featureSet['tinyurl'] = LE.fit_transform(featureSet['tinyurl'])
        featureSet['redirectingurl'] = LE.fit_transform(featureSet['redirectingurl'])
        featureSet['domainexpiry'] = LE.fit_transform(featureSet['domainexpiry'])
        featureSet['standardport'] = LE.fit_transform(featureSet['standardport'])
        featureSet['httpstoken'] = LE.fit_transform(featureSet['httpstoken'])
        featureSet['sfhsuspicious'] = LE.fit_transform(featureSet['sfhsuspicious'])
        featureSet['abnormalurl'] = LE.fit_transform(featureSet['abnormalurl'])
        featureSet['manyredirects'] = LE.fit_transform(featureSet['manyredirects'])
        featureSet['Label'] = LE.fit_transform(featureSet['Label'])
        features = ['ipadress','longurl','tinyurl','redirectingurl','domainexpiry','standardport','httpstoken','sfhsuspicious','abnormalurl','manyredirects']
        target = ['Label']

        features_train, features_test, target_train, target_test = train_test_split(featureSet[features],featureSet[target],
        test_size = 0.33,
        random_state = 54)

        model = GaussianNB()
        model.fit(features_train, target_train)
        pred = model.predict(features_test)
        accuracy = accuracy_score(target_test, pred)
        print "accuracy {} " .format(accuracy)
        return model

def main_model(new_url):


        res = fExtractor(new_url).inputtomodel()
        return res

import time
import csv
def malwareinfo():

	url = 'http://data.phishtank.com/data/online-valid.csv'
	response = urllib2.urlopen(url)
	cr = csv.reader(response)
	while True:
    		c= 0
    		last_scan = redis_db.get("last_scan_time")
    		last_scan_updated = None
    		for row in cr:
        		if c == 0:
            			last_scan_updated = row[4]
            			redis_db.set("last_scan_time", last_scan_updated)
            			c += 1
        		redis_db.set(row[1], "1")
        		if last_scan == row[4]:
            			break
    		time.sleep(3600)
















