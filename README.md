# ProcessTree
Process chaining is something which every blueteamer does when they are dealing with process logs. This python utility takes in a csv file and produces a graphical representation of the processes that were executed

This tool will take csv as an input and will display a displays a graphical representation of the process chaining. 

**Author:** Satheesh Balaji

**Twitter:** @sbc0d

**LinkedIn:** https://www.linkedin.com/in/sb-c0d3


**INPUTS:** The program takes a csv as an input. The file should have the below fields. It can have other fields as well. A sample file 4688.csv is attached.

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

More details about [Event ID: 4688](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4688)

**OUTPUT:** A html file, that contains the graphical representation of the data.

![Result](https://user-images.githubusercontent.com/7699846/137596815-fbf0c045-3ad8-4399-a399-91fa257794a7.JPG)

A popup with more details will appear when mouse is hovered over a node.

![Result1](https://user-images.githubusercontent.com/7699846/137596856-e33e110d-66c3-47e6-94d5-74bbe46868e5.jpg)

