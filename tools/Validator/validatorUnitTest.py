"""
* File: validatorUnitTest.py
* Date: 11/18/2016
* Translation by: Daniel Zhou
* Original Author: Yooyoung Lee
* Status: Complete 

* Description: This object tests the functions of the unit test. 

* Requirements: This code requires the following packages:
    - cv2
    - numpy
    - pandas
    - unittest
  
  The rest should be available on your system.

* Inputs
    * -x, inIndex: index file name
    * -s, inSys: system output file name
    * -vt, valType: validator type: SSD or DSD
    * -v, verbose: Control printed output. -v 0 suppresss all printed output except argument parsng errors, -v 1 to print all output.

* Outputs
    * 0 if the files are validly formatted, 1 if the files are not.

* Disclaimer: 
This software was developed at the National Institute of Standards 
and Technology (NIST) by employees of the Federal Government in the
course of their official duties. Pursuant to Title 17 Section 105 
of the United States Code, this software is not subject to copyright 
protection and is in the public domain. NIST assumes no responsibility 
whatsoever for use by other parties of its source code or open source 
server, and makes no guarantees, expressed or implied, about its quality, 
reliability, or any other characteristic."
"""

import sys
import os
import cv2
import numpy as np
import pandas as pd
from abc import ABCMeta, abstractmethod
import unittest as ut
import contextlib
from validator import SSD_Validator,DSD_Validator

identify=False
NCID='NC2016'
neglectMask=False
procs = 1

identify_string = ''
if identify:
    identify_string = '-id '
nm_string = ''
if neglectMask:
    nm_string = '-nm '

validatorRoot = '../../data/test_suite/validatorTests/'

##want to take in a command and return the printed output to a string
#def print_capture(command):
#    #change stdout to another file
#    sys.stdout = open("validator.log","w")
#    val=exec(command)
#    mystr = 0
#    with open("validator.log","r") as myfile:
#        mystr = myfile.readlines()
#    mystr = "\n".join(mystr)    
#
#    #change back to stdout
#    sys.stdout = sys.__stdout__
#    return val,mystr

def msgcapture(fname):
    with open(fname,"r") as myfile:
        mystr = myfile.readlines()
        mystr = "\n".join(mystr)
        return mystr
    

class TestValidator(ut.TestCase):

    def testSSDName(self):
        import StringIO
        #This code taken from the following site: http://stackoverflow.com/questions/14197009/how-can-i-redirect-print-output-of-a-function-in-python
        @contextlib.contextmanager
        def stdout_redirect(where):
            sys.stdout = where
            try:
                yield where
            finally:
                sys.stdout = sys.__stdout__
        validatorRoot = '../../data/test_suite/validatorTests/'
        global verbose
        verbose = 1

        print("BASIC FUNCTIONALITY validation of SSD validator beginning...")
#        myval = SSD_Validator(validatorRoot + 'foo_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1/foo_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv')
#        self.assertEqual(myval.fullCheck(True,identify,NCID,neglectMask),0)
        myval = os.system("python2 validator.py -nc --ncid {} -vt SSD -s {} -x {} -p {} {}{}> vmb.log".format(NCID,validatorRoot + 'foo_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1/foo_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv',procs,identify_string,nm_string))//256 
        self.assertEqual(myval,0)
        os.system('rm vmb.log')

        #no namecheck case
        myval = os.system("python2 validator.py -vt SSD -s {} -x {} -p {} {}{}> vmb1.log".format(validatorRoot + 'foo/foo.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv',procs,identify_string,nm_string))//256
        self.assertEqual(myval,0)
        os.system('rm vmb1.log')

        #no mask
        myval = os.system("python2 validator.py -vt SSD -s {} -x {} -p {} {}{}> vmb2.log".format(validatorRoot + 'nomask/nomask.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv',procs,identify_string,nm_string))//256
        self.assertEqual(myval,0)
        os.system('rm vmb2.log')

        print("BASIC FUNCTIONALITY validated.")
        
        print("\nBeginning experiment ID naming error validations.")
        print("CASE S0: Validating behavior when files don't exist.")
        
#        myval = SSD_Validator(validatorRoot + 'emptydir_NC2016_UnitTest_Splice_ImgOnly_p-baseline_1/foo__NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index0.csv')
        myval = os.system("python2 validator.py -nc --ncid {} -vt SSD -s {} -x {} -p {} {}{}> vm0.log".format(NCID,validatorRoot + 'emptydir_NC2016_UnitTest_Splice_ImgOnly_p-baseline_1/foo__NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index0.csv',procs,identify_string,nm_string))//256 
        self.assertEqual(myval,1)
        errstr = msgcapture("vm0.log")
        
#        with stdout_redirect(StringIO.StringIO()) as errmsg:
#            result=myval.fullCheck(True,identify,NCID,neglectMask) 
#        errmsg.seek(0)
#        errstr,val = print_capture('myval.fullCheck(True,identify,NCID,neglectMask)')
#        self.assertEqual(val,1)
#        errstr = errmsg.read() #NOTE: len(errmsg.read())==0, but when you set it equal, you get the entire string. What gives?
        self.assertTrue("ERROR: Expected system output" in errstr)
#        errmsg.close()
        
        print("CASE S0 validated.")
        os.system('rm vm0.log')
        
        print("\nCASE S1: Validating behavior when detecting consecutive underscores ('_') in name...")
#        myval = SSD_Validator(validatorRoot + 'foo__NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1/foo__NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv')
        myval = os.system("python2 validator.py -nc --ncid {} -vt SSD -s {} -x {} -p {} {}{}> vm1.log".format(NCID,validatorRoot + 'foo__NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1/foo__NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vm1.log")
        
#        with stdout_redirect(StringIO.StringIO()) as errmsg:
#            result=myval.fullCheck(True,identify,NCID,neglectMask)
#        errmsg.seek(0)
#        errstr = errmsg.read()

#        errstr,val = print_capture('myval.fullCheck(True,identify,NCID,neglectMask)')
        self.assertEqual(myval,1)
        self.assertTrue("ERROR: Task" in errstr)
        self.assertTrue("unrecognized" in errstr)
        print("CASE S1 validated.")
        os.system('rm vm1.log')
        
        print("\nCASE S2: Validating behavior when detecting excessive underscores elsewhere...")
#        myval = SSD_Validator(validatorRoot + 'fo_o_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1/fo_o_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv')
        myval = os.system("python2 validator.py -nc --ncid {} -vt SSD -s {} -x {} -p {} {}{}> vm2.log".format(NCID,validatorRoot + 'fo_o_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1/fo_o_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vm2.log")
        
#        with stdout_redirect(StringIO.StringIO()) as errmsg:
#            result=myval.fullCheck(True,identify,NCID,neglectMask)
#        errmsg.seek(0)
#        errstr,val = print_capture('myval.fullCheck(True,identify,NCID,neglectMask)')
        self.assertEqual(myval,1)
#        errstr = errmsg.read()
        self.assertTrue("ERROR: Task" in errstr)
        self.assertTrue("unrecognized" in errstr)
        print("CASE S2 validated.")
        os.system('rm vm2.log')
        
#        print("\nCASE S3: Validating behavior when detecting '+' in file name and an unrecognized task...")
#        myval = SSD_Validator(validatorRoot + 'foo+_NC2016_UnitTest_Manip_ImgOnly_p-baseline_1/foo+_NC2016_UnitTest_Manip_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv')
#        
#        with stdout_redirect(StringIO.StringIO()) as errmsg:
#            result=myval.fullCheck(True,identify,NCID,neglectMask)
#        errmsg.seek(0)
#        self.assertEqual(result,1)
#        errstr = errmsg.read()
#        self.assertTrue("ERROR: The team name must not include characters" in errstr)
#        self.assertTrue("ERROR: What kind of task is" in errstr)
#        print("CASE S3 validated.")
 
    def testSSDContent(self):
        import StringIO
        @contextlib.contextmanager
        def stdout_redirect(where):
            sys.stdout = where
            try:
                yield where
            finally:
                sys.stdout = sys.__stdout__
        validatorRoot = '../../data/test_suite/validatorTests/'
        global verbose
        verbose = None
        print("Validating syntactic content of system output.\nCASE S4: Validating behavior for incorrect headers and different number of rows than in index file...")
        print("CASE S4a: Validating behavior for incorrect headers")
#        myval = SSD_Validator(validatorRoot + 'foo_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_2/foo_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_2.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv') 
        myval = os.system("python2 validator.py -nc --ncid {} -vt SSD -s {} -x {} -p {} {}{}> vm4a.log".format(NCID,validatorRoot + 'foo_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_2/foo_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_2.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vm4a.log")
#        with stdout_redirect(StringIO.StringIO()) as errmsg:
#            result=myval.fullCheck(True,identify,NCID,neglectMask)
#        errmsg.seek(0)
#        errstr,val = print_capture('myval.fullCheck(True,identify,NCID,neglectMask)')
#        errstr = errmsg.read()
        self.assertEqual(myval,1)
        self.assertTrue("ERROR: The required column" in errstr)
        os.system('rm vm4a.log')

        print("CASE S4b: Validating behavior for duplicate rows and different number of rows than in index file...")
#        myval = SSD_Validator(validatorRoot + 'foob_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_2/foob_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_2.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv')
        myval = os.system("python2 validator.py -nc --ncid {} -vt SSD -s {} -x {} -p {} {}{}> vm4b.log".format(NCID,validatorRoot + 'foob_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_2/foob_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_2.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vm4b.log")
#        with stdout_redirect(StringIO.StringIO()) as errmsg:
#            result=myval.fullCheck(True,identify,NCID,neglectMask)
#        errmsg.seek(0)
#        errstr,val = print_capture('myval.fullCheck(True,identify,NCID,neglectMask)')
#        errstr = errmsg.read()
        self.assertEqual(myval,1)
        self.assertTrue("ERROR: Your system output contains duplicate rows" in errstr)
        self.assertTrue("ERROR: The number of rows in your system output (6) does not match the number of rows in the index file (5)." in errstr)
        os.system('rm vm4b.log')

        #confidence score validation 
        print("CASE S4c: Validating behavior for improper confidence scores...")
#        myval = SSD_Validator(validatorRoot + 'foob_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_2/foob_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_2.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv')
        myval = os.system("python2 validator.py -nc --ncid {} -vt SSD -s {} -x {} -p {} {}{}> vm4c.log".format(NCID,validatorRoot + 'fooc_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1/fooc_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vm4c.log")
#        with stdout_redirect(StringIO.StringIO()) as errmsg:
#            result=myval.fullCheck(True,identify,NCID,neglectMask)
#        errmsg.seek(0)
#        errstr,val = print_capture('myval.fullCheck(True,identify,NCID,neglectMask)')
#        errstr = errmsg.read()
        self.assertEqual(myval,1)
        self.assertTrue("ERROR: The Confidence Scores for probes" in errstr)
        os.system('rm vm4c.log')

        print("CASE S4d: Validating behavior for improper OptOut...")
        myval = os.system("python2 validator.py -nc --ncid {} -vt SSD -s {} -x {} -p {} {}{}> vm4d.log".format(NCID,validatorRoot + 'food_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1/food_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vm4d.log")
        self.assertEqual(myval,1)
        self.assertTrue("Probe status" in errstr)
        self.assertTrue("is not recognized." in errstr)
        os.system('rm vm4d.log')

        print("CASE S4 validated.")
        
        print("\nCASE S5: Validating behavior when mask is not a png...")
#        myval = SSD_Validator(validatorRoot + 'bar_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1/bar_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv')
        myval = os.system("python2 validator.py -nc --ncid {} -vt SSD -s {} -x {} -p {} {}{}> vm5.log".format(NCID,validatorRoot + 'bar_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1/bar_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vm5.log")
        
#        with stdout_redirect(StringIO.StringIO()) as errmsg:
#            result=myval.fullCheck(True,identify,NCID,neglectMask)
#        errmsg.seek(0)
#        errstr,val = print_capture('myval.fullCheck(True,identify,NCID,neglectMask)')
#        errstr = errmsg.read()
        self.assertEqual(myval,1)
        self.assertTrue("is not a png." in errstr)
        print("CASE S5 validated.")
        os.system('rm vm5.log')
        
        print("\nCASE S6: Validating behavior when mask is not single channel and when mask does not have the same dimensions.")
#        myval = SSD_Validator(validatorRoot + 'baz_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1/baz_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv')
        myval = os.system("python2 validator.py -nc --ncid {} -vt SSD -s {} -x {} -p {} {}{}> vm6.log".format(NCID,validatorRoot + 'baz_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1/baz_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vm6.log")
        
#        with stdout_redirect(StringIO.StringIO()) as errmsg:
#            result=myval.fullCheck(True,identify,NCID,neglectMask)
#        errmsg.seek(0)
#        errstr,val = print_capture('myval.fullCheck(True,identify,NCID,neglectMask)')
#        errstr = errmsg.read()
        self.assertEqual(myval,1)
#        self.assertEqual(errstr.count("Dimensions"),2)
        self.assertTrue("ERROR: Expected dimensions" in errstr)
        self.assertTrue("is not single-channel." in errstr)
        print("CASE S6 validated.")
        os.system('rm vm6.log')

        print("\nCASE S6.1: Validating behavior when mask is not single channel and when mask does not have the same dimensions.")
        myval = os.system("python2 validator.py -nc --ncid {} -vt SSD -s {} -x {} --output_revised_system rewritten_output.csv -p {} {}{}> vm6_1.log".format(NCID,validatorRoot + 'baz_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1/baz_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vm6_1.log")
        
        self.assertEqual(myval,1)
        self.assertTrue("ERROR: Expected dimensions" in errstr)
        self.assertTrue("is not single-channel." in errstr)
        print("CASE S6.1 validated.")
        os.system('rm vm6_1.log')
        
        print("\nCASE S6.2: Validating behavior when mask is not single channel and when mask does not have the same dimensions.")
        myval = os.system("python2 validator.py --ncid {} -vt SSD -s {} -x {} -p {} {}{}> vm6_2.log".format(NCID,validatorRoot + 'baz_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1/rewritten_output.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vm6_2.log")
        
#        self.assertEqual(myval,1)
        self.assertTrue("ERROR: Expected dimensions" not in errstr)
#        self.assertTrue("is not single-channel." in errstr)
        print("CASE S6.2 validated.")
        os.system('rm vm6_2.log')
        
        print("\nCASE S7: Validating behavior when system output column number is less than 3.") 
#        myval = SSD_Validator(validatorRoot + 'foo_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_3/foo_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_3.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv')
        myval = os.system("python2 validator.py -nc --ncid {} -vt SSD -s {} -x {} -p {} {}{}> vm7.log".format(NCID,validatorRoot + 'foo_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_3/foo_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_3.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vm7.log")
        
#        with stdout_redirect(StringIO.StringIO()) as errmsg:
#            result=myval.fullCheck(True,identify,NCID,neglectMask)
#        errmsg.seek(0)
#        errstr,val = print_capture('myval.fullCheck(True,identify,NCID,neglectMask)')
#        errstr = errmsg.read()
        self.assertEqual(myval,1)
        self.assertTrue("ERROR: The number of columns of the system output file must be at least" in errstr)
        print("CASE S7 validated.")
        os.system('rm vm7.log')
        
        print("\nCASE S8: Validating behavior when mask file is not present.") 
#        myval = SSD_Validator(validatorRoot + 'foo_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_4/foo_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_4.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv')
        myval = os.system("python2 validator.py -nc --ncid {} -vt SSD -s {} -x {} -p {} {}{}> vm8.log".format(NCID,validatorRoot + 'foo_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_4/foo_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_4.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vm8.log")
        
#        with stdout_redirect(StringIO.StringIO()) as errmsg:
#            result=myval.fullCheck(True,identify,NCID,neglectMask)
#        errmsg.seek(0)
#        errstr,val = print_capture('myval.fullCheck(True,identify,NCID,neglectMask)')
#        errstr = errmsg.read()
        self.assertEqual(myval,1)
        self.assertTrue("Expected mask image" in errstr)
        self.assertTrue("Please check the name of the mask image" in errstr)
        
        print("CASE S8 validated.")
        os.system('rm vm8.log')

    def testSSDVideoContent(self):
        validatorRoot = '../../data/test_suite/validatorTests/'
        global verbose
        verbose = None
        ver='d1v1'
        versfx = ''
        if ver == 'd1v1':
            versfx = '_d1v1'
        print("BASIC FUNCTIONALITY validation of SSD video validator beginning...")
        myval = os.system("python2 validator.py --ncid {} -vt SSD-video -s {} -x {} -p {} {}{}> vvb.log".format(NCID,
                                                                                                                validatorRoot + 'validvidtest/validvidtest.csv',
                                                                                                                validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-video-index{}.csv'.format(versfx),
                                                                                                                procs,
                                                                                                                identify_string,
                                                                                                                nm_string))//256
        self.assertEqual(myval,0)
        os.system('rm vvb.log')

        myval = os.system("python2 validator.py --ncid {} -vt SSD-video -s {} -x {} -p {} {}{}> vvb2.log".format(NCID,
                                                                                                                validatorRoot + 'validvidtest_nc17/validvidtest_nc17.csv',
                                                                                                                validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-video-index{}.csv'.format(versfx),
                                                                                                                procs,
                                                                                                                identify_string,
                                                                                                                nm_string))//256
        self.assertEqual(myval,0)
        os.system('rm vvb2.log')
        print("BASIC FUNCTIONALITY validated.")
        
        print("\nBeginning system output content validation for video.")
        print("\nCASE V0: Validating improper intervals for video.")
        myval = os.system("python2 validator.py --ncid {} -vt SSD-video -s {} -x {} -p {} {}{}> vv0.log".format(NCID,
                                                                                                                validatorRoot + 'badstringvidtest/badstringvidtest.csv',
                                                                                                                validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-video-index{}.csv'.format(versfx),
                                                                                                                procs,
                                                                                                                identify_string,
                                                                                                                nm_string))//256
        self.assertEqual(myval,1)
        errstr = msgcapture('vv0.log')
        self.assertTrue("ERROR: Interval list" in errstr)
        self.assertTrue("cannot be read as intervals" in errstr)

        print("CASE V0 validated.")
        os.system('rm vv0.log')
        
        print("\nCASE V1: Validating intervals that are out of bounds.")
        myval = os.system("python2 validator.py --ncid {} -vt SSD-video -s {} -x {} -p {} {}{}> vv1.log".format(NCID,
                                                                                                                validatorRoot + 'oobvidtest/oobvidtest.csv',
                                                                                                                validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-video-index{}.csv'.format(versfx),
                                                                                                                procs,
                                                                                                                identify_string,
                                                                                                                nm_string))//256
        self.assertEqual(myval,1)
        errstr = msgcapture('vv1.log')
        self.assertTrue("ERROR: Interval" in errstr)
        self.assertTrue("is out of bounds." in errstr)
        print("CASE V1 validated.")
        os.system('rm vv1.log')
        
        print("\nCASE V2: Validating collections of intervals that intersect.")
        myval = os.system("python2 validator.py --ncid {} -vt SSD-video -s {} -x {} -p {} {}{}> vv2.log".format(NCID,
                                                                                                                validatorRoot + 'selfcrossvidtest/selfcrossvidtest.csv',
                                                                                                                validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-video-index{}.csv'.format(versfx),
                                                                                                                procs,
                                                                                                                identify_string,
                                                                                                                nm_string))//256
        self.assertEqual(myval,1)
        errstr = msgcapture('vv2.log')
        self.assertTrue("ERROR: Interval" in errstr)
        self.assertTrue("intersects with" in errstr)
        print("CASE V2 validated.")
        os.system('rm vv2.log')

        print("\nCASE V3: Validating collections of intervals that intersect. Checking behavior for a FailValidation column.")
        myval = os.system("python2 validator.py --ncid {} -vt SSD-video -s {} -x {} -p {} {}{}> vv3.log".format(NCID,
                                                                                                                validatorRoot + 'failvalidvidtest/failvalidvidtest.csv',
                                                                                                                validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-video-index{}.csv'.format(versfx),
                                                                                                                procs,
                                                                                                                identify_string,
                                                                                                                nm_string))//256
        self.assertEqual(myval,0)
        errstr = msgcapture('vv3.log')
        print("CASE V3 validated.")
        os.system('rm vv3.log')

        print("\nCASE V4: Validating intervals that are out of bounds, but can be excused by ignoring EOF.")
        myval = os.system("python2 validator.py --ncid {} -vt SSD-video -s {} -x {} --ignore_eof -p {} {}{}> vv4.log".format(NCID,
                                                                                                                validatorRoot + 'oobvidtest/oobvidtest.csv',
                                                                                                                validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-manipulation-video-index{}.csv'.format(versfx),
                                                                                                                procs,
                                                                                                                identify_string,
                                                                                                                nm_string))//256
        self.assertEqual(myval,0)
        errstr = msgcapture('vv4.log')
        self.assertTrue("Warning: Interval" in errstr)
        self.assertTrue("is out of bounds." in errstr)
        print("CASE V4 validated.")
        os.system('rm vv4.log')

    def testEventVerification(self):
        validatorRoot = '../../data/test_suite/validatorTests/'
        print("BASIC FUNCTIONALITY validation of SSD-event validator beginning...")
        logname = 'vev.log'
        myval = os.system("python2 validator.py --ncid {} -vt SSD-event -s {} -x {} -p {} {}{}> {}".format('ValTest',
                                                                                                                validatorRoot + 'valid_ev/valid_ev.csv',
                                                                                                                validatorRoot + 'evref/indexes/ValTest-eventverification-index.csv',
                                                                                                                procs,
                                                                                                                identify_string,
                                                                                                                nm_string,
                                                                                                                logname))//256
        self.assertEqual(myval,0)
        os.system('rm {}'.format(logname))
        print("BASIC FUNCTIONALITY validated.")
        
        print("\nBeginning system output content validation for event verification.")
        print("\nCASE EV0: Validating incorrect event for probe.")
        logname = 'vev0.log'
        myval = os.system("python2 validator.py --ncid {} -vt SSD-event -s {} -x {} -p {} {}{}> {}".format('ValTest',
                                                                                                                validatorRoot + 'invalid_ev_event/invalid_ev_event.csv',
                                                                                                                validatorRoot + 'evref/indexes/ValTest-eventverification-index.csv',
                                                                                                                procs,
                                                                                                                identify_string,
                                                                                                                nm_string,
                                                                                                                logname))//256
        self.assertEqual(myval,1)
        errstr = msgcapture(logname)
        self.assertTrue("ERROR:" in errstr)
        self.assertTrue("does not exist in the index file" in errstr)
        os.system('rm {}'.format(logname))
        print("CASE EV0 validated.")

        print("\nCASE EV1: Validating incorrect ProbeStatus....")
        logname = 'vev1.log'
        myval = os.system("python2 validator.py --ncid {} -vt SSD-event -s {} -x {} -p {} {}{}> {}".format('ValTest',
                                                                                                                validatorRoot + 'invalid_ev_ps/invalid_ev_ps.csv',
                                                                                                                validatorRoot + 'evref/indexes/ValTest-eventverification-index.csv',
                                                                                                                procs,
                                                                                                                identify_string,
                                                                                                                nm_string,
                                                                                                                logname))//256
        self.assertEqual(myval,1)
        errstr = msgcapture(logname)
        self.assertTrue("ERROR: Probe status" in errstr)
        self.assertTrue("is not recognized" in errstr)
        os.system('rm {}'.format(logname))
        print("CASE EV1 validated.")

    def testCamera(self):
        print("BASIC FUNCTIONALITY validation of SSD-event validator beginning...")
        logname = 'vc.log'
        myval = os.system("python2 validator.py --ncid {} -vt SSD-camera -s {} -x {} -p {} {}{}> {}".format('MFC18',
                                                                                                                validatorRoot + 'valid_cam/valid_cam.csv',
                                                                                                                validatorRoot + 'cref/indexes/MFC18-camera-index.csv',
                                                                                                                procs,
                                                                                                                identify_string,
                                                                                                                nm_string,
                                                                                                                logname))//256
        self.assertEqual(myval,0)
        os.system('rm {}'.format(logname))
        print("BASIC FUNCTIONALITY validated.")
        print("\nBeginning system output content validation for camera.")
        print("\nCASE C0: Validating incorrect TrainCamID.")
        logname = 'vc0.log'
        myval = os.system("python2 validator.py --ncid {} -vt SSD-camera -s {} -x {} -p {} {}{}> {}".format('MFC18',
                                                                                                                validatorRoot + 'invalid_camid/invalid_camid.csv',
                                                                                                                validatorRoot + 'cref/indexes/MFC18-camera-index.csv',
                                                                                                                procs,
                                                                                                                identify_string,
                                                                                                                nm_string,
                                                                                                                logname))//256
        self.assertEqual(myval,1)
        errstr = msgcapture(logname)
        self.assertTrue("ERROR: Expected" in errstr)
        self.assertTrue("in system file. Only found in index file." in errstr)
        os.system('rm {}'.format(logname))
        print("CASE C0 validated.")
        
        print("\nCASE C1: Validating incorrect mask dimensions.")
        logname = 'vc1.log'
        myval = os.system("python2 validator.py --ncid {} -vt SSD-camera -s {} -x {} --output_revised_system revised_cam.csv -p {} {}{}> {}".format('MFC18',
                                                                                                                validatorRoot + 'invalid_cam_mask/invalid_cam_mask.csv',
                                                                                                                validatorRoot + 'cref/indexes/MFC18-camera-index.csv',
                                                                                                                procs,
                                                                                                                identify_string,
                                                                                                                nm_string,
                                                                                                                logname))//256
        self.assertEqual(myval,1)
        errstr = msgcapture(logname)
        self.assertTrue("ERROR: Expected dimensions" in errstr)
        os.system('rm {}'.format(logname))
        print("CASE C1 validated.")
        
        print("\nCASE C2: Validating incorrect mask dimensions for a Failed Validation.")
        logname = 'vc2.log'
        myval = os.system("python2 validator.py --ncid {} -vt SSD-camera -s {} -x {} -p {} {}{}> {}".format('MFC18',
                                                                                                                validatorRoot + 'invalid_cam_mask/revised_cam.csv',
                                                                                                                validatorRoot + 'cref/indexes/MFC18-camera-index.csv',
                                                                                                                procs,
                                                                                                                identify_string,
                                                                                                                nm_string,
                                                                                                                logname))//256
#        self.assertEqual(myval,1)
        errstr = msgcapture(logname)
        self.assertTrue("Warning: Probe" in errstr)
        self.assertTrue("has failed validation due to incorrect mask dimensions, but is excused in this system output." in errstr)
        os.system('rm {}'.format(logname))
        print("CASE C2 validated.")
        
    def testDSDName(self):
        import StringIO
        @contextlib.contextmanager
        def stdout_redirect(where):
            sys.stdout = where
            try:
                yield where
            finally:
                sys.stdout = sys.__stdout__
        validatorRoot = '../../data/test_suite/validatorTests/'
        global verbose
        verbose = None
        
        print("BASIC FUNCTIONALITY validation of DSD validator beginning...")
        myval = os.system("python2 validator.py -nc --ncid {} -vt DSD -s {} -x {} -p {} {}{}> vsb.log".format(NCID,validatorRoot + 'lorem_NC2016_UnitTest_Splice_ImgOnly_p-baseline_1/lorem_NC2016_UnitTest_Splice_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv',procs,identify_string,nm_string))//256 
#        myval = DSD_Validator(validatorRoot + 'lorem_NC2016_UnitTest_Splice_ImgOnly_p-baseline_1/lorem_NC2016_UnitTest_Splice_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv')
#        self.assertEqual(myval.fullCheck(True,identify,NCID,neglectMask,validatorRoot + 'NC2016_Test0516_dfz/reference/splice/NC2016-splice-ref.csv'),0)
        self.assertEqual(myval,0)
        os.system('rm vsb.log')

        #add validation for namecheck
        myval = os.system("python2 validator.py -vt DSD -s {} -x {} -p {} {}{}> vsb1.log".format(validatorRoot + 'lorem/lorem.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv',procs,identify_string,nm_string))//256 
        self.assertEqual(myval,0)
        os.system('rm vsb1.log')
        print("BASIC FUNCTIONALITY validated.")
        
        errmsg = ""
        #Same checks as Validate SSD, but applied to different files
        print("\nBeginning experiment ID naming error validations.")
        print("\nCASE D0: Validating behavior when files don't exist.") 
#        myval = DSD_Validator(validatorRoot + 'emptydir_NC2016_UnitTest_Splice_ImgOnly_p-baseline_1/emptydir_NC2016_UnitTest_Splice_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index0.csv')
        myval = os.system("python2 validator.py -nc --ncid {} -vt DSD -s {} -x {} -p {} {}{}> vs0.log".format(NCID,validatorRoot + 'emptydir_NC2016_UnitTest_Splice_ImgOnly_p-baseline_1/emptydir_NC2016_UnitTest_Splice_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index0.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vs0.log")
#        with stdout_redirect(StringIO.StringIO()) as errmsg:
#            result=myval.fullCheck(True,identify,NCID,neglectMask)
#        errmsg.seek(0)
#        errstr = errmsg.read()
#        errstr,val = print_capture('myval.fullCheck(True,identify,NCID,neglectMask)')
        self.assertEqual(myval,1)
        self.assertTrue("ERROR: Expected system output" in errstr)
        self.assertTrue("ERROR: Expected index file" in errstr)
        print("CASE D0 validated.")
        os.system('rm vs0.log')
        
        print("\nCASE D1: Validating behavior when detecting consecutive underscores ('_') in name...")
#        myval = DSD_Validator(validatorRoot + 'lorem__NC2016_UnitTest_Spl_ImgOnly_p-baseline_1/lorem__NC2016_UnitTest_Spl_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv')
        myval = os.system("python2 validator.py -nc --ncid {} -vt DSD -s {} -x {} -p {} {}{}> vs1.log".format(NCID,validatorRoot + 'lorem__NC2016_UnitTest_Spl_ImgOnly_p-baseline_1/lorem__NC2016_UnitTest_Spl_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vs1.log")
#        with stdout_redirect(StringIO.StringIO()) as errmsg:
#            result=myval.fullCheck(True,identify,NCID,neglectMask)
#        errmsg.seek(0)
#        errstr = errmsg.read()
#        errstr,val = print_capture('myval.fullCheck(True,identify,NCID,neglectMask)')
        self.assertEqual(myval,1)
        self.assertTrue("ERROR: Task" in errstr)
        self.assertTrue("is unrecognized. The task must be \'splice\'." in errstr)
        print("CASE D1 validated.")
        os.system('rm vs1.log')
        
        print("\nCASE D2: Validating behavior when detecting excessive underscores elsewhere...")
#        myval = DSD_Validator(validatorRoot + 'lor_em_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1/lor_em_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv')
        myval = os.system("python2 validator.py -nc --ncid {} -vt DSD -s {} -x {} -p {} {}{}> vs2.log".format(NCID,validatorRoot + 'lor_em_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1/lor_em_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vs2.log")
#        with stdout_redirect(StringIO.StringIO()) as errmsg:
#            result=myval.fullCheck(True,identify,NCID,neglectMask)
#        errmsg.seek(0)
#        errstr = errmsg.read()
#        errstr,val = print_capture('myval.fullCheck(True,identify,NCID,neglectMask)')
        self.assertEqual(myval,1)
        self.assertTrue("ERROR: Task" in errstr)
        self.assertTrue("is unrecognized. The task must be \'splice\'." in errstr)
        print("CASE D2 validated.")
        os.system('rm vs2.log')
        
#        print("\nCASE D3: Validating behavior when detecting '+' in file name and an unrecogized task...\n")
#        myval = DSD_Validator(validatorRoot + 'lorem+_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1/lorem+_NC2016_UnitTest_Manipulation_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv')
#        with stdout_redirect(StringIO.StringIO()) as errmsg:
#            result=myval.fullCheck(True,identify,NCID,neglectMask)
#        errmsg.seek(0)
#        self.assertEqual(result,1)
#        errstr = errmsg.read()
#        self.assertTrue("ERROR: The team name must not include characters" in errstr)
#        self.assertTrue("ERROR: What kind of task is" in errstr)
#        print("CASE D3 validated.")
     
    def testDSDContent(self):
        import StringIO
        @contextlib.contextmanager
        def stdout_redirect(where):
            sys.stdout = where
            try:
                yield where
            finally:
                sys.stdout = sys.__stdout__
        validatorRoot = '../../data/test_suite/validatorTests/'
        global verbose
        verbose = None
        print("Validating syntactic content of system output.\nCASE D4: Validating behavior for incorrect headers, duplicate rows, and different number of rows than in index file...")
        print("CASE D4a: Validating behavior for incorrect headers, duplicate rows, and different number of rows than in index file...")
 #       self.assertEqual(myval,0)
#        myval = DSD_Validator(validatorRoot + 'lorem_NC2016_UnitTest_Splice_ImgOnly_p-baseline_2/lorem_NC2016_UnitTest_Splice_ImgOnly_p-baseline_2.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv')
        myval = os.system("python2 validator.py -nc --ncid {} -vt DSD -s {} -x {} -p {} {}{}> vs4a.log".format(NCID,validatorRoot + 'lorem_NC2016_UnitTest_Splice_ImgOnly_p-baseline_2/lorem_NC2016_UnitTest_Splice_ImgOnly_p-baseline_2.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vs4a.log")
#        with stdout_redirect(StringIO.StringIO()) as errmsg:
#            result=myval.fullCheck(True,identify,NCID,neglectMask)
#        errmsg.seek(0)
#        errstr = errmsg.read()
#        errstr,val = print_capture('myval.fullCheck(True,identify,NCID,neglectMask)')
        self.assertEqual(myval,1)
        self.assertTrue("ERROR: The required column" in errstr)
        os.system('rm vs4a.log')

        print("CASE D4b: Validating behavior for duplicate rows and different number of rows than in index file...")
#        myval = DSD_Validator(validatorRoot + 'loremb_NC2016_UnitTest_Splice_ImgOnly_p-baseline_2/loremb_NC2016_UnitTest_Splice_ImgOnly_p-baseline_2.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv')
        myval = os.system("python2 validator.py -nc --ncid {} -vt DSD -s {} -x {} -p {} {}{}> vs4b.log".format(NCID,validatorRoot + 'loremb_NC2016_UnitTest_Splice_ImgOnly_p-baseline_2/loremb_NC2016_UnitTest_Splice_ImgOnly_p-baseline_2.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vs4b.log")
#        with stdout_redirect(StringIO.StringIO()) as errmsg:
#            result=myval.fullCheck(True,identify,NCID,neglectMask)
#        errmsg.seek(0)
#        errstr = errmsg.read()
#        errstr,val = print_capture('myval.fullCheck(True,identify,NCID,neglectMask)')
        self.assertEqual(myval,1)
#        self.assertTrue("ERROR: Row" in errstr) #TODO: temporary measure until we get duplicates back
        self.assertTrue("ERROR: The number of rows in your system output (6) does not match the number of rows in the index file (5)." in errstr)
        os.system('rm vs4b.log')

        #confidence score validation
        print("CASE D4c: Validating behavior for improper confidence scores...")
#        myval = DSD_Validator(validatorRoot + 'loremb_NC2016_UnitTest_Splice_ImgOnly_p-baseline_2/loremb_NC2016_UnitTest_Splice_ImgOnly_p-baseline_2.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv')
        myval = os.system("python2 validator.py -nc --ncid {} -vt DSD -s {} -x {} -p {} {}{}> vs4c.log".format(NCID,validatorRoot + 'loremc_NC2016_UnitTest_Splice_ImgOnly_p-baseline_1/loremc_NC2016_UnitTest_Splice_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vs4c.log")
#        with stdout_redirect(StringIO.StringIO()) as errmsg:
#            result=myval.fullCheck(True,identify,NCID,neglectMask)
#        errmsg.seek(0)
#        errstr = errmsg.read()
#        errstr,val = print_capture('myval.fullCheck(True,identify,NCID,neglectMask)')
        self.assertEqual(myval,1)
#        self.assertTrue("ERROR: Row" in errstr) #TODO: temporary measure until we get duplicates back
        self.assertTrue("ERROR: The Confidence Score for probe-donor pair" in errstr)
        os.system('rm vs4c.log')

        print("CASE D4d: Validating behavior for inappropriate ProbeStatus and DonorStatus values...")
        myval = os.system("python2 validator.py -nc --ncid {} -vt DSD -s {} -x {} -p {} {}{}> vs4d.log".format(NCID,validatorRoot + 'loremd_NC2016_UnitTest_Splice_ImgOnly_p-baseline_1/loremd_NC2016_UnitTest_Splice_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vs4d.log")
        self.assertEqual(myval,1)
        self.assertTrue("Probe status" in errstr)
        self.assertTrue("Donor status" in errstr)
        self.assertTrue("is not recognized" in errstr)
        os.system('rm vs4d.log')

        print("CASE D4 validated.")
        
#        print("\nCase 5: Validating behavior when the number of columns in the system output is less than 6.")
#        myval = DSD_Validator(validatorRoot + 'lorem_NC2016_UnitTest_Splice_ImgOnly_p-baseline_4/lorem_NC2016_UnitTest_Splice_ImgOnly_p-baseline_4.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv')
#        with stdout_redirect(StringIO.StringIO()) as errmsg:
#            result=myval.fullCheck(True,identify,NCID,neglectMask)
#        errmsg.seek(0)
#        self.assertEqual(result,1)
#        errstr = errmsg.read()
#        self.assertTrue("ERROR: The number of columns of the system output file must be at least" in errstr)
#        print("CASE D5 validated.")
        
        print("\nCASE D6: Validating behavior for mask semantic deviations. NC2016-1893.jpg and NC2016_6847-mask.jpg are (marked as) jpg's. NC2016_1993-mask.png is not single-channel. NC2016_4281-mask.png doesn't have the same dimensions...")
#        myval = DSD_Validator(validatorRoot + 'ipsum_NC2016_UnitTest_Splice_ImgOnly_p-baseline_1/ipsum_NC2016_UnitTest_Splice_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv')
        myval = os.system("python2 validator.py -nc --ncid {} -vt DSD -s {} -x {} -p {} {}{}> vs6.log".format(NCID,validatorRoot + 'ipsum_NC2016_UnitTest_Splice_ImgOnly_p-baseline_1/ipsum_NC2016_UnitTest_Splice_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vs6.log")
#        with stdout_redirect(StringIO.StringIO()) as errmsg:
#            result=myval.fullCheck(True,identify,NCID,neglectMask)
#        errmsg.seek(0)
#        errstr = errmsg.read()
#        errstr,val = print_capture('myval.fullCheck(True,identify,NCID,neglectMask)')
        self.assertEqual(myval,1)
        self.assertTrue("is not a png." in errstr)
#        idx=0
#        count=0
#        while idx < len(errstr):
#            idx = errstr.find("Dimensions",idx)
#            if idx == -1:
#                self.assertEqual(count,2)
#                break
#            else:
#                count += 1
#                idx += len("Dimensions")
        self.assertTrue("ERROR: Expected dimensions" in errstr)
        self.assertTrue("is not single-channel." in errstr)
        self.assertTrue("is not a png." in errstr)
        os.system('rm vs6.log')
        print("CASE D6 validated.")

        #add case for output
        print("\nCASE D6.1: Validating behavior for mask semantic deviations. NC2016-1893.jpg and NC2016_6847-mask.jpg are (marked as) jpg's. NC2016_1993-mask.png is not single-channel. NC2016_4281-mask.png doesn't have the same dimensions...")
        myval = os.system("python2 validator.py -nc --ncid {} -vt DSD -s {} -x {} --output_revised_system revised_splice.csv -p {} {}{}> vs6_1.log".format(NCID,validatorRoot + 'ipsum_NC2016_UnitTest_Splice_ImgOnly_p-baseline_1/ipsum_NC2016_UnitTest_Splice_ImgOnly_p-baseline_1.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vs6_1.log")
        self.assertEqual(myval,1)
        self.assertTrue("is not a png." in errstr)

        self.assertTrue("ERROR: Expected dimensions" in errstr)
        self.assertTrue("is not single-channel." in errstr)
        self.assertTrue("is not a png." in errstr)
        os.system('rm vs6_1.log')
        print("CASE D6.1 validated.")

        #then repeat the run again with the revised output 
        print("\nCASE D6.2: Validating behavior for mask semantic deviations. NC2016-1893.jpg and NC2016_6847-mask.jpg are (marked as) jpg's. NC2016_1993-mask.png is not single-channel. NC2016_4281-mask.png doesn't have the same dimensions...")
        myval = os.system("python2 validator.py --ncid {} -vt DSD -s {} -x {} -p {} {}{}> vs6_2.log".format(NCID,validatorRoot + 'ipsum_NC2016_UnitTest_Splice_ImgOnly_p-baseline_1/revised_splice.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vs6_2.log")
        self.assertEqual(myval,1)
        self.assertTrue("is not a png." in errstr)

        self.assertTrue("ERROR: Expected dimensions" not in errstr)
        self.assertTrue("is not single-channel." in errstr)
        self.assertTrue("is not a png." in errstr)
        os.system('rm vs6_2.log')
        print("CASE D6.2 validated.")

        print("\nCASE D7: Validating behavior when at least one mask file is not empty and not present...") 
#        myval = DSD_Validator(validatorRoot + 'lorem_NC2016_UnitTest_Splice_ImgOnly_p-baseline_3/lorem_NC2016_UnitTest_Splice_ImgOnly_p-baseline_3.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv')
        myval = os.system("python2 validator.py -nc --ncid {} -vt DSD -s {} -x {} -p {} {}{}> vs7.log".format(NCID,validatorRoot + 'lorem_NC2016_UnitTest_Splice_ImgOnly_p-baseline_3/lorem_NC2016_UnitTest_Splice_ImgOnly_p-baseline_3.csv',validatorRoot + 'NC2016_Test0516_dfz/indexes/NC2016-splice-index.csv',procs,identify_string,nm_string))//256 
        errstr = msgcapture("vs7.log")
#        with stdout_redirect(StringIO.StringIO()) as errmsg:
#            result=myval.fullCheck(True,identify,NCID,neglectMask)
#        errmsg.seek(0)
#        errstr = errmsg.read()
#        errstr,val = print_capture('myval.fullCheck(True,identify,NCID,neglectMask)')
        self.assertEqual(myval,1)
        idx=0
        count=0
        while idx < len(errstr):
            idx = errstr.find("Expected mask image",idx)
            if idx == -1:
                self.assertEqual(count,3)
                break
            else:
                count += 1
                idx += len("Expected mask image")
        os.system('rm vs7.log')
        print("CASE D7 validated.")
        
