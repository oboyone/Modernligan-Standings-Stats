import csv

def full_leaderboard(target_key, player_data):
    full_leaderboard_winrate = {}
    for key, value in player_data.items():
        full_leaderboard_winrate[key] = value[target_key]
    full_leaderboard_winrate = sorted(full_leaderboard_winrate.items(), key=lambda x: x[1], reverse=True)
    return full_leaderboard_winrate

def top_ten_players(target_key, player_data, minimum_played_events=0):
    top_ten_dict = {}
    lowest_top_value = float('inf')  # Initialize lowest value to infinity
    
    for key, value in player_data.items():
        if value['Played Events'] < minimum_played_events:
            continue  # Skip players who don't meet the minimum played events requirement
        
        if len(top_ten_dict) < 10:
            top_ten_dict[key] = value[target_key]
            if value[target_key] < lowest_top_value:
                lowest_top_value = value[target_key]
        elif value[target_key] > lowest_top_value:
            # Find and remove the player with the lowest value
            min_key = min(top_ten_dict, key=top_ten_dict.get)
            del top_ten_dict[min_key]
            # Add the current player to the top ten
            top_ten_dict[key] = value[target_key]
            # Update the lowest value
            lowest_top_value = min(top_ten_dict.values())
    
    # Sort the dictionary in reverse order based on the target_key values
    sorted_top_ten_dict = dict(sorted(top_ten_dict.items(), key=lambda item: item[1], reverse=True))
    
    return sorted_top_ten_dict


            
            
def calculate_match_win_percentage(results):
    total_points = sum(int(date) for date in results if date.isnumeric())
    events_played = len([date for date in results if date.isnumeric()])
    matches_played = events_played * 4
    #print (total_points, matches_played)    
    if matches_played == 0:
        return 0
    else:
        matches_won = total_points / 3
        total_matches = matches_played
        #print(matches_won, total_matches)
        return matches_won / total_matches

def count_average_player_point(player_data):
    MATCH_POINTS_PER_WIN = 3
    #MATCHES_PER_EVENT = 4
    
    for player_id, player_info in player_data.items():
        total_score = 0
        date_count = 0
        
        for date in player_info.get('Results', []):
            if date.isnumeric():
                total_score += int(date)
                date_count += 1
        
        match_win_percentage = calculate_match_win_percentage(player_info.get('Results', []))
        player_data[player_id]['Match Win Percentage'] = match_win_percentage
        #print(match_win_percentage)
        player_data[player_id]['Played Events'] = date_count
        
    return player_data



def combine_rows(csv_files):
    player_data = {}

    # Read data from each CSV file
    for csv_file in csv_files:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')
            # Skip header if exists
            #next(reader, None)
            # Process each row
            for row in reader:
                #print(row)
                if player_data.get(row[0].title()):
                    player_data[row[0].title()]['Results'] = player_data[row[0].title()]['Results'] + row[1:]
                else:
                    player_data[row[0].title()] = {'Results':row[1:]}
    return player_data
    

csv_file_current_league = ['Modernligan Season 24 - Standings (New).csv']
historic_files = ['Modernligan Season 24 - Standings (New).csv', 'Modernligan Season 21 - Standings.csv', 'Modernligan Season 22 - Standings (New).csv', 'Modernligan Season 23 - Standings (New).csv', 'Modernligan Season 20 - Standings.csv']


player_data_current_season = combine_rows(csv_file_current_league)
player_data_current_season = count_average_player_point(player_data_current_season)
sorted_player_data_current_season = sorted(player_data_current_season.items())
leader_board_average_current_season = top_ten_players('Match Win Percentage', player_data_current_season)
leaderboard_events_played = top_ten_players('Played Events', player_data_current_season)

#player_data_all_seasons = combine_rows(historic_files)
#player_data_all_seasons = count_average_player_point(player_data_all_seasons)
#sorted_player_data_all_seasons= sorted(player_data_all_seasons.items())
#leader_board_average_all_seasons = top_ten_players_all_seasons('Match Win Percentage', player_data_all_seasons)


print(f"")
print(f"All players in current league statistics (printed in order of current standings)")
for player, data in player_data_current_season.items():
    #temp_score = float("{:.2f}".format(data.get('Match Win Percentage')))
    print(f"{player} have played {data.get('Played Events')} events and has an Match Win Percentage of {format(data.get('Match Win Percentage'), '.2%')} in the current league")

#sorted_current_leaderboard = sorted(leader_board_average_current_season.items(), key=lambda x: x[1], reverse=True)
#sorted_historic_leaderboard = sorted(leader_board_average_all_seasons.items(), key=lambda x: x[1], reverse=True)
#sorted_historic_all_leaderboards = full_leaderboard('Match Win Percentage', player_data_all_seasons)
print(f"")

print(f"Current league leaderboard of match win percentage")
# Printing the sorted dictionary
for name, value in leader_board_average_current_season.items():
    #temp_score=float("{:.2f}".format(value))
    print(f"{name} : {format(value, '.2%')}")

print(f"")

print(f"Current league leaderboard of events played")
# Printing the sorted dictionary
for name, value in leaderboard_events_played.items():
    #temp_score=float("{:.2f}".format(value))
    print(f"{name} : {value}")

print(f"")

""" print(f"Leaderboard of average points per event played for all historic leagues")

for name, value in sorted_historic_leaderboard:
    temp_score=float("{:.2f}".format(value))
    print(f"{name}: {temp_score}")

print(f"")

print(f"All players in all tracked leagues statistics")
for player, data in sorted_player_data_all_seasons:
    temp_score = float("{:.2f}".format(data.get('Match Win Percentage')))
    print(f"{player} have played {data.get('Played Events')} and has an match win percentage of {temp_score}")
 """
