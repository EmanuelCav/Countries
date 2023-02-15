import pandas as pd

df = pd.read_excel("countries.xlsx")

# Calculate the population density of each country

pupulation = df["Population(2000-2005-2010-2015-2020)"].str.split(" ")

df["Population(2000-2005-2010-2015-2020)"] = pupulation

lastPopulation = []

for i, v in df.iterrows():
    lastPopulation.append(int(v["Population(2000-2005-2010-2015-2020)"][4]))

df["Population Density"] = lastPopulation/df["Surface"]

# Percentage of countries per continent

countCountriesPerContinent = df.groupby(["Continent"])["Country"].count()
sumCountries = countCountriesPerContinent.sum()
percentage = (countCountriesPerContinent*100)/sumCountries

# Countries bigger than Chile in surface

chileIndex = df.loc[df["Country"] == "Chile"].index[0]
chileSurface = df.iloc[chileIndex]["Surface"]
df.loc[df["Surface"] > chileSurface].reset_index(drop=True)

# Countries where the population is declining

isPopulationDeclining = []

for i, v in df.iterrows():
    if v["Population(2000-2005-2010-2015-2020)"][3] > v["Population(2000-2005-2010-2015-2020)"][4]:
        isPopulationDeclining.append(True)
    else:
        isPopulationDeclining.append(False)

df["Population Declining"] = isPopulationDeclining

# Percentaje of surface of each country in South America

southAmerica = df.loc[df["Region"] == "South America"].reset_index(drop=True)
totalSurface = southAmerica["Surface"].sum()
southAmerica["Percentage Surface"] = (southAmerica["Surface"]*100)/totalSurface

# The 5 largest landlocked countries

landlockedCountries = df.loc[df["Coastline"] == 0].reset_index(drop=True)
landlockedCountries = landlockedCountries.sort_values("Surface", ascending=False)
landlockedCountries.head()

# What is more in Africa?. Christian countries or Islam countries

africa = df.loc[df["Continent"] == "Africa"].reset_index(drop=True)
religionCounts = africa["Main Religion"].value_counts()
if religionCounts["Christianity"] > religionCounts["Islam"]:
    print("In Africa, there are more christian countries")
else:
    print("In Africa, there are more islam countries")

# Most spoken languages 

mainLanguages = []
lastPopulation = []
df["Languages"] = df["Languages"].str.split(' ')

for i, v in df.iterrows():
    lastPopulation.append(int(v["Population(2000-2005-2010-2015-2020)"][4]))
    mainLanguages.append(v["Languages"][0])

df["Main Language"] = mainLanguages
df["Population"] = lastPopulation
populationForLanguage = df.groupby(["Main Language"]).agg({
    "Population": "sum",
})
populationForLanguage.sort_values("Population", ascending=False)

# Largest country per region

continentMaxSurface = df.groupby(["Region"])["Surface"].max()
countriesMaxSurface = []

for i in range(0, df["Region"].nunique()):
    for j in range(0, df.shape[0]):
        if(continentMaxSurface[i] == df.iloc[j]["Surface"]):
            print("Largest country from {} is {}".format(df.iloc[j]["Region"], df.iloc[j]["Country"]))

# Islands that are not dependents countries

islands = df.loc[df["Land Borders"] == 0].reset_index(drop=True)
islands.loc[islands["Independence Day"] != "Dependent"]




