# compare.py
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 24 Jul 2023

import pandas as pd
import os
import ast

from datetime import datetime


def compare_historic(df):
    # Create filepath for output files
    current_date = datetime.now().strftime('%Y-%m-%d-%H%M')
    filepath = f'historic/weekly_data/{current_date}'
    
    # Open "papers-we-have-seen.txt" which contains the unique indices of all papers observed to date
    with open('historic/papers-we-have-seen.txt','r') as f:
        # save entries as historic_set
        historic_set = ast.literal_eval(f.read()) 
    # Use the indices from df to create recent_set
    recent_set = set(df.index)
    
    '''
    # MAintenance scripts
    # Open "papers-we-have-seen.txt" which contains the unique indices of all papers observed to date
    with open('historic/papers-we-have-seen-test-version.txt','r') as f:
        # save entries as historic_set
        temp_set = ast.literal_eval(f.read()) 
    '''
    # Generate the novel set
    novel_set = recent_set - historic_set
    #historic_set = recent_set - temp_set
    #novel_set = recent_set - historic_set
    
    
    # Save novel data txt
    with open(f'{filepath}.txt','w') as f:
        f.write(str(novel_set))
        
    # Convert the set to a list and get the relevant rows from the df. Then
    # save as csv using filepath. And use utf-8 encoding to ensure special 
    # characters are captured.
    df_novel = df.loc[list(novel_set)]
    df_novel.to_csv(f'{filepath}.csv', encoding='utf-8')
    
    # Adjust the DataFrame before converting it to HTML
    df_novel = df_novel.reset_index(drop=True)  # Reset the index and drop the old index
    # Add hyperlinks to the titles
    df_novel['Title'] = df_novel.apply(lambda row: f'<a href="{row["Link"]}">{row["Title"]}</a>', axis=1)
    # Drop the 'Link' and 'Number' columns
    df_novel = df_novel.drop(['Link', 'Number'], axis=1)
    
    # create a custom order for continents
    source_order = ['NBER', 'FED-BOARD', 'FED-BOARD-NOTES', 'FED-ATLANTA', 'FED-CHICAGO', 'FED-CLEVELAND', 'FED-DALLAS', 'FED-NEWYORK', 'FED-SANFRANCISCO', 'BEA', 'BFI', 'BIS', 'BOE', 'ECB', 'IMF']
    # convert 'continent' column to 'Categorical' data type with custom order
    df_novel['Source'] = pd.Categorical(df_novel['Source'], categories=source_order, ordered=True)
    # sort the dataframe by 'continent' column
    df_novel = df_novel.sort_values(by='Source')
    # Reset the index of df_novel after sorting, and drop the old index
    df_novel = df_novel.reset_index(drop=True)
    print('Sorted DataFrame:\n', df)
    
    # Convert to HTML, set escape=False to prevent HTML syntax from being escaped
    html = df_novel.to_html(escape=False)
    # Save the HTML representation to a file
    with open(f'{filepath}.html', 'w', encoding='utf-8') as f:
        f.write(html)

        
    # Overwrite the historical with the new data
    with open('historic/papers-we-have-seen.txt','w') as f:
        f.write(str(historic_set | recent_set))  # union of the two sets  
  