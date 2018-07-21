import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///.hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurements = Base.classes.measurments
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
            f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start>/<end>"
            )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Query 
    results = session.query(Measurements.prcp).all()
    
    # Convert 
    all_prcp = list(np.ravel(results))
    
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def station_count():
    
    # Query 
    results = session.query(Station.station).all()
    
    # Convert 
    all_station = list(np.ravel(results))
    
    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    
    # Query 
    results = session.query(Measurements.tobs).all()

    all_tob = list(np.ravel(results))
    return jsonify(all_tob)


'''  
    all_tobs = []
    for tob in results:
        tobs_dict = {}
        tobs_dict["station"] = tob.station
        tobs_dict["tob"] = tob.tobs
        all_tobs.append(tobs_dict)
    
    return jsonify(all_tobs)'''


if __name__ == '__main__':
    app.run(debug=True)
