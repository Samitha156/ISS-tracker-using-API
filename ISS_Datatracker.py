
# coding: utf-8

# In[30]:


import urllib.request as urllib2
import json
from datetime import datetime
from datetime import timedelta
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.geocoders import Nominatim
import turtle


# In[31]:


#retrieving data of ISS position and details of the astronauts from the give API
req_1 = urllib2.Request("http://api.open-notify.org/iss-now.json")
req_2 = urllib2.Request("http://api.open-notify.org/astros.json")
position = urllib2.urlopen(req_1)
people = urllib2.urlopen(req_2)

#saving data in two objects
obj_1 = json.loads(position.read())
obj_2 = json.loads(people.read())

#print the live location of ISS 
print("The ISS current location at time",datetime.fromtimestamp(obj_1['timestamp']), " is", obj_1['iss_position']['latitude'],",",obj_1['iss_position']['longitude'])


# In[32]:


#taking use's location as zip code or address 
location = input("Please enter your zip code or address: ",)


# In[33]:


#use geolocatter to get the latitude and longitude of user's location
geolocator = Nominatim(user_agent="My-goelocation-application")
location = geolocator.geocode(location)
print(location.address)


# In[34]:


#To retrieve the passing details of ISS from API you have to submit the url with latitude and longitude
a, b = location.latitude , location.longitude
url = 'http://api.open-notify.org/iss-pass.json?'
url = url + 'lat=' + str(a) +'&lon=' +str(b)

req = urllib2.Request(url)
pos = urllib2.urlopen(req)
isspass = json.loads(pos.read())
print(isspass)


# In[35]:


#retrieve and print ISS-pass details 
over_head = isspass['response'][1]['risetime']
rising_time = datetime.fromtimestamp(over_head)
pass_duration = timedelta(seconds= isspass['response'][1]['duration'])
print('The ISS will be overhead',a ,b, 'at', rising_time, 'for', pass_duration)


# In[36]:


#passing the people data in obj_2 to Pandas DataFrame and expand the people details
df = pd.DataFrame(obj_2)
df2 = pd.DataFrame(df['people'].values.tolist(),index=df.index)
#df2


# In[37]:


#ectracting and printing people data
val = df2['craft'].value_counts()
list_of_crafts = df2['craft'].unique().tolist()
for i in range(len(list_of_crafts)):
    print("There are", val.tolist()[i] , "people abroad the" , val.index.tolist()[i] + ".", "They are" , (', '.join(df2.loc[df2['craft'] == list_of_crafts[i]]['name'].tolist())),"\n")

