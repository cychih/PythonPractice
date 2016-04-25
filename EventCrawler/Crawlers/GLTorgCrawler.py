import requests
from bs4 import BeautifulSoup
from Crawlers import Events


class GLTorgCrawler:

    def Start(self):
        multi_res = []
        res = requests.get("http://www.glt.org.tw/?cat=20&show_yr=2016&show_mo=%25")
        soup = BeautifulSoup(res.text, "html.parser")
        page_flag = soup.select("#pagenum_links")[0]
        pages = page_flag.text.split()
        i = 0
        for page in pages:
            if len(page) != 1:
                page = page[1]
                pages[i] = page
            i += 1

        page_flagToURLs = str(page_flag)
        URLs = []
        URLs.append("http://www.glt.org.tw/?cat=20&show_yr=2016&show_mo=%25")
        URL_find_begin = 0

        while True:
            try:
                URL_index_begin = page_flagToURLs.index("http:", URL_find_begin)
                URL_index_end = page_flagToURLs.index("paged=", URL_index_begin)
                URL_find_begin = URL_index_end
                URL_index_end += 7
                URL = page_flagToURLs[URL_index_begin:URL_index_end]
                URLs.append(URL)
            except:
                break
        for page, url in zip(pages, URLs):
            multi_res.append((page, url))

        for item in multi_res:
            item_res = None
            item_soup = None
            item_res = requests.get(item[1])
            item_soup = BeautifulSoup(item_res.text, "html.parser")
            item_row = str(item_soup.select(".thumbnail"))
            event_url_index_find = 0
            number = 0
            while True:
                try:
                    event_url_index_begin = item_row.index("http://", event_url_index_find)
                    event_url_index_end = item_row.index("?p=", event_url_index_begin)
                    event_url_index_find = event_url_index_end
                    event_url_index_end += 7
                    event_url = item_row[event_url_index_begin:event_url_index_end]
                except:
                    break
                item_event = requests.get(event_url)
                soup_event = BeautifulSoup(item_event.text, "html.parser")

                title_row = soup_event.select("h1")[0].text

                event_id = event_url
                event_title = title_row
                '''event_price =
                event_location ='''
                event_start_time = item_soup.select(".start")[number].text.strip()
                event_end_time = item_soup.select(".end")[number].text.strip()
                number += 1
                event_description = soup_event.select(".post-content")[0].text

                event = Events.DramaEvent("GLTorg", event_id, event_title, event_start_time, event_end_time,
                                          event_description)

                print("ID = " + event.Id)
                print("Title = " + event.Title)
                print("Location = " + event.Location)
                print("Price = " + event.Price)
                print("Start from " + event.Start_time + " to " + event.End_time)
                print("Description = \n" + event.Description)

                print("\n====== End ======\n")






