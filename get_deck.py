
import argparse
import requests
from bs4 import BeautifulSoup
import tempfile
import sqlite3
from zipfile import ZipFile



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
    #Get deck
    deck_file = requests.get(r.url)
    open(deck_path, 'wb').write(deck_file.content)
    print("SUCCESS: "+deck_path+" file obtained!")
    return deck_path




def anki2txt(anki_deck):
    name = anki_deck.replace(".apkg","") + ".cards.txt"
    #Unzip and read and save in a temp file
    with ZipFile(anki_deck, 'r') as f:
        file = f.read('collection.anki2')
    tempdir = tempfile.TemporaryDirectory()
    TEMP_DB = tempdir.name +'/temp_anki_db'
    with open(TEMP_DB, 'wb') as f:
        f.write(file)
    #Load from temp database
    db_conn = sqlite3.connect(TEMP_DB)
    cur = db_conn.cursor()
    cur.execute("SELECT flds FROM notes")
    rows = cur.fetchall()  
    #Remove temp file 
    tempdir.cleanup()
    with open(name, 'w') as f:
        for r in rows:
            line="\t".join([x.replace("\t"," ").replace("\x1f","\t") for x in r])
            _ = f.write(line + '\n')
    print("SUCCESS: "+name+" file created!")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a text file into an anki deck')
    parser.add_argument('url_deck', metavar='file', type=str, help='input file')
    parser.add_argument('--text', '-t', action='store_true', default=False,  help='Flag to extract the text')
    args = parser.parse_args()
    deck_path = download_deck(args.url_deck)
    if args.text:
        print("Converting to text...")
        anki2txt(deck_path)

