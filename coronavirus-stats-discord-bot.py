import os
import random
import discord
import requests
import urllib3
from dotenv import load_dotenv
from bs4 import BeautifulSoup


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
                    r = str(rows[counter].findChildren()[j].contents).replace(" ", "").replace("\\n", " ")
                    new_list.append(r)
            counter += 1
        return new_list

    @staticmethod
    def get_main_stats(text):
        # This code is old, and without the beautiful soup.
        corona_cases = text.split('<h1>Coronavirus Cases:</h1>')[1].split('<span style="color:#aaa">')[1].split('</span>')[0]
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
        self.request = ""

    def get_state_data(self, state_query, table_name):
        self.request = requests.get("https://www.worldometers.info/coronavirus/country/us/")
        soup = BeautifulSoup(self.request.text, "html.parser")
        table = soup.findChildren("table", {"id": table_name})
        rows = table[0].findChildren("tr")

        for i in rows:
            if str(state_query).strip().lower() in str(i).strip().lower():
                # Get the tds within the tr.
                td = i.findChildren("td")

                # And populate.
                total_cases = bf.cleanse_state_string(td[1].contents)
                total_deaths = bf.cleanse_state_string(td[3].contents)
                total_recovered = bf.cleanse_state_string(td[5].contents)

                return {
                    "State": bf.cleanse_state_string(td[0].contents),
                    "Total Cases": bf.cleanse_state_string(td[1].contents),
                    "New Cases": bf.cleanse_state_string(td[2].contents),
                    "Total Deaths": bf.cleanse_state_string(td[3].contents),
                    "New Deaths": bf.cleanse_state_string(td[4].contents),
                    "Total Recovered": total_recovered,
                    "Active Cases": bf.cleanse_state_string(td[6].contents),
                    "Death Rate": bf.get_rate(total_deaths, total_cases),
                    "Recovery Rate": bf.get_rate(total_recovered, total_cases)
                }
        return None


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
        return str(str_to_cleanse).replace("['", "").replace("']", "").replace(",", "").strip()

    @staticmethod
    def cleanse_state_string(str_to_cleanse):
        # We're cleansing 2 spaces due to the way the site is formatted.
        return str(str_to_cleanse).replace("  ", "").replace("\\n", "").\
            replace("['", "").replace("']", "").\
            replace("<strong>", "").replace("</strong>", "").strip()

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

        # Texas is a country, or you're a terrorist. Pick one. And capitalize Texas.
        # All in good fun... don't take it seriously.
        elif message.content.startswith("!country texas"):
            await message.channel.send(f"**[TERRORIST ALERT]** {self.format_username(message.author)} is a terrorist "
                                       f"scum who refuses to capitalize Texas! Scumbag!")

        # This gets state statistics from The Washington Post.
        # Texas is a country, or you're a terrorist. Pick one. And capitalize Texas.
        # All in good fun... don't take it seriously.
        elif message.content.startswith("!state") or message.content.startswith("!country Texas"):

            # We want to get "New York" from the string "!state New York " This is how we do it.
            state_query = ""
            st = message.content.split(" ")
            for i in st:
                if not i.lower() == st[0].lower():
                    state_query += str(i + " ")

            # This gets the data from the state list.
            state_dict = self.states.get_state_data(state_query, "usa_table_countries_today")
            # Is the list above non-empty?
            if state_dict:
                # Now we want to build the state string from the list above, and return it in human-readable format.
                state_string = f"**Coronavirus Stats for {state_query.strip()}**```"
                for k, v in state_dict.items():
                    state_string += k + ": " + v + "\n"
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
                    "Rodent security does not like. ")
            except urllib3.exceptions.MaxRetryError:
                await message.channel.send("There was an error attempting to connect to the the stats server. ")
            except TimeoutError:
                await message.channel.send("There was an error attempting to connect to the the stats server. ")

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
                    stat_string = f"**Coronavirus Statistics for {country_string.strip()}**\n```"
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
                        f"country \"{country_string.strip()}\". ")
            except requests.exceptions.SSLError:
                await message.channel.send(
                    "Attempted Man in the Middle attack detected: "
                    "Incorrect HTTPS response received. Rodent security does not like. ")
            except urllib3.exceptions.MaxRetryError:
                await message.channel.send("There was an error attempting to connect to the the stats server. ")
            except TimeoutError:
                await message.channel.send("There was an error attempting to connect to the the stats server. ")

        elif message.content == 'raise-exception':
            raise discord.DiscordException


if __name__ == "__main__":
    bf = BotFunctions()
    bf.run()
