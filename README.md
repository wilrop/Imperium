![The Imperium logo](docs/images/logo_transparent.png)
# IMPERIUM
Imperium is a data visualisation app that serves investigative journalists and concerned citizens with the knowledge they require and deserve. For too long we have had no idea what goes on in Brussels. Imperium aims to change that.

You can visit a hosted version of the website at [http://imperiumapp.pythonanywhere.com/](http://imperiumapp.pythonanywhere.com/). 
Please keep in mind that this website is hosted on a free plan, which can result in slower loading speeds.

# Requirements

The project was developed using Python 3, using the following main libraries:

+ Dash 1.20.0
+ Flask 1.1.2
+ Pandas 1.2.4
+ Plotly 4.14.3
+ Country-converter 0.7.3
+ Geopy 2.1.0

You can install the required libraries by using pip in a Conda environment or virtualenv with the provided requirements.txt file:

`pip install -r requirements.txt`


## Usage

The `preprocessing.py` will start the preprocessing on the downloaded CSV files and provide two preprocessed CSV files.

The code can be ran using the following command: `python preprocessing.py`


The `imperium_app.py` will start the application and the URL you need to use to visit the web page will be printed in your terminal

The code can be ran using the following command: `python imperium_app.py`
