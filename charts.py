import pandas as pd

import matplotlib.pyplot as plt

def plot_donut_chart(data):
    plt.rcParams["figure.figsize"] = (2,2)
    data['Ποσό'] = pd.to_numeric(data['Ποσό'], errors='coerce')
    summary = data.groupby('Τύπος')['Ποσό'].sum()
    colors = ['green' if typ == 'Έσοδο' else 'red' for typ in summary.index]
    
    fig, ax = plt.subplots()
    ax.pie(summary, startangle=90, colors=colors, wedgeprops=dict(width=0.3))
    # ax.pie(summary, labels=summary.index, autopct='%1.1f%%', startangle=90, colors=colors, wedgeprops=dict(width=0.3))
    centre_circle = plt.Circle((0,0), 0.70, fc='none')
    fig.gca().add_artist(centre_circle)
    ax.axis('equal')
    fig.patch.set_alpha(0.0)
    
    total_income = summary.get('Έσοδο', 0)
    total_expense = summary.get('Έξοδο', 0)
    plt.text(.5, 1, f'Έσοδα: {total_income}', color='green', fontsize=6)
    plt.text(-1.5, 1, f' Έξοδα: {total_expense}', color='red', fontsize=6)
    
    return fig
