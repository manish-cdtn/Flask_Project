from flask import Flask
from config import Config
from flask_cors import CORS
from routes.animal_volume import animal_volume_measurements_bp
from routes.animal_weight import animal_weight_measurements_bp
 

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(animal_volume_measurements_bp)
app.register_blueprint(animal_weight_measurements_bp)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

