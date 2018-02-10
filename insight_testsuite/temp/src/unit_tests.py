# -*- coding: utf-8 -*-
import unittest
from run import check_dt, check_zip, check_validity, check_other_id, check_amt, DataStream, DonationAnalytics, keepcols, preprocess_map
from datetime import datetime
import os


input_data = [('123','BOB SMITH','50512-1234','01012017','1',''),\
        ('123','JERRY PICKER','50512-1235','01012017','500',''),\
        ('123','BOB SMITH','50512-1234','01012018','2','')]                
        
test_data = {check_dt:('02192019',datetime(2019,2,19,0,0)),\
                         check_dt:('021920191',False),\
                         check_zip:("123456","12345"),\
                         check_validity:("",False),\
                         check_other_id:("",True),\
                         check_amt:("335",335.0)}

data_file = "itcont.txt"
percentile_file = "percentile.txt"
output_file = "duplicate_donors.txt"
inputroot = "../input/unit_test/"
outputroot = "../output/unit_test/"        




def set_up(fnd,fnp,output_file, inputroot,outputroot ):    
    os.makedirs(inputroot, exist_ok = True)    
    os.makedirs(outputroot, exist_ok = True)
    fnd = inputroot + fnd
    fnp = inputroot + fnp
    output_file = outputroot + output_file
    
    with open(fnd ,"w") as f:
        #['CMTE_ID', 'NAME', 'ZIP_CODE', 'TRANSACTION_DT', 'TRANSACTION_AMT', 'OTHER_ID']
        
        out = "\n".join(["|".join(x) for x in input_data])
        f.write(out)
    
    with open(fnp,"w") as f:
        data = "30\n"
        f.write(data)
        
        
    datafile = os.path.abspath(fnd)
    percentilefile = os.path.abspath(fnp)
    outputfile = os.path.abspath(output_file)    
    return datafile, percentilefile, outputfile

def tear_down(files,inputroot,outputroot ):
    for file in files:
        os.remove(file)
    os.rmdir(inputroot)
    os.rmdir(outputroot)
        

class TestFunctions(unittest.TestCase):    
    def testFunctions(self):
        for func, data in test_data.items():
            testdata = data[0]
            testcompare = data[1]            
            result = func(testdata)
#            print("comparing {} to {} for func {}".format(result,testcompare, func))
            self.assertEqual(result,testcompare)
            self.assertEqual(type(result),type(testcompare))
                    
    def testDonationAnalytics(self): 
        """
        This could probably be broken down here, but the manual engineering
        of the test data and calculation of the output means that this test
        validates every piece of the class
        """


        files = set_up(data_file,percentile_file,output_file, inputroot,outputroot)        
        
        self.ds = DonationAnalytics(keepcols, keepcols, preprocess_map, files)
        results = self.ds.process_data()
        self.assertEqual(results,['123|50512|2018|2|2|1\n'])        
        
        tear_down(files,inputroot,outputroot)        
    
if __name__ == '__main__':
    unittest.main()
