#!/usr/bin/env python
# coding: utf-8

# '''We need to extract a list with all 'the best' award winners,
# for this purpose Selenium scraping will be used'''

# In[4]:


get_ipython().run_line_magic('pip', 'install selenium')
from selenium import webdriver


# In[5]:


get_ipython().run_line_magic('pip', 'install webdriver-manager')
from webdriver_manager.chrome import ChromeDriverManager


# In[7]:


from selenium.webdriver.chrome.options import Options

opciones=Options()

opciones.add_experimental_option('excludeSwitches', ['enable-automation'])
opciones.add_experimental_option('useAutomationExtension', False)
opciones.headless=False    # si True, no aperece la ventana (headless=no visible)
opciones.add_argument('--start-maximized')         # comienza maximizado
opciones.add_argument('user-data-dir=selenium')    # mantiene las cookies
opciones.add_extension('../driver/adblock.crx')       # adblocker
opciones.add_argument('--incognito')


# '''Loading the web page where data will be extracted from'''

# In[36]:


PATH=ChromeDriverManager().install()
URL='https://www.goal.com/en-in/news/fifa-womens-world-player-of-the-year-award-winners/blt12683887fe8df959'
driver=webdriver.Chrome(PATH)
driver.get(URL)
acepto=driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
acepto.click()


# ''' Scraping the table that has the data needed'''

# In[37]:


table = driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div/article/main/div[3]/div/div[4]')

players = table.find_elements_by_tag_name('tr')

players


# ''' We apply a function that appends each player with the year in which the award was given'''

# In[38]:


import functions as fn


# In[39]:


players2 = transform(players)


# In[50]:


import pandas as pd
col_names=players2[0]
data=players2[1:]
df2=pd.DataFrame(data, columns=col_names)


# In[51]:


df2['Club']=[c.replace('Carolina Courage/Birgit Prinz', 'FFC Frankfurt') for c in df2.Club]


# '''We need another table that combines with this one and add the nationality of each player;
# in this time, we will use BeautifulSoup method'''

# In[43]:


import requests as req

from bs4 import BeautifulSoup as bs
url='https://www.topendsports.com/sport/soccer/list-player-of-the-year-women.htm'
html=req.get(url).content
soup=bs(html, 'html.parser')


# In[44]:


tabla=soup.find('div',{'class':'table-responsive'})
tabla2=tabla.find('table',{'class':'list'})


# In[45]:


filas=tabla2.find_all('tr')
filas=[f.text.strip().split('\n') for f in filas]


# In[46]:


col_names=filas[0]
data=filas[1:]
df3=pd.DataFrame(data, columns=col_names)


# In[47]:


df3 = df3.rename(str.title, axis='columns')
df3 = df3.sort_values(by = ['Year'], ascending=True).reset_index().drop('index',axis=1)


# In[48]:


df3['Player']=[c.replace('Nadine Keßler', 'Nadine Kebler') for c in df3.Player]
df3['Player'] = df3['Player'].apply(lambda x: x.strip())


# In[52]:


df4 = pd.merge(df2,df3,how="inner")


# In[53]:


df4['Nationality']=[c.replace('USA', 'United States') for c in df4.Nationality]
df4['Nationality']=[c.replace('The Netherlands', 'Netherlands') for c in df4.Nationality]


# In[ ]:


df4.to_csv('./data/players.csv', index=False)
