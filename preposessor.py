import re
import pandas as pd


def preprocess(data):
    pattern = '\d+/\d+/\d+,\s\d+:\d+\s\w\w\s-\s'
    message = re.split(pattern, data)[1:]

    dates = re.findall(pattern, data)

    da = []
    am_pm = []
    for val in dates:
        if "PM" in val:
            da.append(val.replace('PM', ''))
            am_pm.append('PM')
        else:
            da.append(val.replace('AM', ''))
            am_pm.append('AM')

    df = pd.DataFrame({'user_message': message, 'Message_data': da})

    # convert message_data type
    df['Message_data'] = pd.to_datetime(df['Message_data'], format='%m/%d/%y, %H:%M - ')

    df.rename(columns={'Message_data': 'datetime'}, inplace=True)

    users = []
    messages = []

    for mess in df['user_message']:
        l = mess.split(':')
        if l[1:]:
            users.append(l[0])
            messages.append(l[1])
        else:
            users.append('Group_notification')
            messages.append(l[0])

    df['User'] = users
    df['Message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['Year'] = df['datetime'].dt.year
    df['Month'] = df['datetime'].dt.month_name()
    df['Month_num'] = df['datetime'].dt.month
    df['Day'] = df['datetime'].dt.day
    df['Hour'] = df['datetime'].dt.hour
    df['Minute'] = df['datetime'].dt.minute
    df['date'] = df['datetime'].dt.date
    df['day_name'] = df['datetime'].dt.day_name()
    df['am_pm'] = am_pm

    period = []
    i = 0
    for hour in df[['day_name', 'Hour']]['Hour']:
        if hour == 12:
            period.append(str(hour) + '-' + str('1') + ' ' + am_pm[i])
        else:
            period.append(str(hour) + '-' + str(hour + 1) + ' ' + am_pm[i])
        i += 1

    df['period'] = period

    return df
