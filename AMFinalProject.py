#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install yfinance')
get_ipython().system('pip install bs4')
get_ipython().system('pip install nbformat')
get_ipython().system('pip install --upgrade plotly')


# In[28]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[29]:


import plotly.io as pio
pio.renderers.default = "iframe"


# In[30]:


import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# In[31]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
    from IPython.display import display, HTML
    fig_html = fig.to_html()
    display(HTML(fig_html))


# In[32]:


tsla = yf.Ticker("TSLA")


# In[33]:


tesla_data = tsla.history(period="max")


# In[34]:


tesla_data.reset_index(inplace=True)


# In[35]:


tesla_data.head()


# In[10]:


html_data = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'


# In[11]:


response = requests.get(html_data)


# In[12]:


soup = BeautifulSoup(response.text,'html.parser')


# In[13]:


rows = []
for tr in soup.find("tbody").find_all("tr"):
    cols = tr.find_all("td")
    date = cols[0].text.strip()
    revenue = cols[1].text.strip()
    rows.append([date, revenue])

tesla_revenue = pd.DataFrame(rows, columns=["Date", "Revenue"])
print(tesla_revenue)


# In[67]:


tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace('[\$,]', '', regex=True)


# In[68]:


tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue']!= ""]


# In[69]:


print(tesla_revenue.tail(5))


# In[50]:


gme = yf.Ticker("GME")


# In[51]:


gme_data = gme.history(period="max")
print(gme_data)


# In[52]:


gme_data.reset_index(inplace=True)
print(gme_data.head(5))


# In[53]:


html_data_2 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'


# In[54]:


soup = BeautifulSoup(response.text, 'html.parser')


# In[55]:


response = requests.get(html_data_2)


# In[56]:


rows = []
for tr in soup.find("tbody").find_all("tr"):
    cols = tr.find_all("td")
    date = cols[0].text.strip()
    revenue = cols[1].text.strip()
    rows.append([date, revenue])

gme_revenue = pd.DataFrame(rows, columns=["Date", "Revenue"])
print(gme_revenue)


# In[63]:


gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace('[\$,]', '', regex=True)


# In[64]:


print(gme_revenue.tail(5))


# In[2]:


make_graph(tesla_data, tesla_revenue,'Tesla')


# In[71]:


make_graph(gme_data, gme_revenue, 'GameStop')


# In[ ]:




