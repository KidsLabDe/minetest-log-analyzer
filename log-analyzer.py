import os
import re
from prettytable import PrettyTable

# get a list of log files in the logs directory
log_dir = 'logs'
log_files = [f for f in os.listdir(log_dir) if os.path.isfile(os.path.join(log_dir, f))]

# prompt the user to select a log file
print('Select a log file to analyze:')
for i, log_file in enumerate(log_files):
    print(f'{i+1}. {log_file}')
selection = input('> ')
try:
    selection = int(selection)
    log_file = os.path.join(log_dir, log_files[selection-1])
except (ValueError, IndexError):
    print('Invalid selection')
    exit()

# define a dictionary to store the counts
action_counts = {}

with open(log_file, 'r') as file:
    for line in file:
        # extract user name and action
        user_name_match = re.search(r'\]:\s(\w+)', line)
        if user_name_match:
            user_name = user_name_match.group(1)
        else:
            continue
        action_match = re.search(r'digs|places', line)
        if action_match:
            action = action_match.group(0)
        else:
            continue
        
        # increment the count for this user and action
        if user_name not in action_counts:
            action_counts[user_name] = {}
        if action not in action_counts[user_name]:
            action_counts[user_name][action] = 0
        action_counts[user_name][action] += 1

# create a table to display the results‚
table = PrettyTable()
table.field_names = ['User', 'Digs', 'Places', 'Total']

# populate the table with the results
for user_name, counts in action_counts.items():
    digs = counts.get('digs', 0)
    places = counts.get('places', 0)
    total = digs + places
    table.add_row([user_name, digs, places, total])

# sort the table by the most actions
table.sortby = 'Total'

# print the table
print(table)
