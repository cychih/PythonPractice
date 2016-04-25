import requests
from bs4 import BeautifulSoup
from Crawlers import Events


class TheWallCrawler:
    def Start(self):
        res = requests.get("http://thewall.tw/shows?sort=soon")
        soup = BeautifulSoup(res.text, "html.parser")
        rows = soup.select(".macho")
        for row in rows:
            row_str = str(row)
            event_id_index_begin = row_str.index("\"/")
            event_id_index_begin += 1
            event_id_index_end = row_str.index("\">", event_id_index_begin)
            event_id_str = row_str[event_id_index_begin : event_id_index_end]
            event_url = "http://thewall.tw" + event_id_str
            res_event = requests.get(event_url)
            soup_event = BeautifulSoup(res_event.text, "html.parser")

            title_row = soup_event.select(".macho")[0].text.strip()

            event_id = event_url
            event_title = title_row
            event_performer = soup_event.select("td")[1].text.strip()
            event_price = soup_event.select("td")[2].text.strip()
            event_location = soup_event.select("td")[3].text.strip()
            event_start_time = soup_event.select(".during")[0].text
            event_end_time = soup_event.select(".during")[0].text
            event_description = soup_event.select(".content")[0].text.strip()

            event = Events.MusicEvent("TheWall", event_id, event_title, event_performer, event_price, event_location,
                                     event_start_time, event_end_time, event_description)


            print("ID = " + event.Id)
            print("Title = " + event.Title)
            print("Performer = " + event.Performer)
            print("Location = " + event.Location)
            print("Price = " + event.Price)
            print("Start from " + event.Start_time + " to " + event.End_time)
            print("Description = \n" + event.Description)

            print("\n====== End ======\n")



