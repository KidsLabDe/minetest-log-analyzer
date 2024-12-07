import os
import re
from prettytable import PrettyTable
import telegram
import argparse
import time


from config import BOT_TOKEN, CHAT_ID, LOG_DIR


# define a list to store the chat messages
chat_messages = []
action_counts = {}

# add a dictionary to store the coordinates of each user's actions
user_coordinates = {}

# create a argument parser
parser = argparse.ArgumentParser(description='Parse the latest log files and send the results to a Telegram bot.')
parser.add_argument('--telegram', action='store_true', help='send results to Telegram bot')
parser.add_argument('--reset', action='store_true', help='reset all state files')
parser.add_argument('--logdir', help='set the log directory')
parser.add_argument('--file', help="choose one specific file to tail")

# parse the command-line arguments
args = parser.parse_args()


# create the Telegram bot
if args.telegram:
    bot = telegram.Bot(token=BOT_TOKEN)
else:
    bot = ""


if args.logdir:
    LOG_DIR = args.logdir
    
# reset all state files if the --reset argument is specified
if args.reset:
    for root, dirs, files in os.walk(LOG_DIR):
        for file in files:
            if file.endswith('.state'):
                state_file = os.path.join(root, file)
                os.remove(state_file)


def calculate_center(coordinates):
    sum_x = sum_y = 0
    for coord in coordinates:
        # x, y = map(int, re.findall(r'-?\d+', coord))  # extract x, y from the coordinate string
        sum_x += coord[0]
        sum_y += coord[1]
    center_x = sum_x / len(coordinates)
    center_y = sum_y / len(coordinates)
    return center_x, center_y

def clear():
 
    os.system('clear')
        
def parseLog(log_file, state_file):
    # Clearing the Screen
    clear()
    last_line = ''
    if os.path.isfile(state_file):
        with open(state_file, 'r') as file:
            last_line = file.read().strip()

    with open(log_file, 'r') as file:
        # skip lines that have already been parsed
        if last_line:
            for line in file:
                if line.strip() == last_line:
                    break
        # parse new lines
        for line in file:
            chat_match = re.search(r'CHAT: (.+)$', line)
            if chat_match:
                chat_message = chat_match.group(1)
                chat_messages.append(chat_message)
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
            if user_name not in action_counts:
                action_counts[user_name] = {}
            if action not in action_counts[user_name]:
                action_counts[user_name][action] = 0
            action_counts[user_name][action] += 1

            # add the coordinates to the user's list of coordinates
            coord_match = re.search(r'\((-?\d+),(-?\d+),(-?\d+)\)', line)
            if coord_match:
                coord = (int(coord_match.group(1)), int(coord_match.group(3)))  # (x, y)
                if user_name not in user_coordinates:
                    user_coordinates[user_name] = []
                user_coordinates[user_name].append(coord)

    # create a table to display the results
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

    # calculate the center for each user
    for user_name, coordinates in user_coordinates.items():
        center_x, center_y = calculate_center(coordinates)
        print(f"The center of {user_name}'s build blocks is at ({center_x}, {center_y})")
        

    # send the table to the Telegram bot if it has entries
    if args.telegram and len(action_counts) > 0:
        message = f'Log file: {log_file}\n{table}'
        bot.send_message(chat_id=CHAT_ID, text=message)
    # output the table to the console if it has entries
    elif not args.telegram and len(action_counts) > 0:
        print(f'Log file: {log_file}')
        print(table)

    # send the chat messages to the Telegram bot if it has entries
    if args.telegram and len(chat_messages) > 0:
        message = 'Chat messages:\n' + '\n'.join(chat_messages)
        bot.send_message(chat_id=CHAT_ID, text=message)
    # output the chat messages to the console if it has entries
    elif not args.telegram and len(chat_messages) > 0:
        print('Chat messages:')
        for message in chat_messages:
            print(message)


    # clear the chat messages and action counts for the next log file

    # write the last line of the log file that was parsed to the state file
    with open(state_file, 'w') as file:
        file.write(line.strip())    

# loop through all log files in the logs directory and its subdirectories

if args.file:
    log_file = args.file
    state_file = args.file + '.state'
    while True:
        parseLog(log_file, state_file)
        time.sleep(2)

    
for root, dirs, files in os.walk(LOG_DIR):
    for file in files:
        if file.endswith('.log'):
            log_file = os.path.join(root, file)
            state_file = os.path.join(root, file + '.state')
            print("Processing log file: " + log_file)
            parseLog(log_file, state_file)
            chat_messages.clear()
            action_counts.clear()

            # read the last line of the log file that was parsed

