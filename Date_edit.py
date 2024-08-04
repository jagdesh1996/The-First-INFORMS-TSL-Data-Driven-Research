import pandas as pd

# Load the dataset
file_path = 'C://Users//hassa//Documents//Date_only.csv'
data = pd.read_csv(file_path)

# Convert the 'date' column to datetime format
data['date'] = pd.to_datetime(data['date'], format='%Y%m%d')

# Add a new column for the day of the week
data['day_of_week'] = data['date'].dt.strftime('%A')

# Save the updated DataFrame to a new CSV file
new_file_path = 'C://Users//hassa//Documents//Updated_date.csv'
data.to_csv(new_file_path, index=False)

# Verify the changes
print(data[['date', 'day_of_week']])
