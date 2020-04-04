import os
import discord
import requests
import urllib3
from dotenv import load_dotenv
from bs4 import BeautifulSoup


class CountryData:
    def __init__(self):
        self.response = ""

    def get_new_stats(self):
        self.response = requests.get("https://www.worldometers.info/coronavirus/")
        return self.get_main_stats(self.response.text) if self.response.status_code == 200 else None

    @staticmethod
    def get_country_info(first, rows, counter):
        new_list = []
        # This is due to the formatting.
        # The index will be 0-8 if it doesn't include "<a" or "<span", otherwise 1-9.
        start = 1 if ("<a" in first or "<span" in first) else 0
        end = 9 if ("<a" in first or "<span" in first) else 8
        for j in range(start, end):
            r = bf.cleanse_string(rows[counter].findChildren()[j].contents)
            new_list.append(r)
        return new_list if len(new_list) > 0 else None

    def get_country_stats(self, markup, country):
        soup = BeautifulSoup(markup, "html.parser")
        # Only get things from the table so we can ignore the rest of the html.
        tables = soup.findChildren("table")
        rows = tables[0].findChildren("tr")

        new_list = []
        counter = 0
        for row in rows:
            # Special parsing for Hong Kong because for some reason  it says "China."
            if country.lower() in str(row).lower() and "hong" in country.lower():
                new_list = self.get_country_info(str(rows[counter].findChildren()[0]), rows, counter)
            elif country.lower() in str(row).lower():
                new_list = self.get_country_info(str(rows[counter].findChildren()[0]), rows, counter)
            counter += 1

        # Then we're going to return this list as a reconstructed dictionary
        # so we can have the same function displaying all results.
        return {
            "Country": new_list[0],
            "Total Cases": new_list[1],
            "New Cases": new_list[2],
            "Death Rate": bf.get_rate(new_list[3], new_list[1]),
            "Recovery Rate": bf.get_rate(new_list[5], new_list[1]),
            "Total Deaths": new_list[3],
            "New Deaths": new_list[4],
            "Total Recovered": new_list[5],
            "Active Cases": new_list[6],
            "Serious/Critical": new_list[7],
        }

    @staticmethod
    def get_main_stats(text):
        # This function's code is old, and does not use BeautifulSoup. Will get around to fixing that some day.
        corona_cases = text.split('<h1>Coronavirus Cases:</h1>')[1].\
            split('<span style="color:#aaa">')[1].split('</span>')[0]

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


class StateData:
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

                # We're gonna clean these strings first so we can use them again without ugly repetition.
                total_cases = bf.cleanse_state_string(td[1].contents)
                total_deaths = bf.cleanse_state_string(td[3].contents)
                active_cases = bf.cleanse_state_string(td[5].contents)
                # They took off the recovery total. We can postulate this information anyway based on current data.
                total_recovered = 0

                # Let's see if we even get a value in the first place.
                try:
                    total_recovered = (int(bf.cleanse_state_string(total_cases))
                                       - int(bf.cleanse_state_string(total_deaths))
                                       - int(bf.cleanse_state_string(active_cases)))
                # Nope. And we don't have to do anything because it's already 0.
                except ValueError:
                    pass

                return {
                    "State": bf.cleanse_state_string(td[0].contents),
                    "Total Cases": total_cases,
                    "New Cases": bf.cleanse_state_string(td[2].contents),
                    "Total Deaths": total_deaths,
                    "New Deaths": bf.cleanse_state_string(td[4].contents),
                    "Active Cases": active_cases,
                    "Death Rate": bf.get_rate(total_deaths, total_cases),
                    "Total Recovered": total_recovered,
                    "Recovery Rate": bf.get_rate(total_recovered, total_cases)
                }
        return None


class BotCommandResults:
    def __init__(self):
        self.states = StateData()
        self.cd = CountryData()
        pass

    # This will make it much easier to add and call new functions.
    def get_master_command_dict(self):
        return {
            "!country texas": self.expose_terrorist,
            "!country Texas": self.print_state,
            "!state": self.print_state,
            "!stats": self.print_countries,
            "!plague": self.print_countries,
            "!country": self.print_country,
            "!help": self.print_help,
        }

    async def print_help(self, message):
        command_string = "**Available commands for this bot**```"
        for key, value in self.get_master_command_dict().items():
            if " " not in key and "!stats" not in key and "!plague" not in key and "!help" not in key:
                command_string += f"{key} <{key.split('!')[1]}_name>\n"
            else:
                command_string += f"{key}\n"
        command_string += "```"
        await message.channel.send(command_string)

    async def print_state(self, message):
        state_query = bf.get_query_string(message.content)
        # This gets the data from the state list.
        state_dict = self.states.get_state_data(state_query, "usa_table_countries_today")
        # Is the list above non-empty?
        if state_dict:
            # Now we want to build the state string from the list above, and return it in human-readable format.
            state_string = bf.get_result_string(state_dict, f"Coronavirus Stats for {state_query.strip()}")
            await message.channel.send(state_string)
        # Annnnnnd it's empty.
        else:
            await message.channel.send("There was an error acquiring the state list")

    async def print_countries(self, message):
        try:
            stat_dict = self.cd.get_new_stats()
            if stat_dict:
                stat_string = bf.get_result_string(stat_dict, f"Global Statistics")
                stat_string += "Do you want more stats by Country? Use `!country <name>`"
                await message.channel.send(stat_string)
            else:
                await message.channel.send(f"Unable to update global statistics.")
        except requests.exceptions.SSLError:
            await message.channel.send("Potential Man in the Middle attack attempted: Bad HTTPS Response.")
        except urllib3.exceptions.MaxRetryError:
            await message.channel.send("There was an error attempting to connect to the the stats server. ")
        except TimeoutError:
            await message.channel.send("There was an error attempting to connect to the the stats server. ")

    async def print_country(self, message):
        try:
            # This builds our country string. e.g.: "!country Bosnia and Herzegovina "
            # becomes "Bosnia and Herzegovina"
            country_string = bf.get_query_string(message.content)

            # Get info from the page on worldometers.
            response = requests.get("https://www.worldometers.info/coronavirus/")
            country_dict = self.cd.get_country_stats(response.text, country_string.strip())

            # We got something, right?
            if country_dict:
                stat_string = bf.get_result_string(country_dict,
                                                   f"Coronavirus Statistics for {country_string.strip()}")

                await message.channel.send(bf.cleanse_string(stat_string))
            # Nope, we didn't.
            else:
                await message.channel.send(
                    f"Sorry, {bf.format_username(message.author)}! I can't find the "
                    f"country \"{country_string.strip()}\". ")
        except requests.exceptions.SSLError:
            await message.channel.send("Potential Man in the Middle attack attempted: Bad HTTPS Response.")
        except urllib3.exceptions.MaxRetryError:
            await message.channel.send("There was an error attempting to connect to the the stats server. ")
        except TimeoutError:
            await message.channel.send("There was an error attempting to connect to the the stats server. ")

    @staticmethod
    async def expose_terrorist(message):
        await message.channel.send(f"**[TERRORIST ALERT]** {bf.format_username(message.author)} is a terrorist "
                                   f"scum who refuses to capitalize Texas! Scumbag!")


class BotFunctions:
    def __init__(self):
        # Load the environment variables.
        load_dotenv()
        # And pass them here
        self.token = os.getenv('DISCORD_TOKEN')

        self.client = discord.Client()

        # Instantiate our own classes so we can do the thing.
        self.cmd = BotCommandResults()

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
        try:
            return str(str_to_cleanse).replace("['", "").replace("']", "").replace(",", "").strip()
        except ValueError:
            return 0

    @staticmethod
    def get_query_string(query_string):
        # This builds our string. e.g.: "!country Bosnia and Herzegovina "
        # becomes "Bosnia and Herzegovina"
        result = ""
        st = query_string.split(" ")
        for i in st:
            if not i.lower() == st[0].lower():
                result += str(i + " ")
        return result

    @staticmethod
    # This will print out the statistic dictionary.
    def get_result_string(result_dict, header):
        state_string = f"**{header}**```"
        for k, v in result_dict.items():
            state_string += f"{k}: {v}\n"
        state_string += "```"
        return state_string

    @staticmethod
    def cleanse_state_string(str_to_cleanse):
        try:
            # We're cleansing 2 spaces due to the way the site is formatted.
            return str(str_to_cleanse).replace("  ", "").replace("\\n", "").\
                replace("['", "").replace("']", "").\
                replace("<strong>", "").replace("</strong>", "").strip()
        except ValueError:
            return 0

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

        # Let's just make an easy-to-edit master list with their accompanying commands, yes?
        elif message.content.startswith("!"):
            for key, value in self.cmd.get_master_command_dict().items():
                if message.content.startswith(key):
                    try:
                        await value(message)
                    except IndexError:
                        await message.channel.send("Your query returned nothing.")
                    # We don't need to continue the loop, we found the key and executed the value.
                    break

        elif message.content == "raise-exception":
            raise discord.DiscordException


if __name__ == "__main__":
    bf = BotFunctions()
    bf.run()
