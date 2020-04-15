
import sys
import genanki
import random
import os


card_template = genanki.Model(
	random.randrange(1 << 30, 1 << 31),
		'Simple Model',
	fields=[
		{'name': 'Question'},
		{'name': 'Answer'},
	],
	templates=[
	{
		'name': 'Card',
		'qfmt': '<div style="text-align: center;font-size: 30px;">{{Question}}</div>',
		'afmt': '<div style="text-align: center;font-size: 30px;">{{Question}}</div><hr>'+
			'<div style="text-align: center;font-size: 20px;">{{Answer}}</div>',
	},
	])


class Deck:
	def __init__(self, name):
		rand_id = random.randrange(1 << 30, 1 << 31)
		self.name = name
		self.deck = genanki.Deck( rand_id, name)
	#Add a pair of [question,answer] as a card to the deck
	def add_card(self,QA):
		[Q,A]=QA
		card = genanki.Note(model=card_template,fields=[Q,A])
		self.deck.add_note(card)
	#Export the deck to a apkg file
	def export(self):
		genanki.Package(self.deck).write_to_file(self.name+'.apkg')




if len(sys.argv)-1 != 1:
	print("ERROR: "+str(len(sys.argv)-1) +" parameters found")
	print("Usage: python3 generate_anki.py deck_name path/to/file")
	exit()


vocab_path = sys.argv[1]

#Get the name
[head, tail]= os.path.split(vocab_path) 
name = os.path.splitext(tail)[0]



#Load file
with open(vocab_path) as f:
	raw_vocab = f.readlines()


#Try different characters to find the separator
def find_split_char(raw_vocab):
	vocab_size=len(raw_vocab)
	split_char_candidates=[",","\t",";","|"]
	for ch in split_char_candidates:
		if ([x.count(ch) for x in raw_vocab] == [1]*vocab_size):
			return ch
	return ","

split_char=find_split_char(raw_vocab)
cards_list=[x.strip().split(split_char) for x in raw_vocab]



#Create deck and add cards
deck=Deck(name)
for card in cards_list:
	deck.add_card(card)


deck.export()


print("SUCCESS: "+name+".apkg file created!")