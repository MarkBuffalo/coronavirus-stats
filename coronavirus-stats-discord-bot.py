import os
import random
import discord
import requests
import urllib3
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver


class CommandParser:
    def __init__(self):
        self.response = ""

    def get_new_stats(self):
        self.response = requests.get("https://www.worldometers.info/coronavirus/")
        return self.get_main_stats(self.response.text) if self.response.status_code == 200 else ""

    @staticmethod
    def clean_str(text):
        return int(float(str(text.strip().replace(",", "").replace("+", ""))))

    @staticmethod
    def traverse_html(markup, country):
        soup = BeautifulSoup(markup, "html.parser")
        # Only get things from the table so we can ignore the rest of the html.
        tables = soup.findChildren('table')
        rows = tables[0].findChildren('tr')

        new_list = []
        counter = 0
        for row in rows:
            if country.lower() in str(row).lower():
                first = str(rows[counter].findChildren()[0])
                start = 1 if ("<a" in first or "<span" in first) else 0
                end = 9 if ("<a" in first or "<span" in first) else 8
                for j in range(start, end):
                    r = str(rows[counter].findChildren()[j].contents)
                    new_list.append(r)
            counter += 1
        return new_list

    @staticmethod
    def get_main_stats(text):
        corona_cases = \
            text.split('<h1>Coronavirus Cases:</h1>')[1].split('<span style="color:#aaa">')[1].split('</span>')[0]
        corona_deaths = text.split('<h1>Deaths:</h1>')[1].split('<span>')[1].split('</span>')[0]
        corona_recoveries = text.split('<h1>Recovered:</h1>')[1].split('<span>')[1].split('</span>')[0]

        death_rate = bf.get_rate(corona_deaths, corona_cases)
        recovery_rate = bf.get_rate(corona_recoveries, corona_cases)

        # Active cases
        active_cases = text.split('<div class="number-table-main">')[1].split('</div>')[0]
        mild_conditions = text.split('<span class="number-table"')[1].split(">")[1].split("</span")[0]
        serious_or_critical = text.split('<span class="number-table"')[2].split(">")[1].split("</span")[0]

        # Closed cases
        total_closed_cases = text.split('<div class="number-table-main">')[2].split('</div>')[0]
        recovered_discharged = text.split('<span class="number-table"')[3].split(">")[1].split("</span")[0]
        deaths = text.split('<span class="number-table"')[4].split(">")[1].split("</span")[0]

        return {
            "Total Cases": corona_cases.strip(),
            "Total Deaths": corona_deaths.strip(),
            "Death Rate": str(death_rate),
            "Recovery Rate": str(recovery_rate),
            "Total Recoveries": corona_recoveries.strip(),
            "Total Active Cases": active_cases.strip(),
            "Total Mild Cases": mild_conditions.strip(),
            "Total Serious/Critical": serious_or_critical.strip(),
            "Total Closed Cases": total_closed_cases.strip(),
            "Closed because recovered/discharged": recovered_discharged.strip(),
            "Closed because of deaths": deaths.strip()
        }


class GetStateData:
    def __init__(self):
        self.options = webdriver.FirefoxOptions()
        self.options.add_argument('-headless')
        self.browser = webdriver.Firefox(options=self.options)
        self.update_state_data()
        pass

    def update_state_data(self):
        self.browser.get("https://www.washingtonpost.com/world/2020/01/22/mapping-spread-new-coronavirus/?arc404=true")

    def get_state_data(self, state_query):
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        table = soup.findChildren("div", {"id": "us-case-count-table"})
        rows = table[0].findChildren("div", {"class": "table-row"})

        state_list = []
        for i in rows:
            if str(state_query).strip().lower() in str(i).lower():
                state = i.findChildren("span")[0].contents
                cases = i.findChildren("span")[1].contents
                deaths = i.findChildren("span")[2].contents
                state_list.append([state, cases, deaths])
        return state_list


class BotFunctions:
    def __init__(self):
        # Load the environment variables.
        load_dotenv()
        # And pass them here
        self.token = os.getenv('DISCORD_TOKEN')

        self.client = discord.Client()

        # Instantiate our own classes so we can do the thing.
        self.cmd = CommandParser()
        self.states = GetStateData()

        # Setup event handlers for bot functions instead of using decorators.
        self.on_ready = self.client.event(self.on_ready)
        self.on_message = self.client.event(self.on_message)
        self.on_member_join = self.client.event(self.on_member_join)

    # This runs the bot with the token credentials.
    def run(self):
        self.client.run(self.token)

    # This is dumb, and likely unnecessary at this time. Doing it anyway because of reasons.
    @staticmethod
    def cleanse_string(str_to_cleanse):
        return str(str_to_cleanse).replace("['", "").replace("']", "").replace(",", "")

    # Gets the rate of deaths/recoveries/salads per face/whatever.
    def get_rate(self, bad, total):
        try:
            return "{0:.2f}%".format((int(self.cleanse_string(bad)) / int(self.cleanse_string(total))) * 100)
        except ValueError:
            return "Incomplete data"

    # This gets the partial username to avoid ugly text. e.g.: CoronaVirus#20109 because CoronaVirus.
    @staticmethod
    def format_username(username):
        return str(username).split('#')[0]

    # When we connect to discord, this function is called.
    async def on_ready(self):
        print(f"{self.client.user.name} has connected to Discord! The following channels are available:")
        for channel in self.client.get_all_channels():
            print(f"#{channel}")

    # Whenever a member joins. We aren't going to do anything right now. Hard pass.
    @staticmethod
    async def on_member_join(member):
        pass

    # Whenever a user sends a message.
    async def on_message(self, message):
        # Makes sure the bot doesn't put itself in an infinite loop triggering on itself indefinitely.
        if message.author == self.client.user:
            return

        # This updates the web stats because of strange design issues which prevent a full population of
        # statistics on slow connections, leading to zero data returning.
        if message.content == "!update":
            self.states.update_state_data()
            await message.channel.send("Just updated the state data!")

        # Texas is a country, or you're a terrorist. Pick one. And capitalize Texas.
        elif message.content.startswith("!country texas"):
            await message.channel.send(f"**[TERRORIST ALERT]** {self.format_username(message.author)} is a terrorist "
                                       f"scum who refuses to capitalize Texas! Scumbag!")

        # This gets state statistics from The Washington Post.
        # Texas is a country, or you're a terrorist. Pick one. And capitalize Texas.
        elif message.content.startswith("!state") or message.content.startswith("!country Texas"):
            # We want to get "New York" from the string "!state New York" This is how we do it.
            state_query = ""
            st = message.content.split(" ")
            for i in st:
                if not i.lower() == st[0].lower():
                    state_query += str(i + " ")

            # This gets the data from the state list.
            state_list = self.states.get_state_data(state_query)

            # Is the list above non-empty?
            if len(state_list) > 0:
                # Now we want to build the state string from the list above, and return it in human-readable format.
                state_string = f"**Coronavirus Stats for {state_query.strip()}**```"
                state = self.cleanse_string(state_list[0][0])
                cases = self.cleanse_string(state_list[0][1])
                deaths = self.cleanse_string(state_list[0][2])
                death_rate = self.get_rate(deaths, cases)

                state_string += f"State: {state}\n" \
                                f"Cases: {cases}\n" \
                                f"Deaths: {deaths}\n" \
                                f"Death Rate: {death_rate}"

                await message.channel.send(state_string + "```")
            # Annnnnnd it's empty.
            else:
                await message.channel.send("There was an error acquiring the state list")

        # When you want the global statistics.
        elif message.content == '!stats' or message.content == "!plague":
            try:
                stat_list = self.cmd.get_new_stats()

                stat_string = f"**Global Statistics**```"
                for k, v in stat_list.items():
                    stat_string += k + ": " + v + "\n"
                stat_string += "```\n Do you want more stats by Country? Use `!country <name>`"
                await message.channel.send(stat_string)
            except requests.exceptions.SSLError:
                await message.channel.send(
                    "Attempted Man in the Middle attack detected: Incorrect HTTPS response received. "
                    "Rodent security does not like. :8(")
            except urllib3.exceptions.MaxRetryError:
                await message.channel.send("There was an error attempting to connect to the the stats server. :8(")
            except TimeoutError:
                await message.channel.send("There was an error attempting to connect to the the stats server. :8(")

        # When you want stats for a specific country.
        elif message.content.startswith("!country"):
            try:
                # This builds our country string. e.g.: "!country Bosnia and Herzegovina "
                # becomes "Bosnia and Herzegovina"
                country_string = ""
                st = message.content.split(" ")
                for i in st:
                    if not i.lower() == st[0].lower():
                        country_string += str(i + " ")

                # We're going to a new request each time because, well... it's more stable than the Washington Post
                # since we won't need to run geckodriver to get the contents.
                response = requests.get("https://www.worldometers.info/coronavirus/")
                country_list = self.cmd.traverse_html(response.text, country_string.strip())

                # We got something, right?
                if len(country_list) > 0:
                    stat_string = f'**Coronavirus Statistics for {country_string.strip()}**\n```'
                    stat_string += f"Country: {country_list[0]}\n"
                    stat_string += f"Total Cases: {country_list[1]}\n"
                    stat_string += f"New Cases: {country_list[2]}\n"
                    stat_string += f"Death Rate: {self.get_rate(country_list[3], country_list[1])}\n"
                    stat_string += f"Recovery Rate: {self.get_rate(country_list[5], country_list[1])}\n"
                    stat_string += f"Total Deaths: {country_list[3]}\n"
                    stat_string += f"New Deaths: {country_list[4]}\n"
                    stat_string += f"Total Recovered: {country_list[5]}\n"
                    stat_string += f"Active Cases: {country_list[6]}\n"
                    stat_string += f"Serious/Critical: {country_list[7]}\n"
                    stat_string += f"```\n"
                    await message.channel.send(self.cleanse_string(stat_string))
                # Nope, we didn't.
                else:
                    await message.channel.send(
                        f"Sorry, {self.format_username(message.author)}! I can't find the "
                        f"country \"{country_string.strip()}\". :8(")
            except requests.exceptions.SSLError:
                await message.channel.send(
                    "Attempted Man in the Middle attack detected: "
                    "Incorrect HTTPS response received. Rodent security does not like. :8(")
            except urllib3.exceptions.MaxRetryError:
                await message.channel.send("There was an error attempting to connect to the the stats server. :8(")
            except TimeoutError:
                await message.channel.send("There was an error attempting to connect to the the stats server. :8(")

        elif message.content == 'raise-exception':
            raise discord.DiscordException


if __name__ == "__main__":
    bf = BotFunctions()
    bf.run()
