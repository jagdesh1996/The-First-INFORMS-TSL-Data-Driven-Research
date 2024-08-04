import pandas as pd

# Load the dataset from the CSV file
file_path = 'C://Users//hassa//Documents//all_locations.csv'
data = pd.read_csv(file_path)

# Convert coordinates to the correct format by dividing by 1e6
columns_to_convert = ['sender_lng', 'sender_lat', 'recipient_lng', 'recipient_lat', 'grab_lng', 'grab_lat']

for col in columns_to_convert:
    data[col] = data[col] / 1e6

# Save the updated DataFrame to a new CSV file
new_file_path = 'C://Users//hassa//Documents//Updated_all_locations.csv'
data.to_csv(new_file_path, index=False)

# Verify the changes
print(data.head())
