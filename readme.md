# Personal Magic The Gathering Collection Tracker  

*I have been playing Magic The Gathering  for over 20 years.*  
*This hobby has led to large collection of cards and a significant financial investment*  
*There are many commercially available tools for monitoring price fluctuations and inventory tracking for collections of this size
 , none of them have given me all the features I would like, so I decided to make my own*  
 *I have no desire to engage with the more serious financial speculation of the Magic Card community I would still like to be able to capitalize on price spikes
 and leverage the unused portion of my inventory into more useful cards*
 
 ## The Process  
 
 ### Daily Inventory Export  
 *I use [Deckbox](https://www.deckbox.org) as a collection tracking tool*  
 *This site gives me all the basic inventory organization tools I require, however there is no historical price tracking*
 #### Step 1. Export  
 Create a python script to export the daily price of each card in my collection.  
 Deckbox does not have a publicaly available API to interface with, So I have used the python package selenium and windows task scheduler 
 to automate the export.
 
 :point_down: **I am here**  
 #### Step 2. Manipulate  
 Create another scheduled script to strip the pricing information from my daily download and create a master price history 
 database using the python package pandas.   
 Maintain a seperate database for individual charateristics of each card I own for detailed price tracking by card categories and attributes. 
 
 #### Step 3. Visualize  
 Create Tableau Dashaboards to monitor price of subsets of my collection  
 
 
 
 
 

