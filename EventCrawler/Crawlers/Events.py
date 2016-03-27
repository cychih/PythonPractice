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