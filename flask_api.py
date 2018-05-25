import redis
from flask import Flask, jsonify, request

from url_classifier import main_model, dummy_set,malwareinfo

app = Flask(__name__)
redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)

"""
make  training model global
"""
TRAINED_MODEL = dummy_set()




@app.route("/")
def test():
        return "Hello"

@app.route("/GET/URLINFO/1",methods = ["POST"])
def geturlinfo():

        #Get url information

        data = request.json
        if data.get('url'):
                if redis_db.get(data['url']):
                        value = redis_db.get(data['url'])
                else:
                        li = main_model(data['url'])
                        value = TRAINED_MODEL.predict([li])

        if value == "1":
            return jsonify({'ok': True, 'Malware': 'Yes'})
        else:
            return jsonify({'ok': True, 'Malware': 'No'})


if __name__ == "__main__":

        app.run(debug=True, use_reloader=False)
        malwareinfo()
