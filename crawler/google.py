import requests
import re
import urllib2
import os
import cookielib
import json
from bs4 import BeautifulSoup


class Google(object):

    @classmethod
    def get_soup(self, url,header):
        return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

    @classmethod
    def get_image(self, image_name, num_images=1):
        google_url = "https://www.google.com"
        image_type = "ActiOn"

        image_name = image_name.split()
        image_name ='+'.join(image_name)
        
        url = google_url + "/search?q="+image_name+"&source=lnms&tbm=isch"

        print url

        DIR="../images"
        header={
            'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        }
        soup = self.get_soup(url,header)

        actual_images = []
        for i, a in enumerate(soup.find_all("div",{"class":"rg_meta"})):
            if i == num_images:
                break
            link , Type = json.loads(a.text)["ou"] , json.loads(a.text)["ity"]
            actual_images.append((link,Type))

        if not os.path.exists(DIR):
            os.mkdir(DIR)
        
        for i , (img , Type) in enumerate(actual_images):
            if Type != "gif":
                try:
                    req = urllib2.Request(img, headers={'User-Agent' : header})
                    raw_img = urllib2.urlopen(req).read()

                    cntr = image_name + "_" + str(len([i for i in os.listdir(DIR) if image_name in i]) + 1)

                    if len(Type) == 0:
                        f = open(os.path.join(DIR , str(cntr)+".jpg"), 'wb')
                    else :
                        f = open(os.path.join(DIR , str(cntr)+"."+Type), 'wb')

                    f.write(raw_img)
                    f.close()
                except Exception as e:
                    print "could not load : "+img
                    print e
        print "DIR:", DIR
        


if __name__ == '__main__':

    pokemons = ["pikachu", "charmander", "bulbassaur", "diglett", "mewtwo", "magikarp", "staryu", "onix", "machop",
                "charizard", "snorlax", "blastoise", "mew", "psyduck", "gengar", "dragonite", "gyrados", "scyther",
                "growlithe", "arcanine", "articuno", "zapdos", "haunter", "squirtle", "eevee", "alakazam", "lapras"]

    for pokemon in pokemons:
        Google.get_image(pokemon, num_images=40)

    
