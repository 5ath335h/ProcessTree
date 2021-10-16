#!/usr/bin/env python3

'''
This tool will take csv as an input and will display a displays a graphical representation of the process chaining. 

INPUTS: The program takes a csv as an input. The file should have the below fields.

Input file format: The csv should have the below column names
        'TimeCreated'       - The date time field at which the process was created. Make sure the file is sorted in ASC based on this column.
        'ProcName'          - Name of the created process
        'ProcessId'         - Process of the created process 
        'ProcPath'          - Path of the created process
        'ParentProcessName' - Name of the parent process
        'ParentProcessId'   - Process ID of the parent process
        'CommandLine'       - Command Line of the created process
        'TokenElevationType'- TokenElevationType of the process
        'SubjectDomainName' - Domain name of the user account which created the process
        'SubjectUserName'   - Name of the account which created the process
        'SubjectLogonId'    - Logon ID of the user which created the process

    More details about Event ID (4688): https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4688

OUTPUT: A html file, that contains the graphical representation of the data.

Author: Satheesh Balaji
Twitter: https://twitter.com/sbc0d
Github: https://github.com/sbc0d
LinkedIn: https://www.linkedin.com/in/sb-c0d3
'''

import pandas as pd
from pyvis.network import Network

graph = Network(height='100%', width='100%',font_color="black",directed=True)
graph.force_atlas_2based()

'''
Mapprocesses(): Maps the nodes based on parent and child relationship. 
Param 1: fullPrcsDF - A dataframe that holds the full process list.
Param 2: subPrcsDF - A sub dataframe that hols the child processes.
'''

def mapProcesses(fullPrcsDF,subPrcsDF=pd.DataFrame({'A' : []})):
    df = pd.DataFrame({'A' : []})
    if subPrcsDF.empty != True:
        df = subPrcsDF
    else:
        df = fullPrcsDF
    for index in range(0, len(df)):
        prcsNodeName = df.iloc[index]['ProcName'] + '_' + df.iloc[index]['ProcessId']
        if prcsNodeName not in processedValues:
            prcsCreatedTime = df.iloc[index]['TimeCreated']
            samePIDDF = fullPrcsDF[(fullPrcsDF.ProcessId == df.iloc[index]['ProcessId']) & (fullPrcsDF.TimeCreated > prcsCreatedTime)].sort_values('TimeCreated')
            tSubPrcsDF = ''
            if(len(samePIDDF.index) > 0):
                nextPrcsCreateTimeForSamePID = samePIDDF['TimeCreated'].values[0]
                tSubPrcsDF = fullPrcsDF[(fullPrcsDF.ParentProcessId == df.iloc[index]['ProcessId']) & (fullPrcsDF.ParentProcessName == df.iloc[index]['ProcPath']) & (fullPrcsDF.TimeCreated > nextPrcsCreateTimeForSamePID)]
            else:
                tSubPrcsDF = fullPrcsDF[(fullPrcsDF.ParentProcessId == df.iloc[index]['ProcessId']) & (fullPrcsDF.ParentProcessName == df.iloc[index]['ProcPath'])]
            tparentNode = str(df.iloc[index]['ParentProcessName']).split('\\')[-1] + '_' + df.iloc[index]['ParentProcessId']
            if tSubPrcsDF.empty != True:
                childprcsNodeName = mapProcesses(fullPrcsDF, tSubPrcsDF)
            graph.add_edge(tparentNode, prcsNodeName)
            processedValues.append(prcsNodeName)
    graph.set_edge_smooth('dynamic')


'''
iterateDF_CreateNodes(): Creates the nodes for each process.
Param 1: processExecutiondDF - A dataframe that holds the list of process is passed as an input.
'''
def iterateDF_CreateNodes(processExecutiondDF):
	prcsList = []
	tokenElevation = {'%%1936': 'Type 1: Full token with no privileges removed', '%%1937': 'Type 2: Elevated token with no privileges removed', '%%1938': 'Type 3: Limited token with admin privileges removed'}
	for index, Row in processExecutiondDF.iterrows():
	    if Row['ProcessId'] != "":
	        prcsNodeName = Row['ProcName'] + '_' + Row['ProcessId']
	        if prcsNodeName not in prcsList:
	            prcsList.append(prcsNodeName)
	            commandLine = Row['CommandLine']
	            tokenElevationType = tokenElevation[Row['TokenElevationType']]
	            tempCommandLine = "</br>".join([commandLine[i:i+70] for i in range(0, len(commandLine), 70)])
	            prcsNodeLabel = "<b>AccountName: </b>" + Row['SubjectUserName'] + "<br>" + "<b>CommandLine: </b>" + tempCommandLine + "<br>" + "<b>TokenElevationType: </b>" + tokenElevationType + "<br>"
	            graph.add_node(prcsNodeName, title = prcsNodeLabel)
	for index, Row in processExecutiondDF.iterrows():
	    parentNodeName = Row['ParentProcessName'].split('\\')[-1] + '_' + Row['ParentProcessId']
	    if parentNodeName not in prcsList:
	        prcsList.append(parentNodeName)
	        parentProcPath = Row['ParentProcessName']
	        SubjectUserName = Row['SubjectDomainName'] + '/' + Row['SubjectUserName']
	        SubjectLogonId = Row['SubjectLogonId']
	        prcsNodeLabel =  "<b>LogonId: </b>" + SubjectLogonId + "<br><b>AccountName: </b>" + SubjectUserName + "<br><b>ProcessPath: </b>" + parentProcPath
	        graph.add_node(parentNodeName, title = prcsNodeLabel)
	        graph.add_edge(str('4688'), parentNodeName)
'''
readCSV() reads the file.
Param 1: filePath - location of the file.
Returns: a pandas dataframe of the csv file.
'''
def readCSV(filePath):
	return pd.read_csv(filePath).sort_values('TimeCreated')

if __name__ == "__main__":
    eventId = 4688
    eventName = 'A new process has been created'
    rootNode = 'rootPrcs'

    #graph.add_node(rootNode, title = rootNode, shape='image', image='https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/User_icon_2.svg/2048px-User_icon_2.svg.png')
    graph.add_node(str(eventId), title = eventName, shape='image', image='https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/User_icon_2.svg/2048px-User_icon_2.svg.png')
    #graph.add_edge(rootNode, str(eventId))

    print("""
    [+] Description: This tool will takes csv as an input and displays a graphical representation of the parent child processes.
    [+] Python version: > 3.6.*
    [+] Input file format: The csv should have the below column names
        'TimeCreated'       - The date time field at which the process was created. Make sure the file is sorted in ASC based on this column.
        'ProcName'          - Name of the created process
        'ProcessId'         - Process of the created process 
        'ProcPath'          - Path of the created process
        'ParentProcessName' - Name of the parent process
        'ParentProcessId'   - Process ID of the parent process
        'CommandLine'       - Command Line of the created process
        'TokenElevationType'- TokenElevationType of the process
        'SubjectDomainName' - Domain name of the user account which created the process
        'SubjectUserName'   - Name of the account which created the process
        'SubjectLogonId'    - Logon ID of the user which created the process

    More details about Event ID (4688): https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4688
    """)

    filePath = input('Enter the csv file location:- ')
    if(filePath != ""):
        processExecutionDF = readCSV(filePath)
        iterateDF_CreateNodes(processExecutionDF)

        processedValues = []
        mapProcesses(processExecutionDF)

        graph.show('result.html')

