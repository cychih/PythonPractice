class BaseEvent:
    def __init__(self, site, id, title, start_date, location, description, price = 0):
        self.Site = site
        self.Id = id
        self.Title = title
        self.StartDate = start_date
        self.Location = location
        self.Description = description
        self.Price = price
    def __eq__(self, other):
        return self.Id ==  other.Id
    def __str__(self):
        return self.Title


class MusicEvent(BaseEvent):

    def __init__(self, site, id, title, performer, price, location, start_time, end_time, description):
        self.Site = site
        self.Id = id
        self.Title = title
        self.Performer = performer
        self.Price = price
        self.Location = location
        self.Start_time = start_time
        self.End_time = end_time
        self.Description = description

class DramaEvent(BaseEvent):

    def __init__(self, site, id, title, start_time, end_time, description, price='', location=''):
        self.Site = site
        self.Id = id
        self.Title = title
        self.Price = price
        self.Location = location
        self.Start_time = start_time
        self.End_time = end_time
        self.Description = description

