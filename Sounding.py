import pandas as pd

def parse_balloon_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    launches = []
    current_launch = None

    for line in lines:
        if line.startswith("#"):
            if current_launch:
                launches.append(current_launch)
            current_launch = {'header': line.strip(), 'data': []}
        else:
            current_launch['data'].append(line.strip().split())

    if current_launch:
        launches.append(current_launch)

    launch_dataframes = []
    for launch in launches:
        header = launch['header']
        data = launch['data']

        header_info = header.split()
        station_id = header_info[0][1:]
        year = int(header_info[1])
        month = int(header_info[2])
        day = int(header_info[3])
        hour = int(header_info[4])

        columns = [
            'Station_ID', 'Year', 'Month', 'Day', 'Hour', 'Level', 
            'Pressure', 'Geopotential', 'Temperature', 'Relative_Humidity', 
            'Dew_Point_Depression', 'Wind_Direction', 'Wind_Speed'
        ]
        launch_dict = {col: [] for col in columns}

        for record in data:
            if len(record) >= 9:  # Ensure there are enough elements in the record
                launch_dict['Station_ID'].append(station_id)
                launch_dict['Year'].append(year)
                launch_dict['Month'].append(month)
                launch_dict['Day'].append(day)
                launch_dict['Hour'].append(hour)
                launch_dict['Level'].append(float(record[0]))
                
                # Remove any non-numeric characters and convert to float
                pressure = ''.join(filter(lambda x: x.isdigit() or x == '.', record[2]))
                launch_dict['Pressure'].append(float(pressure) if pressure else None)
                
                geopotential = ''.join(filter(lambda x: x.isdigit() or x == '.', record[3]))
                launch_dict['Geopotential'].append(float(geopotential) if geopotential else None)
                
                temperature = float(record[4][:-1]) * 0.1  # Multiply by 0.1 and handle the 'B' character
                launch_dict['Temperature'].append(temperature)
                
                # Handle relative humidity
                relative_humidity = ''.join(filter(lambda x: x.isdigit() or x == '.', record[5]))
                if relative_humidity == '-9999':
                    launch_dict['Relative_Humidity'].append(None)
                else:
                    launch_dict['Relative_Humidity'].append(float(relative_humidity) * 0.1)
                
                # Check for missing dew point depression data
                dew_point_depression = record[6]
                if dew_point_depression == '-9999':
                    launch_dict['Dew_Point_Depression'].append(None)
                else:
                    dew_point_depression = float(dew_point_depression[:-1]) * 0.1  # Multiply by 0.1 and handle the 'B' character
                    launch_dict['Dew_Point_Depression'].append(dew_point_depression)
                
                wind_direction = ''.join(filter(lambda x: x.isdigit() or x == '.', record[7]))
                launch_dict['Wind_Direction'].append(float(wind_direction) if wind_direction else None)
                
                wind_speed = ''.join(filter(lambda x: x.isdigit() or x == '.', record[8]))
                launch_dict['Wind_Speed'].append(float(wind_speed) if wind_speed else None)

        df = pd.DataFrame(launch_dict)
        launch_dataframes.append(df)

    return launch_dataframes

# Read data from the file
file_path = '/Users/annmarietschanz/Oklahoma/Data/Data.txt'
launch_dataframes = parse_balloon_data(file_path)

# Set pandas display options to prevent wrapping
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)
pd.set_option('display.colheader_justify', 'left')

# Now you can inspect launch_dataframes interactively without row wrapping
# For example, you can display the first DataFrame to see the settings in action
launch_dataframes[0]