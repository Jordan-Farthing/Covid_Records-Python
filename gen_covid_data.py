import numpy as np
import sys
import argparse
import random
import string
import csv

parser = argparse.ArgumentParser(prog = 'gen_covid_data',
    description = 'Show top lines from each file')
parser.add_argument('-fname',type = str, default='coviddata.csv')
parser.add_argument('-no', type=int, default=100000)
args = parser.parse_args()

filename=args.fname
no_of_patients=int(args.no)

list_county=[]
with open('county.txt','r') as reader:
	county_data=reader.readlines()

i=0
for l in county_data:
	county_data[i]=l.rstrip('\n')
	i=i+1


data_to_append=[]

#id numbers
patient_numbers_list=[]
i=0
test_number=100000
while i < no_of_patients:
	test_number=test_number+1
	patient_numbers_list.append(test_number)
	i=i+1	

data_to_append.append(patient_numbers_list)

#age
patient_age_list=[]
i=0
while i < no_of_patients:
	test_number=random.randrange(120)
	test_number=test_number + round(random.random(),1)
	patient_age_list.append(test_number)
	i=i+1	

data_to_append.append(patient_age_list)

#gender
gender = np.random.choice(['M','F'], no_of_patients,
              p=[.5,.5])
data_to_append.append(list(gender))

#county
county= np.random.choice(county_data, no_of_patients)
data_to_append.append(list(county))

#Illness Status
illness_types=['U','N','P']
illness= np.random.choice(illness_types, no_of_patients,p=[.4,.3,.3])
data_to_append.append(list(illness))

#Patient Status
patient_types=['U','Q','H','I','R','D']
patient_status=np.random.choice(patient_types, no_of_patients)
data_to_append.append(list(patient_status))

#test confirmation date
date_list=[]
import datetime
start_date = datetime.date(2020, 1, 1)
end_date = datetime.date.today()
time_between_dates = end_date - start_date
days_between_dates = time_between_dates.days

i=0
while i < no_of_patients:
	random_number_of_days = random.randrange(days_between_dates)
	random_date = start_date + datetime.timedelta(days=random_number_of_days)
	year=random_date.year
	month=random_date.month
	day=random_date.day
	random_str= str(month) + ', ' +str(day) + ', ' +str(year)
	random_strObject = datetime.datetime.strptime(random_str,"%m, %d, %Y")
	random_strConverted = random_strObject.strftime("%B, %d, %Y")
	date_list.append(random_strConverted)
	i=i+1
	
data_to_append.append(list(date_list))

#email
email_list=[]
def randomString(stringLength=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
	
i=0
while i < no_of_patients:
	email=randomString(6)+'@'+randomString(3)+'.'+randomString(3)
	email_list.append(email)
	i=i+1

data_to_append.append(email_list)
	
header_list=[]	
header_list.append('Patient number')
header_list.append('Age')
header_list.append('Gender')
header_list.append('County')
header_list.append('Illness Status')
header_list.append('Patient Status')
header_list.append('Test confirmation date')
header_list.append('Email')
header_list.append('History')
header_list.append('Notes')

list_row_writer=[]
with open(filename, 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
	writer.writerow(header_list)
	x=0
	y=0
	while y< no_of_patients:
		x=0
		while x<len(data_to_append):
			list_row_writer.append(data_to_append[x][y])
			x=x+1
		y=y+1
		writer.writerow(list_row_writer)
		list_row_writer.clear()
	
	

