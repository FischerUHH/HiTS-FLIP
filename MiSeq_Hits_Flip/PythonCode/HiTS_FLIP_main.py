# -*- coding: utf-8 -*-
"""
This code switches the valve by reading the log files as they are being created.
The position of the valve is coded in the duration of the lines containing   <Wait Duration="987xx"/> .

1. Get all data from ini file and sample sheet 

2. In a Loop:
    - check if new cycle is available (Log File)
    - if new cycle is available:
        raise cycle number
    - get content from .log file
    - strip whole content of string from last loop, so the "waitCommand" is faster to find
    - find "waitCommand" 
    - get string vom parenthesis after "waitCommand" 
    - if first 3 chars == 987:
        if last 2 chars are between 1 and 12:
            set valve to position
            (for PrimeAlt)
        elseif last 2 chars == 20:
            compare cycle number to data from ini file
            set valve to cycle dependent position
            (For target incubation)

       
            
Position written in   <Wait Duration="987xx"/>    in chemisty.xml
WaitCommand(987xx)
xx = 1-12:  Switch valve to Position xx
xx = 20:    Switch valve to cycle-dependent position given in ini-file
"""


import os
import time
import shutil
import pandas
import threading

class HitsFlipMain():
    def __init__(self):
        # set constants
        self.HFM_LOG_PATH   = 'C:\\MiSeq_Hits_Flip\\HiTS_FLIP_Logs\\'
        
        # set variables
        self.oldLogString   = ''
        self.newLogString   = ''

        self.loopNo         = 0
        self.cycleNo        = 1
        
        # get info from files
        self.get_run_id()

        # set filename for HF-log
        self.hfmLogFile     = ''.join([self.HFM_LOG_PATH,
                                       'HitsFlipLog_',
                                       self.runId,
                                       '_',
                                       time.strftime('%y_%m_%d %H_%M.csv')])
        
        self.read_sample_sheet()
        self.read_ini()

        # in case the HiTS-FLIP is already running, get current cycle
        # if none is found, we start with 1
        try:
            # the max found cycle. 1 for now
            cyclemax = 1

            #find all filenames in \temp\<ID>\logs
            f = []
            for (dirpath, dirnames, filenames) in os.walk(self.basePathLog):
                f.extend(filenames)
                break

            # find the log file with highest cycle-number  
            for i in f:
                c = int(i.split('_Cycle')[1].split('_Log.')[0])
                if c > cyclemax:
                    cyclemax = c

            # make the maximal found cycle the start cycle
            self.cycleNo = cyclemax
                
        except Exception as error:
            print(error)
        
        # set name of first MiSeq log-file
        self.logFileName    = self.runId + '_Cycle'+str(self.cycleNo)+'_Log.00.log'
             
        # set loop and variables
        self.loopStopFlag   = 1
        self.loop()
        
    
    def loop(self):
        # I use this to kill the programm by keyboardInterrupt
        while self.loopStopFlag:
            time.sleep(.05)
            
            try:
                while 1:
                    # loop number is just the number how often this eternal loop has been executed
                    self.loopNo +=1
                    
                    time.sleep(.5)

                    # check if the log-file is still being written to
                    self.check_for_end(self.oldLogString)
                    
                    # print('Loop #: '+str(self.loopNo)+', Cycle #: '+str(self.cycleNo))

                    # get the whole content of log-file
                    log                 = self.read_log(self.logFileName)

                    # get the parts, which have been added to the log file since last loop                    
                    logNew              = self.find_new_lines(log)

                    # check if "waitcommand" is in the newly added string from log
                    #if it is present, also switch valve
                    self.check_for_wait_command(logNew)

                    #finally remember the content log file from the current loop for the next one
                    self.oldLogString   = log
                    
                    
            except KeyboardInterrupt:
                # kills the eternal loop
                self.loopStopFlag = 0   
                print('Loop function terminated by user')
                self.write_to_hf_log('Loop function terminated by user')
                
            except Exception as error:
                # happens before creation of log-file or between the cycles (eg. paired end turnaround)
                if "[Errno 2] No such file or directory: 'D:\\\\Illumina\\\\MiSeqTemp" in str(error) and 'Logs' in str(error):
                    print('   Waiting for first/next log file')
                    
                else:
                    # raise error
                    # print(error)
                    self.write_to_hf_log(str(error))
                    

    def get_run_id(self):
        # get all files and dirs in MiSeqTemp
        allLogs = os.listdir('D:\\Illumina\\MiseqTemp')
        allLogs = sorted(allLogs)

        # sourt out files. we only want dirs!
        dirs = []
        for element in allLogs:
            if os.path.isdir('D:\\Illumina\\MiseqTemp\\'+element):
                dirs.append(element)

        # get the most recent dir and make it our base working directory       
        self.runId = dirs[-1]                 
        self.basePathRunId      = ''.join(['D:\\Illumina\\MiSeqTemp\\',self.runId])
        self.basePathLog        = ''.join([self.basePathRunId,'\\Logs'])
        
        
    def read_ini(self):
        # read ini data
        xlsSheetName = 'C:\\MiSeq_Hits_Flip\\HiTS_FLIP_Inis\\HiTS_FLIP_ini.xlsx'
        xls = pandas.ExcelFile(xlsSheetName)

        # a dataframe is more convenient to handle
        self.iniDataFrame = xls.parse(xls.sheet_names[0])

        # wirte the dataframe-header to the HF-Log
        self.write_to_hf_log('Ini Details:')
        self.write_to_hf_log('CycleNumber,SolutionName,PortNumber')

        # write the dataframe to HF-log line by line
        for e in range(0,len(self.iniDataFrame['PortNumber'].values.tolist())):
            self.write_to_hf_log(str(self.iniDataFrame['CycleNumber'].values.tolist()[e])+','+
                                 str(self.iniDataFrame['SolutionName'].values.tolist()[e])+','+
                                 str(self.iniDataFrame['PortNumber'].values.tolist()[e]))
            
        
    def read_sample_sheet(self):
        print('reading samplesheet')

        #read samplesheet
        fid                     = open(self.basePathRunId+'\\SampleSheet.csv')
        content                 = fid.read()
        fid.close()

        # read cycles for the four reads
        readCycles = content.split('[Reads]')[1].split('[Settings]')[0].split('\n')
        self.read1Cycles        = readCycles[1]
        self.read2Cycles        = readCycles[2]
        self.indexRead1Cycles   = 8

        # check, if we have our HiTS_FLIP_RECIPE in use
        self.recipe = content.split('Chemistry,')[1].split('[\nReads]')[0].split('\n')[0]

        # print and wirte to HF-log
        out='   recipe:     '+self.recipe
        print(out)
        self.write_to_hf_log(out.replace(':     ',',').replace(' ',''))
        out='   FirstRead:  '+str(self.read1Cycles)
        print(out)
        self.write_to_hf_log(out.replace(':  ',',').replace(' ',''))
        out='   IndexRead:  '+str(self.indexRead1Cycles)
        print(out)
        self.write_to_hf_log(out.replace(':  ',',').replace(' ',''))
        out='   SecondRead: '+str(self.read2Cycles)
        print(out)
        self.write_to_hf_log(out.replace(': ',',').replace(' ',''))
        
        
    def read_log(self,fileName):
        # read file
        fid     = open('\\'.join([self.basePathLog,fileName]))
        content = fid.read()
        fid.close()

        # use a list
        if not content[-1] == '\n':
            li = content.split('\n')
            content = '\n'.join(li[0:len(li)-1])
            
        return content
    
    
    def find_new_lines(self,string):
        # removes old lines from previous loop
        newLogString   = string.replace(self.oldLogString,'')
        return newLogString
    
    
    def check_for_end(self,string):
        # if this string found in log-file
        # (this shound be the standard-entry with which the log-file ends)
        if 'time end. Duration was ' in string:
            print('END OF CYCLE #: '+str(self.cycleNo))

            # raise cycle no
            self.cycleNo        += 1

            # reset string containing log-file
            self.oldLogString   = ''

            # update name of log-file
            self.logFileName    = self.runId + '_Cycle'+str(self.cycleNo)+'_Log.00.log'
            self.write_to_hf_log('Set Cycle to No.:'+str(self.cycleNo).replace(' ','').replace(':',','))
            try:
                # I like to be notified...
                if self.cycleNo in list(range(0,150,10)):
                    pass
            except:
                pass
            
        # if new log-file has been generated but old file has not yet been terminated
        # (encountered this only once)
        elif os.path.isfile(self.basePathLog + "\\" + self.runId + '_Cycle'+str(self.cycleNo+1)+'_Log.00.log'):
            out = 'Setting cycle number to : '+str(self.cycleNo+1)

            #raise cycle no
            self.cycleNo        += 1

            # reset string containing log-file
            self.oldLogString   = ''

            # update name of log-file
            self.logFileName    = self.runId + '_Cycle'+str(self.cycleNo)+'_Log.00.log'
            print (out)
            self.write_to_hf_log(out.replace(':',','))
            try:
                # in this event I MUST be notified 
                if self.cycleNo in list(range(0,150,10)):
                    pass
            except:
                pass
            

    def check_for_wait_command(self,string):        # WaitCommand(10000) start
        # how often does the substring appear? remember number of element of list (lines of log)
        timeli = []
        if 'WaitCommand(' in string:
            occ = ([(i, string[i:i+12]) for i in findall('WaitCommand(',string)])

            #if it appears
            if not occ == []:
                # for every occurence check if 'start' also mentioned
                for element in occ:
                    line = (string[element[0]:element[0]+32])
                    if 'start' in line:

                            # remember al the durations in the brackets
                            timeli.append(line.split('(')[1].split(')'[0])[0])

        # should be maximum one command, have been more during simulation                    
        for command in timeli:

            # check if our magical number is present
            if command[0:3] == '135':
                lastDigits = command[-2:len(command)]

                # if you use a valve with more than 12 ports, change this
                # if position betrween 1 and 12
                if int(lastDigits) <=12 and int(lastDigits) >=1:
                    out = '   Setting valve to: '+str(int(lastDigits))
                    print(out)
                    
                    # sets valve to position 
                    f_set_valve(lastDigits)
                    
                    self.write_to_hf_log(out.replace(': ',',').replace('   ',''))

                # check if "20" signals a cycle-dependent position
                elif lastDigits == '20':
                    index = find(self.iniDataFrame['CycleNumber'] ,self.cycleNo)

                    # if there is no error in ini-file
                    if not index == []:
                        index = index[0]

                        # get info from ini
                        reagentName = self.iniDataFrame['SolutionName'][index]
                        portNumber = self.iniDataFrame['PortNumber'][index]
                        
                        out = 'Setting Valve to: '+reagentName+', PortNo: '+str(portNumber)
                        print(out)
                        self.write_to_hf_log(out.replace(':',','))

                        # set valve accordingly
                        f_set_valve(portNumber)

                    # if there is an error in ini file document but don't raise   
                    else:
                        print('Command 13520 unmatched with cycleNo from ini file!')
                        self.write_to_hf_log('Command 13520 unmatched with cycleNo from ini file!')

                # for later implementation of buffers etc.
                elif lastDigits == '30':
                    pass
                
                # for later implementation of buffers etc.
                elif lastDigits == '40':
                    pass
                
                else:
                    print('Unknown command found: '+command)
                    self.write_to_hf_log('Unknown command found'+command)
            
            
    def write_to_hf_log(self,string):
        #write Sting to file with timestamp
        fid = open(self.hfmLogFile,'a+')
        fid.write(time.strftime('%d.%m.%y. %H:%M:%S')+','+string+'\n')
        fid.close()
        
        
def findall(p, s):
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)
    
    
def find(inList,obj):
    cnt = -1
    out = []
    for i in inList:
        cnt +=1
        if str(i) == str(obj):
            out.append(cnt)
    return out
        

def f_set_valve(args):
    print('SettingValve to: '+str(args))
    os.system ('py C:\\MiSeq_Hits_Flip\\PythonCode\\setValve.py '+str(int(args)))
    try:
        pass
    except:
        pass
    
    
    

if __name__ == '__main__':
    hfm = HitsFlipMain()

