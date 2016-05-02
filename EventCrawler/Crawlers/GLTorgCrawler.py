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
        URL_iter = 1
        URLs = []
        First_page_URL = "http://www.glt.org.tw/?cat=20&show_yr=2016&show_mo=%25"
        URLs.append(First_page_URL)
        if len(pages) > 1:
            while URL_iter < len(pages):
                Next_page_URL = First_page_URL + "&paged=" + str((URL_iter+1))
                URL_iter += 1
                URLs.append(Next_page_URL)

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
                    event_url_index_begin = item_row.index("href=\"http://", event_url_index_find)
                    event_url_index_end = item_row.index("?p=", event_url_index_begin)
                    event_url_index_find = event_url_index_end
                    event_url_index_begin += 6
                    event_url_index_end += 7
                    event_url = item_row[event_url_index_begin:event_url_index_end]
                except:
                    break

                item_event = requests.get(event_url)
                #item_event = requests.get("http://www.glt.org.tw/?p=7049")
                soup_event = BeautifulSoup(item_event.text, "html.parser")

                title_row = soup_event.select("h1")[0].text

                event_id = event_url
                event_title = title_row
                event_location = ''
                event_location_parser = soup_event.select("p")

                if "地點" in str(event_location_parser):
                    iter_event_location_parser = 0
                    while iter_event_location_parser < 7: # predict index number for location in lists won't exceed 5
                        if "牯嶺街" in str(event_location_parser[iter_event_location_parser]):
                            event_location_raw = event_location_parser[iter_event_location_parser].text.strip()
                            try:
                                event_location_index_begin = event_location_raw.index("牯")

                                if "1F" in event_location_raw:
                                    try:
                                        event_location_index_end = event_location_raw.index("實驗", event_location_index_begin)
                                        event_location_index_end += 4
                                    except:
                                        print("1F location index has error")
                                elif "3F" in event_location_raw:
                                    try:
                                        event_location_index_end = event_location_raw.index("練場", event_location_index_begin)
                                        event_location_index_end += 2
                                    except:
                                        print("3F location index has error")
                                else:
                                    try:
                                        event_location_index_end = event_location_raw.index("間", event_location_index_begin)
                                        event_location_index_end += 1
                                    except:
                                        print("Other floors' location index has error")
                            except:
                                print("location index has error")
                            event_location = event_location_raw[event_location_index_begin:event_location_index_end]
                            break
                        iter_event_location_parser += 1

                event_price = ''
                event_price_parser = soup_event.select("p")

                if "票價" in str(event_price_parser):
                    iter_event_price_parser = 0
                    while iter_event_price_parser < len(event_price_parser):
                        if "票價" in str(event_price_parser[iter_event_price_parser]):
                            event_price_raw = event_price_parser[iter_event_price_parser].text.strip()
                            price_nums = event_price_raw.split("、")
                            for price_num in price_nums:
                                if "票價" in price_num:
                                    if len(price_num) < 9:
                                        event_price += price_num + '、'
                                    else:
                                        try:
                                            event_price_index_begin = price_num.index("票價")
                                            event_price_index_end = price_num.index("\n", event_price_index_begin)
                                            event_price += price_num[event_price_index_begin:event_price_index_end]
                                            break
                                        except:
                                            try:
                                                event_price_index_end = price_num.index("元", event_price_index_begin)
                                                event_price_index_end += 1
                                                event_price += price_num[event_price_index_begin:event_price_index_end]
                                                break
                                            except:
                                                if "免費" in price_num:
                                                    try:
                                                        event_price_index_end = price_num.index("免費", event_price_index_begin)
                                                        event_price_index_end += 2
                                                        event_price += price_num[event_price_index_begin:event_price_index_end]
                                                        break
                                                    except:
                                                        print("{0} has special price rules".format(event_url))
                                                print("{0} price index has error".format(event_url))
                                elif "元" in price_num:
                                    if len(price_num) < 6:
                                        event_price += price_num + '、'
                                elif "00" in price_num:
                                    if len(price_num) < 12:
                                        event_price += price_num + '、'
                        iter_event_price_parser += 1
                elif "索" in str(event_price_parser):
                    event_price_raw = str(event_price_parser)
                    try:
                        event_price_index_begin = event_price_raw.index("索票")
                        event_price_index_begin -= 3 # 下面索票的 if 不知道為什麼一定會跑到, 所以這邊 range 給大一些
                        event_price_index_end = event_price_index_begin + 7
                        event_price = event_price_raw[event_price_index_begin:event_price_index_end]
                    except:
                        print("索票入場 index has error")
                if event_price is not '':
                    if event_price[-1] == '、':
                        event_price = event_price[:-1]
                    if "索票" or "免費" not in event_price:
                        event_price = event_price[3:]
                event_start_time = item_soup.select(".start")[number].text.strip()
                event_end_time = item_soup.select(".end")[number].text.strip()
                number += 1
                event_description = soup_event.select(".post-content")[0].text

                event = Events.DramaEvent("GLTorg", event_id, event_title, event_start_time, event_end_time,
                                          event_description, event_location, event_price)

                print("ID = " + event.Id)
                print("Title = " + event.Title)
                print("Location = " + event.Location)
                print("Price = " + event.Price)
                print("Start from " + event.Start_time + " to " + event.End_time)
                print("Description = \n" + event.Description)

                print("\n====== End ======\n")












