
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]


def draw_line_plot():
    df_copy = df.copy()
    fig, ax = plt.subplots(figsize=(15, 5))

    ax.plot(df_copy.index, df_copy['value'], color='red')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    df_copy = df.copy()
    df_copy['year'] = df_copy.index.year
    df_copy['month'] = df_copy.index.month

    df_group = df_copy.groupby(['year', 'month'])['value'].mean()
    df_group = df_group.unstack()

    fig, ax = plt.subplots(figsize=(10, 7))
    df_group.plot(kind='bar', ax=ax)

    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(
        title='Months',
        labels=[
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
    )

    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    df_copy = df.copy().reset_index()

    df_copy['year'] = df_copy['date'].dt.year
    df_copy['month'] = df_copy['date'].dt.strftime('%b')
    df_copy['month_num'] = df_copy['date'].dt.month
    df_copy = df_copy.sort_values('month_num')

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    sns.boxplot(data=df_copy, x='year', y='value', ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    sns.boxplot(
        data=df_copy,
        x='month',
        y='value',
        order=[
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ],
        ax=axes[1]
    )
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    fig.savefig('box_plot.png')
    return fig
