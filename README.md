# 🤖 Discord Bot: Coronavirus Stats 🦠 📈 

This is a bot for discord that's designed to help you get updated information on current coronavirus statistics. If you don't read this README, you're going to have a bad time. 

   * [Requirements](#requirements)
   * [Install](#install)
      * [Part One](#part-one)
         * [Without Docker](#without-docker)
         * [With Docker](#with-docker)
      * [Part Two](#part-two)
   * [Forking](#forking)
   * [Usage](#usage)
   * [Missing Countries](#missing-countries)
   * [Valid States and Countries](#valid-states-and-countries)
      * [Valid States](#valid-states)
      * [Valid Countries](#valid-countries)

# Requirements

- python3.6+
- pip3
- docker (optional)

# Install

## Part One

### Without Docker

Edit `.env-sample` and rename to `.env`

```
$ pip3 install -r requirements.txt
$ python3 coronavirus-stats-discord-bot.py
```

### With Docker

Edit `.env-sample` and rename to `.env`

```
docker build -t coronavirus-stats .
docker run -ti coronavirus-stats
```

## Part Two 

This guide assumes you know how to set up and run a discord bot. That is unfortunately beyond the scope of this readme, but I'll give you some TLDR steps:

1. [Create a bot for Discord](https://discordapp.com/developers/applications/) on their developer page.
2. Get your token and server id
3. Visit the generated URL and allow it access to your discord server.
4. Rename `.env-sample` to `.env`
5. Update the `.env` file with your token and server ID.


# Forking

If you want to easily add your own commands, it's now very easy. You can just look at this function:

- `def get_master_command_dict(self):`

Just update the dictionary with a command and a value. 

The key will be the trigger, e.g.: `"!state":`, and the `value` will point to a function that does whatever you want. This is the only thing you need to update.

All of this assumes the `message` parameter will be passed to the function. See `def on_message(self, message)` for how it's parsed using `await value(message)`. 


# Usage

## To run

```$ python3 coronavirus-stats-discord-bot.py```

or if using Docker:

```$ docker run -ti coronavirus-stats```

## To use in the server...

### To get all global statistics

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
### For countries:

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
### For Individual U.S. States:

```!state Texas```

**Returns**:

```
Coronavirus Stats for Texas
State: Texas
Total Cases: 429
New Cases: +35
Total Deaths: 5
New Deaths: 
Total Recovered: 4
Active Cases: 420
Death Rate: 1.17%
Recovery Rate: 0.93%
```
# Missing Countries

- `South Korea` exists, but it's  `S. Korea`

# Valid States and Countries

If you're having trouble finding states, regions, territories or countries to use with `!state` or `!country`, check the below list to make sure you're spelling it according to the way that the host websites are displaying them:

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
