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
import sqlite3
import pandas as pd
import numpy as np

DIR = #Insert Directory for SQL Database here

# Connect to database
conn = sqlite3.connect(DIR)

# ##################
# Extract
# ##################

# Read in SQL queries to dataFrames
df1 = pd.read_sql_query('SELECT questionID_id, response FROM surveys_response', conn)
df2 = pd.read_sql_query('SELECT questionTextID, factorID_id, positive_p FROM surveys_question_text', conn)
df3 = pd.read_sql_query('SELECT surveyID, userID_id, creationDate, completionDate FROM surveys_survey', conn)
df4 = pd.read_sql_query('SELECT factorID, factorName, studyID_id FROM surveys_factor', conn)
df5 = pd.read_sql_query('SELECT questionID, questionTextID_id, surveyID_id FROM surveys_question', conn)
df6 = pd.read_sql_query('SELECT userID, userGroup, age, location, hireDate FROM surveys_user', conn)

# ##################
# Transform
# ##################

# Rename foreign ID keys to enable merging with the same column titles
df1.rename(columns={'questionID_id':'questionID'}, inplace = True)
df2.rename(columns={'factorID_id':'factorID'}, inplace = True)
df3.rename(columns={'userID_id':'userID'}, inplace = True)
df4.rename(columns={'studyID_id':'studyID'}, inplace = True)
df5.rename(columns={'questionTextID_id':'questionTextID'}, inplace = True)
df5.rename(columns={'surveyID_id':'surveyID'}, inplace = True)

# Logic for merging along foreign keys
# df1 questionID_id -> df5 questionID
# df5 questionTextID_id -> df2 questionTextID
# df2 factorId_id -> df4 factorID
# df5 surveyID_id -> df3 surveyID
# df3 userID_id -> df6 userID

# Pseudocode for merging
# df1 LJ df5 -> df1_5
# df1_5 LJ df2 -> df1_2_5
# df1_5_2 LJ df4 -> df1_5_2_4
# df1_5_2_4 LJ df3 -> df1_5_2_4_3
# df1_5_2_4_3 LJ df6 -> dw_df

# Perform merges
df1_5       = df1.merge(df5, how='left')
df1_5_2     = df1_5.merge(df2, how='left')
df1_5_2_4   = df1_5_2.merge(df4, how='left')
df1_5_2_4_3 = df1_5_2_4.merge(df3, how='left')
dw_df       = df1_5_2_4_3.merge(df6, how='left')

# ##################
# Clean
# ##################

# Dictionary mapping column names to index in the dw_df DataFrame
getColIdx = {dw_df.columns[i]: i for i in range( len(dw_df.columns) )}

idx = getColIdx['response']                         # get the column number of response
for i in range(len(dw_df['response'])):             # loop through the items in response column
    try:                                            # try to make the response an integer
        dw_df.iloc[i, idx] = int(dw_df.iloc[i, idx])
    except:                                         # if an exception is thrown, that response is not
        dw_df.iloc[i, idx] = np.nan                 # an integer and is replaced with numpy nan
dw_df.dropna(subset=['response'], inplace=True) # remove rows that have a numpy nan as a response

idx2 = getColIdx['positive_p']                      # get the column number of positive_p
for i in range( len( dw_df ) ):                     # loop through items in positive_p column
    if dw_df.iloc[i, idx2] == 0:                    # if the positive_p value is 0:
        dw_df.iloc[i, idx] = 7-dw_df.iloc[i, idx]       # invert the response
       
dw_df['creationDate'] = pd.to_datetime(dw_df['creationDate']) # turn creationDate into dateTime format

# ##################
# Load
# ##################

file = open('dw_df.csv', 'w')   # open a new csv file called 'dw_df.csv' for writing
file.write( dw_df.to_csv() )    # write dw_df to the file in csv format
file.close()                    # close the file and write it to the current working directory
