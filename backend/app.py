"""Module for running frontend part."""
import streamlit as st
import pandas as pd
from collect_data import collect_data

#UI setup
st.set_page_config(
    page_title="Internet Quality Dashboard",
    page_icon="✅",
    layout="wide",
)
st.title('Internet Quality Dashboard')

#Input field
title = st.text_input('Enter site or ip', 'ya.ru')
st.write('The current site is', title)

def print_statistics(title: str) -> None :
  """Do prints Accessibility data on protocols and live graph on latency and loss."""
  arr = collect_data(title)
  accessibility = arr['accessibility']
  loss = []
  latency = []
  placeholder = st.empty()
  
  for _ in range(100):
    arr = collect_data(title)
    loss.append(arr['loss'])
    latency.append(arr['latency'])

    with placeholder.container():
      #Accessibility table
      st.markdown("### "+title+" protocols accessibility")
      df = pd.DataFrame(accessibility, columns=['Protocol', 'Status'])
      st.write(df)

      #Loss and Latency graph
      st.markdown("### Detailed Loss and Latency graph")
      chart_data = pd.DataFrame(
        {'Loss': loss, 'Latency': latency}
      )
      st.line_chart(chart_data)
      st.dataframe(chart_data)

print_statistics(title)


