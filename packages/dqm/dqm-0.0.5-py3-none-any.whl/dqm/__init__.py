import numpy as np
import pandas as pd
import os
import json
import re
from datetime import datetime
from shutil import move
import pytz


############################################################
#  HELPER FUNCTIONS.   #
############################################################
def custom_function(timestamp_string):
    # Make sure timestamp is in string format.
    timestamp_str = timestamp_string.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    #print("custom_function timestamp_string: ",timestamp_string.split(" ")[1],"\n")
    return timestamp_str.split(" ")[1]

#"04:42:43.358"
def format_ts_seconds(timestamp_str):
    #print("format_ts_seconds ():/  timestamp_str: ",timestamp_str,timestamp_str.split(".")[0])
    return timestamp_str.split(".")[0]



def extract_and_convert(x):
    try:
        return int(x.split("_")[1]) #int(x[1])
    except (IndexError, ValueError):
        return None  # or any default value you prefer.
    
# to check the correctness of the data.
def percentage_zeros_hr(df_hr):
    # Count the total number of zeros
    total_zeros = (df_hr == 0).sum().sum()
    # Count the total number of elements
    total_elements = df_hr.size
    # Calculate the percentage of zeros
    percentage_zeros = (total_zeros / total_elements) * 100
    return percentage_zeros

def snr_hr(df_hr):
     
    try:
        snr_value =df_hr["bpm"].mean()/df_hr["bpm"].std()
        # Code that might raise an error
        # result = 10 / 0  # This will raise ZeroDivisionError
    except ZeroDivisionError as e:
        snr_value = -1
        # Handle the specific error
        print(f"Error occurred: {e}")

    return snr_value

def percentage_missing_hr(df):

    # Create DataFrame
    df = pd.DataFrame(df)
    # Convert watch_timestamp to datetime
    df['watch_timestamp'] = pd.to_datetime(df['watch_timestamp'])
    # Generate a complete time index.
    start_time = df.iloc[0]["watch_timestamp"] #df['watch_timestamp'].min()
    end_time = df.iloc[-1]["watch_timestamp"] #df['watch_timestamp'].max()
    print("start_time,end_time: ",start_time,end_time)
    full_time_index = pd.date_range(start=start_time, end=end_time, freq='1S')
    print("df: ",df.shape[0],"len(full_time_index): ",len(full_time_index))
    expected_number_of_samples = len(full_time_index)
    recieved_number_of_samples = df.shape[0]
    percentage_missing=  ((expected_number_of_samples-recieved_number_of_samples)/expected_number_of_samples)*100
    print("Percentage of missing data: ", percentage_missing)
    return percentage_missing

# ['x(m/s^2)', 'y(m/s^2)', 'z(m/s^2)', 'internal_ts', 'watch_timestamp',
# 'relative_timestamp', 'Session_ID', 'PID', 'ts_only', 'ts_seconds']
                        
def snr_gyro(df_gry):
    snr_gyr_x = df_gry["x(rad)"].mean()/df_gry["x(rad)"].std()
    snr_gyr_y = df_gry["y(rad)"].mean()/df_gry["y(rad)"].std()
    snr_gyr_z = df_gry["z(rad)"].mean()/df_gry["z(rad)"].std()
    return snr_gyr_x ,snr_gyr_y,snr_gyr_z
def snr_acc(df_acc):

    snr_acc_x = df_acc["x(m/s^2)"].mean()/df_acc["x(m/s^2)"].std()
    snr_acc_y = df_acc["y(m/s^2)"].mean()/df_acc["y(m/s^2)"].std()
    snr_acc_z = df_acc["z(m/s^2)"].mean()/df_acc["z(m/s^2)"].std()
    return snr_acc_x,snr_acc_y,snr_acc_z


def percentage_missing_imu(df):

    # Create DataFrame
    df = pd.DataFrame(df)
    # Convert watch_timestamp to datetime
    df['watch_timestamp'] = pd.to_datetime(df['watch_timestamp'])
    # Generate a complete time index.
    start_time = df.iloc[0]["watch_timestamp"] #df['watch_timestamp'].min()
    end_time = df.iloc[-1]["watch_timestamp"] #df['watch_timestamp'].max()
    print("start_time,end_time: ",start_time,end_time)
    full_time_index = pd.date_range(start=start_time, end=end_time, freq='33.33ms')
    print("df: ",df.shape[0],"len(full_time_index): ",len(full_time_index))
    expected_number_of_samples = len(full_time_index)
    recieved_number_of_samples = df.shape[0]
    percentage_missing=  ((expected_number_of_samples-recieved_number_of_samples)/expected_number_of_samples)*100
    print("Percentage of missing data: ", percentage_missing)
    return percentage_missing


