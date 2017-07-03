import requests
import urllib
import os
import json
from bs4 import BeautifulSoup


class Google(object):

    @classmethod
    def get_soup(self, url,header):
        return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)),'html.parser')

    @classmethod
    def get_image(self, image_name, num_images=1):
        google_url = "https://www.google.com"
        #image_type = "ActiOn"

        image_name = image_name.split()
        image_name ='+'.join(image_name)

        url = google_url + "/search?q="+image_name+"&source=lnms&tbm=isch"
        print(url)

        DIR="../images"
        header={
            'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        }
        soup = self.get_soup(url,header)

        #Extrai os links das imagens imagens do HTML Soup.
        #"ou": link da imagem
        #"ity": tipo da imagem (ex: .png)
        actual_images = []
        for i, a in enumerate(soup.find_all("div",{"class":"rg_meta"})):
            if i == num_images:
                break
            link , Type = json.loads(a.text)["ou"] , json.loads(a.text)["ity"]
            actual_images.append((link,Type))

        #cria diretorio /images, se nao existir
        if not os.path.exists(DIR):
            os.mkdir(DIR)

        #cria diretorio para o pokemon /images/<nome_do_pokemon>, se nao existir
        DIR = os.path.join(DIR, image_name.split()[0])
        if not os.path.exists(DIR):
            os.mkdir(DIR)
        
        #Salva cada imagem no diretório.
        for i , (img , Type) in enumerate(actual_images):
            try:
                req = urllib.request.Request(img, headers=header)
                raw_img = urllib.request.urlopen(req).read()

                cntr = image_name + str(len([i for i in os.listdir(DIR)]) + 1)

                if len(Type) == 0:
                    f = open(os.path.join(DIR , str(cntr)+".jpg"), 'wb')
                else :
                    f = open(os.path.join(DIR , str(cntr)+"."+Type), 'wb')

                f.write(raw_img)
                f.close()
            except Exception as e:
                print("could not load : "+img)
                print(str(e)+"\n")
        print("DIR:", DIR)
        return DIR


if __name__ == '__main__':

    pokemons = ["snorlax"]
    #pokemons = ["snorlax", "pikachu", "bulbassaur", "charmander", "squirtle"]

    for pokemon in pokemons:
        Google.get_image(pokemon, num_images=10)

    
