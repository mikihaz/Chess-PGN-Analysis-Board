# A Web Interface made with Streamlit to Analysis and Read a Chess Game in PGN format 
# The user can paste or upload the PGN Data
# Then User can see the match details
# User can also go through each and every move of the match
# User can also see the analysis of the match

# Importing the required libraries
import streamlit as st
import chess
import chess.pgn
import chess.engine
import io
import base64
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os
import sys
import re
import requests
import json
import urllib.request
import urllib.parse
import urllib.error
import ssl
import urllib.request, urllib.parse, urllib.error
import json
import ssl
import urllib.request, urllib.parse, urllib.error


# Setting the title of the Web App
st.title("Chess PGN Analysis")

# Setting the Subtitle of the Web App
st.subheader("A Web App to Analysis a Chess Game in PGN format")

# Setting the Text input for the PGN Data
st.markdown("### Enter the PGN Data")

# Setting the Text Area for the PGN Data
pgn_data = st.text_area("Paste the PGN Data here")

# Setting the File Uploader for the PGN Data
pgn_file = st.file_uploader("Upload the PGN File here")

# Setting the Engine Depth
st.markdown("### Enter the Engine Depth")

# Setting the Slider for the Engine Depth
engine_depth = st.slider("Select the Engine Depth", 1, 20, 10)

