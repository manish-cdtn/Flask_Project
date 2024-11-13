from flask import Flask
from flask_cors import CORS
from routes.animal_volume import animal_volume_measurements_bp
from routes.animal_weight import animal_weight_measurements_bp
import logging, watchtower


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(animal_volume_measurements_bp)
app.register_blueprint(animal_weight_measurements_bp)


# Set up CloudWatch logging
logging.basicConfig(filename='flask_project.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
cloudwatch_handler = watchtower.CloudWatchLogHandler(log_group_name="FlaskProjectLogs")
app.logger.addHandler(cloudwatch_handler)
app.logger.info("Flask project started.")

# Set logging level for werkzeug to WARNING to reduce verbosity
logging.getLogger('werkzeug').setLevel(logging.WARNING)



@app.route("/health")
def index():
    return "I AM WORKING FINE"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

