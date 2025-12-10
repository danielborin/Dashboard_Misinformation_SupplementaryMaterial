import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
from pynamicalsys import PlotStyler

def plot_veen_diagram(df):
    df_size_keyword = df.groupby('Keyword Matches').size().reset_index(name='Fraction of # Publication')
    num_total_pub = len(df)

    df_size_keyword['Fraction of # Publication'] = round(df_size_keyword['Fraction of # Publication'] / num_total_pub, 4)

    # Create a new column with initials
    df_size_keyword['Initials'] = df_size_keyword['Keyword Matches'].apply(
        lambda x: ''.join(word[0].upper() for word in x.split('-'))
    )

    # Create a lookup dict for fractions
    lookup = { ''.join(sorted(k)): v for k, v in zip(df_size_keyword['Initials'], df_size_keyword['Fraction of # Publication']) }

    # Extract fractions for Venn diagram
    only_D = lookup.get('D', 0)
    only_F = lookup.get('F', 0)
    only_M = lookup.get('M', 0)
    D_F = lookup.get('DF', 0)
    F_M = lookup.get('FM', 0)
    D_M = lookup.get('DM', 0)
    D_F_M = lookup.get('DFM', 0)



    # Now create the subsets tuple for venn3:

    subsets = (
        only_D,     # Only D
        only_F,     # Only F
        D_F,                    # D & F only
        only_M,     # Only M
        D_M,                    # D & M only
        F_M,                    # F & M only
        D_F_M                          # D & F & M
    )

    # Create Venn diagram
    PlotStyler(fontsize = 15).apply_style()
    fig = plt.figure(figsize=(8,8))
    v = venn3(subsets=subsets, set_labels=('Disinformation', 'Fake News', 'Misinformation'), set_colors = ('darkviolet', 'deepskyblue', 'blue'))
    # plt.title("Venn Diagram of Keyword Matches")

    # Replace default labels with percentages
    for subset in v.subset_labels:
        if subset:  # Check label is not None (some subsets may be empty)
            # Get the numeric value from the label text (it's a float)
            val = float(subset.get_text())
            # Format as percentage with 1 decimal place
            subset.set_text(f"{val*100:.2f}%")

    return fig

def split_keyword(df):
    df['Keyword Split'] = df['Keyword Matches'].str.split('-')

    # Explode to make one row per keyword
    df = df.explode('Keyword Split')


    # Group by year and keyword, count occurrences
    df_yearly_keyword_count = (
        df
        .groupby(['Publication Year', 'Keyword Split'])
        .size()
        .reset_index(name='Count')
        .rename(columns={'Keyword Split': 'Keyword'})
    )

    # Pivot to get years as rows, keywords as columns
    df_pivot = df_yearly_keyword_count.pivot(index='Publication Year', columns='Keyword', values='Count')

    # Replace NaN with 0 (for years with no publications for a keyword)
    df_pivot = df_pivot.fillna(0).astype(int)

    # Create a new column 'Total Keywords' which is the sum of all keyword columns for each year
    df_pivot['All Keywords'] = df_pivot.sum(axis=1)

    # Optional: reset index to make 'Publication Year' a column again
    df_pivot = df_pivot.reset_index()

    return df_pivot