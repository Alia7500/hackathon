import pandas as pd
import matplotlib.pyplot as plt
import random
import json


months = {
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'may': 5,
    'june': 6,
    'july': 7,
    'august': 8,
    'september': 9,
    'october': 10,
    'november': 11,
    'december': 12
}
req1 = {
  'period': 'november',
  'result_type': 'number',
  'calc_type': 'net_profit',
  'parameter': 'commodity_name'
}
req2 = {
    'period': 'january',
    'result_type': 'dynamics',
    'calc_type': 'planned_revenue',
    'parameter': 'basis_name_short'
}
req3 = {
    'period': 'december',
    'result_type': 'dynamics',
    'calc_type': 'full_expenditure',
    'parameter': 'commodity_name'
}


def REQUEST_RESULT(req_dict, name_csv):
    if req_dict['result_type'] == 'number':
        STR = ''
        res = dict()
        df = pd.read_csv(name_csv, delimiter=',')
        df = df.dropna(subset=[req_dict['calc_type'], req_dict['parameter'], 'date_unloading'])
        df['date_unloading'] = pd.to_datetime(df['date_unloading'])
        if req_dict['period'] in months:
            df = df[df['date_unloading'].dt.month == months[req_dict['period']]]
        else:
            df = df[df['date_unloading'].dt.year == int(req_dict['period'])]
        for name in set(df[req_dict['parameter']]):
            res[name] = df.loc[df[req_dict['parameter']] == name, req_dict['calc_type']].sum()
            STR += name + ': ' + str(res[name]) + '\n'
        return STR, None
    elif req_dict['result_type'] == 'dynamics':
        res = dict()
        df = pd.read_csv(name_csv, delimiter=',')
        df = df.dropna(subset=[req_dict['calc_type'], req_dict['parameter'], 'date_unloading'])
        df['date_unloading'] = pd.to_datetime(df['date_unloading'])
        if req_dict['period'] in months:
            df = df[df['date_unloading'].dt.month == months[req_dict['period']]]
            for name in set(df[req_dict['parameter']]):
                res[name] = df.loc[df[req_dict['parameter']] == name, req_dict['calc_type']].sum()
            plt.figure(figsize=(10, 10))
            flag = random.randint(0, 1)
            if flag:
                plt.pie(list(res.values()), labels=list(res.keys()), autopct='%1.1f%%')
            else:
                plt.bar(list(res.keys()), list(res.values()), color='green')
            plt.savefig('pic.jpeg')
        return None, 'pic.jpeg'

    return None, None


Nm = 'shipping_data_plan_general.csv'
rez = REQUEST_RESULT(req3, Nm)
if rez[0] != None:
    print(rez[0])
elif rez[1] != None:
    print('Check picture!')



