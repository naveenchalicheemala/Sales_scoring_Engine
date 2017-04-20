from __future__ import division
import csv
import os
import sys
import math
import pandas as pd



freader = pd.read_csv('data.csv')


# Weights associated for each event
web_weight = 1.0
email_weight = 1.2
social_weight = 1.5
webinar_weight = 2.0

#Function to calculate weighted score for each event
def calculate_score(freader):
    
    score = [] #Initialize a list named score to store scores of each contact

    #Iterate through each row of dataframe and calculate score for each contact based on event type
    for row in freader.itertuples():

        #check for event type: web
        if row[2] == 'web':
            web_score = float(row[3]) * web_weight
            score.append(web_score)
        #check for event type: email
        elif row[2] == 'email':
            email_score = float(row[3]) * email_weight
            score.append(email_score)
        #check for event type: social
        elif row[2] == 'social':
            social_score = float(row[3]) * social_weight
            score.append(social_score)
        #check for event type: webinar
        elif row[2] == 'webinar':
            webinar_score = float(row[3]) * webinar_weight
            score.append(webinar_score)
            
    #print(score)    #--uncomment print statement if needed
    return score    
      

#Call function to calculate score
score = calculate_score(freader)
#Convert list score into series and then append it as a new column for dataframe freader
sc = pd.Series(score)
freader['fscore'] = sc.values

#print(freader) #--uncomment print statement if needed

#All the scores will be summed by contact id to get the total score for each contact
x = freader.groupby('Id')['fscore'].sum()
df = pd.DataFrame({'Id': x.index, 'fscore': x.values})

#Function to normalize summed scores on a scale of 0 to 100
def normalize(values, new_min = 0, new_max = 100):
    output = []
    old_min, old_max = min(values), max(values)
    if (old_min == old_max):                    #Condition check to avoid division by zero error
            new_value = new_min
            output.append(new_value)
    else:
        for v in values:
            # calculate new value on a scale of 0 to 100
            new_value = (((new_max - new_min) / (old_max - old_min)) * (v - old_min)) + new_min
            output.append(new_value)
            
    #Round the scores to the closest integer
    norm_output = [int(round(n, 0)) for n in output]
    return norm_output

tmp = df['fscore'].tolist()
#Call normalize function to normalize the scores on a scale of 0 to 100
norm_list = normalize(tmp)

#print(norm_list) #--uncomment print statement if needed

#Delete the summed scores column as it is not needed
df.drop('fscore', axis=1, inplace=True)

#Convert the normalization scores list into series and then add it as a column to dataframe
norm = pd.Series(norm_list)
df['normalized_score'] = norm.values

#print(df) #--uncomment print statement if needed

#Function to calculate median and Quartile2
def get_median(lst):
    
    length = len(lst)
    mid_pos = int(length / 2)
    
    if length < 2:
        return lst[0]
    elif length == 2:
        return (lst[0] + lst[1]) / 2
    elif length % 2 != 0:
        return lst[mid_pos]
    return (lst[mid_pos-1] + lst[mid_pos]) / 2

#Function to calculate lower half of data and Quartile1
def get_lower_half(lst):
    mid_pos = int(math.floor(len(lst) / 2))
    return(lst[0:mid_pos])

#Function to calculate upper half of data and Quartile3
def get_upper_half(lst):
    mid_pos = int(math.ceil(len(lst) / 2))
    return(lst[mid_pos:])

def show_results(df):
    
    lst = df['normalized_score'].tolist()  #Convert normalized score column into list to calculate quartiles
    lst.sort() #Sort the list

    q1 = get_median(get_lower_half(lst))   #Calculate Q1
    q2 = get_median(lst)                   #Calculate Q2
    q3 = get_median(get_upper_half(lst))   #Calculate Q3

    #   --uncomment print statements if needed
    '''
        print("Q1: %s" %(q1))
        print("Q2: %s" %(q2))
        print("Q3: %s" %(q3))
    '''

    final = []  #Create a list to store quartile labels for each contact

    print("\nScoring Engine Output: \n")
    #Iterate through each row of data frame
    for row in df.itertuples():

        #Check for bronze quartile
        if (0 <= row[2] <= q1):
            final.append('bronze')
            print("%d, bronze, %d" %(row[1],row[2]))
            
        #Check for Silver quartile
        elif (q1 < row[2] <= q2):
            final.append('silver')
            print("%d, silver, %d" %(row[1],row[2]))

        #Check for Gold quartile    
        elif (q2 < row[2] <= q3):
            final.append('gold')
            print("%d, gold, %d" %(row[1],row[2]))

        #Check for Platinum quartile    
        elif (q3 < row[2] <= 100):
            final.append('platinum')
            print("%d, platinum, %d" %(row[1],row[2]))

    return final

final_list = show_results(df)

#Convert list into series and add the quartile label as a column to dataframe
lb = pd.Series(final_list)
df['label'] = lb.values

#Save the data frame into csv file
df.to_csv('result.csv', sep = ',', index = False) 

print("\nFinal result is also saved in result.csv file")
    

