# Sqlalchemy_Challenge

Used Python and SQLAlchemy to perform basic climate analysis and data exploration of your climate database. Completed the following tasks by using SQLAlchemy ORM queries, Pandas, and Matplotlib.

# Climate Analysis and Exploration:
Used SQLAlchemy’s `create_engine` to connect SQLite database.
Used SQLAlchemy’s `automap_base()` to reflect tables into classes and saved a reference to the classes called `Station` and `Measurement`.
Linked Python to the database by creating a SQLAlchemy session.

# Precipitation Analysis
performed an analysis for precipitation in the area by finding the most recent date in the dataset.
Used this date to retrieve the previous 12 months of precipitation data by querying the 12 previous months of data.
selected the date and prcp values.
sorted the dataframe values by date and plotted them.

# Station Analysis:
Calculated the total number of stations in the dataset.
Found the most active stations (the stations with the most rows).
Listed the stations and observation counts in descending order.
Highest number of observations station id has.






