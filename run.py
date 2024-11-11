from flask import Flask
from flask_cors import CORS
from routes.animal_volume import animal_volume_measurements_bp
from routes.animal_weight import animal_weight_measurements_bp
 

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(animal_volume_measurements_bp)
app.register_blueprint(animal_weight_measurements_bp)


@app.route("/health")
def index():
    return "I AM WORKING FINE"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

