#Import dependencies
import datetime as dt
from venv import create
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Set up the database
engine = create_engine('sqlite:///hawaii.sqlite')

#Reflect database into classes
Base = automap_base()
Base.prepare(engine, reflect=True)

#Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create session link
session = Session(engine)

#Set up Flask
app = Flask(__name__)

#Create routes
#Define the 'Welcome' route
@app.route('/')

def welcome():
    return(
        '''
        Welcome to the Climate Analysis API!
        Available Routes:
        /api/v1.0/precipitation
        /api/v1.0/stations
        /api/v1.0/tobs
        /api/v1.0/temp/start/end
        '''
    )

#Create 'Precipitation' route
@app.route('/api/v1.0/precipitation')

def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#Create 'Stations' route
@app.route('/api/v1.0/stations')

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#Create 'Temperature' route
@app.route('/api/v1.0/tobs')

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    return