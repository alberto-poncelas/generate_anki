
import argparse
import requests
from bs4 import BeautifulSoup



def download_deck(url_deck,save_path="./"):
    #Get deck info
    url_request=requests.get(url_deck)
    soup=BeautifulSoup(url_request.text,"html.parser")
    #Get title
    title = soup.select('h1')[0].text
    title = title.replace(" ","_") + ".apkg"
    deck_path = save_path+"/"+title
    #Build request
    dwld_url = url_deck.replace("https://","https://dl15.").replace("/info/","/downloadDeck/")
    deck_form = soup.select('form input')[0]
    data= {
        deck_form["name"]: deck_form["value"]
    }
    r = requests.post(dwld_url,data=data)
    #get deck
    deck_file = requests.get(r.url)
    open(deck_path, 'wb').write(deck_file.content)
    return deck_path




parser = argparse.ArgumentParser(description='Convert a text file into an anki deck')
parser.add_argument('url_deck', metavar='file', type=str, help='input file')
args = parser.parse_args()



def main():
    deck_path = download_deck(args.url_deck,save_path="./")
    print("SUCCESS: "+deck_path+" file obtained!")



if __name__ == "__main__":
	main()

