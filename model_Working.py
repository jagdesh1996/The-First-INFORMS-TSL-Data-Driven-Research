import pandas as pd
from datetime import timedelta
import numpy as np


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def process_first_100_orders(data, max_distance_km, max_time_window, max_sender_distance_km):
    grouped_orders = []
    ungrouped_orders = data.copy()

    while not ungrouped_orders.empty:
        current_order = ungrouped_orders.iloc[0]
        current_group = [current_order['order_id']]
        current_time = current_order['platform_order_time']
        current_sender_lat = current_order['sender_lat']
        current_sender_lng = current_order['sender_lng']
        current_recipient_lat = current_order['recipient_lat']
        current_recipient_lng = current_order['recipient_lng']

        indices_to_drop = [0]

        for i in range(1, len(ungrouped_orders)):
            other_order = ungrouped_orders.iloc[i]
            time_diff = other_order['platform_order_time'] - current_time

            if time_diff <= max_time_window:
                sender_distance = haversine(
                    current_sender_lng, current_sender_lat,
                    other_order['sender_lng'], other_order['sender_lat']
                )
                recipient_distance = haversine(
                    current_recipient_lng, current_recipient_lat,
                    other_order['recipient_lng'], other_order['recipient_lat']
                )

                if sender_distance <= max_sender_distance_km and recipient_distance <= max_distance_km:
                    current_group.append(other_order['order_id'])
                    indices_to_drop.append(i)
            else:
                break  # No need to check further as the list is time-ordered

        grouped_orders.append(current_group)
        ungrouped_orders = ungrouped_orders.drop(indices_to_drop).reset_index(drop=True)

    return grouped_orders


# File path and parameters
file_path = "C:/Users/hassa/Documents/Updated_all_delivery_times.csv"
max_distance_km = 3
max_sender_distance_km = 1.5
max_time_window = timedelta(minutes=3)

# Read the first 100 rows
data = pd.read_csv(file_path, nrows=100)

# Convert relevant columns to datetime
data['platform_order_time'] = pd.to_datetime(data['platform_order_time'])

# Process the first 100 orders
grouped_orders = process_first_100_orders(data, max_distance_km, max_time_window, max_sender_distance_km)

# Convert the results to a DataFrame and save
grouped_orders_df = pd.DataFrame({'Group': range(len(grouped_orders)), 'Orders': grouped_orders})
grouped_orders_df.to_csv("C:/Users/hassa/Documents/grouped_orders_100.csv", index=False)

print("Grouped orders identified and saved to 'grouped_orders_100.csv'")
