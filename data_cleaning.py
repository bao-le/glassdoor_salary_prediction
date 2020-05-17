# -*- coding: utf-8 -*-
"""
Created on Fri May 15 14:05:12 2020

@author: baole
"""
import pandas as pd
df = pd.read_csv('glassdoor_jobpostings.csv')

##Clean up Salary Estimate

#Remove salary = -1 rows 
df=df[df['Salary Estimate'] != '-1']

#Remove glassdoor est, employer provided salary
salary =df['Salary Estimate'].apply(lambda x: x.split(" (")[0])
salary =df['Salary Estimate'].apply(lambda x: x.split("(")[0])

#Add column hourly and employer provided for salary
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)

#Remove dollar sign, k and any extra information
remove_dk = salary.apply(lambda x: x.replace("$","").replace("K",""))
remove_extra = remove_dk.apply(lambda x: x.lower().replace("per hour","").replace("employer provided salary:",""))

#Make min, max and average salary after salary column is cleaned
df['min_salary'] = pd.to_numeric(remove_extra.apply(lambda x: x.split("-")[0]))
df['max_salary'] = pd.to_numeric(remove_extra.apply(lambda x: x.split("-")[1]))
df['avg_salary'] = (df['min_salary']+df['max_salary'])/2

#Parse Company name
df['company_text'] = df['Company Name'].apply(lambda x: x[:-3] if x != '-1' else x) 

#Separate states
df['state'] = df.apply(lambda x: x['Location'][-2:], axis = 1)

#Job posting same state with headquarter?
df['same_state'] = df.apply(lambda x: 1 if x.Location[-2:] == x.Headquarters[-2:] else 0, axis =1)

#Age of company
df['comapny_age'] = df.apply(lambda x: (2020 - pd.to_numeric(x.Founded)) if x.Founded > -1 else x.Founded, axis = 1)

#Job description parsing

skills = ['python','sql','java','spark','aws','c++']

for skill in skills:
    df[skill] = df['Job Description'].apply(lambda x: 1 if skill in x.lower() else 0)

df.to_csv('cleaned_data.csv')
