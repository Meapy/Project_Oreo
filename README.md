# Project_Oreo
NLP chat bot using tmdb as the dataset to query information about Movies (actors, runtime, directors, etc.........)

Uses Tensorflow and TF learn to create a nural network which then trains itself. 

Task's done:

Daniel Krasovski: Came up with the Idea and came up with the way the app will work, Coded the backend AI using online tutorials, attatched the backend to the GUI.

Raphael Offeimu & Sasha Kuchenmiester: Sparql queries to get the CSV files.

Harry Bebbington: Designed the GUI.

Types of quieries the app responds to:
  Langugage
  Genre
  Most Popular movies
  Highest Budget
  and more
 
 Adding more quieres is as simple as getting more CSV files with a list of movies and then adding it to the intents.json file with the relevent information
 and then retraining the model. The app is also really fast as it does no machine learning after you write in your query. it is all done before the program is ran.


To run this project, run Main.ipynb first and then gui.py
