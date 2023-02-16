import pandas as pd
import matplotlib.pyplot as plt

plt.figure(figsize=[13, 6])
plt.style.use("ggplot")

df = pd.read_excel("countries.xlsx")

# Calculate the population density of each country

population = df["Population(2000-2005-2010-2015-2020)"].str.split(" ")
df["Population(2000-2005-2010-2015-2020)"] = population
populationInt = []

for i, v in df.iterrows():
    intPopulation = []
    for j in range(0, 5):
        intPopulation.append(int(v["Population(2000-2005-2010-2015-2020)"][j]))
    populationInt.append(intPopulation)

df["Population(2000-2005-2010-2015-2020)"] = populationInt

lastPopulation = []

for i, v in df.iterrows():
    lastPopulation.append(v["Population(2000-2005-2010-2015-2020)"][4])

df["Population Density"] = lastPopulation/df["Surface"]

# Percentage of countries per continent

countCountriesPerContinent = df.groupby(["Continent"])["Country"].count()
sumCountries = countCountriesPerContinent.sum()
percentage = (countCountriesPerContinent*100)/sumCountries

amountCountriesperContinent = []

for i in range(0, countCountriesPerContinent.shape[0]):
    amountCountriesperContinent.append(countCountriesPerContinent.iloc[i])

plt.pie(x=amountCountriesperContinent, labels=sorted(df["Continent"].unique()), autopct="%.2f%%")
plt.title("Percentage of countries per continent")
plt.show()

# Countries bigger than Chile in surface

chileIndex = df.loc[df["Country"] == "Chile"].index[0]
chileSurface = df.iloc[chileIndex]["Surface"]
biggerThanChile = df.loc[df["Surface"] > chileSurface].reset_index(drop=True)

plt.barh(biggerThanChile["Country"], biggerThanChile["Surface"], color="y")
plt.xlabel("Surface (km^2)")
plt.ylabel("Countries")
plt.title("Countries bigger than Chile in surface")
plt.show()

# Countries where the population is declining

isPopulationDeclining = []

for i, v in df.iterrows():
    if v["Population(2000-2005-2010-2015-2020)"][3] > v["Population(2000-2005-2010-2015-2020)"][4]:
        isPopulationDeclining.append(True)
    else:
        isPopulationDeclining.append(False)

df["Population Declining"] = isPopulationDeclining

decliningPopCountries = df.loc[df["Population Declining"]]

for i, v in decliningPopCountries.iterrows():
    plt.plot([2000, 2005, 2010, 2015, 2020], v["Population(2000-2005-2010-2015-2020)"], marker='o', color="b", label=v["Country"])

plt.title("Countries where the population is declining")
plt.xlabel("Years")
plt.ylabel("Population")
plt.xticks([2000, 2005, 2010, 2015, 2020])
plt.legend(loc="lower left")
plt.show()

# Percentaje of surface of each country in South America

southAmerica = df.loc[df["Region"] == "South America"].reset_index(drop=True)
totalSurface = southAmerica["Surface"].sum()
southAmerica["Percentage Surface"] = (southAmerica["Surface"]*100)/totalSurface

plt.pie(x=southAmerica["Surface"], labels=southAmerica["Country"], shadow=True, autopct='%.2f%%')
plt.title("Percentage of surface of each country in South America")
plt.axis("equal")
plt.show()

# The 5 largest landlocked countries

landlockedCountries = df.loc[df["Coastline"] == 0].reset_index(drop=True)
landlockedCountries = landlockedCountries.sort_values("Surface", ascending=False)
landlockedCountries.head()

plt.barh(landlockedCountries["Country"], landlockedCountries["Surface"], color="g")
plt.xlabel("Surface (km^2)")
plt.ylabel("Countries")
plt.title("Largest Landlocked Countries")
plt.xticks([0, 300000, 1000000, 3000000])
plt.show()

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
    lastPopulation.append(v["Population(2000-2005-2010-2015-2020)"][4])
    mainLanguages.append(v["Languages"][0])

df["Main Language"] = mainLanguages
df["Population"] = lastPopulation
populationForLanguage = df.groupby(["Main Language"]).agg({
    "Population": "sum",
})
populationForLanguage = populationForLanguage.sort_values("Population", ascending=False)

# Largest country per region

continentMaxSurface = df.groupby(["Region"])["Surface"].max()
countriesMaxSurface = []

for i in range(0, df["Region"].nunique()):
    for j in range(0, df.shape[0]):
        if(continentMaxSurface[i] == df.iloc[j]["Surface"]):
            print("Largest country from {} is {}".format(df.iloc[j]["Region"], df.iloc[j]["Country"]))

# Islands that are not dependents countries

islands = df.loc[df["Land Borders"] == 0].reset_index(drop=True)
independentsIslands = islands.loc[islands["Independence Day"] != "Dependent"]
