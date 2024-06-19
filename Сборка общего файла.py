import pandas as pd
import matplotlib.pyplot as plt
import datetime


def CSV_PROCESSING(names_of_files):
    DateFrames = list()
    for name in names_of_files:
        DateFrames.append(pd.read_csv(name, delimiter=','))

    ((pd.merge(DateFrames[0], DateFrames[1][['request_number', 'date_unloading', 'volume_unloaded']], on='request_number',
    how='left')).sort_values(by='date_loading_planned')).to_csv("shipping_data_plan_general.csv", index=False)

    df_plan_general = pd.read_csv("shipping_data_plan_general.csv")

    df_delivery_costs = DateFrames[2][DateFrames[2]['cost_name'] == "Доставка автотранспортом (первичное перемещение)"]
    df_forwarding_costs = DateFrames[2][DateFrames[2]['cost_name'] == "Экспедирование при автоперевозках"]
    df_losses_costs = DateFrames[2][
        DateFrames[2]['cost_name'] == "Потери при автоперевозке в пределах норм естественной убыли"]

    merged_df = pd.merge(df_plan_general, df_delivery_costs[['request_number', 'value']], on='request_number',
                         how='left')
    merged_df = pd.merge(merged_df, df_forwarding_costs[['request_number', 'value']], on='request_number', how='left')
    merged_df = pd.merge(merged_df, df_losses_costs[['request_number', 'value']], on='request_number', how='left')

    merged_df.rename(columns={'value_x': 'delivery', 'value_y': 'forwarding', 'value': 'losses'}, inplace=True)

    merged_df['full_expenditure'] = merged_df[['delivery', 'forwarding', 'losses']].sum(axis=1)

    merged_df['planned_revenue'] = merged_df['price'] * merged_df['volume_planned']

    merged_df['actual_revenue'] = merged_df['price'] * merged_df['volume_unloaded']

    merged_df['net_profit'] = merged_df['actual_revenue'] - merged_df['full_expenditure']

    merged_df['volume_loss'] = merged_df['volume_planned'] - merged_df['volume_unloaded']

    merged_df.to_csv("shipping_data_plan_general.csv", index=False)


CSV_PROCESSING(['shipping_data_plan.csv', 'shipping_data_fact.csv', 'cost_data.csv'])
