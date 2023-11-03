import requests,json
import pandas as pd
import os
import dotenv

import altair as alt

import streamlit as st

import plotly.express as px

import os
print(os.getcwd())

dotenv.load_dotenv()


api_key=os.getenv("API_KEY")
sheet_id=os.getenv("SHEET_ID")
#sheet_id = "1iSOLIKLDOn3uysScNUDOY9uR5qHx4HXiJhAT2wXB33Y"

range_name = 'Sheet1!A1:K9729'



# Build the URL for the Google Sheets API
url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{range_name}?key={api_key}'


response = requests.get(url)


data = response.json()
values = data.get('values', [])
df=pd.DataFrame(values[1:],columns=values[0])




df['complaint_id'] = df['complaint_id'].astype(int)

#st.dataframe(df)

#st.table(df)

#df['complaint_id']

#df['complaint_id'].sum()
#complaints_with_closed=df[df['company_response'].str.contains("Closed")]
st.set_page_config(
    page_title="Financial Complaints Dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)




st.title("Financial Consumer Complaints")

#st.subheader(subheader)


#st.write("Display Data for 'All States' or 'any' State")
#col2=st.columns(5)


container1=st.container()
con_col1,con_col2,con_col3,con_col4,con_col5=container1.columns(5)
with con_col5:
    selected_state = st.selectbox("Select State", ["All States"] + df['state'].unique().tolist())

    if selected_state == "All States":
        filtered_df = df
        subhead=f"Display Data for {selected_state}"
    else:
        filtered_df = df[df['state'] == selected_state]
        subhead=f"Display Data for {selected_state}"

st.subheader(subhead)

with con_col1:
    

    st.metric("Total Number of Complaints", filtered_df['complaint_id'].sum())
  

with con_col2:

    complaints_with_closed = filtered_df[filtered_df['company_response'].str.contains("Closed")]
    total_closed_complaints = complaints_with_closed['complaint_id'].sum()
    st.metric("Total Number of Complaints with Closed Status", total_closed_complaints)
 
with con_col3:
    timely_ratio=filtered_df[filtered_df['timely'] =='Yes']['complaint_id'].sum()/filtered_df['complaint_id'].sum()
    st.metric("% of Timely Responded Complaints",f"{timely_ratio:.2%}")

with con_col4:
    st.metric("Total Number of Complaints with In Progress Status",filtered_df[filtered_df['company_response'] =='In progress']['complaint_id'].sum())
#df['company_response'].value_counts()


#complaints_with_closed['complaint_id'].sum()

#df[df['timely'] =='Yes']['complaint_id'].sum()/df['complaint_id'].sum()



#df['company_response'].value_counts()


#df[df['company_response'] =='In progress']['complaint_id'].sum()

container2=st.container()
chart1, chart2 = container2.columns(2)
chart_data = filtered_df.groupby('product')['complaint_id'].sum().reset_index()
chart = alt.Chart(chart_data).mark_bar().encode(
    x='complaint_id:Q',
    y=alt.Y('product:N', sort='-x'),
    color='product:N',
).properties(
    title="Number of Complaints by Product",
    width=300
)

chart1.altair_chart(chart, use_container_width=True)

chart_data=filtered_df.groupby('month_year')['complaint_id'].sum().reset_index().sort_values(by='month_year')
line_chart = alt.Chart(chart_data).mark_line().encode(
    x=alt.X('month_year:O'),
    y=alt.Y('complaint_id:Q'),
    tooltip=['month_year:O', 'complaint_id:Q'],
).properties(
    title='Number of Complaints Over Time',
    width=400
)


chart2.altair_chart(line_chart, use_container_width=True)

#df.groupby('month_year')['complaint_id'].sum().reset_index().sort_values(by='month_year')


#df.columns

#df['month_year'].astype(date)

#df['month_year'] = pd.to_datetime(df['month_year'], errors='coerce')


container3=st.container()
chart3, chart4 = container3.columns(2)
chart_data = filtered_df.groupby('submitted_via')['complaint_id'].sum().reset_index()
pie_chart = alt.Chart(chart_data).mark_arc().encode(
    color='submitted_via:N',
    angle=alt.X('complaint_id:Q', title='Complaints'),
    tooltip=['submitted_via:N', 'complaint_id:Q'],
).properties(
    title='Complaints by Submission Method',
    width=400
)

chart3.altair_chart(pie_chart, use_container_width=True)


treemap_data = filtered_df.groupby(['issue','sub_issue'])['complaint_id'].sum().reset_index()
treemap = px.treemap(treemap_data, path=['issue', 'sub_issue'], values='complaint_id', title='Number Over Complaints by Issue and Sub-Issue')
treemap.update_layout(
    title='Number Over Complaints by Issue and Sub-Issue'
    )
treemap.update_traces(hovertemplate='Number of complaints: %{value}')
treemap.update_traces(textinfo="label+value")

chart4.plotly_chart(treemap,use_container_width=True, )

#chart4.altair_chart(treemap, use_container_width=True)

st.markdown("Designed by Muneeza")

