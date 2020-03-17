# 🦠 📈 🤖

# Coronavirus Discord Bot 

This is a bot for discord that's designed to help you get updated information on current coronavirus statistics.

# Install

```
pip install -r requirements.txt
```
This guide assumes you know how to set up and run a discord bot. That is unfortunately beyond the scope of this readme, but I'll give you some TLDR steps:

1. [Create a bot for Discord](https://discordapp.com/developers/applications/) on their developer page.
2. Get your token and server id
3. Visit the generated URL and allow it access to your discord server.
4. Create an `.env` file in the same folder as `coronavirus-stats-discord-bot.py`
5. Update the `.env` file with your token and server ID.


# Usage:

To run: 

```$ python3 coronavirus-stats-discord-bot.py```

To use in the server...


**To get all global statistics:**

```!stats``` or ```!plague```

**Returns:**


```
Global Statistics
Total Cases: 182,700
Total Deaths: 7,173
Death Rate: 3.93%
Recovery Rate: 43.72%
Total Recoveries: 79,883
Total Active Cases: 95,644
Total Mild Cases: 89,481
Total Serious/Critical: 6,163
Total Closed Cases: 87,056
Closed because recovered/discharged: 79,883
Closed because of deaths: 7,173
```


**For countries:**


```
!country Italy
```

**Returns**:

```
Coronavirus Statistics for Italy
Country: Italy
Total Cases: 27980
New Cases:  
Death Rate: 7.71%
Recovery Rate: 9.82%
Total Deaths:  2158 
New Deaths:  
Total Recovered: 2749 
Active Cases:  23073 
Serious/Critical: 1851 
```

**For Individual U.S. States:**


```!state Washington```


**Returns**:


```
Coronavirus Stats for Washington
State: Washington
Cases: 904
Deaths: 48
Death Rate: 5.31%
```


# Dumb Design Problem

You will occasionally need to type:

```
!update
```

In order to update U.S. states. 

This is mostly due to the way I designed the program. This was created in a hurry (<2 hours), so it's not meant to be production quality. 


# Missing Countries

- `South Korea` exists, but it's  `S. Korea`


# Valid States and Countries

If you're having trouble finding states, regions, territories or countries, check the below list:

## Valid States

- Alabama
- Alaska
- Arizona
- Arkansas
- California
- Colorado
- Connecticut
- Delaware
- District of Columbia
- Florida
- Georgia
- Guam
- Hawaii
- Idaho
- Illinois
- Indiana
- Iowa
- Kansas
- Kentucky
- Louisiana
- Maine
- Maryland
- Massachusetts
- Michigan
- Minnesota
- Mississippi
- Missouri
- Montana
- Nebraska
- Nevada
- New Hampshire
- New Jersey
- New Mexico
- New York
- North Carolina
- North Dakota
- Ohio
- Oklahoma
- Oregon
- Pennsylvania
- Puerto Rico
- Rhode Island
- South Carolina
- South Dakota
- Tennessee
- Texas
- Utah
- Vermont
- Virgin Islands
- Virginia
- Washington
- Wisconsin
- Wyoming


## Valid Countries

- Afghanistan
- Albania
- Algeria
- Andorra
- Antigua and Barbuda
- Argentina
- Armenia
- Aruba
- Australia
- Austria
- Azerbaijan
- Bahamas
- Bahrain
- Bangladesh
- Belarus
- Belgium
- Benin
- Bhutan
- Bolivia
- Bosnia and Herzegovina
- Brazil
- Brunei
- Bulgaria
- Burkina Faso
- Cambodia
- Cameroon
- Canada
- CAR
- Cayman Islands
- Channel Islands
- Chile
- China
- Colombia
- Congo
- Costa Rica
- Croatia
- Cuba
- Curaçao
- Cyprus
- Czechia
- Denmark
- Diamond Princess
- Dominican Republic
- DRC
- Ecuador
- Egypt
- Equatorial Guinea
- Estonia
- Eswatini
- Ethiopia
- Faeroe Islands
- Finland
- France
- French Guiana
- French Polynesia
- Gabon
- Georgia
- Germany
- Ghana
- Gibraltar
- Greece
- Greenland
- Guadeloupe
- Guam
- Guatemala
- Guinea
- Guyana
- Honduras
- Hong Kong
- Hungary
- Iceland
- India
- Indonesia
- Iran
- Iraq
- Ireland
- Israel
- Italy
- Ivory Coast
- Jamaica
- Japan
- Jordan
- Kazakhstan
- Kenya
- Kuwait
- Latvia
- Lebanon
- Liberia
- Liechtenstein
- Lithuania
- Luxembourg
- Macao
- Malaysia
- Maldives
- Malta
- Martinique
- Mauritania
- Mayotte
- Mexico
- Moldova
- Monaco
- Mongolia
- Morocco
- Namibia
- Nepal
- Netherlands
- New Zealand
- Nigeria
- North Macedonia
- Norway
- Oman
- Pakistan
- Palestine
- Panama
- Paraguay
- Peru
- Philippines
- Poland
- Portugal
- Puerto Rico
- Qatar
- Réunion
- Romania
- Russia
- Rwanda
- S. Korea
- Saint Lucia
- Saint Martin
- San Marino
- Saudi Arabia
- Senegal
- Serbia
- Seychelles
- Singapore
- Slovakia
- Slovenia
- Somalia
- South Africa
- Spain
- Sri Lanka
- St. Barth
- St. Vincent Grenadines
- Sudan
- Suriname
- Sweden
- Switzerland
- Taiwan
- Tanzania
- Thailand
- Togo
- Trinidad and Tobago
- Tunisia
- Turkey
- U.S. Virgin Islands
- UAE
- UK
- Ukraine
- Uruguay
- USA
- Uzbekistan
- Vatican City
- Venezuela
- Vietnam
