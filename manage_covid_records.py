"""Important notes for use
	Whenver asked for searched criteria examples:
	Age:13.2
	County:Wake County
	Tdt:February,23,2020
	Email:oxuavc@cor.bvc
	Age:13.2, Gen:F, Email:oxuavx@cor.bvc
	
	Different Modes:
	change, add, import, search
	
	Please Read Descriptions for each mode by
	calling program with -h
"""
import numpy as np
import sys
import argparse
import random
import string
import csv
import re
import datetime
help_mode="Different mode arguments are search,add,change,import. You can add number of people to add argument by add <no>. Import mode argument = import <filename>"

parser = argparse.ArgumentParser(prog = 'manage_covid_records',
	description = 'Data Analysis of Covid19')
parser.add_argument('-f',type = str, default='coviddata.csv', help='name of csv file to work with, ex. coviddata.csv. default is coviddata.csv')
parser.add_argument('-m', type=str,nargs='+',help=help_mode)
parser.add_argument('-i', '--i', help="Analyze data as a whole, picking options a-g",
                    action="store_true")
parser.add_argument('-g', type=str,nargs='+',help="Graphs, argument required, call by -g <mode>, mode can be day, age, gen, county")
args = parser.parse_args()

#use to test for correct input for add function


try:
	if len(args.m)==2:
		args.m=args.m[0]+' '+args.m[1]
	else:
		args.m=args.m[0]
	test_mode_add=re.findall('(add)\s(\d+)|add',args.m)
except:
	test_mode_add=''
try:
	test_mode_import=re.findall('import \w+\.csv|import \w+\.txt',args.m)
except:
	test_mode_import=''



fix_mode=0
while fix_mode==0:
	if args.m != 'search'and len(test_mode_add)!=1 and args.m!='change' and len(test_mode_import)!=1 and args.m!='import':
		if args.i==True or args.g!=None:
			break
		args.m=input('Mode is: ')
		try:
			test_mode_add=re.findall('(add)\s(\d+)|add',args.m)
		except:
			test_mode_add=''
		
	else: 
		fix_mode=1
		

#when using the string search istead of just the name of county, type full txt with County, ex 'Wake County'
def search_file(search_string, file):
	import re
	key_list=[]
	value_list=[]
	full_list_search=[]
	found_list=[]
	found_data=[]
	group_list=re.findall('(Tdt):(\w+, \w+, \w+)|(\w+):(\w+ \w+)|(\w+):(\w+@\w+.\w+)|(\w+):(\w+\.*\w*)',search_string)
	for i in group_list:
		x=0
		while x<len(group_list[0]):
			if i[x]!='':
				key_list.append(i[x])
				value_list.append(i[x+1])
				break
			x=x+1
	full_list_search=full_data_list(file)
	i=0
	while i <len(key_list):
		if key_list[i]=='Pno':
			key_list[i]=0
		if key_list[i]=='Age':
			key_list[i]=1
		if key_list[i]=='Gen':
			key_list[i]=2
		if key_list[i]=='County':
			key_list[i]=3
		if key_list[i]=='IStatus':
			key_list[i]=4
		if key_list[i]=='PStatus':
			key_list[i]=5
		if key_list[i]=='Tdt':
			key_list[i]=6
		if key_list[i]=='Email':
			key_list[i]=7
		if key_list[i]=='History':
			key_list[i]=8
		if key_list[i]=='Notes':
			key_list[i]=9
		i=i+1
			
	iterations=len(key_list)
	total_size_search=len(full_list_search[0])
	i=0
	while i<total_size_search:
		x=0
		while x<iterations:
			if full_list_search[key_list[x]][i]!=value_list[x]:
				break
			x=x+1
			
		if x==iterations:
			y=0
			while y<10:
				found_data.append(full_list_search[y][i])
				y=y+1
			z=0
			temp_list=[]
			while z<len(found_data):
				temp_list.append(found_data[z])
				z=z+1
			found_list.append(temp_list)
			found_data.clear()
		i=i+1
	return found_list

			
def full_data_list(filename):
	from csv import reader
	import string
	list=[]
	i=0
	while i<10:
		list.append([])
		i=i+1
	with open(filename, 'r') as read_obj:
		csv_reader = reader(read_obj)
		for row in csv_reader:
			i=0
			while i<10:
				try:
					list[i].append(row[i])
				except:
					list[i].append('')
				i=i+1
	i=0
	while i<10:
		list[i].pop(0)
		i=i+1
	return list
 
def full_data_list_write(filename):
	from csv import reader
	import string
	list=[]
	i=0
	while i<10:
		list.append([])
		i=i+1
	with open(filename, 'r') as read_obj:
		csv_reader = reader(read_obj)
		for row in csv_reader:
			i=0
			while i<10:
				try:
					list[i].append(row[i])
				except:
					list[i].append('')
				i=i+1
	return list
#search mode 
if args.m=='search':
	search_criteria=input('Enter your search criteria: ')
	patient_list=[]
	total_list=full_data_list(args.f)
	
	try:
		patient_list=search_file(search_criteria, args.f)
	except:
		exit('help text about the program')
	
	if len(patient_list)==(len(total_list[0])):
		exit('None Found')
	total_patients_found=len(patient_list)
	y=0
	if total_patients_found>10:
		y= input('more than 10 matching the criteria, print (y/n)')
	
	x=0
	while x==0:
		if total_patients_found>10 and y!='y' and y!='n':
			y= input('more than 10 matching the criteria, print (y/n)')
		else:
			x=1
	if y=='y':
		for i in patient_list:
			print(i)
	if y=='n'or total_patients_found<10:
		i=0
		while i < 10:
			if i == len(patient_list):
				break
			print(patient_list[i])
			i=i+1


#add mode all under the test check if statement
try:
	test_mode_add=re.findall('(add)\s(\d+)|add',args.m)	
except:
	test_mode_add=[]
if len(test_mode_add)==1:
	if test_mode_add[0][1]=='':
		number_records=1
	else:
		x=test_mode_add[0][1]
		number_records=int(x)
	list=full_data_list_write('coviddata.csv')
	total_id_numbers=len(list[0])-1+100000
	patient_data=[]
	i=0
	while i<number_records:
		x=0
		while x<10:
			if x==0:
				total_id_numbers=total_id_numbers+1
				patient_data.append(str(total_id_numbers))
			if x==1:
				flag=0
				while flag==0:
					test=input('input age as {Age:Float}, ex. Age:12.2 , must include decimal: ')
					test=str(test)
					test_mode_add=re.findall('(\w+):(\d+\.*\d)',test)
					print(test_mode_add)
					if len(test_mode_add)==1:
						flag=1
						patient_data.append(test_mode_add[0][1])
					else:
						print('warning must use proper entry')
			if x==2:	
				flag=0
				while flag==0:
					test=input('input gender as Gen:{M,F} , ex Gen:M - ')
					if test=='':
						patient_data.append('')
						break;
					test_mode_add=re.findall('(\w+):(\w+)',test)
					if len(test_mode_add)==1:
						flag=1
						patient_data.append(test_mode_add[0][1])
					else:
						print('warning must use proper entry')
			if x==3:
				flag=0
				while flag==0:
					test=input('input gender as County:(Name County) ex. County:Wake County - ')
					test_mode_add=re.findall('(\w+):(\w+ \w+)',test)
					if len(test_mode_add)==1:
						flag=1
						patient_data.append(test_mode_add[0][1])
					else:
						print('warning must use proper entry')
			if x==4:
				flag=0
				while flag==0:
					test=input('input Illness as (IStatus^):{U:Unconfirmed, N:Negative, P:Positive} , ex IStatus:U - ')
					if test=='':
						patient_data.append('U')
						break;
					test_mode_add=re.findall('(\w+):(\w+)',test)
					if len(test_mode_add)==1:
						if test_mode_add[0][1]!='U' and\
							test_mode_add[0][1]!='N' and test_mode_add[0][1]!='P':
							flag=0
						else:
							flag=1
							patient_data.append(test_mode_add[0][1])
					else:
						print('warning must use proper entry')
			if x==5:
				flag=0
				while flag==0:
					test=input('input Patient as (PStatus^):{U:Unk, Q:Quaran, H:Hosp, I:ICU, R:Rec, D:Dead}, ex PStatus:U - ')
					if test=='':
						patient_data.append('U')
						break;
					test_mode_add=re.findall('(\w+):(\w+)',test)
					if len(test_mode_add)==1:
						if test_mode_add[0][1]!='U' and test_mode_add[0][1]!='Q' and \
							test_mode_add[0][1]!='H' and test_mode_add[0][1]!='I' and \
							test_mode_add[0][1]!='R' and test_mode_add[0][1]!='D':
							flag=0
						else:
							flag=1
							patient_data.append(test_mode_add[0][1])
					else:
						print('warning must use proper entry')
			if x==6:
				flag=0
				while flag==0:
					test=input('input Test Confirm Date as (Tdt^): Date format <Month, dd, year>, E.g. Tdt:June, 05, 2020 - ')
					if test=='':
						today=datetime.date.today()
						format_date=today.strftime("%B, %d, %Y")
						patient_data.append(format_date)
						break;
					test_mode_add=re.findall('(Tdt):(\w+, \w+, \w+)',test)
					if len(test_mode_add)==1:
						flag=1
						patient_data.append(test_mode_add[0][1])
					else:
						print('warning must use proper entry or press enter')
			if x==7:
				flag=0
				while flag==0:
					test=input('Enter email as Email:<username@domain name>  Domain name should be <string.string>, ex. Email:jordie@hvs.net - ')
					if test=='':
						patient_data.append('')
						break;
					test_mode_add=re.findall('(\w+):(\w+@\w+\.\w+)',test)
					if len(test_mode_add)==1:
						flag=1
						patient_data.append(test_mode_add[0][1])
					else:
						print('warning must use proper entry or press enter')
			if x==8:
				flag=0
				while flag==0:
					test=input('History input example P:January 2, 2020, H:January 8, 2020, R:January 31, 2020  - ')
					if test=='':
						patient_data.append('')
						break;
					test_mode_add=re.findall('(\w:\w+ \d+, \d+,*)',test)
					if len(test_mode_add)>=1:
						flag=1
						history=''
						y=0
						while y<len(test_mode_add):
							history=history+test_mode_add[y]+' '
							y=y+1
						patient_data.append(history)
					else:
						print('warning must use proper entry or press enter')
			if x==9:
				flag=0
				while flag==0:	
					test=input('Enter Notes - ')
					if test=='':
						patient_data.append('')
						break;
					else:
						flag=1
						patient_data.append(test)
				#append the list
				#clear the list
				#next i iteration
				with open(args.f, 'a', newline='') as csvfile:
					writer = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
					writer.writerow(patient_data)
				patient_data.clear()
			x=x+1
		i=i+1
		
#modify patient status
if(args.m=='change'):

	x=0
	while x!=1:
		search_string=input('Enter Search Criteria: ')
		if search_string=='':
			exit('You Exited Out')
		patient=search_file(search_string,args.f)
		if len(patient)!=1:
			print('Not selective Criteria, Enter more sophisticated search for 1 patient:')
			continue
		x=1
	print(patient)
	print('Pick Number Option to change: ')
	print('1:Age')
	print('2:Gender')
	print('3:County')
	print('4:Illness Status')
	print('5:Patient Status')
	print('7:Email')
	print('8:History')
	print('9:Notes')
	
	x=0
	while x!=1:
		attribute_number=int(input('Pick Number Option to change: '))
		if attribute_number==0 or attribute_number==6 or attribute_number<0 or attribute_number>10:
			exit('Cant Change That')
		try:
			value=patient[0][attribute_number]
			x=1
		except:
			print('Cant access that attribute')
	print('Value you have: ',value)
	new=input('Enter new Value: ')
	
	x=0
	while x!=1:
		if attribute_number==1:
			test_mode_add=re.findall('\d+.*\d+',new)
			pass
		if attribute_number==2:
			test_mode_add=re.findall('[MF]',new)
			pass
		if attribute_number==3:
			test_mode_add=re.findall('\w+ County',new)
			pass
		if attribute_number==4:
			test_mode_add=re.findall('[UNP]',new)
			pass
		if attribute_number==5:
			test_mode_add=re.findall('[UQHIRD]',new)
			pass
		if attribute_number==7:
			test_mode_add=re.findall('\w+@\w+\.\w+',new)
			pass
		if attribute_number==8:
			test_mode_add=re.findall('\w:\w+ \d+, \d+',new)
			pass			
		if attribute_number==9:
			test_mode_add=re.findall('.+',new)
			pass	
		if len(test_mode_add)==1:
			x=1
		else:
			new=input('Enter Correct Value: ')
	patient[0][attribute_number]=test_mode_add[0]
	data_list=full_data_list_write(args.f)
	i=0
	while i<len(data_list[0]):
		if data_list[0][i]==patient[0][0]:
			x=0
			while x<10:
				data_list[x][i]=patient[0][x]
				x=x+1
		i=i+1
	with open(args.f, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
		x=0
		writing_list=[]
		while x<len(data_list[0]):
			y=0
			while y<10:
				writing_list.append(data_list[y][x])
				y=y+1
			writer.writerow(writing_list)	
			writing_list.clear()
			x=x+1
		
#import data
if(len(test_mode_import)==1):
	fopen_switch=re.findall('csv|txt',args.m)
	file_to_open=re.findall('\w+\.csv|\w+\.txt',args.m)
	import_data=[]
	record_data=full_data_list(args.f)
	i=0
	while i<10:
		import_data.append([])
		i=i+1
	with open(file_to_open[0]) as csv_file:
		reader = csv.reader(csv_file, delimiter=',')
		for row in reader:
			i=0
			while i<10:
				try:
					import_data[i].append(row[i])
				except:
					import_data[i].append('')
				i=i+1
	i=0
	while i<10:
		import_data[i].pop(0)
		i=i+1
	check_invalid=0
	number_invalid=0
	missing_list=[]
	i=0
	while i<10:
		missing_list.append(0)
		i=i+1
	i=0
	total_patients=len(import_data[0])
	number_invalid=0
	while i<total_patients:
		#test id number (Working)
		test_invalid=re.findall('\d+',import_data[0][i])
		if len(import_data[0][i])!=6 or len(test_invalid)!=1:
			check_invalid=1
			missing_list[0]=missing_list[0]+1

		#test age (Working)
		test_invalid=re.findall('\d+\.*\d+',import_data[1][i])
		test_age=0
		if len(test_invalid)!=1:
			test_age=test_age+1
		test_invalid=re.findall('[a-zA-Z]',import_data[1][i])
		if len(test_invalid)!=0:
			test_age=test_age+1
		if test_age!=0:
			check_invalid=1
			missing_list[1]=missing_list[1]+1
		
		#test gender (Working)
		test_invalid=re.findall('[MF]',import_data[2][i])
		if len(test_invalid)!=1 or len(import_data[2][i])!=1:
				check_invalid=1
				missing_list[2]=missing_list[2]+1
		#test county (Working)
		test_invalid=re.findall('\w+ County',import_data[3][i])
		if len(test_invalid)!=1 or len(import_data[3][i])!=len(test_invalid[0]):
			if import_data[3][i]!='New Hanover County':
				check_invalid=1
				missing_list[3]=missing_list[3]+1
		#Test Illness
		test_invalid=re.findall('[UNP]',import_data[4][i])
		test_illness=0
		if len(import_data[4][i])!= 1:
			test_illness=test_illness+1
		if len(test_invalid)!=1:
			test_illness=test_illness+1
		if test_illness!=0:
			check_invalid=1
			missing_list[4]=missing_list[4]+1
		#Test Patient Status
		test_invalid=re.findall('[UQHIRD]',import_data[5][i])
		test_patient=0
		if len(test_invalid)!=1:
			test_patient=test_patient+1
		if len(import_data[5][i])!=1:
			test_patient=test_patient+1
		if test_patient!=0:
			check_invalid=1
			missing_list[5]=missing_list[5]+1
		#Date Test (working)
		test_invalid=re.findall('\w+, \d+, \d+',import_data[6][i])
		if len(test_invalid)!=1 or len(test_invalid[0])!=len(import_data[6][i]):
			check_invalid=1
			missing_list[6]=missing_list[6]+1
		#Email Test 
		test_invalid=re.findall('\w+@\w+\.\w+',import_data[7][i])
		if len(test_invalid)!=1 or len(test_invalid[0])!=len(import_data[7][i]) :
			check_invalid=1
			missing_list[7]=missing_list[7]+1
		#History Test
		test_invalid=re.findall('[UNPQHIRD]:\w+ \d+, \d+,*',import_data[8][i])
		history_test=0
		if len(test_invalid)==0 and len(import_data[8][i])!=0 :
			history_test=history_test+1
			check_invalid=1
			missing_list[8]=missing_list[8]+1
			
		number_invalid=number_invalid+1
		if check_invalid==1:
			y=0
			while y<10:
				import_data[y].pop(i)
				y=y+1
			check_invalid=0
			total_patients=total_patients-1
			continue
			
		i=i+1
	
	i=0
	str1='records missing '
	while i<10:
		if i==0:
			str2=' Id'
		if i==1:
			str2=' Age'
		if i==2:
			str2=' Gender'
		if i==3:
			str2=' County'
		if i==4:
			str2=' Illness Status'
		if i==5:
			str2=' Patient Status'	
		if i==6:
			str2=' Test confirmation date'
		if i==7:
			str2=' Email'
		if i==8:
			str2=' History'
		if i==9:
			str2=' Notes'
		if missing_list[i]!=0:
			print(missing_list[i],str2,str1)
		i=i+1

	found=0
	i=0
	total_size=len(import_data[0])
	pop_list=[]
	while i <len(record_data[0]):
		x=0
		while x < total_size:
			if import_data[0][x]==record_data[0][i]:
				y=0
				while y<10:
					record_data[y][i]=import_data[y][x]
					y=y+1
				pop_list.append(x)
			x=x+1
		i=i+1
	
	pop_list.sort()
	i=0
	while i<len(pop_list):
		max=pop_list[-1]
		y=0
		while y<10:
			import_data[y].pop(max)
			y=y+1
		pop_list.pop(-1)
	detected=len(import_data[0])

	if len(import_data[0])!=0:
		with open(args.f, 'a', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
			x=0
			list_write=[]
			while x < len(import_data[0]):
				y=0
				while y<10:
					list_write.append(import_data[y][x])
					y=y+1
				writer.writerow(list_write)
				list_write.clear()
				x=x+1
	print(detected, 'new patient records detected')
	
if(args.i==True):
	data= full_data_list(args.f)
	total_number_tested=len(data[0])
	total_confirmed=0
	total_dead=0
	mortality_rate=0
	average_age=0
	average_age_deceased=0
	total_male=0
	total_female=0
	total_confirmed_gender=0
	i=0
	while i<len(data[0]):
		if data[4][i]=='P':
			total_confirmed=total_confirmed+1
		i=i+1
	i=0
	while i<len(data[0]):
		if data[5][i]=='D':
			total_dead=total_dead+1
		i=i+1	
	mortality_rate=total_dead/total_confirmed
	i=0
	while i<len(data[0]):
		average_age=average_age+float(data[1][i])
		i=i+1	
	i=0
	while i<len(data[0]):
		if data[5][i]=='D':
			average_age_deceased=average_age_deceased+float(data[1][i])
		i=i+1	
	i=0
	while i<len(data[0]):
		if data[2][i]=='M' or data[2][i]=='F':
			total_confirmed_gender=total_confirmed_gender+1
			if data[2][i]=='M':
				total_male=total_male+1
			if data[2][i]=='F':
				total_female=total_female+1
		i=i+1	

	average_age=average_age/total_number_tested
	average_age_deceased=average_age_deceased/total_dead
	female_percent=total_female/total_confirmed_gender*100
	male_percent=total_male/total_confirmed_gender*100
	print('a. Total number of people tested: <>')
	print('b. Total confirmed cases: <>  : These are the number of records with IStatus Positive.')
	print('c. Total deaths: <> These are the number of records with PStatus Deceased')
	print('d. Current mortality rate:<> Total deaths /  Total confirmed cases')
	print('e. Average age: <> This is the average age of positively tested people')
	print('f. Average deceased age : <> This is the average age of deceased people')
	print('g. %Female: <>  & %Male: <>   This is percentage of total confirmed females and males. It the gender is not specified,do not count those cases.\n')

	switch_test=0
	while switch_test!=1:
		switch=input('Pick an option (a-g) ex. a: ')
		if switch>='a' and switch<='g':
			switch_test=1	
	if switch=='a':
		print('Total Tested: ',total_number_tested) 
	if switch=='b':
		print('Total Confirmed cases: ',total_confirmed)
	if switch=='c':
		print('Total Deaths: ',total_dead)
	if switch=='d':
		print('Current Mortality Rate: ',mortality_rate)
	if switch=='e':
		print('Average Age: ',average_age)
	if switch=='f':
		print('Average deceased age: ', average_age_deceased)
	if switch=='g':
		print('Confirmed Female Percent: ', female_percent, ' Confirmed Male Percent: ', male_percent)
	

if(args.g!=None):
	import matplotlib.pyplot as plt
	import numpy as np
	
	switch=0
	if args.g[0]!='day' and args.g[0]!='age' and args.g[0]!='gen' and args.g[0]!='county':
		switch=1
	while switch!=0:
		args.g[0]=input('Must be input by typing either day, age, gen, or county, Ex. day \nChoose:')
		if args.g[0]=='day' or args.g[0]=='age' or args.g[0]=='gen' or args.g[0]=='county':
			print(args.g)
			switch=0
	if args.g[0]=='day':
		data=full_data_list(args.f)
		confirmed_by_date=[]
		confirmed_total_by_date=[]
		date_list=[]
		current_date=datetime.date(2020, 1, 1)
		date_to_compare=0
		end_data=datetime.datetime.now().date()
		delta=end_data-current_date
		confirmed_deaths=0
		date_to_append=0
		z=0
		while z <= int(delta.days):
			confirmed_deaths_today=0
			i=0
			date_to_compare=current_date.strftime("%B, %d, %Y")
			while i<len(data[0]):
				if data[6][i]==date_to_compare and data[4][i]=='P':
					confirmed_deaths_today=confirmed_deaths_today+1
				i=i+1
			confirmed_deaths=confirmed_deaths+confirmed_deaths_today
			date_to_append=current_date.strftime("%B, %d")
			date_list.append(date_to_append)
			confirmed_total_by_date.append(confirmed_deaths)
			confirmed_by_date.append(confirmed_deaths_today)
			current_date=current_date+datetime.timedelta(days=1)
			z=z+1
	
		if len(date_list)>40:
			x=0
			while x!=1:
				if len(date_list)>40:
					
					i=0
					while i<len(confirmed_total_by_date):
						confirmed_total_by_date[i]=confirmed_total_by_date[i]-confirmed_by_date[0]
						i=i+1
					confirmed_by_date.pop(0)
					confirmed_total_by_date.pop(0)
					date_list.pop(0)
				else:
					x=1

		# Note that even in the OO-style, we use `.pyplot.figure` to create the figure.
		fig, ax = plt.subplots(figsize=(20, 10))  # Create a figure and an axes.
		ax.plot(date_list, confirmed_total_by_date, label='Total Confirmed')  # Plot some data on the axes.
		ax.plot(date_list, confirmed_by_date, label='Confimred each Day')  # Plot more data on the axes...
		ax.set_xlabel('Date Days')  # Add an x-label to the axes.
		ax.set_ylabel('Confirmed')  # Add a y-label to the axes.
		ax.set_title("Corona Virus Confirmed Cases")  # Add a title to the axes.
		ax.legend()  # Add a legend.
		ax.tick_params(axis='x', which='major', labelsize=6)
		ax.set_xticklabels(date_list, rotation = 45)
		plt.show()
		
	if args.g[0]=='age':
		data=full_data_list(args.f)
		age_list_labels=[]
		age_list_confirmed=[]
		age_lit_deceased=[]
		age_list_labels.append('Under 5')
		age_list_labels.append('5 to 9')
		age_list_labels.append('9 to 14')
		age_list_labels.append('14 to 17')
		age_list_labels.append('17 to 24')
		age_list_labels.append('24 to 34')
		age_list_labels.append('34 to 44')
		age_list_labels.append('44 to 54')
		age_list_labels.append('54 to 64')
		age_list_labels.append('64 to 74')
		age_list_labels.append('64 to 74')
		age_list_labels.append('Over 84')
		count_confirmed=0
		count_deceased=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])<5 and data[4][i]=='P':
				count_confirmed=count_confirmed+1
			if float(data[1][i])<5 and data[5][i]=='D':
				count_deceased=count_deceased+1
			i=i+1
		age_list_confirmed.append(count_confirmed)
		age_lit_deceased.append(count_deceased)
		
		count_confirmed=0
		count_deceased=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>5 and float(data[1][i])<10 and data[4][i]=='P':
				count_confirmed=count_confirmed+1
			if float(data[1][i])>5 and float(data[1][i])<10 and data[5][i]=='D':
				count_deceased=count_deceased+1
			i=i+1
		age_list_confirmed.append(count_confirmed)
		age_lit_deceased.append(count_deceased)
		
		count_confirmed=0
		count_deceased=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>10 and float(data[1][i])<15 and data[4][i]=='P':
				count_confirmed=count_confirmed+1
			if float(data[1][i])>10 and float(data[1][i])<15 and data[5][i]=='D':
				count_deceased=count_deceased+1
			i=i+1
		age_list_confirmed.append(count_confirmed)
		age_lit_deceased.append(count_deceased)

		count_confirmed=0
		count_deceased=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>15 and float(data[1][i])<18 and data[4][i]=='P':
				count_confirmed=count_confirmed+1
			if float(data[1][i])>15 and float(data[1][i])<18 and data[5][i]=='D':
				count_deceased=count_deceased+1
			i=i+1
		age_list_confirmed.append(count_confirmed)
		age_lit_deceased.append(count_deceased)

		count_confirmed=0
		count_deceased=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>18 and float(data[1][i])<25 and data[4][i]=='P':
				count_confirmed=count_confirmed+1
			if float(data[1][i])>18 and float(data[1][i])<25 and data[5][i]=='D':
				count_deceased=count_deceased+1
			i=i+1
		age_list_confirmed.append(count_confirmed)
		age_lit_deceased.append(count_deceased)
		
		count_confirmed=0
		count_deceased=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>25 and float(data[1][i])<35 and data[4][i]=='P':
				count_confirmed=count_confirmed+1
			if float(data[1][i])>25 and float(data[1][i])<35 and data[5][i]=='D':
				count_deceased=count_deceased+1
			i=i+1
		age_list_confirmed.append(count_confirmed)
		age_lit_deceased.append(count_deceased)
		
		count_confirmed=0
		count_deceased=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>35 and float(data[1][i])<45 and data[4][i]=='P':
				count_confirmed=count_confirmed+1
			if float(data[1][i])>35 and float(data[1][i])<45 and data[5][i]=='D':
				count_deceased=count_deceased+1
			i=i+1
		age_list_confirmed.append(count_confirmed)
		age_lit_deceased.append(count_deceased)
		
		count_confirmed=0
		count_deceased=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>45 and float(data[1][i])<55 and data[4][i]=='P':
				count_confirmed=count_confirmed+1
			if float(data[1][i])>45 and float(data[1][i])<55 and data[5][i]=='D':
				count_deceased=count_deceased+1
			i=i+1
		age_list_confirmed.append(count_confirmed)
		age_lit_deceased.append(count_deceased)

		count_confirmed=0
		count_deceased=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>55 and float(data[1][i])<65 and data[4][i]=='P':
				count_confirmed=count_confirmed+1
			if float(data[1][i])>55 and float(data[1][i])<65 and data[5][i]=='D':
				count_deceased=count_deceased+1
			i=i+1
		age_list_confirmed.append(count_confirmed)
		age_lit_deceased.append(count_deceased)
		
		count_confirmed=0
		count_deceased=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>65 and float(data[1][i])<75 and data[4][i]=='P':
				count_confirmed=count_confirmed+1
			if float(data[1][i])>65 and float(data[1][i])<75 and data[5][i]=='D':
				count_deceased=count_deceased+1
			i=i+1
		age_list_confirmed.append(count_confirmed)
		age_lit_deceased.append(count_deceased)

		count_confirmed=0
		count_deceased=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>75 and float(data[1][i])<85 and data[4][i]=='P':
				count_confirmed=count_confirmed+1
			if float(data[1][i])>75 and float(data[1][i])<85 and data[5][i]=='D':
				count_deceased=count_deceased+1
			i=i+1
		age_list_confirmed.append(count_confirmed)
		age_lit_deceased.append(count_deceased)
		
		count_confirmed=0
		count_deceased=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>85 and data[4][i]=='P':
				count_confirmed=count_confirmed+1
			if float(data[1][i])>85 and data[5][i]=='D':
				count_deceased=count_deceased+1
			i=i+1
		age_list_confirmed.append(count_confirmed)
		age_lit_deceased.append(count_deceased)
	
		fig, ax=plt.subplots()
		N=len(age_list_labels)
		ind = np.arange(N)
		width = .35
		rects1=plt.bar(ind, age_list_confirmed, width, label='Confirmed')
		def autolabel(rects):
			for rect in rects:
				height = rect.get_height()
				ax.text(rect.get_x() + rect.get_width()/2, 1*height,
                '%d' % int(height), ha='center', va='bottom')
		autolabel(rects1)
		rects2=plt.bar(ind+width, age_lit_deceased, width, label='Deceased')
		autolabel(rects2)
		plt.ylabel('Age')
		plt.title('Cases by age')
		
		plt.xticks(ind + width / 2, (age_list_labels))
		plt.legend(loc='best')
		plt.xticks(fontsize= 6)
		plt.show()
		

	if args.g[0]=='gen':
		data=full_data_list(args.f)
		age_list_labels=[]
		male_list_confirmed=[]
		female_list_confirmed=[]
		age_list_labels.append('Under 5')
		age_list_labels.append('5 to 9')
		age_list_labels.append('9 to 14')
		age_list_labels.append('14 to 17')
		age_list_labels.append('17 to 24')
		age_list_labels.append('24 to 34')
		age_list_labels.append('34 to 44')
		age_list_labels.append('44 to 54')
		age_list_labels.append('54 to 64')
		age_list_labels.append('64 to 74')
		age_list_labels.append('64 to 74')
		age_list_labels.append('Over 84')
		
		male_count=0
		female_count=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])<5 and data[2][i]=='M' and data[4][i]=='P':
				male_count=male_count+1
			if float(data[1][i])<5 and data[2][i]=='F' and data[4][i]=='P':
				female_count=female_count+1
			i=i+1
		male_list_confirmed.append(male_count)
		female_list_confirmed.append(female_count)

		male_count=0
		female_count=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>5 and float(data[1][i])<10 and data[2][i]=='M' and data[4][i]=='P':
				male_count=male_count+1
			if float(data[1][i])>5 and float(data[1][i])<10 and data[2][i]=='F' and data[4][i]=='P':
				female_count=female_count+1
			i=i+1
		male_list_confirmed.append(male_count)
		female_list_confirmed.append(female_count)

		male_count=0
		female_count=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>10 and float(data[1][i])<15 and data[2][i]=='M' and data[4][i]=='P':
				male_count=male_count+1
			if float(data[1][i])>10 and float(data[1][i])<15 and data[2][i]=='F' and data[4][i]=='P':
				female_count=female_count+1
			i=i+1
		male_list_confirmed.append(male_count)
		female_list_confirmed.append(female_count)

		male_count=0
		female_count=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>15 and float(data[1][i])<18 and data[2][i]=='M' and data[4][i]=='P':
				male_count=male_count+1
			if float(data[1][i])>15 and float(data[1][i])<18 and data[2][i]=='F' and data[4][i]=='P':
				female_count=female_count+1
			i=i+1
		male_list_confirmed.append(male_count)
		female_list_confirmed.append(female_count)
		
		male_count=0
		female_count=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>18 and float(data[1][i])<25 and data[2][i]=='M' and data[4][i]=='P':
				male_count=male_count+1
			if float(data[1][i])>18 and float(data[1][i])<25 and data[2][i]=='F' and data[4][i]=='P':
				female_count=female_count+1
			i=i+1
		male_list_confirmed.append(male_count)
		female_list_confirmed.append(female_count)
		
		male_count=0
		female_count=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>25 and float(data[1][i])<35 and data[2][i]=='M' and data[4][i]=='P':
				male_count=male_count+1
			if float(data[1][i])>25 and float(data[1][i])<35 and data[2][i]=='F' and data[4][i]=='P':
				female_count=female_count+1
			i=i+1
		male_list_confirmed.append(male_count)
		female_list_confirmed.append(female_count)
		
		male_count=0
		female_count=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>35 and float(data[1][i])<45 and data[2][i]=='M' and data[4][i]=='P':
				male_count=male_count+1
			if float(data[1][i])>35 and float(data[1][i])<45 and data[2][i]=='F' and data[4][i]=='P':
				female_count=female_count+1
			i=i+1
		male_list_confirmed.append(male_count)
		female_list_confirmed.append(female_count)
		
		male_count=0
		female_count=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>45 and float(data[1][i])<55 and data[2][i]=='M' and data[4][i]=='P':
				male_count=male_count+1
			if float(data[1][i])>45 and float(data[1][i])<55 and data[2][i]=='F' and data[4][i]=='P':
				female_count=female_count+1
			i=i+1
		male_list_confirmed.append(male_count)
		female_list_confirmed.append(female_count)

		male_count=0
		female_count=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>55 and float(data[1][i])<65 and data[2][i]=='M' and data[4][i]=='P':
				male_count=male_count+1
			if float(data[1][i])>55 and float(data[1][i])<65 and data[2][i]=='F' and data[4][i]=='P':
				female_count=female_count+1
			i=i+1
		male_list_confirmed.append(male_count)
		female_list_confirmed.append(female_count)
		
		male_count=0
		female_count=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>65 and float(data[1][i])<75 and data[2][i]=='M' and data[4][i]=='P':
				male_count=male_count+1
			if float(data[1][i])>65 and float(data[1][i])<75 and data[2][i]=='F' and data[4][i]=='P':
				female_count=female_count+1
			i=i+1
		male_list_confirmed.append(male_count)
		female_list_confirmed.append(female_count)
		
		male_count=0
		female_count=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>75 and float(data[1][i])<85 and data[2][i]=='M' and data[4][i]=='P':
				male_count=male_count+1
			if float(data[1][i])>75 and float(data[1][i])<85 and data[2][i]=='F' and data[4][i]=='P':
				female_count=female_count+1
			i=i+1
		male_list_confirmed.append(male_count)
		female_list_confirmed.append(female_count)
		
		male_count=0
		female_count=0
		i=0
		while i <len(data[0]):
			if float(data[1][i])>85 and data[2][i]=='M' and data[4][i]=='P':
				male_count=male_count+1
			if float(data[1][i])>85 and data[2][i]=='F' and data[4][i]=='P':
				female_count=female_count+1
			i=i+1
		male_list_confirmed.append(male_count)
		female_list_confirmed.append(female_count)
		
		fig, ax=plt.subplots()		
		def autolabel(rects):
			for rect in rects:
				height = rect.get_height()
				ax.text(rect.get_x() + rect.get_width()/2, 1*height,
                '%d' % int(height), ha='center', va='bottom')		
		N=len(age_list_labels)
		ind = np.arange(N)
		width = 0.35
		rects1=plt.bar(ind, male_list_confirmed, width, label='Male')
		autolabel(rects1)
		rects2=plt.bar(ind+width, female_list_confirmed, width, label='Female')
		autolabel(rects2)
		plt.ylabel('Age')
		plt.title('Cases by Gender')
		
		plt.xticks(ind + width / 2, (age_list_labels))
		plt.legend(loc='best')
		plt.xticks(fontsize= 6)
		plt.show()
		
	if args.g[0]=='county':
		data=full_data_list(args.f)
		county_list=[]
		county_count_confirmed=[]
		county_count_total=[]
		i=0
		while i<len(data[0]):
			if data[3][i] not in county_list:
				county_list.append(data[3][i])
			i=i+1
		i=0
		while i < len(county_list):
			x=0
			count_confirmed=0
			count_total=0
			while x<len(data[0]):
				if data[4][x]=='P' and data[3][x]==county_list[i]:
					count_confirmed=count_confirmed+1
				if data[3][x]==county_list[i]:
					count_total=count_total+1
				x=x+1
			county_count_confirmed.append(count_confirmed)
			county_count_total.append(count_total)	
			i=i+1

		
		i=0
		while i < len(county_count_total)-1:
			if county_count_total[i]<county_count_total[i+1]:
				x=county_count_total.pop(i)
				y=county_count_confirmed.pop(i)
				z=county_list.pop(i)
				county_count_total.append(x)
				county_count_confirmed.append(y)
				county_list.append(z)
				i=0
				continue
			i=i+1
		x=0
		while x!=1:
			if len(county_list)>20:
				county_count_total.pop(-1)
				county_count_confirmed.pop(-1)
				county_list.pop(-1)
			else:
				x=1
		
		plt.rcdefaults()
		fig, ax = plt.subplots(figsize=(20, 10))
		N=len(county_list)
		ind = np.arange(N)
		width = 0.01
		y_pos = county_list
		

		ax.barh(ind, county_count_total,height=-.3,align='edge')
		for index, value in enumerate(county_count_total):
			plt.text(value, index, str(value))
		ax.barh(ind+width, county_count_confirmed, height=.3,align='edge')
		for index, value in enumerate(county_count_confirmed):
			plt.text(value, index, str(value))
		ax.set_yticks(ind)
		ax.set_yticklabels(county_list)
		ax.invert_yaxis()  # labels read top-to-bottom
		ax.set_xlabel('number of patients')
		ax.set_title('Total cases by county')
		labels=['Confirmed','Deaths']
		ax.legend(labels)
		plt.show()
		

		
		

	
	
	
	
	
	

