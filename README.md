# 🤖 Discord Bot: Coronavirus Stats 🦠 📈 

This is a bot for discord that's designed to help you get updated information on current coronavirus statistics. This bot provides information for **countries**, **states** and **the world**. 

Before you scroll down to the instructions, etc., consider reading about what you can do to help slow this pandemic. I've added some common sense here.

# What can I do to help stop this pandemic?

## You can practice Social Distancing 

Please consider Social Distancing. It really works and really helps save lives. Here's why:

![Image of Yaktocat](https://i.imgur.com/EzHvdeo.jpg)

Just because you are healthy doesn't mean you can't pass the disease to others and kill them.


## You can remember The FIVE.

1. **HANDS** - Wash them often
2. **ELBOW** - Cough into it
3. **FACE** - Don't touch it
4. **SPACE** - Keep safe distance
5. **HOMES** - Stay if you can

# Why did you make this?

I'm trying to do my part to help stop the spread of misinformation. You can help too!

There's a lot of bad information surrounding the coronavirus pandemic. You've probably heard a million and a half people downplaying the severity for months. This bot attempts to show you basic stats that the average person can understand.

Please get your information from the [Center for Disease Control and Prevention](https://www.cdc.gov/coronavirus/2019-ncov/index.html) and reputable media outlets such as [CBS](https://www.cbsnews.com). 

A lot of well-meaning individuals are pushing bogus information without realizing it. However, most major media companies, vet their information before airing it, so stick with reputable media outlets.

# Table of Contents

   * [Requirements](#requirements)
   * [Install](#install)
      * [Part One](#part-one)
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

You can start with `!help`:

```
Available commands for this bot
!country texas
!country Texas
!state <state_name>
!stats
!plague
!country <country_name>
!help
```

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
- Angola 
- Anguilla 
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
- Barbados 
- Belarus 
- Belgium 
- Belize 
- Benin 
- Bermuda 
- Bhutan 
- Bolivia 
- Bosnia and Herzegovina 
- Botswana 
- Brazil 
- British Virgin Islands 
- Brunei 
- Bulgaria 
- Burkina Faso 
- Burundi 
- CAR 
- Cabo Verde 
- Cambodia 
- Cameroon 
- Canada 
- Caribbean Netherlands 
- Cayman Islands 
- Chad 
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
- DRC 
- Denmark 
- Diamond Princess 
- Djibouti 
- Dominica 
- Dominican Republic 
- Ecuador 
- Egypt 
- El Salvador 
- Equatorial Guinea 
- Eritrea 
- Estonia 
- Eswatini 
- Ethiopia 
- Faeroe Islands 
- Falkland Islands 
- Fiji 
- Finland 
- France 
- French Guiana 
- French Polynesia 
- Gabon 
- Gambia 
- Georgia 
- Germany 
- Ghana 
- Gibraltar 
- Greece 
- Greenland 
- Grenada 
- Guadeloupe 
- Guatemala 
- Guinea 
- Guinea-Bissau 
- Guyana 
- Haiti 
- Honduras 
- Hong Kong 
- Hungary 
- Iceland 
- India 
- Indonesia 
- Iran 
- Iraq 
- Ireland 
- Isle of Man 
- Israel 
- Italy 
- Ivory Coast 
- Jamaica 
- Japan 
- Jordan 
- Kazakhstan 
- Kenya 
- Kuwait 
- Kyrgyzstan 
- Laos 
- Latvia 
- Lebanon 
- Liberia 
- Libya 
- Liechtenstein 
- Lithuania 
- Luxembourg 
- MS Zaandam 
- Macao 
- Madagascar 
- Malawi 
- Malaysia 
- Maldives 
- Mali 
- Malta 
- Martinique 
- Mauritania 
- Mauritius 
- Mayotte 
- Mexico 
- Moldova 
- Monaco 
- Mongolia 
- Montenegro 
- Montserrat 
- Morocco 
- Mozambique 
- Myanmar 
- Namibia 
- Nepal 
- Netherlands 
- New Caledonia 
- New Zealand 
- Nicaragua 
- Niger 
- Nigeria 
- North Macedonia 
- Norway 
- Oman 
- Pakistan 
- Palestine 
- Panama 
- Papua New Guinea 
- Paraguay 
- Peru 
- Philippines 
- Poland 
- Portugal 
- Qatar 
- Romania 
- Russia 
- Rwanda 
- Réunion 
- S. Korea 
- Saint Kitts and Nevis 
- Saint Lucia 
- Saint Martin 
- Saint Pierre Miquelon 
- San Marino 
- Sao Tome and Principe 
- Saudi Arabia 
- Senegal 
- Serbia 
- Seychelles 
- Sierra Leone 
- Singapore 
- Sint Maarten 
- Slovakia 
- Slovenia 
- Somalia 
- South Africa 
- South Sudan 
- Spain 
- Sri Lanka 
- St. Barth 
- St. Vincent Grenadines 
- Sudan 
- Suriname 
- Sweden 
- Switzerland 
- Syria 
- Taiwan 
- Tanzania 
- Thailand 
- Timor-Leste 
- Togo 
- Trinidad and Tobago 
- Tunisia 
- Turkey 
- Turks and Caicos 
- UAE 
- UK 
- USA 
- Uganda 
- Ukraine 
- Uruguay 
- Uzbekistan 
- Vatican City 
- Venezuela 
- Vietnam 
- Western Sahara 
- Yemen 
- Zambia 
- Zimbabwe 
