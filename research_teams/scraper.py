from enums.platform import Platform

# TODO: IMPLEMENT THIS CLASS!
class Scraper:
    def __init__(self, theme):
        self.theme = theme

    def scrape(self, platform) -> list:
        if platform == Platform.TWITTER:
            return self._scrape_twitter()
        
        if platform == Platform.WEB:
            return self._scrape_web(platform)
        
        if platform == Platform.INSTAGRAM:
            return self._scrape_instagram()

        return []

    def _scrape_twitter(self) -> list:
        return [
            "Best Gin recipie ever: 10cl Gin, 2 strawberries, tonic, cucumber",
            {"fun_facts": "Gin is made from juniper berries"},
            "Look out Gin lovers, there is a new Gin in town! I tried Stooker's Gin the other day with some of my friends and it was truly amazing! Currently you can't buy it from the store, but I ordered mine from https://stooker.nl",
        ]
    

    def _scrape_web(self, platform) -> list:
        print("Scraping web content related to the platform: " + str(platform))
        return [
            {"site": "https://www.thespruceeats.com/gin-cocktail-recipes-4151053", "text": "Gin Cocktail Recipes"},
            {"site": "http://demo.org", "text": "My journey to find the best Gin in the world has been a fun one, and I finally found it! Stooker's Gin is the best Gin I have ever tasted. I ordered mine from https://stooker.nl"},
        ]
    
    
    def _scrape_instagram(self) -> list:
        return [
            {"site": "https://www.instagram.com/p/CPq3Kp6LX8Q/", "text": "Gin Cocktail Recipes"},
            {"site": "https://www.instagram.com/p/CPq3Kp6LX8Q/", "text": "My journey to find the best Gin in the world has been a fun one, and I finally found it! Stooker's Gin is the best Gin I have ever tasted. I ordered mine from https://stooker.nl"},
        ]
    
