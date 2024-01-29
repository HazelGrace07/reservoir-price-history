import requests
import pandas as pd
import streamlit as st
from web3 import Web3

import datetime

def convert_timestamp_to_datetime(timestamp):

    return datetime.datetime.utcfromtimestamp(timestamp / 1000)

w3 = Web3()

def wei_to_ether(wei_amount):
    return int(wei_amount) / 10 ** 18

# Step 1: Fetch the data
url = "https://sample-62256-default-rtdb.europe-west1.firebasedatabase.app/nftPrices.json"
response = requests.get(url)
data = response.json()



# Step 2: Process the data
all_data = []
for collection, timestamps in data.items():
    for timestamp, prices in timestamps.items():
        all_data.append({
            'Collection': collection,
            'Timestamp': pd.to_datetime(timestamp, unit='ms'),  # Assuming timestamps are in milliseconds
            'BidPrice': wei_to_ether(prices['bidPrice']),
            'AskPrice': wei_to_ether(prices['floorPrice'])
        })

print(all_data)

df = pd.DataFrame(all_data)

# Step 3: Set up Streamlit and plot the data
st.title('NFT Prices Over Time')

# You might want to plot each collection separately
collections = df['Collection'].unique()
for collection in collections:
    st.subheader(f"Collection: {collection}")
    collection_df = df[df['Collection'] == collection].set_index('Timestamp')
    st.line_chart(collection_df[['BidPrice', 'AskPrice']])

# The Streamlit app will run when this script is executed
