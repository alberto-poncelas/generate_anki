
import sys
import genanki
import random
import os
import argparse


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
		self.id=rand_id
		self.name = name
		self.deck = genanki.Deck( rand_id, name)
	#Add a pair of [question,answer] as a card to the deck
	def add_card(self,QA):
		[Q,A]=QA
		self.id=self.id+1
		card = genanki.Note(model=card_template,fields=[Q,A],guid=self.id)
		self.deck.add_note(card)
	#Export the deck to a apkg file
	def export(self):
		genanki.Package(self.deck).write_to_file(self.name+'.apkg')




parser = argparse.ArgumentParser(description='Convert a text file into an anki deck')
parser.add_argument('vocab_path', metavar='file', type=str, help='input file')
parser.add_argument('--sep', dest='separator', type=str, default="," , help='columns separator')
args = parser.parse_args()




vocab_path = args.vocab_path
split_char = args.separator
name = os.path.split(vocab_path)[-1]



def main():
	#Load file
	cards_list=[]
	file_error=False
	idx=0
	with open(vocab_path) as f:
		for raw_line in f:
			idx=idx+1
			QA_pair=raw_line.strip().split(split_char)
			if len(QA_pair)!=2:
				print("ERROR: Line "+str(idx) +" does not have two fields")
				file_error=True
			cards_list.append(QA_pair)

	if file_error:
		sys.exit("Process finished with errors")

	#Create deck and add cards
	deck=Deck(name)
	for card in cards_list:
		deck.add_card(card)
	deck.export()

	print("SUCCESS: "+name+".apkg file created!")




if __name__ == "__main__":
	main()
