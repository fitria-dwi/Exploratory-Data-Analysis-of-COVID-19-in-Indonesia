#!/usr/bin/env python
# coding: utf-8

# **Author: Fitria Dwi Wulandari (wulan391@sci.ui.ac.id) - September 16, 2021.**

# # Exploratory Data Analysis of COVID-19 in West Java

# ## **COVID-19 Cases in Indonesia**

# ### Data Loading

# #### Accessing covid19.go.id

# In[13]:


import requests
resp = requests.get('https://data.covid19.go.id/public/api/update.json')


# #### Status Code

# In[14]:


print(resp)


# It indicates that the REST API successfully carried out whatever action the client requested. 

# #### Headers

# In[15]:


print(resp.headers)


# #### Extracting Response

# In[16]:


cov_id_raw  = resp.json()


# In[17]:


print('Length of cov_id_raw : %d.' %len(cov_id_raw))
print('Component of cov_id_raw  : %s.' %cov_id_raw.keys())
cov_id_update = cov_id_raw['update']


# ### Understanding COVID-19 Cases in Indonesia

# In[18]:


# When is the update date for the new cases?
print('Update date of new cases :', cov_id_update['penambahan']['tanggal'])
# What is the number of new recovered cases?
print('Number of new recovered cases :', cov_id_update['penambahan']['jumlah_sembuh'])
# What is the number of new deaths cases?
print('Number of new deaths cases :', cov_id_update['penambahan']['jumlah_meninggal'])
# What is the total number of positive cases?
print('Total number of positive cases :', cov_id_update['total']['jumlah_positif'])
# What is the total number of deaths cases
print('Total number of deaths cases :', cov_id_update['total']['jumlah_meninggal'])


# ## **COVID-19 Cases in West Java**

# ### Data Loading

# In[19]:


import requests
resp_jabar = requests.get('https://data.covid19.go.id/public/api/prov_detail_JAWA_BARAT.json')
cov_jabar_raw = resp_jabar.json()


# ### Understanding COVID-19 Cases in West Java

# In[20]:


print('Main element names:\n', cov_jabar_raw.keys())
print('\nTotal number of COVID-19 cases in West Java : %d' %cov_jabar_raw['kasus_total'])
print('Percentage of deaths from COVID-19 in West Java : %f.2%%' %cov_jabar_raw['meninggal_persen'])
print('Percentage of recovery rate from COVID-19 in West Java : %f.2%%' %cov_jabar_raw['sembuh_persen'])


# ### Data Preprocessing

# In[21]:


import numpy as np
import pandas as pd

cov_jabar = pd.DataFrame(cov_jabar_raw['list_perkembangan'])

print('Information of data frame:')
cov_jabar.info()
print('\nTop 5 data:\n', cov_jabar.head())


# #### Correcting

# Features that require correction are as follows:
# 1. Delete the `CARE_OR_ISOLATED` column and all columns that contain cumulative values.
# 2. Change the writing format of all columns to lowercase.
# 3. Renaming the `case` column to `new_case`.
# 4. Reformat data type in `date` column using pd.to_datetime.

# In[22]:


cov_jabar_tidy = (cov_jabar.drop(columns=[item for item in cov_jabar.columns 
                                               if item.startswith('AKUMULASI') 
                                                  or item.startswith('DIRAWAT')])
                           .rename(columns=str.lower)
                           .rename(columns={'kasus': 'kasus_baru'})
                  )
cov_jabar_tidy['tanggal'] = pd.to_datetime(cov_jabar_tidy['tanggal']*1e6, unit='ns')

print('Top 5 data:\n', cov_jabar_tidy.head())


# ### Visualization

# #### **Daily Cases of COVID-19**

# **1. Daily Positive Cases of COVID-19 in West Java**

# In[23]:


import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.clf()
fig, ax = plt.subplots(figsize=(15,8))
ax.bar(data=cov_jabar_tidy, x='tanggal', height='kasus_baru', color='orange')
fig.suptitle('Daily Positive Cases of COVID-19 in West Java', 
             y=1.00, fontsize=20, fontweight='bold', ha='center')
ax.set_title('There was a spike in cases in early July due to the Bandung Army Secapa cluster',
             fontsize=15)
ax.set_xlabel('')
ax.set_ylabel('Number of new cases')
ax.text(1, -0.2, 'Data source: covid.19.go.id', color='blue',
        ha='right', transform=ax.transAxes)
ax.set_xticklabels(ax.get_xticks(), rotation=90)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

plt.grid(axis='y')
plt.tight_layout()
plt.show()


# It can be seen that there is a fluctuation in the daily positive cases.

# **2. Daily Recovered Cases of COVID-19 in West Java**

# In[24]:


plt.clf()
fig, ax = plt.subplots(figsize=(15,10))
ax.bar(data=cov_jabar_tidy, x='tanggal', height='sembuh', color='teal')
ax.set_title('Daily Recovered Cases of COVID-19 in West Java',
             fontsize=20)
ax.set_xlabel('')
ax.set_ylabel('Number of cases')
ax.text(1, -0.2,'Data source: covid.19.go.id', color='blue',
        ha='right', transform=ax.transAxes)
ax.set_xticklabels(ax.get_xticks(), rotation=90)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

plt.grid(axis='y')
plt.tight_layout()
plt.show()


# **3. Daily Deaths Case of COVID-19 in West Java**

# In[25]:


plt.clf()
fig, ax = plt.subplots(figsize=(15,10))
ax.bar(data=cov_jabar_tidy, x='tanggal', height='meninggal', color='indianred')
ax.set_title('Daily Death Case of COVID-19 in West Java',
             fontsize=20)
ax.set_xlabel('')
ax.set_ylabel('Number of cases')
ax.text(1, -0.2,'Data source: covid.19.go.id', color='blue',
        ha='right', transform=ax.transAxes)
ax.set_xticklabels(ax.get_xticks(), rotation=90)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

plt.grid(axis='y')
plt.tight_layout()
plt.show()


# #### **Weekly Cases of COVID-19**

# In[26]:


cov_jabar_pekanan = (cov_jabar_tidy.set_index('tanggal')['kasus_baru']
                      .resample('W')
                      .sum()
                      .reset_index()
                      .rename(columns={'kasus_baru': 'jumlah'})
)
                 
cov_jabar_pekanan['tahun'] = cov_jabar_pekanan['tanggal'].apply(lambda x: x.year)
cov_jabar_pekanan['pekan_ke'] = cov_jabar_pekanan['tanggal'].apply(lambda x: x.weekofyear)
cov_jabar_pekanan = cov_jabar_pekanan[['tahun', 'pekan_ke', 'jumlah']]

print('Infomation of data frame:')
cov_jabar_pekanan.info()
print('\nTop 5 data:\n', cov_jabar_pekanan.head())


# **Is This Week Better than Last Week?**

# In[27]:


cov_jabar_pekanan['jumlah_pekanlalu'] = cov_jabar_pekanan['jumlah'].shift().replace(np.nan, 0).astype(np.int)
cov_jabar_pekanan['lebih_baik'] = cov_jabar_pekanan['jumlah'] < cov_jabar_pekanan['jumlah_pekanlalu']

print('Top 10 data:\n', cov_jabar_pekanan.head(10))


# **How are Cases Progressing in a Span of Weeks?**

# In[28]:


plt.clf()
jml_tahun_terjadi_covid19 = cov_jabar_pekanan['tahun'].nunique()
tahun_terjadi_covid19 = cov_jabar_pekanan['tahun'].unique()
fig, axes = plt.subplots(nrows=jml_tahun_terjadi_covid19,
                         figsize=(10, 3*jml_tahun_terjadi_covid19))

fig.suptitle('Weekly Positive Case of COVID-19 in West Java',
            y=1.00, fontsize=16, fontweight='bold', ha='center')
for i, ax in enumerate(axes):
    ax.bar(data=cov_jabar_pekanan.loc[cov_jabar_pekanan['tahun']==tahun_terjadi_covid19[i]],
            x='pekan_ke', height='jumlah',
            color=['mediumseagreen' if x is True else 'salmon'
            for x in cov_jabar_pekanan['lebih_baik']])
    if i == 0:
        ax.set_title('The green column shows the addition of new cases is less than the previous week',
                    fontsize=10)
    elif i == jml_tahun_terjadi_covid19-1:
        ax.text(1, -0.2, 'Data source: covid.19.go.id', color='blue',
                ha='right',transform=ax.transAxes)

    ax.set_xlim([0, 52.5])
    ax.set_ylim([0,max(cov_jabar_pekanan['jumlah'])])
    ax.set_xlabel('')
    ax.set_ylabel('Number of cases %d'%(tahun_terjadi_covid19[i],))
    ax.grid(axis='y')

plt.tight_layout()
plt.show()


# It can be seen that some have finally recovered, but not a few have died from COVID-19. Meanwhile, the addition of new cases continues to occur in the society.

# **Until Now, How Many Active Cases?**
# 
# - Active cases means being in treatment or isolation.
# - The number of active cases can be calculated by subtracting the number of accumulated positives by the number of accumulated recoveries and the number of accumulated deaths.

# In[29]:


cov_jabar_akumulasi = cov_jabar_tidy[['tanggal']].copy()
cov_jabar_akumulasi['akumulasi_aktif'] = (cov_jabar_tidy['kasus_baru'] - cov_jabar_tidy['sembuh'] - cov_jabar_tidy['meninggal']).cumsum()
cov_jabar_akumulasi['akumulasi_sembuh'] = cov_jabar_tidy['sembuh'].cumsum()
cov_jabar_akumulasi['akumulasi_meninggal'] = cov_jabar_tidy['meninggal'].cumsum()
print(cov_jabar_akumulasi.tail())


# In[30]:


plt.clf()
fig, ax = plt.subplots(figsize=(10,5))
ax.plot('tanggal', 'akumulasi_aktif', data=cov_jabar_akumulasi, lw=2, color='brown')

ax.set_title('Accumulation of active COVID-19 in West Java',
             fontsize=20)
ax.set_xlabel('')
ax.set_ylabel('Active accumulation')
ax.text(1, -0.3, 'Data source: covid.19.go.id', color='blue',
        ha='right', transform=ax.transAxes)
ax.set_xticklabels(ax.get_xticks(), rotation=90)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

plt.grid()
plt.tight_layout()
plt.show()


# #### **Comparative Graph Between the Accumulation of Active Cases, Recovered Cases, and Death Cases**

# In[31]:


plt.clf()
fig, ax = plt.subplots(figsize=(10,5))
cov_jabar_akumulasi_ts = cov_jabar_akumulasi.set_index('tanggal')
cov_jabar_akumulasi_ts.plot(kind='line', ax=ax, lw=3,
                            color=['orange', 'teal', 'indianred'])

ax.set_title('Dynamics of COVID-19 Cases in West Java',
        fontsize=20)
ax.set_xlabel('')
ax.set_ylabel('Active accumulation')
ax.text(1, -0.2, 'Data source: covid.19.go.id', color='blue',
        ha='right', transform=ax.transAxes)

plt.grid()
plt.tight_layout()
plt.show()

