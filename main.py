# importing libraries required for our process
from flask import Flask, request, jsonify
import similarity
import json
from flask_cors import CORS

# initializing the flask application by passing in Python's special __name__
# for configuring other partd of the application
app = Flask(__name__)
CORS(app)


# We are using the Python decorator to provide the routing to our API
@app.route('/reportAPI', methods=['POST'])
def checkPlagiarism():
    input_json = request.get_json(force=True)
    similaritiesList = similarity.returnMatchingSites(similarity.report(str(input_json['text'])))
    similarityDataJSON = json.dumps(similaritiesList, sort_keys=True)
    return similarityDataJSON


# We are using the Python decorator to provide the routing to our API
@app.route('/checkGrammar', methods=["POST"])
def checkGrammar():
    input_json = request.get_json(force=True)
    dictToReturn = {'text': similarity.getGrammarCorrections(input_json['text'])}
    return jsonify(dictToReturn)


# We are using If command which will run the web server only if we run the file explicitly
if __name__ == '__main__':
    app.run(debug=True)
