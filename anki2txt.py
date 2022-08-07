
import argparse
import os
import tempfile
import sqlite3
from zipfile import ZipFile



def load_from_db(db_name):
    db_conn = sqlite3.connect(db_name)
    cur = db_conn.cursor()
    #cur.execute("SELECT flds,sfld FROM notes")
    cur.execute("SELECT flds FROM notes")
    rows = cur.fetchall()  
    return rows


def load_anki(deck):
    #Unzip and read
    with ZipFile(deck, 'r') as f:
        file = f.read('collection.anki2')
    #save in a temp file
    tempdir = tempfile.TemporaryDirectory()
    TEMP_DB = tempdir.name +'/temp_anki_db'
    with open(TEMP_DB, 'wb') as f:
        f.write(file)
    #load 
    rows = load_from_db(TEMP_DB)
    # remove temp file and return
    tempdir.cleanup()
    return rows



def write_rows(rows,filename):
    with open(filename, 'w') as f:
        for r in rows:
            line="\t".join([x.replace("\t"," ").replace("\x1f","\t") for x in r])
            _ = f.write(line + '\n')



def get_name(anki_path):
    name = os.path.basename(anki_path)
    name = name.replace(".apkg","") + ".txt"
    return name




parser = argparse.ArgumentParser(description='Convert a text file into an anki deck')
parser.add_argument('anki_deck', metavar='file', type=str, help='input file')
args = parser.parse_args()



def main():
    rows=load_anki(args.anki_deck)
    name = get_name(args.anki_deck)
    write_rows(rows,name)
    print("SUCCESS: "+name+" file created!")



if __name__ == "__main__":
	main()




