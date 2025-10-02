import pandas as pd

df = pd.read_csv('Prem_Stats.csv')

converted = pd.DataFrame({
    'name': df['Player'],
    'nation': df['Nation'],
    'position': df['Pos'],
    'age': df['Age'],
    'matches_played': df['MP'],
    'starts': df['Starts'],
    'minutes_played': df['Min'],
    'goals': df['Gls'],
    'assists': df['Ast'],
    'penalties_scored': df['PK'],
    'yellow_cards': df['CrdY'],
    'red_cards': df['CrdR'],
    'expected_goals': df['xG'],
    'expected_assists': df['xAG'],
    'team_name': df['Team']
})

converted.to_csv('stats.csv', index=False)
print("Fixed stats.csv created")