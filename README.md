# Sqlalchemy-challenge

**Overview:**

In this activity, we learned about using SQLAlchemy how to extract data from SQL Lite and transform it into useful data regarding climate and temperature data. These were broken out in the following sections:

<ins>Analyze and Explore Climate Data:</ins>
* Use the SQLAlchemy create_engine() function to connect to your SQLite database.
* Use the SQLAlchemy automap_base() function to reflect your tables into classes, and then save references to the classes named station and measurement.
* Link Python to the database by creating a SQLAlchemy session.
* Conduct Precipiation Analysis
* Conduct Station Analysis



<ins> Design Your Climate App: </ins>
* Start at the homepage and List all the available routes
* Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
* Query the dates and temperature observations of the most-active station for the previous year of data..
* Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.



