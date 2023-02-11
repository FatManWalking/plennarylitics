# plennarylitics
A full-stack application to analyse plannary sessions in the German Bundestag using Svelte(Kit), FastAPI and ElasticSearch

## Team Members:

Björn Bulkens (bjoern.bulkens@stud.uni-heidelberg.de)
Klemens Gerber (klemens.gerber@stud.uni-heidelberg.de)
Daniel M. Knorr (ax280@stud.uni-heidelberg.de)

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
* Implementation of more statistics
* Connection of frontend and backend via FastAPI

# Data Analysis

## Data Sources
The Data sources we are using are the plenary protocols from the Bundesregierung. We get access to the protocols via an API-Key we got from the Bundesregierung. In the current state of the project we don’t use all plenary protocols but only a small amount to test our code. This amount of protocols belong to plenary protocols since 26.09.2021.

## Preprocessing
The following steps were taken to preprocess the Data:
* 1. Extraction of text from the XML Format
* 2. Splitting into different parts (preamble, actual discussions, additional content)

The preprocessing of the data was actually a smaller part of the data extraciton process, than making ourselves familiar with the differences in text structure. Our approach up to this point relies heavily splitting the long strings that we get from the Bundestag API into smaller, more manageable parts. This includes differenc speeches from MPs as well as answers from the plenum and other strings. Looking for these different strings to split on and making up for differences between different XML files was a very large part of the project.

# Basic Statistics

Up to this point, we are including 50 files from the current legislative period into elasticsearch. For the current legislatice parties, we have split the documents into the speeches of the members of the parliament. These speeches are assiegned to the politician giving them and are the documents we are actually saving in elasticsearch. Additionally to this, we are currently saving the missing MPs on a per party basis. In the following graphic, we have for example the top 20 missing MPs by Number for the AfD in the curtrent legislative period. The statistic was extracted from the elasticsearch dashboard. 

![alt text](https://github.com/FatManWalking/plennarylitics/blob/klemens-branch/Visualizations/Top_20_missing_mpsAfD.png)

## Week 44/45

* Setting up project proposal
  * defining goal
  * defining work packages
  * defining work distribution / member roles
* Setting up repo and a blank sceleton for the web app (Björn)

## Week 46
* Text Processing
 * Preprocessing Single Plennar Documents to find patterns
 * Planning Document Storage


## Week 47/48
* Setting up Frontend Functionalities
* Setting up ElastiSearch to store Documents in predefinded way
* Pulling documents directly from the API
* Setting up barebone FastAPI scelton
* Further preprocessing of files to generilize Process


## Week 49/50
* Dockerizing applications, while ensuring communication (work in process)


## Week 51/52
* Holiday

## Week 1
* Working on Report
* Getting connection of the "reaction component" with Elasticsearch setup
* Getting API and Backend setup
* Testing API and Backend
* Getting Pancake setup

## Week 2
* Working on Report
* Finalise Dockerization of the components
* Conception of Frontend Data Visualisations
* Code Cleanup
* Conception of interesting insights with the Data we currently have

