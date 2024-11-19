#!/usr/bin/env python3
"""
Grid Message Decoder for Google Docs
Fetches and decodes character-based grid messages from a published Google Doc.

Requirements:
- beautifulsoup4
- pandas
- urllib3

Functions:
    fetch_table: Retrieves HTML table from URL
    fetch_data: Converts HTML table to pandas DataFrame
    create_df: Organizes coordinate data into sorted DataFrame
    decode_msg: Renders character grid from coordinates
    main: Orchestrates the decoding process
"""

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

def fetch_table(debug: int, url: str) -> list:
    """
    Fetches and parses HTML table from a URL.
    
    Args:
        debug: Enable debug output if 1
        url: URL to fetch HTML from
        
    Returns:
        List of BeautifulSoup table elements
    """
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')

    if debug == 1:
        print(html)

    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all('table')

def fetch_data(debug: int, table: list) -> pd.DataFrame:
    """
    Extracts data from HTML table into DataFrame.
    
    Args:
        debug: Enable debug output if 1
        table: List of BeautifulSoup table elements
        
    Returns:
        DataFrame containing table data
        
    Raises:
        SystemExit: If no table is found
    """
    if not table:
        print("\nERROR: No table found! Can not continue.\n")
        exit(1)
        
    table_data = pd.read_html(StringIO(str(table[0])), header=0)[0]

    if debug == 1:
        print(f'TYPE: {type(table_data)}, SIZE: {len(table_data)}')
        print(table_data)

    return table_data

def create_df(debug: int, table_data: pd.DataFrame) -> pd.DataFrame:
    """
    Creates and sorts DataFrame from coordinate data.
    
    Args:
        debug: Enable debug output if 1
        table_data: Input DataFrame with coordinate data
        
    Returns:
        Sorted DataFrame with columns ['cols', 'chars', 'rows']
    """
    # Extract coordinates and characters
    df = pd.DataFrame({
        'cols': table_data['x-coordinate'],
        'chars': table_data['Character'],
        'rows': table_data['y-coordinate'],
    })

    if debug == 1:
        print("Data Frame (not sorted)")
        print(df)

    # Sort by row then column
    df_sorted = df.sort_values(by=['rows', 'cols'], ascending=[True, True])
    
    if debug == 1:
        print("Data Frame (sorted)")
        print(df_sorted)

    return df_sorted

def decode_msg(debug: int, df_sorted: pd.DataFrame) -> bool:
    """
    Prints 2D grid representation of characters.
    
    Args:
        debug: Enable debug output if 1
        df_sorted: Sorted DataFrame with character positions
        
    Returns:
        True if message was successfully decoded
    """
    last_row = 0
    track_col = 0
    print()
    
    for index, row in df_sorted.iterrows():
        this_row = row['rows']
        this_col = row['cols']
        this_char = row['chars']

        # Handle new rows
        if this_col == 0 and this_row > last_row:
            print()
            track_col = 0

        # Print empty columns
        while track_col < this_col:
            print(" ", end="")
            track_col += 1

        # Print character
        print(this_char, end="")
        track_col += 1
        last_row = this_row

    print()
    return True

def main(url: str) -> None:
    """
    Main function to orchestrate the grid message decoding.
    
    Args:
        url: URL of published Google Doc containing the grid message
    """
    debug = 0
    table = fetch_table(debug, url)
    data = fetch_data(debug, table)
    df_sorted = create_df(debug, data)
    ret_val = decode_msg(debug, df_sorted)
    print(f'\nProcess finished with value of {ret_val}.\n')

if __name__ == "__main__":
    # Source document with unicode chars
    url = "https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub"
    main(url)