from selenium import webdriver
import pandas as pd
import random
import time


out_csv = 'sample_with_citations.csv'	#The output file
driver = webdriver.Firefox()

def get_profiles(file_path):
	scholars = pd.read_csv(file_path)
	return scholars

df = get_profiles('sample.csv')		#Your input CSV file
dups = df.duplicated("scholarid", keep='first')

def get_citations(scholar_id):
	scholar_profile = "https://scholar.google.com/citations?user=" + scholar_id
	driver.get(scholar_profile)
	element = driver.find_element_by_id("gsc_rsb_st")
	data = element.text
	data_lines = data.split("\n")
	citations = {}
	for line in data_lines:
		line_content = line.split(" ")
		citations[line_content[0]] = line_content[1]
	return citations

def append_citations(index, citation_data):
	print(citation_data)
	if(citation_data['Zitate']):
		citation_data['Citations'] = citation_data['Zitate']
	df.loc[index, 'citations'] = citation_data['Citations']
	df.loc[index, 'h-index'] = citation_data['h-index']
	df.loc[index, 'i-10-index'] = citation_data['i10-index']
	df.to_csv(out_csv)

def write_current_index():
	global current_index
	outF = open("current_index.txt", "w")
	outF.write(str(current_index))
	outF.close()

def generate_citations():
	global current_index
	for index, row in df.iterrows():
		if row['scholarid'] is not 'NOSCHOLARPAGE' and index >= current_index and dups.get(index) == False:
			try:
				citation_data = get_citations(row['scholarid'])
				append_citations(index, citation_data)
				current_index = index-1
				write_current_index()
				rnd = random.random() * 30
				time.sleep(30 + rnd)
			except:
				break


inF = open("current_index.txt", "r")
current_index = int(inF.read())
inF.close()

generate_citations()

driver.close()
