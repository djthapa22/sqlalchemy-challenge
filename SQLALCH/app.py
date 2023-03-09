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

#  Starting the route for Home Page
@app.route("/")
def home():
    # Main page text callout
    """This is the Api of the SQL Alchemy challenge""" 
    return(
    # Defining route availabilities/ links:
      f"Listed below are the available routes:<br/>"
      f"/api/v1.0/precipitation<br/>"
      f"/api/v1.0/stations<br/>"
      f"/api/v1.0/tobs<br/>"
     f"/api/v1.0/start<br/>"
    f"/api/v1.0/start/end<br/>"
    )

# Creating a path for Precipatation
@app.route("/api/v1.0/precipitation")
def precp():
    session= Session(engine)
# Query the dates and temperature observations of the most-active station for the previous year of data.
    last_date= session.query(func.max(Measurement.date)).scalar()
    year_ago= dt.datetime.strptime(last_date,"%Y-%m-%d")-dt.timedelta(days=365)
    first_date= year_ago.strftime("%Y-%m-%d")
    year_date = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=first_date).all()
# Using a list, dictionary and iterable for loop to unpack precp. values to jsonify
    most_active_list=[]
    for date,prcp in year_date:
        m_dict={}
        m_dict[date]= prcp
        most_active_list.append(m_dict)
    return jsonify(most_active_list)
# Creating a path for Temp data
@app.route("/api/v1.0/tobs")
# Query the dates and temperature observations of the most-active station for the previous year of data.
def most_active():
    
#   Creating a query to find temp data for the most active station
    session= Session(engine)
    last_date= session.query(func.max(Measurement.date)).scalar()
    year_ago= dt.datetime.strptime(last_date,"%Y-%m-%d")-dt.timedelta(days=365)
    first_date= year_ago.strftime("%Y-%m-%d")
    most_active = 'USC00519281'
    sel= [Measurement.tobs,Measurement.date]
    temp_active= session.query(*sel).filter(Measurement.station == most_active).filter(Measurement.date>=first_date).all()
    session.close()
   
#    Using list, iterable loop, dictionaries to append and show jsonified dictionary of query pull:
    most_act_list=[]
    for tobs,date in temp_active:
        most_act_dict={}
        most_act_dict["Date"]= date
        most_act_dict["Temp"]=tobs
        most_act_list.append(most_act_dict)
    return jsonify(most_act_list)

# Creating a rout for stations query:
@app.route("/api/v1.0/stations")
def station():
#    Creating a query to find station data using station table to find below metrics:
    session=Session(engine)
    station_name= session.query(Station.id,Station.name,Station.station, Station.latitude, Station.longitude, Station.elevation).all()
    # Using list, dictionary, iterable loop to unpack station metrics mentioned above and jsonifying to output.
    stations_list=[]
    for id,station,name,latitude,longitude,elevation in station_name:
        station_dict={}
        station_dict["Station ID"]=id
        station_dict["name"]=name
        station_dict["station"]=station
        station_dict["lattitude"]=latitude
        station_dict["longitutde"]=longitude
        station_dict["elevation"]=elevation
        stations_list.append(station_dict)
    return jsonify(stations_list)



#   Testing an iterating start to max date (was using it to find)
# @app.route("/api/v1.0/s/<start>")
# def starting_path1(start):
#     """Finding avg, min and max temp for start dates"""
#     session= Session(engine)
#     max_date= session.query(func.max(Measurement.date))
#     sel= [Measurement.date,Measurement.tobs]
#     s_path= session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <=max_date).all()
#     session.close()

#     start_date= []
#     for date,tobs in s_path:
#         start_dict={}
#         start_dict['Date']=date
#         start_dict['Tobs']=tobs
#         start_date.append(start_dict)
   
#     return jsonify(start_date)


# Creating route to start date
@app.route("/api/v1.0/<start>")
def start_path(start):
    
#    Querying a start date to the final date within the Measurement table
    session= Session(engine)
    sel= [Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    s_path= session.query(*sel).filter(Measurement.date >= start).group_by(Measurement.date).all()
    session.close()
    start_date= []
    # Creating a iterable loop to unpack date,min,max and avg to append to the start date list and then jsonify list
    for date,min,max,avg in s_path:
        start_dict={}
        start_dict['Date']=date
        start_dict['Min']=min
        start_dict['Max']=max
        start_dict['Avg']=avg
        start_date.append(start_dict)

    return jsonify(start_date)
# Creating a path for start and end date
@app.route("/api/v1.0/<start>/<end>")
def start_and_stop_path(start,end):
#    Querying start to end date for temp data using groupby
    session= Session(engine)
    sel= [Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    s_path= session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    session.close()
    start_and_stop_date= []
    # Using a for loop to iterate the metrics below to append to a list for start and stop and jsonify it.
    for date,min,max,avg in s_path:
        start_dict={}
        start_dict['Date']=date
        start_dict['Min']=min
        start_dict['Max']=max
        start_dict['Avg']=avg
        start_and_stop_date.append(start_dict)
    
    return jsonify(start_and_stop_date)


if __name__=="__main__":
    app.run(debug=True)