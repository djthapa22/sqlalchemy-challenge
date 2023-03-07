# Importing modules
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# Save refrence to table
Measurement= Base.classes.measurement
Station= Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


@app.route("/")
def home():
    """This is the Api of the SQL Alchemy challenge""" 
    return(
      f"Listed below are the available routes:<br/>"
      f"/api/v1.0/precipitation<br/>"
      f"/api/v1.0/stations<br/>"
      f"/api/v1.0/tobs<br/>"
      f"/api/v1.0/<start> <br/>"
      f" /api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precp():
    session= Session(engine)
# Query the dates and temperature observations of the most-active station for the previous year of data.
    last_date= session.query(func.max(Measurement.date)).scalar()
    year_ago= dt.datetime.strptime(last_date,"%Y-%m-%d")-dt.timedelta(days=365)
    first_date= year_ago.strftime("%Y-%m-%d")
    year_date = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=first_date).all()

    most_active_list=[]
    for date,prcp in year_date:
        m_dict={}
        m_dict[date]= prcp
        most_active_list.append(m_dict)
    return jsonify(most_active_list)

@app.route("/api/v1.0/tobs")
# Query the dates and temperature observations of the most-active station for the previous year of data.
def most_active():
    """Finding the min,max and average of the most active station"""
    session= Session(engine)
    last_date= session.query(func.max(Measurement.date)).scalar()
    year_ago= dt.datetime.strptime(last_date,"%Y-%m-%d")-dt.timedelta(days=365)
    first_date= year_ago.strftime("%Y-%m-%d")
    most_active = 'USC00519281'
    sel= [Measurement.tobs,Measurement.date]
    temp_active= session.query(*sel).filter(Measurement.station == most_active).filter(Measurement.date>=first_date).all()
    session.close()
    most_act_list=[]
    for tobs,date in temp_active:
        most_act_dict={}
        most_act_dict["Date"]= date
        most_act_dict["Temp"]=tobs
        most_act_list.append(most_act_dict)
    return jsonify(most_act_list)


@app.route("/api/v1.0/stations")
def station():
    """Finding the list of stations from datset"""
    session=Session(engine)
    station_name= session.query(Station.name,Station.station, Station.latitude, Station.longitude, Station.elevation).all()
    stations_list=[]
    for station,name,latitude,longitude,elevation in station_name:
        station_dict={}
        station_dict["name"]=name
        station_dict["station"]=station
        station_dict["lattitude"]=latitude
        station_dict["longitutde"]=longitude
        station_dict["elevation"]=elevation
        stations_list.append(station_dict)
    return jsonify(stations_list)

@app.route("/api/v1.0/<start>")
def starting_path(start):
    """Finding avg, min and max temp for start dates"""
    session= Session(engine)
    sel= [Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    s_path= session.query(*sel).filter(Measurement.date >= start).all()

    for path in 

@app.route("/api/v1.0/<start>/<end>")




if __name__=="__main__":
    app.run(debug=True)