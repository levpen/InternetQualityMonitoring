"""Module for running frontend part."""
import json
import sqlite3
import streamlit as st
import pandas as pd
from persistence import MetricsRepository
from collect_data import collect_data

# UI setup
st.set_page_config(
    page_title="Internet Quality Dashboard",
    page_icon="✅",
    layout="wide",
)
st.title('Internet Quality Dashboard')

def print_statistics(title: str, db: sqlite3) -> None :
  """Do prints Accessibility data on protocols and live graph on latency and loss."""
  # db_data = db.get_metrics(24)
  # print(db_data[0])
  # filtered_data = filter(lambda x: x[1] == title, db_data)
  # loss_data = [*map(lambda x: x[3], filtered_data)]
  # print(*filtered_data)
  # latency_data = [*map(lambda x: x[4], filtered_data)]
  # print(loss_data, latency_data)

  arr = collect_data(title)
  print(title)
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

#Database connection
db_path = "metrics.db"
with MetricsRepository(db_path) as metrics_repo:
  hosts = metrics_repo.get_hosts()
  col1, col2 = st.columns(2)
  with col2:
    st.dataframe({"Monitored hosts": hosts}, use_container_width=True)
  with col1:
  #Host addition
    new_host = st.text_input('Enter site or ip to add to hosts', 'ya.ru')
    if st.button('Add host'):
      try:
        metrics_repo.add_host(new_host)
        st.rerun()
      except sqlite3.IntegrityError:
        st.write('Enter new site')
    
    #Host deletion
    old_host = st.text_input('Enter site or ip to delete from hosts', '')
    if col1.button('Delete host'):
      # try:
        metrics_repo.delete_host(old_host)
        st.rerun()
      # except sqlite3.IntegrityError:
      #   st.write('Enter old site')

  #Host to monitor selection
  host_to_monitor = st.selectbox('Enter host to monitor', ['.'.join(item) for item in hosts], index=None, placeholder="Select host...")
  # print(host_to_monitor)
  if host_to_monitor:
    print_statistics(host_to_monitor, metrics_repo)

  





# def load_as_json(data: str) -> None:
#     """Loads data as json."""
#     json_data = json.dumps(data)


# # print_statistics(title)
# st.dataframe({"site": ["ya.ru", ""]})
# if st.button('Load data'):
#   load_as_json()