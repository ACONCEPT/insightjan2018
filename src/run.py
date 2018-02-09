#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
For each recipient, zip code, and calendar year, calculate: 
    total dollars received
    total number of contributions
    donation amount percentile
    
two input files:
    percentile.txt : contains percentile value to calculate
    
    itcont.txt has a line for each campaign contribution made on a particular 
    date from a donor to a campaign -- KEEP ONLY id, name, zipcode, amount, date, 
    
    
    
if a donor is a repeat donor, (DONOR KEY IS (NAME, ZIP CODE)) in a prior year 

input file cleaning
KEEP ONLY THE FIRST 5 CHARS OF ZIP_CODE
use name and zip code to identify unique donors
do not assume the year field holds any particular value
transactions can be out of order
we are only interested in individual contributions, so only select records with other_id set to empty
igore if:
    transaction_dt is an invalid date
    zip_code is invalid (empty, or fewer than five digits)
    name is invale(empty, or malformed)
    if CMTE_ID  or  TRANSACTION_AMT fields are empty
    
other fields should not affect processing


FEC COLUMNS : https://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml
"""
import sys
from os.path import basename,splitext
import os
from datetime import datetime



header = ['CMTE_ID',\
          'AMNDT_IND',\
          'RPT_TP',\
          'TRANSACTION_PGI',\
          'IMAGE_NUM',\
          'TRANSACTION_TP',\
          'ENTITY_TP',\
          'NAME',\
          'CITY',\
          'STATE',\
          'ZIP_CODE',\
          'EMPLOYER',\
          'OCCUPATION',\
          'TRANSACTION_DT',\
          'TRANSACTION_AMT',\
          'OTHER_ID',\
          'TRAN_ID',\
          'FILE_NUM',\
          'MEMO_CD',\
          'MEMO_TEXT',\
          'SUB_ID']

keepcols = ['CMTE_ID','NAME','ZIP_CODE','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID']

def check_dt(val):          
    try:            
        return datetime.strptime(val,"%m%d%Y")
    except:
        return val
    
def check_zip(val):
    try:
        return val[:5]
    except:    
        return False           
    
def check_validity(val):
    if val == "":
        return False
    else:
        return val
    
def check_other_id(val):
    if val == "":
        return val
    else:
        return False
    
def check_amt(val):
    if val == "":
        return False
    else:
        try:                
            return float(val)
        except:
            return False
        
preprocess_map = {'TRANSACTION_DT':check_dt,
                  'ZIP_CODE':check_zip,
                  'NAME':check_validity,
                  'CMTE_ID':check_validity,
                  'OTHER_ID':check_other_id,
                  'TRANSACTION_AMT':check_amt}

class dataStream(object):
    def __init__(self,header,keepcols,preprocess_map):
        
        self.inputfiles = []        
        self.outputfiles = []
        for item in sys.argv:
            if "arg" in item:
                item = os.environ[item]                
                
            if "input" in item:                    
                self.inputfiles.append(item)
                    
            elif "output" in item:
#                toreplace = "insight_testsuite/temp/" 
#                if toreplace in item:
#                    print("replacing {} in outfolder".format(toreplace))
#                    item = item.replace(toreplace,'')
                    
                self.outputfile = item
                print("output file is {} ".format(self.outputfile))
                
        self.col_index = {col:header.index(col) for col in keepcols}
        self.preprocess_rules = preprocess_map
        self.import_stream_data()
        
    def import_stream_data(self):
        for file in self.inputfiles:
            with open(file,"r") as infile:
                name = splitext(basename(file))[0]
                print("setting attribute {} of read {}".format(name,file))
                setattr(self,name,infile.read())
        self.percentile = int(self.percentile)
                
        
                
    def preprocess(self,record):
        record = record.split("|")
        namedrow = {k: self.preprocess_rules[k](record[indx]) \
                    for k,indx \
                    in self.col_index.items()}
        
        test = [x for x in list(namedrow.values()) if x == False]
        if len(test) == 0:            
            return namedrow
        else:
            return False
        
    def stream(self):        
        try:
            os.remove(self.outputfile)
        except:
            pass 
        for row in self.itcont.split("\n"):            
            if row == "":
                return False        
            result = self.preprocess(row)
            if result:
                yield(result)
            else:
                pass
                
        
class donationAnalytics(dataStream):
    def __init__(self,header,keepcols,preprocess_map):
        """
        output file columns:
            CMTE_ID
            ZIP_CODE
            YEAR
            PERCENTILE
            Sum of repeat contributions in this zip code this year
            number of repeat contributions in this zip code this year
        """
        ds = dataStream(header, keepcols, preprocess_map)
        self.stream =  ds.stream()
        self.percentile = ds.percentile
        self.outputfile = ds.outputfile
        self.previous_donors = {}
        self.donations = {}
        self.outputrecords = []
    
    def ranked_percentile(self,donation_list):
        rank = (self.percentile/100 ) * len(donation_list)
        if rank < 1.5 and rank > 0:
            rank = 0
        else:
            rank = round(rank) - 1
            
        return donation_list[rank]
    
    def process_row(self,row):
        donor_key = (row['NAME'],row['ZIP_CODE'])
        year = str(row['TRANSACTION_DT'].year)
        donation_key = (row['CMTE_ID'], row['ZIP_CODE'],year)
        repeat_donor = self.previous_donors.get(donor_key,False)
        if repeat_donor :
            repeat_donation_list = self.donations.get(donation_key,False)            
            if repeat_donation_list:
                pass
            else:
                repeat_donation_list = []
                
            repeat_donation_list.append(row['TRANSACTION_AMT'])            
            
            result = {}
#            result['CMTE_ID'] = str(row['CMTE_ID'])
#            result['ZIP_CODE'] = row['ZIP_CODE']
#            result['YEAR'] = year
#            result['PERCENTILE'] = str(self.ranked_percentile(repeat_donation_list))
#            result['REPEAT_CONTRIBUTIONS_SUM'] = str(sum(repeat_donation_list)) 
#            result['REPEAT_CONTRIBUTIONS_COUNT'] = str(len(repeat_donation_list))
            #identifier
            result = (str(row['CMTE_ID']),\
                      #zipcode
                      row['ZIP_CODE'],\
                      # year 4-digit
                      year,\
                      # ranked percentile according to the input/percentile file
                      str(int(self.ranked_percentile(repeat_donation_list))),\
                      # sum of repeat donations per year per zipcode, streamed out
                      str(int(round(sum(repeat_donation_list)))),\
                      # count of repeat donations per year per zipcode, streamed out
                      str(int(len(repeat_donation_list))))
            
            self.donations.update({donation_key:repeat_donation_list})
            
            return result        
        else:
            self.previous_donors.update({donor_key:True})
            return False            
        
    def process_data(self):
        result = {}        
        for row in self.stream:
            result = self.process_row(row)
#            print(result)
            if result:
                with open(self.outputfile,'a') as out:                    
                    writeln = "|".join(result) + "\n"
                    print("writing line " + writeln)
                    out.write(writeln )
#                    out.write("|".join(list(result.values())) + "\n" )
                    
                    
if __name__ == "__main__":    
    check = donationAnalytics(header, keepcols, preprocess_map)
    check.process_data()






#
#for x in check.stream:
#    print(x)
#        
#round(1.4)
test = '/home/joe/repos/donation-analytics/insight_testsuite/temp/output/repeat_donors.txt'

check = test.replace("insight_testsuite/temp/","")