from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/analise_seca-MS', methods=['GET'])
def test_route():
    return jsonify({"message": "Rota funcionando!"})

if __name__ == '__main__':
    app.run(debug=True, port=5001) 