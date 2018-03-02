
# coding: utf-8

# # Capstone 2: Biodiversity Project

# # Introduction
# You are a biodiversity analyst working for the National Parks Service.  You're going to help them analyze some data about species at various national parks.
# 
# Note: The data that you'll be working with for this project is *inspired* by real data, but is mostly fictional.

# # Step 1
# Import the modules that you'll be using in this assignment:
# - `from matplotlib import pyplot as plt`
# - `import pandas as pd`

# In[1]:


import matplotlib.pyplot as plt
import pandas as pd


# # Step 2
# You have been given two CSV files. `species_info.csv` with data about different species in our National Parks, including:
# - The scientific name of each species
# - The common names of each species
# - The species conservation status
# 
# Load the dataset and inspect it:
# - Load `species_info.csv` into a DataFrame called `species`

# In[2]:


species = pd.read_csv('species_info.csv')


# Inspect each DataFrame using `.head()`.

# In[3]:


species.head()


# # Step 3
# Let's start by learning a bit more about our data.  Answer each of the following questions.

# How many different species are in the `species` DataFrame?

# In[4]:


num_species = len(species.scientific_name.unique()) #does the same as .nunique
print(num_species)


# What are the different values of `category` in `species`?

# In[5]:


category_species = species.category.unique()
print (category_species)


# What are the different values of `conservation_status`?

# In[6]:


status_species = species.conservation_status.unique()
print(status_species)


# # Step 4
# Let's start doing some analysis!
# 
# The column `conservation_status` has several possible values:
# - `Species of Concern`: declining or appear to be in need of conservation
# - `Threatened`: vulnerable to endangerment in the near future
# - `Endangered`: seriously at risk of extinction
# - `In Recovery`: formerly `Endangered`, but currnetly neither in danger of extinction throughout all or a significant portion of its range
# 
# We'd like to count up how many species meet each of these criteria.  Use `groupby` to count how many `scientific_name` meet each of these criteria.

# In[7]:


grp_by_status = species.groupby(['conservation_status']).scientific_name.nunique().reset_index()
species.groupby(['conservation_status']).scientific_name.nunique().reset_index()


# As we saw before, there are far more than 200 species in the `species` table.  Clearly, only a small number of them are categorized as needing some sort of protection.  The rest have `conservation_status` equal to `None`.  Because `groupby` does not include `None`, we will need to fill in the null values.  We can do this using `.fillna`.  We pass in however we want to fill in our `None` values as an argument.
# 
# Paste the following code and run it to see replace `None` with `No Intervention`:
# ```python
# species.fillna('No Intervention', inplace=True)
# ```

# In[8]:


species.fillna('No Intervention', inplace=True)


# Great! Now run the same `groupby` as before to see how many species require `No Protection`.

# In[9]:


grp_by_status = species.groupby(['conservation_status']).scientific_name.nunique().reset_index()
species.groupby(['conservation_status']).scientific_name.nunique().reset_index()


# Let's use `plt.bar` to create a bar chart.  First, let's sort the columns by how many species are in each categories.  We can do this using `.sort_values`.  We use the the keyword `by` to indicate which column we want to sort by.
# 
# Paste the following code and run it to create a new DataFrame called `protection_counts`, which is sorted by `scientific_name`:
# ```python
# protection_counts = species.groupby('conservation_status')\
#     .scientific_name.count().reset_index()\
#     .sort_values(by='scientific_name')
# ```

# In[10]:


protection_counts = species.groupby('conservation_status')    .scientific_name.nunique().reset_index()    .sort_values(by='scientific_name').reset_index(drop=True)
protection_counts


# Now let's create a bar chart!
# 1. Start by creating a wide figure with `figsize=(10, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `scientific_name` column of `protection_counts`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `conservation_status` in `protection_counts`
# 5. Label the y-axis `Number of Species`
# 6. Title the graph `Conservation Status by Species`
# 7. Plot the grap using `plt.show()`

# In[11]:


import numpy as np
plt.figure(figsize=(10,4))
ax = plt.subplot()
x = np.arange(len(protection_counts))
plt.bar(x, protection_counts.scientific_name)
plt.xticks(x, protection_counts.conservation_status)
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
plt.show()


# In[12]:


# plot number of species in each conservation status with y-log 
plt.figure(figsize=(10,4))
ax = plt.subplot()
x = np.arange(len(protection_counts))
plt.bar(x, protection_counts.scientific_name, log=1)

plt.xticks(x, protection_counts.conservation_status)
ax.set_yticks([1,10,100,1000,10000])
plt.ylabel('Log number of Species')
plt.title('Conservation Status by Species')

plt.show()


# # Step 4
# Are certain types of species more likely to be endangered?

# Let's create a new column in `species` called `is_protected`, which is `True` if `conservation_status` is not equal to `No Intervention`, and `False` otherwise.

# In[13]:


species['is_protected'] = species.apply(lambda row: True if row.conservation_status != 'No Intervention' else False, axis=1)
species.head()


# Let's group by *both* `category` and `is_protected`.  Save your results to `category_counts`.

# In[14]:


category_counts = species.groupby(['category','is_protected']).scientific_name.nunique().reset_index()


# Examine `category_count` using `head()`.

# In[15]:


category_counts


# It's going to be easier to view this data if we pivot it.  Using `pivot`, rearange `category_counts` so that:
# - `columns` is `conservation_status`
# - `index` is `category`
# - `values` is `scientific_name`
# 
# Save your pivoted data to `category_pivot`. Remember to `reset_index()` at the end.

# In[16]:


category_pivot = category_counts.pivot(index='category', columns='is_protected', values='scientific_name').reset_index()
#there is no column called 'conservation_status' I am assuming that instead 'is_protected' is meant...


# Examine `category_pivot`.

# In[17]:


category_pivot


# Use the `.columns` property to  rename the categories `True` and `False` to something more description:
# - Leave `category` as `category`
# - Rename `False` to `not_protected`
# - Rename `True` to `protected`

# In[18]:


category_pivot.columns = ['category','not_protected', 'protected']


# Let's create a new column of `category_pivot` called `percent_protected`, which is equal to `protected` (the number of species that are protected) divided by `protected` plus `not_protected` (the total number of species).

# In[21]:


percent_list = category_pivot.protected / (category_pivot.not_protected + category_pivot.protected)
category_pivot['percent_protected']= [round(elem,2) for elem in percent_list]


# Examine `category_pivot`.

# In[22]:


category_pivot


# It looks like species in category `Mammal` are more likely to be endangered than species in `Bird`.  We're going to do a significance test to see if this statement is true.  Before you do the significance test, consider the following questions:
# - Is the data numerical or categorical?
# - How many pieces of data are you comparing?

# Based on those answers, you should choose to do a *chi squared test*.  In order to run a chi squared test, we'll need to create a contingency table.  Our contingency table should look like this:
# 
# ||protected|not protected|
# |-|-|-|
# |Mammal|?|?|
# |Bird|?|?|
# 
# Create a table called `contingency` and fill it in with the correct numbers

# In[23]:


contingency = pd.DataFrame({'protected':[30,75 ],'not protected':[146,413]})
contingency


# In order to perform our chi square test, we'll need to import the correct function from scipy.  Past the following code and run it:
# ```py
# from scipy.stats import chi2_contingency
# ```

# In[24]:


from scipy.stats import chi2_contingency


# Now run `chi2_contingency` with `contingency`.

# In[25]:


_,p,_,_=chi2_contingency(contingency)
print("p= "+str(p))


# It looks like this difference isn't significant!
# 
# Let's test another.  Is the difference between `Reptile` and `Mammal` significant?

# In[26]:


contingency2 = pd.DataFrame({'protected':[30,5 ],'not protected':[146,73]})
contingency2
_,p2,_,_=chi2_contingency(contingency2)
print()
print("p2= "+str(p2))


# Yes! It looks like there is a significant difference between `Reptile` and `Mammal`!

# # Step 5

# Conservationists have been recording sightings of different species at several national parks for the past 7 days.  They've saved sent you their observations in a file called `observations.csv`.  Load `observations.csv` into a variable called `observations`, then use `head` to view the data.

# In[31]:


observations = pd.read_csv('observations.csv')
observations.head()
#observations.park_name.nunique()


# Some scientists are studying the number of sheep sightings at different national parks.  There are several different scientific names for different types of sheep.  We'd like to know which rows of `species` are referring to sheep.  Notice that the following code will tell us whether or not a word occurs in a string:

# In[32]:


# Does "Sheep" occur in this string?
str1 = 'This string contains Sheep'
'Sheep' in str1


# In[33]:


# Does "Sheep" occur in this string?
str2 = 'This string contains Cows'
'Sheep' in str2


# Use `apply` and a `lambda` function to create a new column in `species` called `is_sheep` which is `True` if the `common_names` contains `'Sheep'`, and `False` otherwise.

# In[34]:


species['is_sheep'] = species.apply(lambda row: True if 'Sheep' in row.common_names else False, axis=1)
species.head()


# Select the rows of `species` where `is_sheep` is `True` and examine the results.

# In[35]:


species[species.is_sheep]


# Many of the results are actually plants.  Select the rows of `species` where `is_sheep` is `True` and `category` is `Mammal`.  Save the results to the variable `sheep_species`.

# In[36]:


sheep_species = species[(species.is_sheep) & (species.category == 'Mammal')]
sheep_species


# Now merge `sheep_species` with `observations` to get a DataFrame with observations of sheep.  Save this DataFrame as `sheep_observations`.

# In[37]:


sheep_observations = observations.merge(sheep_species)
sheep_observations


# How many total sheep observations (across all three species) were made at each national park?  Use `groupby` to get the `sum` of `observations` for each `park_name`.  Save your answer to `obs_by_park`.
# 
# This is the total number of sheep observed in each park over the past 7 days.

# In[38]:


obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()
obs_by_park


# Create a bar chart showing the different number of observations per week at each park.
# 
# 1. Start by creating a wide figure with `figsize=(16, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `observations` column of `obs_by_park`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `park_name` in `obs_by_park`
# 5. Label the y-axis `Number of Observations`
# 6. Title the graph `Observations of Sheep per Week`
# 7. Plot the grap using `plt.show()`

# In[47]:


plt.figure(figsize=(16,4))
ax = plt.subplot()
plt.bar(np.arange(len(obs_by_park)), obs_by_park.observations)
plt.xticks(np.arange(len(obs_by_park)), obs_by_park.park_name)
plt.title('Observations of Sheep per Week')
plt.ylabel('Number of Observations')

plt.show()


# Our scientists know that 15% of sheep at Bryce National Park have foot and mouth disease.  Park rangers at Yellowstone National Park have been running a program to reduce the rate of foot and mouth disease at that park.  The scientists want to test whether or not this program is working.  They want to be able to detect reductions of at least 5 percentage point.  For instance, if 10% of sheep in Yellowstone have foot and mouth disease, they'd like to be able to know this, with confidence.
# 
# Use the sample size calculator at <a href="https://www.optimizely.com/sample-size-calculator/">Optimizely</a> to calculate the number of sheep that they would need to observe from each park.  Use the default level of significance (90%).
# 
# Remember that "Minimum Detectable Effect" is a percent of the baseline.

# ------------------
# Minimum detectable effect = 0.05/0.15 * 100
#                             = 1/3 * 100
#                             =~ 33%
# ,Baseline = 15

# In[40]:


sample_size = 520


# How many weeks would you need to observe sheep at Bryce National Park in order to observe enough sheep?  How many weeks would you need to observe at Yellowstone National Park to observe enough sheep?

# In[41]:


weeks_observation_BNP = sample_size / 250.
weeks_observation_YNP = sample_size / 507.
print(weeks_observation_BNP)
print(weeks_observation_YNP)


# # Step 6 Which species are in danger
# 

# In[68]:


species[species.conservation_status=="Endangered"].groupby('category').scientific_name.nunique()


# In[69]:

#create a list of endangered species
species[species.conservation_status=="Endangered"]


# # Step 7 Further analysis of the data
# 
# Further analysis will:
#   1. Investigate the data further, using:
#     a. a Pie Chart
#     b. a histogram?
#     c. Create aggregates with groupby to learn more.
#   2. Merge Data, what can we learn?
#   
#   First lets look at the observations data
#   
# 
# 

# In[42]:


print(observations.columns)
print("------------------")
print(species.columns)


# Lets see how many unique scientific names are in observations. After this take a look at the amount of unique names that are both in observations and species. How could these be merged best?

# In[43]:


print('number of unique observations:', observations.scientific_name.nunique())
print('number of unique names in species:', species.scientific_name.nunique())


# We want to compare the amount of wolfs to the amount of moose, dear and elk. To do this 
# 
# First lets look at the amount of wolfs.

# In[44]:


#species.drop('is_wolf', axis=1, inplace=True)
species.drop('is_sheep', axis=1, inplace=True)
species['group'] = 'None'

def is_wolf(common_name, category, group):
    if (('Wolf' in common_name) & (category == 'Mammal')):
        return 'Wolf'
    else:
        return group
    
species['group'] = species.apply(lambda x: is_wolf(x.common_names, x.category, x.group),axis=1)


#is_wolf = lambda row: 'Wolf' if 'Wolf' in row.common_names else row.group
#species['group'] = species.apply(is_wolf, axis=1)
#wolf_species = species[(species.is_wolf) & (species.category == 'Mammal')]
species[species.group=='Wolf']


# Lets do the same for moose, dear and elk and lets make a group for 'Bat' and 'Mouse' aswell.

# In[45]:



def is_group(common_name, category, group):
    if (('Bat' in common_name) & (category == 'Mammal')):
        return 'Bat'
    elif (('Mouse' in common_name) & (category == 'Mammal')):
        return 'Mouse'
    elif ((('Elk' in common_name) | ('Moose' in common_name) | ('Deer' in common_name)) & (category == 'Mammal')):
        return 'Elk_Deer_Moose'
    else:
        return group
    
species['group'] = species.apply(lambda x: is_group(x.common_names, x.category, x.group),axis=1)

species_wolf_ElkDeerMoose=(species[(species.group==('Wolf') ) | (species.group==('Elk_Deer_Moose'))])
species_wolf_ElkDeerMoose


# Now lets merge the data with the observation data to see how many Wolfs and Elk,Deer,Moose citings there where for each park. We can then further analyse which species is more dominant at each park with the use of a pie chart.

# In[48]:


merged_wolf_ElkDeerMoose=(species_wolf_ElkDeerMoose.merge(observations))
wolf_elk_obs = merged_wolf_ElkDeerMoose.groupby(['scientific_name','park_name']).observations.sum().reset_index()
#print(wolf_elk_obs)

plt.figure(figsize=(10,4))
ax1 = plt.subplot(131, aspect='equal')
wolf_elk_obs_BNP = wolf_elk_obs[wolf_elk_obs.park_name == 'Bryce National Park']
wolf_elk_obs_BNP.observations.plot(kind='pie', labels=wolf_elk_obs_BNP.scientific_name,autopct='%.1f', fontsize=12)

plt.figure(figsize=(10,4))
ax2 = plt.subplot(132, aspect='equal')
wolf_elk_obs_GSM = wolf_elk_obs[wolf_elk_obs.park_name == 'Great Smoky Mountains National Park']
#print(wolf_elk_obs_GSM )
wolf_elk_obs_GSM.observations.plot(kind='pie', labels=wolf_elk_obs_GSM.scientific_name,autopct='%.1f', fontsize=12)

plt.figure(figsize=(10,4))
ax3 = plt.subplot(132, aspect='equal')
wolf_elk_obs_YSNP = wolf_elk_obs[wolf_elk_obs.park_name == 'Yellowstone National Park']
#print(wolf_elk_obs_YSNP )
wolf_elk_obs_YSNP.observations.plot(kind='pie', labels=wolf_elk_obs_YSNP.scientific_name,autopct='%.1f', fontsize=12)




merged_wolf_ElkDeerMoose=(species_wolf_ElkDeerMoose.merge(observations))
#print(merged_wolf_ElkDeerMoose.groupby(['group','park_name']).observations.sum().reset_index())

plt.show()

