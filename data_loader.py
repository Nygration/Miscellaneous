def data_loader():
    ## The point is to take the data files from the field and automatically generate the default file layout.
    # navigate to the desired location first, its easier that way
    
    #Generally the layout should match below
    # Job#_Name
    #     Cruise/Deployment#_Date Range
    #         01_Log Sheets and Field Notes
    #         02_Data_FromField                #this inconsistancy should be addressed if it hasn't been already
    #             MooringName
    #                 Inst#_InstrumentType_Serial#
    #         03_Processing
    #             MooringName
    #                 M#I#_InstrumentType_Serial#         # again the inconsistancy should be addressed
    #         04_PrelimDeliverables
    #             Appendices
    #             Data
    #             Figures
    #             Report
    #             Tables
    #         05_FinalProducts
    
    # deployment and recovery logs should also be printed and stored as hard copies
    # ---> make function to ID appropriate documents, organize them and print them
    
    # if there are multiple raw data files concatenate them and renumber the ensembles using BBSub
    # if the instrument collected waves, divide the file using Parse
    # Use WinADCP to open/select the raw data file *.000 # see processing instructions for more details on WinADCP
    # Fill out the processing log sheet ----->(automate it)
    import os
    
    target_directory = os.getcwd()
    job_number = input('Job number: ')
    job_name = input('Job name: ')
    
    
    os.mkdir(f'{job_number}_{job_name}') # top directory
    os.chdir(f'{job_number}_{job_name}')
    
    os.mkdir('01_Log Sheets and Field Notes')
    os.mkdir('02_Data_FromField')
    os.mkdir('03_Processing')
    os.mkdir('04_PrelimDeliverables')
    os.mkdir('05_FinalProducts')
    
    os.chdir('04_PrelimDeliverables')
    os.mkdir('Appendices')
    os.mkdir('Data')
    os.mkdir('Figures')
    os.mkdir('Report')
    os.mkdir('Tables')
    os.chdir('..')
    
    
    
    os.chdir(target_directory)