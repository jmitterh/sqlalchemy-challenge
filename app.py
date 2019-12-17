# Docs on session basics
# https://docs.sqlalchemy.org/en/13/orm/session_basics.html

import numpy as np
import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

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
    '''
    List all available api routes.
    '''
    return render_template ("index.html")


@app.route("/api/v1.0/precipitation")
def precipitation():
    '''
    Convert the query results to a Dictionary using date as the key and prcp as the value.
    Return the JSON representation of your dictionary.
    '''
    # Query all date and prcp for table Measurment
    session = Session(engine)
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date)

    # close the session to end the communication with the database
    session.close()

    list = []
    for data in results:
        dict = {}
        dict["date"] = data.date
        dict["prcp"] = data.prcp
        list.append(dict)

    return jsonify(list)


@app.route("/api/v1.0/stations")
def stations():
    '''
    Return a JSON list of stations from the dataset.
   '''
    # Query all Stations table
    session = Session(engine)
    results = session.query(Station).all()

    # close the session to end the communication with the database
    session.close()

    # Convert list of tuples into normal list
    list = []
    for data in results:
        dict = {}
        dict["elevation"] = data.elevation
        dict["longitude"] = data.longitude
        dict["latitude"] = data.latitude
        dict["name"] = data.name
        dict["station"] = data.station
        list.append(dict)

    return jsonify(list)


@app.route("/api/v1.0/tobs")
def tobs():
    '''
    query for the dates and temperature observations from a year from the last data point.
    Return a JSON list of Temperature Observations (tobs) for the previous year.
    '''
    # Query all Measurement table
    session = Session(engine)
    results = session.query(Measurement.station,Measurement.date,Measurement.tobs).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date)

    # close the session to end the communication with the database
    session.close()

    list = []
    for data in results:
        dict = {}
        dict["station"] = data.station
        dict["date"] = data.date
        dict["tobs"] = data.tobs
        list.append(dict)

    return jsonify(list)
 

@app.route("/api/v1.0/<start>")
def start(start):
    '''
    Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    '''
    # Query all Stations table
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    # close the session to end the communication with the database
    session.close()

    list = []
    for data in results:
        dict = {}
        dict["min"] = data[0]
        dict["avg"] = data[1]
        dict["max"] = data[2]
        list.append(dict)
        
    return jsonify(list)


@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    '''
    Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    '''
    # Query all Stations table
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # close the session to end the communication with the database
    session.close()

    list = []
    for data in results:
        dict = {}
        dict["min"] = data[0]
        dict["avg"] = data[1]
        dict["max"] = data[2]
        list.append(dict)
        
    return jsonify(list)



if __name__ == "__main__":
    app.run(debug=True)