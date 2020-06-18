import flask
import pickle
import pandas as pd

# Use pickle to load in the pre-trained model
with open('model/dt-model.pkl', 'rb') as f:
    model = pickle.load(f)

# Initialise the Flask app
app = flask.Flask(__name__, template_folder='templates')

# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('main.html'))
    
    if flask.request.method == 'POST':
        # Extract the input
        Accuracy = flask.request.form['accuracy']
        Bearing = flask.request.form['bearing']
        AccelerometerX = flask.request.form['accX']
        AccelerometerY = flask.request.form['accY']
        AccelerometerZ = flask.request.form['accZ']
        GyroscopeX = flask.request.form['gyroX']
        GyroscopeY = flask.request.form['gyroY']
        GyroscopeZ = flask.request.form['gyroZ']
        
        # Make DataFrame for model
        input_variables = pd.DataFrame([[Accuracy , Bearing, AccelerometerX, AccelerometerY, AccelerometerZ,GyroscopeX, GyroscopeY, GyroscopeZ]],
                                       columns=['Accuracy', 'Bearing', 'AccX', 'AccY', 'AccZ', 'GyroX', 'GyroY', 'GyroZ'],
                                       dtype=float,
                                       index=['input'])

        # Get the model's prediction
        prediction = model.predict(input_variables)[0]
        if prediction < 1:
            prediction='Safe'
        else:
            prediction='Dangerous'
            
        # Render the form again, but add in the prediction and remind user
        # of the values they input before
        return flask.render_template('main.html',
                                     original_input={'Accuracy':Accuracy,
                                                     'Bearing':Bearing,
                                                     'Accelerometer-X':AccelerometerX,
                                                     'Accelerometer-Y':AccelerometerY,
                                                     'Accelerometer-Z':AccelerometerZ,
                                                     'Gyroscope-X':GyroscopeX,
                                                     'Gyroscope-Y':GyroscopeY,
                                                     'Gyroscope-Z':GyroscopeZ},                         
                                     result=prediction,
                                     )

if __name__ == '__main__':
    app.run()