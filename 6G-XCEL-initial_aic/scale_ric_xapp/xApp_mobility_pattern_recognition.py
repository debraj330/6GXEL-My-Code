import numpy as np
from numpy import ndarray

from xapp_interface.decorators.xApp import xApp
from xapp_interface.Xapp import Xapp
from xapp_interface.XappController import XappController
from xapp_interface.enums import *
from utils.fifo_queue import FifoQueue
from tensorflow import keras
import os

from flask import Flask, jsonify, request # TODO - install in the xApp container

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the root directory by navigating up the directory tree
root_path = os.path.abspath(os.path.join(current_dir, './MobilityPatternModels'))

sequence_length = 6
features = [MeasurementsHandler.PHY_UL_PUCCH_RSSI.value,
            MeasurementsHandler.PHY_UL_PUCCH_SINR.value,
            MeasurementsHandler.PHY_UL_PUSCH_RSSI.value,
            MeasurementsHandler.PHY_UL_PUSCH_SINR.value,
            MeasurementsHandler.PHY_UL_PUCCH_NI.value,
            MeasurementsHandler.MAC_DL_CQI.value,
            MeasurementsHandler.MAC_DL_CQI_OFFSET.value,
            MeasurementsHandler.MAC_DL_MCS.value,
            MeasurementsHandler.PHY_UL_MCS.value,
            MeasurementsHandler.PHY_DL_MCS.value]
measures_pool = []
predictions_queue = FifoQueue()
# Load the model from the file
model: keras.Sequential = keras.models.load_model(os.path.abspath(os.path.join(root_path, 'rnn_1_16.h5')))
# Define class labels
labeled_classed = ['bus', 'car', 'pedestrian', 'static', 'train']

app = Flask(__name__)

@xApp(name="MobilityPatternPredictor")
class MobilityPatternPredictor(Xapp):
    time_interval = 1 # set the same time cadence of the dataset (tenth of second) # TODO - not working under the second
    read_measurements = [MeasurementsHandler.ALL_MEASUREMENTS]
    send_commands = []
    cell_ids = [0]

    @classmethod
    def process(cls, measurements):
        if len(measurements) != 0:
                measures_pool.append(cls.filter_measures(measurements))
                print('Measure ', len(measures_pool), ' received')

        if len(measures_pool) >= sequence_length:
            # If measures are continuous over time
            if cls.check_continuity(measures_pool): # TODO - is timestamp info present ???

                print("series obtained")
                # Remove unnecessary data (e.g. timestamp) and adjust series shape
                series = cls.shape_and_clean_series(measures_pool)

                print("predicting class")
                # Model prediction
                predicted_class = cls.predict(series) # TODO - return int or str ???

                print("elaborating stats")
                # Retrieve average stats of the series
                cqi, rssi, sinr, ni = cls.retrieve_stats(measures_pool) # TODO - decide fourth metric to use

                # Append prediction and related stats to the queue
                cls.store_prediction(predicted_class=predicted_class, cqi=cqi, rssi=rssi, sinr=sinr, ni=ni)

                print("prediction and stats added to the queue")

            # Remove old measures from pool
            measures_pool.clear()
            print(predictions_queue)

    @classmethod
    def filter_measures(cls, measurements) -> dict:
        selected_metrics = {metric: measurements[0][metric] for metric in features}
        return selected_metrics

    @classmethod
    def check_continuity(cls, measures:[]):
        # TODO
        return True

    @classmethod
    def shape_and_clean_series(cls, measures:[])-> ndarray:
        # Get the keys from the first dictionary in the list
        keys = measures[0].keys()

        # Create an empty ndarray with the desired shape
        arr = np.empty((len(measures), len(keys)))

        # Iterate over the list of dictionaries and populate the ndarray
        for i, d in enumerate(measures):
            arr[i] = [d[key] for key in keys]

        # Expand dimensions of the array, desired shape is (1, sequence length, n features)
        expanded_arr = np.expand_dims(arr, axis=0)

        return expanded_arr

    @classmethod
    def predict(cls, series:ndarray):
        # Use the loaded model to make predictions
        prediction = model.predict(series)

        # Retrieve the predicted class
        predicted_class = np.argmax(prediction, axis=1)

        # Return the predicted class label
        return labeled_classed[predicted_class[0]]

    @classmethod
    def retrieve_stats(cls, measures: [dict]):
        cqi_values = []
        rssi_values = []
        sinr_values = []
        ni_values = []

        for measure in measures:
            if MeasurementsHandler.MAC_DL_CQI in measure:
                cqi_values.append(measure[MeasurementsHandler.MAC_DL_CQI])
            if MeasurementsHandler.PHY_UL_PUCCH_RSSI in measure:
                rssi_values.append(measure[MeasurementsHandler.PHY_UL_PUCCH_RSSI])
            if MeasurementsHandler.PHY_UL_PUCCH_SINR in measure:
                sinr_values.append(measure[MeasurementsHandler.PHY_UL_PUCCH_SINR])
            if MeasurementsHandler.PHY_UL_PUCCH_NI in measure:
                ni_values.append(measure[MeasurementsHandler.PHY_UL_PUCCH_NI])

        cqi_mean = sum(cqi_values) / len(cqi_values) if cqi_values else None
        rssi_mean = sum(rssi_values) / len(rssi_values) if rssi_values else None
        sinr_mean = sum(sinr_values) / len(sinr_values) if sinr_values else None
        ni_mean = sum(ni_values) / len(ni_values) if ni_values else None

        return cqi_mean, rssi_mean, sinr_mean, ni_mean

    @classmethod
    def store_prediction(cls, predicted_class:str, cqi:int, rssi:float, sinr:float, ni:float):
        prediction = {'class': predicted_class,
                      'cqi': cqi,
                      'rssi': rssi,
                      'sinr': sinr,
                      'ni': ni}
        predictions_queue.enqueue(prediction)


XappController().run()

# To call the method -> http://localhost:5000/api/get_prediction
@app.route('/api/get_prediction', methods=['GET'])
def get_data():
    return jsonify(predictions_queue.dequeue())

@app.route('/api/set_configuration', methods=['POST'])
def add_data():
    config = request.get_json()
    #change_configuration(config=config)
    return jsonify({'message': ''.join(['Configuration changed to ', str(config), ' successfully'])})

def change_configuration(config):
    # TODO
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)
