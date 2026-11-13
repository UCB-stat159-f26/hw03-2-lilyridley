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
    y_min = int(np.floor(min(career_df['age_diff'].min(), 0) / 10) * 10)
    y_max = int(np.ceil(max(career_df['age_diff'].max(), 0)))
    ticks = list(range(y_min, y_max // 10 * 10 + 1, 10))
    ax.set_xlim(low, high)
    ax.set_xticks(range(low, high+1, 2))
    ax.set_ylim(y_min, y_max)
    ax.set_yticks(ticks)
    ax.set_yticklabels(['Same age' if t==0 else f'{t:+d}' for t in ticks])

def _add_text(ax, career_df):
    '''Add the labels, title, and legend'''
    low, high = int(career_df['player_age'].min()), int(career_df['player_age'].max())
    ticks = ax.get_yticks()
    ax.text(0, 1.06, 'Age:', transform=ax.transAxes, ha='left', va='bottom', color='gray')
    ax.text(-0.012, ticks[-1] - 5, 'Older \nthan \nopponent', transform=ax.get_yaxis_transform(), ha='right', va='center', color='dimgray')
    ax.text(-0.012, ticks[0] + 5, 'Younger \nthan \nopponent', transform=ax.get_yaxis_transform(), ha='right', va='center', color='dimgray')
    ax.set_title(f'Professional Matches, Age {low} to {high}', pad=105, fontweight='bold')
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.22), ncol=2, frameon=False)

def _style_axes(ax):
    '''Age axis on top, light gridlines, no frame, gray ticks'''
    ax.xaxis.tick_top()
    ax.grid(color='lightgray', linewidth=0.5)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_axisbelow(True)
    ax.tick_params(colors='dimgray', length=0)

def plot_age_gap(career_df):
    '''Make scatter plot of player age vs. age difference, colored by win/loss'''
    fig, ax = plt.subplots(figsize=(10, 6))
    _draw_points(ax, career_df)
    _set_axes(ax, career_df)
    _add_text(ax, career_df)
    _style_axes(ax)
    fig.tight_layout()
    plt.show()