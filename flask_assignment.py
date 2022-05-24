from ast import dump
import datetime as dt
from dateutil.relativedelta import relativedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database Setup


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Flask Setup


app = Flask(__name__)

# Flask Routes


# Create a home page route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Hawaii Climate Analysis and Exploration Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>Dictionary of date and precipitation<br/><br/>"
        f"/api/v1.0/stations<br/>List of the weather stations<br/><br/>"
        f"/api/v1.0/tobs<br/>Dictionary of date and tobs of the most active station for the last year of the data<br/><br/>"
        f"/api/v1.0/<start_date_only><br/>Min, max, avg tobs for all dates greater than and equal to the start date.<br/><br/>"
        f"/api/v1.0/<start_date>/<end_date><br/>Min, max, avg tobs for dates between the start and end date inclusive.<br/><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the date and prcp for the last 12 months
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>='2016-08-23').group_by(Measurement.date).order_by(Measurement.date).all()

    session.close()

    #create a dictionary using date as key and prcp as the value
    precipitation_list = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict['prcp'] = prcp
        precipitation_list.append(precipitation_dict)

    #Return the JSON representation of your dictionary
    return jsonify(precipitation_list)


@app.route("/api/v1.0/stations")
def stations ():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the station name
    result = session.query(Station.station,Station.name).all()

    session.close()

    #create a list of stations
    station_list = []
    for station,name in result:
        station_dict = {}
        station_dict['station'] = station
        station_dict['name'] = name
        station_list.append(station_dict)

    #Return a JSON list of stations from the dataset
    return jsonify(station_list)
    

@app.route("/api/v1.0/tobs")
def tobs():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query the dates and temperature observations of the most active station
    Result =  session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>='2016-08-23').filter(Station.station == Measurement.station).filter(Station.name == 'WAIHEE 837.5, HI US').all()

    session.close()

    #Return a JSON list of temperature observations (TOBS)
    tobs_list = []
    for date, tobs in Result:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs 
        tobs_list.append(tobs_dict)

    #Return a JSON list of tobs from the dataset
    return jsonify(tobs_list)


@app.route("/api/v1.0/<start_date_only>")
def StartDate(start_date_only):
     # Create our session (link) from Python to the DB
    session = Session(engine)

    Results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start_date_only).group_by(Measurement.date).all()

    session.close()

    #Return JSON list of max, min, avg tobs
    start_list = []
    for date,tmin,tmax,tavg in Results:
        start_dict = {}
        start_dict['Date'] = date
        start_dict['TMIN'] = tmin
        start_dict['TMAX'] = tmax
        start_dict['TAVG'] = tavg
        start_list.append(start_dict)

    return jsonify(start_list)

@app.route("/api/v1.0/<start_date>/<end_date>")
def StartDateEndDate(start_date,end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    Resultss = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date<=end_date).group_by(Measurement.date).all()

    session.close()

    #Return JSON list of max, min, avg tobs
    startend_list = []
    for date,Tmin,Tmax,Tavg in Resultss:
        startend_dict = {}
        startend_dict['Date'] = date
        startend_dict['TMIN'] = Tmin
        startend_dict['TMAX'] = Tmax
        startend_dict['TAVG'] = Tavg
        startend_list.append(startend_dict)

    return jsonify(startend_list)

if __name__ == '__main__':
    app.run(debug=True)