import requests
from bs4 import BeautifulSoup
from Crawlers import Events

class SongYenCrawler:
    def Start(self):
        res = requests.get("http://www.songshanculturalpark.org/ExhibitionList.aspx")
        soup = BeautifulSoup(res.text, "html.parser")
        rows = soup.select("h2")
        for row in rows:
            row_str = str(row)
            event_id_index_begin = row_str.index("?ID=")
            event_id_index_end = row_str.index("');", event_id_index_begin)
            event_id_str = row_str[event_id_index_begin : event_id_index_end]
            event_url = "http://www.songshanculturalpark.org/Exhibition.aspx" + event_id_str
            res_event = requests.get(event_url)
            soup_event = BeautifulSoup(res_event.text, "html.parser")

            title_row = soup_event.select("h5")[3].select("strong")

            event_id = event_id_str[4:]
            event_title = title_row[0].text.strip()
            date_location_row = soup_event.select("dl")[0]
            event_date = date_location_row.select("dd")[0].text.strip()
            event_location = date_location_row.select("dd")[1].text.strip()
            description_row = soup_event("p")[1]
            event_description = description_row.text.strip()

            event = Events.BaseEvent("SongYen", event_id, event_title, event_date, event_location, event_description)

            print("ID = " + event.Id)
            print("Title = " + event.Title)
            print("Date = " + event.StartDate)
            print("Location = " + event.Location)
            print("Description = \n" + event.Description)

            print("\n====== End ======\n")