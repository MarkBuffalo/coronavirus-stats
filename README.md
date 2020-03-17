# 🦠 Coronavirus Discord Bot 🤖

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
