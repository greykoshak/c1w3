import argparse
import requests
from prettytable import PrettyTable
from colorama import Fore


class YahooService:
    def __init__(self):
        self._city_cache = {}

    def get(self, city):
        if city in self._city_cache:
            return self._city_cache[city]

        url = f"https://query.yahooapis.com/v1/public/yql?q=select%20*%20 \
              from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20 \
              from%20geo.places(1)%20where%20text%3D%22{city}%22)%20and%20u%3D%22c%22 \
              &format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
        print("Sending HTTP requests for {}".format(city))

        data_yahoo = requests.get(url).json()
        data_forecast = data_yahoo["query"]["results"]["channel"]["item"]["forecast"]

        weather_forecast = []
        for day_forecast in data_forecast:
            weather_forecast.append({
                "date": day_forecast["date"],
                "day": day_forecast["day"],
                "high": day_forecast["high"],
                "low": day_forecast["low"],
                "text": day_forecast["text"],
            })
        self._city_cache[city] = weather_forecast

        return weather_forecast


class CityInfo:
    def __init__(self, city, forecast=None):
        self.city = city
        self._forecast = forecast or YahooService()

    def get_forecast(self):
        return self._forecast.get(self.city)


def _main():
    forecast = YahooService()
    city_info = CityInfo(args.city, forecast=forecast)
    city_forecast = city_info.get_forecast()

    pt = PrettyTable()
    pt.field_names = ["Дата", "День", "Max", "Min", "Погода"]

    for day_data in city_forecast:
        pt.add_row([day_data["date"], day_data["day"],
                    Fore.RED + day_data["high"] + Fore.RESET,
                    Fore.BLUE + day_data["low"] + Fore.RESET, day_data["text"]])

    print(pt)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", type=str, help="City name for given forecast")
    args = parser.parse_args()

    _main()
