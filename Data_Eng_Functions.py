def transform_wind_directions_to_numeric(wind_direction):
    '''This function can be used in Exercise1 to transform compass-directions to numeric format'''

    wind_direction_numeric = []
    for item in wind_direction:
        if item == "N":
            wind_direction_numeric.append(0) #north is heading degree 0
        elif item == "NNE":
            wind_direction_numeric.append(22.5)
        elif item == "NE":
            wind_direction_numeric.append(45)
        elif item == "ENE":
            wind_direction_numeric.append(67.5)
        elif item == "E":
            wind_direction_numeric.append(90)
        elif item == "ESE":
            wind_direction_numeric.append(111.5)
        elif item == "SE":
            wind_direction_numeric.append(135)
        elif item == "SSE":
            wind_direction_numeric.append(157.5)
        elif item == "S":
            wind_direction_numeric.append(180)
        elif item == "SSW":
            wind_direction_numeric.append(202.5)
        elif item == "SW":
            wind_direction_numeric.append(225)
        elif item == "WSW":
            wind_direction_numeric.append(247.5)
        elif item == "W":
            wind_direction_numeric.append(270)
        elif item == "WNW":
            wind_direction_numeric.append(292.5)
        elif item == "NW":
            wind_direction_numeric.append(315)
        elif item == "NNW":
            wind_direction_numeric.append(337.5)
    return wind_direction_numeric

def parseHTMLfiles(data_folder):
    '''Parse HTML-files from the folder to get electricity prices into Dataframe in Exercise 2'''

    #imports for file and folder handling
    import pathlib 
    import pandas as pd

    #add "r" in front of folder-path so interpreter understands backslashes
    #data_folder = r"D:\DataEng\Electric_prices_data"

    date_list = []#list for storing dates
    prices_list = []#list for storing hourly prices
    prices_nested_list = []#list for storing dates and tables
    prices_dict = dict()

    for path in (pathlib.Path(data_folder).rglob('*')):# iterate through every sub-folder and file in the folder    
        #if path.is_file(): #if current path corresponds to file and not folder then enter
        if ".html" in str(path): #if there is html-file in path, then enter
            HtmlFile = open(path, 'r', encoding='utf-8')
            source_code = HtmlFile.read() 

            # read_html Returns list of all tables on page and in this case there is only one table
            # note that decimal points need to be correct in parsing
            table = pd.read_html(source_code, decimal=',', thousands='.')[0].values 
            
            if len(table)>0:#enter if list is not empty
                folder_name = path.parts[-2]#parse sub-folder name which includes date of current table
                current_date = folder_name.split('_tuntihinnat')[0]#parse date of folder name, assuming all folder names have same syntax
                current_date = current_date.replace('_', '-')#transform date string to format which Pandas understands DD-MM-YYYY
                for item in table:
                    #item is array where first element is string and split it to get first hour of corresponding price
                    
                    hour = str(item[0]).split('-')[0]
                    hour = int(hour)#+1 #add 1 because time format needs to be 1-24, not 0-23
                    prices_list.append(float(item[-1])) #append prices as float
                    current_date_time = current_date+'-'+str(hour) #create string in Dataframe Datetime form
                    date_list.append(current_date_time)

    prices_dict = {"Date":date_list, "Price":prices_list}#make dict of collected lists
    df = pd.DataFrame(prices_dict)
    df['Date'] = pd.to_datetime(df['Date'], format="%d-%m-%Y-%H", errors='ignore') #ignoring errors might cause data loss if formatting fails
    df = df.sort_values(by = 'Date')
    df.info()
    return df


def parseHTMLfilesColab(data_folder):
    '''Parse HTML-files from the folder to get electricity prices into Dataframe in Exercise 2, Colab-version with Google Drive folder'''

  #imports for file and folder handling
    import pathlib 
    import pandas as pd
    import glob

    #add "r" in front of folder-path so interpreter understands backslashes
    #data_folder = r"D:\DataEng\Electric_prices_data"

    date_list = []#list for storing dates
    prices_list = []#list for storing hourly prices
    prices_nested_list = []#list for storing dates and tables
    prices_dict = dict()

    for path in glob.glob(data_folder + '**/*.html'):
    #for path in (pathlib.Path(data_folder).rglob('*')):# iterate through every sub-folder and file in the folder    
        #if path.is_file(): #if current path corresponds to file and not folder then enter
        if ".html" in str(path): #if there is html-file in path, then enter
            HtmlFile = open(path, 'r', encoding='utf-8')
            source_code = HtmlFile.read() 

            # read_html Returns list of all tables on page and in this case there is only one table
            # note that decimal points need to be correct in parsing
            table = pd.read_html(source_code, decimal=',', thousands='.')[0].values 
            
            if len(table)>0:#enter if list is not empty
                try:
                    folder_name = path.parts[-2]#parse sub-folder name which includes date of current table
                except:
                    folder_name = path.split('/')[-2]
                current_date = folder_name.split('_tuntihinnat')[0]#parse date of folder name, assuming all folder names have same syntax
                current_date = current_date.replace('_', '-')#transform date string to format which Pandas understands DD-MM-YYYY
                for item in table:
                    #item is array where first element is string and split it to get first hour of corresponding price
                    
                    hour = str(item[0]).split('-')[0]
                    hour = int(hour)#+1 #add 1 because time format needs to be 1-24, not 0-23
                    prices_list.append(float(item[-1])) #append prices as float
                    current_date_time = current_date+'-'+str(hour) #create string in Dataframe Datetime form
                    date_list.append(current_date_time)

    prices_dict = {"Date":date_list, "Price":prices_list}#make dict of collected lists
    df = pd.DataFrame(prices_dict)
    df['Date'] = pd.to_datetime(df['Date'], format="%d-%m-%Y-%H", errors='ignore') #ignoring errors might cause data loss if formatting fails
    df = df.sort_values(by = 'Date')
    df.info()
        
    return df


