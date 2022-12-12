# plennarylitics
A full-stack application to analyse plannary sessions in the German Bundestag using Svelte(Kit), FastAPI and ElasticSearch

# Data Processing

* Establish a connection to the Bundestag APi and request an API token
* Try pulling relevant data from this api 
* Extract data about missing MPs from the XML Files
* Extract data about comments and other reactions from the plenary from the XML files
* Split the XML files in a way, that enables easy querying in elasticseach

## Frontend
* Get a basic frontend structure up and running
* Make routing between different pages possible and set up the frontend in a way, that makes the display of our data structures easier
* Read about FastAPI and get an early state of the connection running

## Backend

* Install elasticsearch and get it running
* Import first data from the Budnestag API in elasticsearch
* Connect elasticsearch to the preprocessign pipeline
* Load the split documents into elasticsearch
* Load the data about missing MPs in elasticseach
 

## Timeline for the second part of the project:

* Final implementation of the frontend and addition of visuals
* Connection to the backend and exchange of data with the frontend


## Week 44/45

* Setting up project proposal
  * defining goal
  * defining work packages
  * defining work distribution / member roles
* Setting up repo and a blank sceleton for the web app (Björn)

## Week 46


## Week 47


## Week 48


## Week 49


## Week 50

# Data Analysis

## Preprocessing
The following steps were taken to preprocess the Data:
* 1. Extraction of text from the XML Format
* 2. Splitting into different parts (preamble, actual discussions, additional content)

The preprocessing of the data was actually a smaller part of the data extraciton process, than making ourselves familiar with the differences in text structure. Our approach up to this point relies heavily splitting the long strings that we get from the Bundestag API into smaller, more manageable parts. This includes differenc speeches from MPs as well as answers from the plenum and other strings. Looking for these different strings to split on and making up for differences between different XML files was a very large part of the project.

# Basic Statistics

Up to this point, we are including 50 files from the current legislative period into elasticsearch. These include 7 Parties (SPD, AfD, CDU, BUENDNIS90/DIE GRUENEN, FDP, DIELINKE and FRAKTIONSLOS). For each of these parties, we save the missing MPs per plenary meeting, as well as the different speeches  per person. These speeches actually are the documents, we are saving in elasticsearch. 

An example for the missing mps is the following graphic, we have drawn from elasticsearch, displaying the top 20 missing MPs for the AfD in the current 50 plennary meetings. 

![alt text](https://github.com/FatManWalking/plennarylitics/blob/klemens-branch/Visualizations/Top_20_missing_mpsAfD.png)

