"""
* Date: 10/20/2016
* Authors: Yooyoung Lee and Timothee Kheyrkhah

* Description: this code calculates performance measures (for points, AUC, and EER)
on system outputs (confidence scores) and return report plot(s) and table(s).

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

import argparse
import numpy as np
import pandas as pd
import os # os.system("pause") for windows command line
import sys

from matplotlib.pyplot import cm
from collections import OrderedDict
from itertools import cycle

lib_path = "../../lib"
sys.path.append(lib_path)
import Render as p
import detMetrics as dm
import Partition as f
#import time


########### Command line interface ########################################################

if __name__ == '__main__':

    # Boolean for disabling the command line
    debug_mode_ide = False

    # Command-line mode
    if not debug_mode_ide:

        def is_file_specified(x):
            if x == '':
                raise argparse.ArgumentTypeError("{0} not provided".format(x))
            return x
            
        def restricted_float(x):
            x = float(x)
            if x < 0.0 or x > 1.0:
                raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
            return x
        
        parser = argparse.ArgumentParser(description='NIST detection scorer.')

        #Task Type Options
        parser.add_argument('-t','--task', default='manipulation', 
                            choices=['manipulation','splice'], # add provenanceFiltering and provenance in future
                            help='Define the target manipulation task type for evaluation:[manipulation] and [splice] (default: %(default)s)',metavar='character')
        
        #Input Options
        parser.add_argument('--refDir', default='.',
                            help='Specify the reference and index data path: [e.g., ../NC2016_Test] (default: %(default)s)', metavar='character')
                            #type=lambda x: is_dir(parser, x))#Optional

        parser.add_argument('-r','--inRef', default='', type=is_file_specified,
                            help='Specify the reference CSV file (under the refDir folder) that contains the ground-truth and metadata information: [e.g., reference/manipulation/reference.csv]', metavar='character') 
                            #type=lambda x: is_file(parser, x))# Mandatory     

        parser.add_argument('-x','--inIndex',default='', type=is_file_specified,
                            help='Specify the index CSV file: [e.g., indexes/index.csv] (default: %(default)s)',metavar='character')

        parser.add_argument('--sysDir',default='.',
                            help='Specify the system output data path: [e.g., /mySysOutputs] (default: %(default)s)',metavar='character') #Optional

        parser.add_argument('-s','--inSys',default='', type=is_file_specified,
                            help='Specify the CSV file of the system performance result formatted according to the specification: [e.g., ~/expid/system_output.csv] (default: %(default)s)',metavar='character')    

        # Metric Options
        parser.add_argument('--farStop',type=restricted_float, default = 1,
                            help="Specify the stop point of FAR for calculating partial AUC, range [0,1] (default: %(default) for full AUC)",metavar='float')
        
        parser.add_argument('--ci', action='store_true',
                            help="Calculate the lower and upper confidence interval for AUC if this option is specified. The option will slowdown the speed due to the bootstrapping method.")

        # Output Options
        parser.add_argument('--outRoot',default='.',
                            help='Specify the report output path and the file name prefix for saving the plot(s) and table (s). For example, if you specify "--outRoot test/NIST_001", you will find the plot "NIST_001_det.png" and the table "NIST_001_report.csv" in the "test" folder: [e.g., temp/xx_sys] (default: %(default)s)',metavar='character')

        parser.add_argument('--dump', action='store_true',
                            help="Save the dump files (formatted as a binary) that contains a list of FAR, FPR, TPR, threshold, AUC, and EER values. The purpose of the dump files is to load the point values for further analysis without calculating the values again.")
        
        parser.add_argument('-v', '--verbose', action='store_true',
                            help="Print output with procedure messages on the command-line if this option is specified.")
        
        # Plot Options
        parser.add_argument('--plotType',default='roc', choices=['roc', 'det'],
                            help="Define the plot type:[roc] and [det] (default: %(default)s)", metavar='character')
    
        parser.add_argument('--display', action='store_true',
                            help="Display a window with the plot (s) on the command-line if this option is specified.")
        
        parser.add_argument('--multiFigs', action='store_true',
                            help="Generate plots (with only one curve) per a partition ")
        # Custom Plot Options
        parser.add_argument('--configPlot', action='store_true',
                            help="Open a JSON file that allows the user to customize the plot (e.g. change the title font size) by augmenting the json files located in the 'plotJsonFiles' folder.")

        # Performance Evaluation by Query Options
        factor_group = parser.add_mutually_exclusive_group()

        factor_group.add_argument('-q', '--query', nargs='*',
                                  help="Evaluate algorithm performance on a partitioned dataset (or subset) using multiple queries. Depending on the number (N) of queries, the option generates N report tables (CSV) and one plot (PDF) that contains N curves.", metavar='character')

        factor_group.add_argument('-qp', '--queryPartition',
                                  help="Evaluate algorithm performance on a partitioned dataset (or subset) using one query. Depending on the number (M) of partitions provided by the cartesian product on query conditions, this option generates a single report table (CSV) that contains M partition results and one plot that contains M curves. (syntax retriction: '==[]','<','<=')", metavar='character')

        factor_group.add_argument('-qm', '--queryManipulation', nargs='*',
                                  help="This option is similar to the '-q' option; however, the queries are only applied to the target trials (IsTarget == 'Y') and use all of non-target trials. Depending on the number (N) of queries, the option generates N report tables (CSV) and one plot (PDF) that contains N curves.", metavar='character')

        #TBD: may need this one for provenance filtering
        #Note that this requires different mutually exclusive gropu to use both -qm and -qn at the same time
#        parser.add_argument('-qn', '--queryNonManipulation',
#        help="Provide a simple interface to evaluate algorithm performance by given query (for filtering non-target trials)", metavar='character')


        args = parser.parse_args()

        # Verbosity option
        if args.verbose:
            def _print(*args):
                for arg in args:
                   print (arg),
                print
        else:
            _v_print = lambda *a: None      # do-nothing function

        global v_print
        v_print = _v_print

        if (not args.query) and (not args.queryPartition) and (not args.queryManipulation) and (args.multiFigs is True):
            print("ERROR: The multiFigs option is not available without query options.")
            exit(1)

        #print("Namespace :\n{}\n".format(args))

        # Loading the reference file
        try:
            myRefFname = args.refDir + "/" + args.inRef
            #myRef = pd.read_csv(myRefFname, sep='|', dtype = ref_dtype)
            myRef = pd.read_csv(myRefFname, sep='|')
            myRefDir =  os.path.dirname(myRefFname) #to use for loading JTJoin and JTMask files
        except IOError:
            print("ERROR: There was an error opening the reference csv file '" + myRefFname + "'")
            exit(1)

        # Loading the JTjoin and JTmask file
        inJTJoin = "NC2017-manipulation-ref-probejournaljoin.csv"
        inJTMask = "NC2017-manipulation-ref-journalmask.csv"
        myJTJoinFname = myRefDir + "/" + inJTJoin
        myJTMaskFname = myRefDir + "/" + inJTMask
        # check existence of the JTjoin and JTmask csv files
        if os.path.isfile(myJTJoinFname) and os.path.isfile(myJTMaskFname):
            myJTJoin = pd.read_csv(myJTJoinFname, sep='|')
            myJTMask = pd.read_csv(myJTMaskFname, sep='|')
        else:
            v_print("Either JTjoin or JTmask csv file do not exist and merging process with the reference file will be skipped")

        # Loading the index file
        try:

            myIndexFname = args.refDir + "/" + args.inIndex
           # myIndex = pd.read_csv(myIndexFname, sep='|', dtype = index_dtype)
            myIndex = pd.read_csv(myIndexFname, sep='|')
        except IOError:
            print("ERROR: There was an error opening the index csv file")
            exit(1)

        # Loading system output for SSD and DSD due to different columns between SSD and DSD
        try:

            if args.task in ['manipulation', 'provenancefiltering', 'provenance']:
                sys_dtype = {'ProbeFileID':str,
                         'ConfidenceScore':str, #this should be "string" due to the "nan" value, otherwise "nan"s will have different unique numbers
                         'ProbeOutputMaskFileName':str}
            elif args.task in ['splice']:
                sys_dtype = {'ProbeFileID':str,
                         'DonorFileID':str,
                         'ConfidenceScore':str, #this should be "string" due to the "nan" value, otherwise "nan"s will have different unique numbers
                         'ProbeOutputMaskFileName':str,
                         'DonorOutputMaskFileName':str}
            mySysFname = args.sysDir + "/" + args.inSys
            v_print("Sys File Name {}".format(mySysFname))
            mySys = pd.read_csv(mySysFname, sep='|', dtype = sys_dtype)
            #mySys['ConfidenceScore'] = mySys['ConfidenceScore'].astype(str)
        except IOError:
            print("ERROR: There was an error opening the system output csv file")
            exit(1)

        # merge the reference and system output for SSD/DSD reports
        if args.task in ['manipulation', 'provenancefiltering', 'provenance']:
            m_df = pd.merge(myRef, mySys, how='left', on='ProbeFileID')
        elif args.task in ['splice']:
            m_df = pd.merge(myRef, mySys, how='left', on=['ProbeFileID','DonorFileID'])

        # if the confidence scores are 'nan', replace the values with the mininum score
        m_df[pd.isnull(m_df['ConfidenceScore'])] = mySys['ConfidenceScore'].min()
        # convert to the str type to the float type for computations
        m_df['ConfidenceScore'] = m_df['ConfidenceScore'].astype(np.float)

        # the performers' result directory
        if '/' not in args.outRoot:
            root_path = '.'
            file_suffix = args.outRoot
        else:
            root_path, file_suffix = args.outRoot.rsplit('/', 1)

        if root_path != '.' and not os.path.exists(root_path):
            os.makedirs(root_path)

         # Partition Mode
        if args.query or args.queryPartition or args.queryManipulation: # add or targetManiTypeSet or nontargetManiTypeSet
            v_print("Query Mode ... \n")
            partition_mode = True
            #SSD
            if args.task in ['manipulation', 'provenancefiltering', 'provenance']:
                 # merge the reference and index csv only
                subIndex = myIndex[['ProbeFileID', 'ProbeWidth', 'ProbeHeight']]
                pm_df = pd.merge(m_df, subIndex, how='left', on= 'ProbeFileID')

                # if the files exist, merge the JTJoin and JTMask csv files with the reference and index file
                if os.path.isfile(myJTJoinFname) and os.path.isfile(myJTMaskFname):
                    v_print("Merging the JournalJoin and JournalMask csv file with the reference files ...\n")
                    # merge the reference and index csv
                    df_1 = pd.merge(m_df, subIndex, how='left', on= 'ProbeFileID')
                    # merge the JournalJoinTable and the JournalMaskTable
                    df_2 = pd.merge(myJTJoin, myJTMask, how='left', on= 'JournalID')
                    # merge the dataframes above
                    pm_df = pd.merge(df_1, df_2, how='left', on= 'ProbeFileID')
            #DSD
            elif args.task in ['splice']: #TBD
                subIndex = myIndex[['ProbeFileID', 'DonorFileID', 'ProbeWidth', 'ProbeHeight', 'DonorWidth', 'DonorHeight']] # subset the columns due to duplications
                pm_df = pd.merge(m_df, subIndex, how='left', on= ['ProbeFileID','DonorFileID'])

            if args.query:
                query_mode = 'q'
                query = args.query
            elif args.queryPartition:
                query_mode = 'qp'
                query = args.queryPartition
            elif args.queryManipulation:
                query_mode = 'qm'
                query = args.queryManipulation

            v_print("Query : {}\n".format(query))
            v_print("Creating partitions...\n")
            selection = f.Partition(pm_df, query, query_mode, fpr_stop=args.farStop, isCI=args.ci)
            DM_List = selection.part_dm_list
            v_print("Number of partitions generated = {}\n".format(len(DM_List)))
            v_print("Rendering csv tables...\n")
            table_df = selection.render_table()
            if isinstance(table_df,list):
                v_print("Number of table DataFrame generated = {}\n".format(len(table_df)))
            if args.query:
                for i,df in enumerate(table_df):
                    df.to_csv(args.outRoot + '_q_query_' + str(i) + '.csv', index = False)
            elif args.queryPartition:
                table_df.to_csv(args.outRoot + '_qp_query.csv')
            elif args.queryManipulation:
                for i,df in enumerate(table_df):
                    df.to_csv(args.outRoot + '_qm_query_' + str(i) + '.csv', index = False)


        # No partitions
        else:
            DM = dm.detMetrics(m_df['ConfidenceScore'], m_df['IsTarget'], fpr_stop = args.farStop, isCI=args.ci)

            DM_List = [DM]
            table_df = DM.render_table()
            table_df.to_csv(args.outRoot + '_all.csv', index = False)

        if isinstance(table_df,list):
            print("\nReport tables:\n")
            for i, table in enumerate (table_df):
                print("\nPartition {}:".format(i))
                print(table)
        else:
            print("Report table:\n{}".format(table_df))


        # Generating a default plot_options json config file
        p_json_path = "./plotJsonFiles"
        if not os.path.exists(p_json_path):
            os.makedirs(p_json_path)
        dict_plot_options_path_name = "./plotJsonFiles/plot_options.json"
        
                       
        if os.path.isfile(dict_plot_options_path_name):
            # Loading of the plot_options json config file
            plot_opts = p.load_plot_options(dict_plot_options_path_name)
        else:
            p.gen_default_plot_options(dict_plot_options_path_name, args.plotType.upper())
            plot_opts = p.load_plot_options(dict_plot_options_path_name)
        
        # opening of the plot_options json config file from command-line
        if args.configPlot:
            p.open_plot_options(dict_plot_options_path_name)


        # Dumping DetMetrics objects
        if args.dump:
            for i,DM in enumerate(DM_List):
                DM.write(root_path + '/' + file_suffix + '_query_' + str(i) + '.dm')

        # Creation of defaults plot curve options dictionnary (line style opts)
        Curve_opt = OrderedDict([('color', 'red'),
                                 ('linestyle', 'solid'),
                                 ('marker', '.'),
                                 ('markersize', 8),
                                 ('markerfacecolor', 'red'),
                                 ('label',None),
                                 ('antialiased', 'False')])

        # Creating the list of curves options dictionnaries (will be automatic)
        opts_list = list()
        colors = ['red','blue','green','cyan','magenta','yellow','black']
        linestyles = ['solid','dashed','dashdot','dotted']
        # Give a random rainbow color to each curve
        #color = iter(cm.rainbow(np.linspace(0,1,len(DM_List)))) #YYL: error here
        color = cycle(colors)
        lty = cycle(linestyles)
        for i in range(len(DM_List)):
            new_curve_option = OrderedDict(Curve_opt)
            col = next(color)
            new_curve_option['color'] = col
            new_curve_option['markerfacecolor'] = col
            new_curve_option['linestyle'] = next(lty)
            opts_list.append(new_curve_option)

        # Renaming the curves for the legend
        if args.query or args.queryPartition or args.queryManipulation:
            for curve_opts,query in zip(opts_list,selection.part_query_list):
                curve_opts["label"] = query

        # Creation of the object setRender (~DetMetricSet)
        configRender = p.setRender(DM_List, opts_list, plot_opts)
        # Creation of the Renderer
        myRender = p.Render(configRender)
        # Plotting
        myfigure = myRender.plot_curve(args.display,multi_fig=args.multiFigs)

        # save multiple figures if multi_fig == True
        if isinstance(myfigure,list):
            for i,fig in enumerate(myfigure):
                fig.savefig(args.outRoot + '_' + args.plotType + '_' + str(i) + '.pdf')
        else:
            myfigure.savefig(args.outRoot + '_' + args.plotType + '_all.pdf')

    # Debugging mode
    else:

        print('Starting debug mode ...\n')

        refDir = '/Users/yunglee/YYL/MEDIFOR/data'
        sysDir = '../../data/test_suite/detectionScorerTests'
        task = 'manipulation'
        outRoot = './test/sys_01'
        farStop = 1
        ci = False
        plotType = 'roc'
        display = True
        multiFigs = False
        dump = False
        verbose = False
 #       queryManipulation = None
        arg_query = None
        queryPartition = None
#        queryManipulation = "Purpose ==['remove', 'splice', 'add']"
#       factor = ["Purpose ==['remove', 'splice', 'add']"]
#        queryManipulation = "Operation ==['PasteSplice', 'FillContentAwareFill']"
#        queryManipulation = "SemanticLevel ==['PasteSplice', 'FillContentAwareFill']"targetFilter
#        factor = "Purpose ==['remove']"
        queryManipulation = ["Purpose ==['add']", "Purpose ==['remove']"]
#        factor = ["Purpose ==['remove', 'splice', 'add']","Operation ==['PasteSplice', 'FillContentAwareFill']"]
#        print("f query {}".format(factor))

#        queryPartition = "Purpose ==['remove', 'splice']"

        if (not query) and (not queryPartition) and (multiFigs is True):
            print("ERROR: The multiFigs option is not available without querys options.")
            exit(1)

#        if task == 'manipulation':
#            refFname = "reference/manipulation/NC2016-manipulation-ref.csv"
#            indexFname = "indexes/NC2016-manipulation-index.csv"
#            sysFname = "../../data/SystemOutputs/results/dct02.csv"
#        if task == 'splice':
#            refFname = "reference/splice/NC2016-splice-ref.csv"
#            indexFname = "indexes/NC2016-splice-index.csv"
#            sysFname = "../../data/SystemOutputs/splice0608/results.csv"

        if task == 'manipulation':
            inRef = "NC2017-1215/NC2017-manipulation-ref.csv"
            inIndex = "NC2017-1215/NC2017-manipulation-index.csv"
            inJTJoin = "NC2017-manipulation-ref-probejournaljoin.csv"
            inJTMask = "NC2017-manipulation-ref-journalmask.csv"
            inSys = "baseline/NC17_copymove01.csv"


        # Loading the reference file
        try:

            myRefFname = refDir + "/" + inRef
            #myRef = pd.read_csv(myRefFname, sep='|', dtype = ref_dtype)
            myRef = pd.read_csv(myRefFname, sep='|')
            myRefDir =  os.path.dirname(myRefFname)
            #print ("Ref path {}".format(myRefDir))
        except IOError:
            print("ERROR: There was an error opening the reference csv file")
            exit(1)

#        try:
#
#            myJTJoinFname = myRefDir + "/" + inJTJoin
#            myJTJoin = pd.read_csv(myJTJoinFname, sep='|')
#        except IOError:
#            print("ERROR: There was an error opening the JournalJoin csv file")
#            exit(1)
#
#        try:
#
#            myJTMaskFname = myRefDir + "/" + inJTMask
#            myJTMask = pd.read_csv(myJTMaskFname, sep='|')
#        except IOError:
#            print("ERROR: There was an error opening the JournalMask csv file")
#            exit(1)
        # check existence of the JTjoin csv file and then load the file
        inJTJoin = "NC2017-manipulation-ref-probejournaljoin.csv"
        inJTMask = "NC2017-manipulation-ref-journalmask.csv"
        myJTJoinFname = myRefDir + "/" + inJTJoin
        myJTMaskFname = myRefDir + "/" + inJTMask
        if os.path.isfile(myJTJoinFname) and os.path.isfile(myJTMaskFname):
            myJTJoin = pd.read_csv(myJTJoinFname, sep='|')
            myJTMask = pd.read_csv(myJTMaskFname, sep='|')
        else:
            print("Note: either JTjoin or JTmask csv file do not exist and merging with the reference file will be skipped")



        try:

            myIndexFname = refDir + "/" + inIndex
           # myIndex = pd.read_csv(myIndexFname, sep='|', dtype = index_dtype)
            myIndex = pd.read_csv(myIndexFname, sep='|')
        except IOError:
            print("ERROR: There was an error opening the index csv file")
            exit(1)

        try:
            # Loading system output for SSD and DSD due to different columns between SSD and DSD
            if task in ['manipulation', 'provenancefiltering', 'provenance']:
                sys_dtype = {'ProbeFileID':str,
                         'ConfidenceScore':str, #this should be "string" due to the "nan" value, otherwise "nan"s will have different unique numbers
                         'ProbeOutputMaskFileName':str}
            elif task in ['splice']:
                sys_dtype = {'ProbeFileID':str,
                         'DonorFileID':str,
                         'ConfidenceScore':str, #this should be "string" due to the "nan" value, otherwise "nan"s will have different unique numbers
                         'ProbeOutputMaskFileName':str,
                         'DonorOutputMaskFileName':str}
            mySysFname = sysDir + "/" + inSys
            print("Sys File Name {}".format(mySysFname))
            mySys = pd.read_csv(mySysFname, sep='|', dtype = sys_dtype)
            #mySys['ConfidenceScore'] = mySys['ConfidenceScore'].astype(str)
        except IOError:
            print("ERROR: There was an error opening the system output csv file")
            exit(1)

        # merge the reference and system output for SSD/DSD reports
        if task in ['manipulation', 'provenancefiltering', 'provenance']:
            m_df = pd.merge(myRef, mySys, how='left', on='ProbeFileID')
        elif task in ['splice']:
            m_df = pd.merge(myRef, mySys, how='left', on=['ProbeFileID','DonorFileID'])

         # if the confidence scores are 'nan', replace the values with the mininum score
        m_df[pd.isnull(m_df['ConfidenceScore'])] = mySys['ConfidenceScore'].min()
        # convert to the str type to the float type for computations
        m_df['ConfidenceScore'] = m_df['ConfidenceScore'].astype(np.float)

        # the performers' result directory
        if '/' not in outRoot:
            root_path = '.'
            file_suffix = outRoot
        else:
            root_path, file_suffix = outRoot.rsplit('/', 1)

        if root_path != '.' and not os.path.exists(root_path):
            os.makedirs(root_path)

        # Partition Mode
        if args_query or queryPartition or queryManipulation: # add or targetManiTypeSet or nontargetManiTypeSet
            print("Partition Mode \n")
            partition_mode = True

            if task in ['manipulation', 'provenancefiltering', 'provenance']:
                # merge the reference and index csv only
                subIndex = myIndex[['ProbeFileID', 'ProbeWidth', 'ProbeHeight']]
                pm_df = pd.merge(m_df, subIndex, how='left', on= 'ProbeFileID')

                # if the files exist, merge the JTJoin and JTMask csv files with the reference and index file
                if os.path.isfile(myJTJoinFname) and os.path.isfile(myJTMaskFname):
                    print("Merging the JournalJoin and JournalMask csv file with the reference files ...\n")
                    # merge the reference and index csv
                    df_1 = pd.merge(m_df, subIndex, how='left', on= 'ProbeFileID')
                    # merge the JournalJoinTable and the JournalMaskTable
                    df_2 = pd.merge(myJTJoin, myJTMask, how='left', on= 'JournalID')
                    # merge the dataframes above
                    pm_df = pd.merge(df_1, df_2, how='left', on= 'ProbeFileID')
                    #pm_df.to_csv(outRoot + 'test.csv', index = False)
##    #                # for queryManipulation, drop duplicates conditioning by the chosen columns (e.g., ProbeFileID and Purpose)
#                    if args.queryManipulation:
#                        print("Removing duplicates of the chosen column for filtering target trials ...\n")
#                        chosenField = [x.strip() for x in args.queryManipulation.split('==')]
#                        #fm_df.sort(['ProbeFileID', chosenField[0]], inplace=True) #TODO: not necesary, but for testing
#                        pm_df = pm_df.drop_duplicates(['ProbeFileID', chosenField[0]]) #remove duplicates for the chosen column

            elif task in ['splice']: #TBD
                subIndex = myIndex[['ProbeFileID', 'DonorFileID', 'ProbeWidth', 'ProbeHeight', 'DonorWidth', 'DonorHeight']] # subset the columns due to duplications
                pm_df = pd.merge(m_df, subIndex, how='left', on= ['ProbeFileID','DonorFileID'])

            if args_query:
                query_mode = 'q'
                query = args_query #TODO: double-check
            elif args_queryPartition:
                query_mode = 'qp'
                query = args_queryPartition
            elif args_queryManipulation: #TODO: testcases
                query_mode = 'qm'
                query = args_queryManipulation
                #query = ["("+targetFilter+ " and IsTarget == ['Y']) or IsTarget == ['N']"] #TODO: double-check
                #print("targetQuery {}".format(query))

            print("Query : {}\n".format(query))
            print("Creating partitions...\n")
            selection = f.Partition(pm_df, query, query_mode, fpr_stop=farStop, isCI=ci)
            DM_List = selection.part_dm_list
            print("Number of partitions generated = {}\n".format(len(DM_List)))
            print("Rendering csv tables...\n")
            table_df = selection.render_table()
            if isinstance(table_df,list):
                print("Number of table DataFrame generated = {}\n".format(len(table_df)))
            if args_query:
                for i,df in enumerate(table_df):
                    df.to_csv(outRoot + '_q_query_' + str(i) + '.csv', index = False)
            elif args_queryPartition:
                table_df[0].to_csv(outRoot + '_qp_query.csv') #table_df is List type
            elif args_queryManipulation:
                for i,df in enumerate(table_df):
                    df.to_csv(outRoot + '_qm_query_' + str(i) + '.csv', index = False)

        # No partitions
        else:
            DM = dm.detMetrics(m_df['ConfidenceScore'], m_df['IsTarget'], fpr_stop = farStop, isCI=ci)

            DM_List = [DM]
            table_df = DM.render_table()
            table_df.to_csv(outRoot + '_all.csv', index = False)

        if isinstance(table_df,list):
            print("\nReport tables...\n")
            for i, table in enumerate (table_df):
                print("\nPartition {}:".format(i))
                print(table)
        else:
            print("Report table:\n{}".format(table_df))


        # Generating a default plot_options json config file
        p_json_path = "./plotJsonFiles"
        if not os.path.exists(p_json_path):
            os.makedirs(p_json_path)
        dict_plot_options_path_name = "./plotJsonFiles/plot_options.json"
                
        if os.path.isfile(dict_plot_options_path_name):
            # Loading of the plot_options json config file
            plot_opts = p.load_plot_options(dict_plot_options_path_name)
        else:
            p.gen_default_plot_options(dict_plot_options_path_name, args.plotType.upper())
            plot_opts = p.load_plot_options(dict_plot_options_path_name)
        
        # opening of the plot_options json config file from command-line
        configPlot = False
        if configPlot:
            p.open_plot_options(dict_plot_options_path_name)

        # Dumping DetMetrics objects
        if dump:
            for i,DM in enumerate(DM_List):
                DM.write(root_path + '/' + file_suffix + '_query_' + str(i) + '.dm')

        # Creation of defaults plot curve options dictionnary (line style opts)
        Curve_opt = OrderedDict([('color', 'red'),
                                 ('linestyle', 'solid'),
                                 ('marker', '.'),
                                 ('markersize', 8),
                                 ('markerfacecolor', 'red'),
                                 ('label',None),
                                 ('antialiased', 'False')])

        # Creating the list of curves options dictionnaries (will be automatic)
        opts_list = list()
        colors = ['red','blue','green','cyan','magenta','yellow','black']
        linestyles = ['solid','dashed','dashdot','dotted']
        # Give a random rainbow color to each curve
        #color = iter(cm.rainbow(np.linspace(0,1,len(DM_List)))) #YYL: error here
        color = cycle(colors)
        lty = cycle(linestyles)
        for i in range(len(DM_List)):
            new_curve_option = OrderedDict(Curve_opt)
            col = next(color)
            new_curve_option['color'] = col
            new_curve_option['markerfacecolor'] = col
            new_curve_option['linestyle'] = next(lty)
            opts_list.append(new_curve_option)

        # Renaming the curves for the legend
        if args_query or args_queryPartition or args_queryManipulation:
            for curve_opts,query in zip(opts_list,selection.part_query_list):
                curve_opts["label"] = query


        # Creation of the object setRender (~DetMetricSet)
        configRender = p.setRender(DM_List, opts_list, plot_opts)
        # Creation of the Renderer
        myRender = p.Render(configRender)
        # Plotting
        myfigure = myRender.plot_curve(display,multi_fig=multiFigs)

        # save multiple figures if multi_fig == True
        if isinstance(myfigure,list):
            for i,fig in enumerate(myfigure):
                fig.savefig(outRoot + '_' + plotType + '_' + str(i) + '.pdf')
        else:
            myfigure.savefig(outRoot + '_' + plotType + '_all.pdf')