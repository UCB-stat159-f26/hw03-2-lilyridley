import matplotlib.pyplot as plt
import numpy as np

def _draw_points(ax, career_df):
    '''Make a scatter plot of the matches, colored by result, plus the "same age" line'''
    won = career_df[career_df['result'] == 'W']
    lost = career_df[career_df['result'] == 'L']
    ax.scatter(won['player_age'], won['age_diff'], color='#5BC0E8', alpha=0.7, s=15, label='Match won')
    ax.scatter(lost['player_age'], lost['age_diff'], color='#7B2D8E', alpha=0.7, s=15, label='Match lost')
    ax.axhline(0, color='dimgray', linewidth=1)

def _set_axes(ax, career_df):
    '''Add axis limits, ticks, and labels fit to the player's data'''
    low = int(np.floor(career_df['player_age'].min()))
    high = int(np.ceil(career_df['player_age'].max()))
    limit = int(np.ceil(career_df['age_diff'].abs().max() / 10) * 10)
    ticks = list(range(-limit, limit+1, 10))
    ax.set_xlim(low, high)
    ax.set_xticks(range(low, high+1, 2))
    ax.set_yticks(-limit-2, limit+2)
    ax.set_yticklabels(['Same age' if t==0 else f'{t:+d}' for t in ticks])
    ax.xaxis.tick_top()