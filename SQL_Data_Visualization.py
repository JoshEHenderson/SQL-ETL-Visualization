'''
Copyright 2022 Joshua Henderson

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

# Imports
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

# roundMin is passed a date with type datetime
# roundMin returns the date rounded down to the minute (sets the value of date.second to 0)
def roundMin(date):
    return dt.datetime(date.year, date.month, date.day, date.hour, date.minute, 0)

dw_df = pd.read_csv("dw_df.csv")                # read in data from file 'dw_df.csv' on the current working directory
dw_df = dw_df.drop(['Unnamed: 0'], axis = 1)    # drop the index column created by the writing to a csv

# when stored and read, datetime gets converted to an object, so put back into datetime format
dw_df['creationDate'] = pd.to_datetime(dw_df['creationDate'])
# round creation date down to the nearest minute to make graphs more readable
dw_df['creationDate'] = [roundMin(dw_df['creationDate'][i]) for i in range( len(dw_df) )]

# ##################
# Analyze
# ##################

study3_df = dw_df[dw_df.studyID == 3]           # create a new dataframe with only survey 3 data
plt.hist(study3_df['response'], range(1, 8))    # plot the responses in a histogram
plt.title('Responses Over All Factors')         # title the histogram
plt.show()                                      # display the histogram

for fact in set(study3_df['factorName']):       # loop through the factors present
    # create a new dataframe to work with that stores creationDate along with average response
    # average responses are grouped by minutes since we rounded to the nearest minute earlier
    curr_df = study3_df[study3_df.factorName == fact].groupby(['creationDate'], as_index = False).agg({'response':'mean'})
    
    plt.plot(curr_df['creationDate'], curr_df['response'] ) # plot the average responses by creationDate
    plt.title(fact)                                         # title the graph with the current factor
    plt.show()                                              # display plot