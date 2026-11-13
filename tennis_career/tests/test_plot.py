import matplotlib.pyplot as plt
import pandas as pd

from tennis_career import plot_age_gap

def test_plot_draws_every_match(monkeypatch):
    # Test that the plot function draws a point for every match
    monkeypatch.setattr(plt, 'show', lambda: None)
    df = pd.DataFrame({'result': ['W', 'L', 'W'], 'player_age': [20.0, 25.5, 30.2], 'age_diff': [-4.0, 3.5, 12.0]})
    plot_age_gap(df)
    ax = plt.gcf().axes[0]
    assert sum(len(c.get_offsets()) for c in ax.collections) == 3
    plt.close('all')