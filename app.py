import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import os
import sys

print(os.path.dirname(__file__))

root_project_path = os.path.join(os.path.dirname(__file__))
sys.path.insert(0, root_project_path)

hawaii_path = os.path.join(root_project_path, "Resources\hawaii.sqlite")
print(hawaii_path)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///"+hawaii_path)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

print(Base.classes.keys())

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    print("List all available api routes.")
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation' target='_blank'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations' target='_blank'>/api/v1.0/stations</a><br />"
        f"<a href='/api/v1.0/tobs' target='_blank'>/api/v1.0/tobs</a><br />"
        f"<a href='/api/v1.0/&lt;start&gt;' target='_blank'>/api/v1.0/&lt;start&gt;</a><br />"
        f"<a href='/api/v1.0/&lt;end&gt;' target='_blank'>/api/v1.0/&lt;start&gt;/&lt;end&gt;</a>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    print("Return a list of all measurements")
    # Query all passengers
    results = session.query(Measurement.date,Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    precipitations = []    
    for date, prcp in results:
        measurment_dict = {}
        measurment_dict["date"] = date
        measurment_dict["prcp"] = prcp        
        precipitations.append(measurment_dict)        
    return jsonify(precipitations)    


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    print("Return a list of all stations")
    # Query all passengers
    results = session.query(Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = []
    
    for station,name,latitude,longitude,elevation in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)


    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    print("Return a list of measurements from most poppular station USC00519281 from 2016-08-23 on")
    # Query all passengers
    USC00519281_measurements = []
    for d,p in session.query(Measurement.date,Measurement.prcp).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23'):    
        tobs_dict = {}
        tobs_dict["date"] = d        
        tobs_dict["prcp"] = p
        USC00519281_measurements.append(tobs_dict)

    session.close()

 
    return jsonify(USC00519281_measurements)

@app.route("/api/v1.0/<start>/")
def get_measurments_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    print("Return a list of measurments from <start> date on")
    # Query all passengers
    
    measurements = []
    
    for min_tobs, max_tobs,avg_tobs in session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all():    
        print(f'Lowest temperature: {min_tobs} F')
        print(f'Highest temperature: {max_tobs} F')
        print(f'Average temperature: {round(avg_tobs,1)} F')        
        measurement_dict = {}
        measurement_dict["Min Temp"] = min_tobs    
        measurement_dict["Max Temp"] = max_tobs
        measurement_dict["Avg Temp"] = avg_tobs
        measurements.append(measurement_dict)
        
    session.close()

    return jsonify(measurements)

@app.route("/api/v1.0/<start>/<end>")
def get_measurments_startend(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    print("Return a list of measurments from <start> date on")
    # Query all passengers
    
    measurements = []
    
    for min_tobs, max_tobs,avg_tobs in session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all():    
        print(f'Lowest temperature: {min_tobs} F')
        print(f'Highest temperature: {max_tobs} F')
        print(f'Average temperature: {round(avg_tobs,1)} F')        
        measurement_dict = {}
        measurement_dict["Min Temp"] = min_tobs    
        measurement_dict["Max Temp"] = max_tobs
        measurement_dict["Avg Temp"] = avg_tobs
        measurements.append(measurement_dict)
        
    session.close()

    return jsonify(measurements)

if __name__ == '__main__':
    app.run(debug=False)
