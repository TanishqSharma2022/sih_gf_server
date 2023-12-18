from flask import Flask, request, jsonify

from search import get_recommendations
from flask_cors import CORS
app = Flask(__name__)

CORS(app)
@app.route('/api/job_recommend', methods=['POST'])
def job_recommend():
    try:
        data = request.json
        print(data)
        search_words = data.get('search_words')
        if search_words:
            recommendations = get_recommendations(search_words)
            return jsonify(recommendations)
        else:
            return jsonify({'error': 'Search words not provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# print(get_recommendations('technology'))

if __name__ == '__main__':
    app.run(debug=True)