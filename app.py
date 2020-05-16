import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify
app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station



@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        "Hello there!<br/>"
        f"Below are your available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start-date<br/>"
        f"/api/v1.0/start-date/end-date<br/>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    

# Create our session (link) from Python to the DB
    session = Session(engine)
    
#Query to get precipitation dates for the year
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > '2016-08-23').\
    order_by(Measurement.date).all()

    session.close()
    
    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)


    return jsonify(prcp_list)




@app.route("/api/v1.0/stations")
def stations():
    
    
# Create our session (link) from Python to the DB
    session = Session(engine)

# Query all stations
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

    




@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
#Query to get precipitation dates for the year at Waihee
    temps = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > '2016-08-23', Measurement.date < '2017-08-24',   Measurement.station=='USC00519281').\
    order_by(Measurement.date).all()
    

    session.close()
    
    temps_list = []
    for date, tobs in temps:
        temps_dict = {}
        temps_dict["date"] = date
        temps_dict["tobs"] = tobs
        temps_list.append(temps_dict)


    return jsonify(temps_list)

#@app.route("/api/v1.0/<start-date>")
#def temps_from_start_date(start-date):
    """Fetch the min, max, avg temps from
       the date variable supplied by the user, or a 404 if not."""

    #canonicalized = start-date.replace(" ", "").lower()
    #for temp in temps:
       # search_term = temp["tobs"].replace(" ", "").lower()

        #if search_term == canonicalized:
            #return jsonify(temps_from_start_date)

   # return jsonify({"error": Temps for {start-date} not found."}), 404



if __name__ == "__main__":
    app.run(debug=True)

