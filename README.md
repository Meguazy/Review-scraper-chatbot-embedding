# Indeed scraping for chatbot interaction

This repo contain the project code for the course "Technologies for Big Data Management" held by professor Massimo Callisto at the university of Camerino. 

### Table of Contents:
1. [Introduction](#introduction)
1. [Technologies](#technologies)  
1. [Prerequisites](#prerequisites)
1. [Installation & Configuration](#installation-and-configuration)  
    1. [Kafka](#kafka)
    1. [MQTT Dumper](#mqtt-dumper)
    1. [Kakfa Stream](#kafkastream-1)
    1. [MongoDB](#mongodb-1)
    1. [MongoDB Sink Connector](#mongodb-sink-connector)
    1. [Presto](#presto)
1. [Usage](#usage)  
    1. [IoT Simulator](#iot-simulator-1)
    1. [MQTT Dumper](#mqtt-dumper-1)
    1. [Kafka Stream](#kafkastream-2)
    1. [Presto](#presto-1)
    1. [Jupyter Connection](#jupyter-1)
1. [Results](#results)  
    1. [Line Chart](#linechart-1)
    1. [Bar Chart](#barchart-1)
    1. [Pie Chart](#piechart-1)
1. [License](#license)
1. [Contact Information](#contact-information) 

## Introduction
The scope of this project is to dynamically scrape reviews from Indeed in order to embed them in the context of a chatbot. This chatbot will then communicate with the user and it will be able to answer questions about said company. For example, a user might be interested in the salary level of a certain company but maybe doesn't want to read thousands of reviews to find that out. This project aims to find a solution just to that.
The application scrapes data from the web, then embeds it into a vector database in order for them to be used later when the user asks a question.

## Technologies
For this project we used different technologies.
