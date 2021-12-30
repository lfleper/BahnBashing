import scrapy
import csv
from datetime import datetime, timedelta, date
import urllib.parse

URL = 'https://reiseauskunft.bahn.de/bin/query.exe/' \
    'dn?revia=yes&existOptimizePrice-deactivated=1&country=DEU&' \
    'dbkanal_007=L01_S01_D001_qf-bahn-svb-kl2_lz03&start=1&protocol=https%3A&' \
    'REQ0JourneyStopsS0A=1&S={start}&' \
    'REQ0JourneyStopsZ0A=1&Z={end}&' \
    'date={date}&time={time}&timesel=depart&returnDate=&returnTime=&returnTimesel=depart&' \
    'optimize=0&auskunft_travelers_number=1&tariffTravellerType.1=E&tariffTravellerReductionClass.1=0&' \
    'tariffClass=2&rtMode=DB-HYBRID&externRequest=yes&HWAI=JS%21js%3Dyes%21ajax%3Dyes%21&externRequest=yes'


class Spider(scrapy.Spider):
    name = 'spider'

    @staticmethod
    def get_data():
        with open('data/routes.csv', "r") as file:
            reader = csv.reader(file)
            for row in reader:
                yield row[0], row[1], row[2], row[3]

    def start_requests(self):
        requests = []
        for data in Spider.get_data():
            for day in range(31):
                day_date = datetime.today() + timedelta(days=day)
                url_forward = URL.format(
                    start=urllib.parse.quote(data[1]),
                    end=urllib.parse.quote(data[2]),
                    date=date.strftime(day_date.date(), '%d.%m.%Y'),
                    time=urllib.parse.quote(data[3])
                )
                url_backward = URL.format(
                    start=urllib.parse.quote(data[2]),
                    end=urllib.parse.quote(data[1]),
                    date=date.strftime(day_date.date(), '%d.%m.%Y'),
                    time=urllib.parse.quote(data[3])
                )

                date_input = datetime.fromisoformat(day_date.isoformat())

                requests.append(scrapy.Request(url=url_forward, callback=self.parse, cb_kwargs=dict(req_date=date_input,route_id=data[0])))
                requests.append(scrapy.Request(url=url_backward, callback=self.parse, cb_kwargs=dict(req_date=date_input,route_id=data[0])))
        return requests

    def parse(self, response, req_date, route_id):
        for connection in response.css('tbody.boxShadow.scheduledCon'):
            first_row = connection.css('tr.firstrow')
            second_row = connection.css('tr.last')
            departure_station = first_row.css('td.station.first::text').get().strip()
            arrival_station = second_row.css('td.station.stationDest::text').get().strip()
            departure_time_raw = first_row.css('td.time::text').get().strip()
            arrival_time_raw = second_row.css('td.time::text').get().strip()
            duration_raw = first_row.css('td.duration.lastrow::text').get().strip()
            num_changes = int(first_row.css('td.changes.lastrow::text').get().strip())
            products = first_row.css('td.products.lastrow::text').get().strip()
            capacity = first_row.css('td.center.lastrow').css('img::attr(title)').get().strip()
            first_price = float(first_row.css('td.farePep').css('span.fareOutput::text').get().strip()
                              .split(u'\xa0')[0].replace(",", "."))

            second_price = float(first_row.css('td.fareStd').css('span.fareOutput::text').get().strip()
                               .split(u'\xa0')[0].replace(",", "."))
            price = min(first_price, second_price)

            departure_time_result = departure_time_raw.split(":")
            departure_time = req_date.replace(hour=int(departure_time_result[0]), minute=int(departure_time_result[1]))
            arrival_time_result = arrival_time_raw.split(":")
            arrival_time = req_date.replace(hour=int(arrival_time_result[0]), minute=int(arrival_time_result[1]))

            duration_result = duration_raw.split(":")
            duration = int(duration_result[0]) * 60 + int(duration_result[1])

            yield {
                'route_id': int(route_id),
                'departure_station': departure_station,
                'departure_time': departure_time,
                'arrival_station': arrival_station,
                'arrival_time': arrival_time,
                'price': price,
                'duration': duration,
                'num_changes': num_changes,
                'products': products,
                'capacity': capacity
            }