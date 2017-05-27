import random
from rnn import Rnn
import numpy as np

class TextRnn(Rnn):
	escape_control = '<><><>'

	def __init__(self,filename):
		super(TextRnn, self).__init__(filename)
		self.hidden_size = 25 # size of hidden layer of neurons
		self.iterations_per_log = 10

	def readFile(self, filename):
		'''Get data from a specified filename for use in this'''
		self.data_name = filename + '.rnnpy'
		file_data = open(filename, 'r').read()
		self.data = self.split_file_data(file_data)
		self.chars = self.find_unique_words()
		self.data_size, self.vocab_size = len(self.data), len(self.chars)
		print('data has {0} characters, {1} of which are unique.'.format(self.data_size, self.vocab_size))
		self.char_to_ix = { ch:i for i,ch in enumerate(self.chars) }
		self.ix_to_char = { i:ch for i,ch in enumerate(self.chars) }

	def split_file_data(self, data):
		'''Adds a special escape control character to help with stepping'''
		d = data.replace('\n', ' {0} '.format(TextRnn.escape_control))
		return d.split()

	def find_unique_words(self):
		unique = set(self.data)
		unique.remove(TextRnn.escape_control)
		return list(unique)

	def measure_sequence(self, p):
		'''Looks for an escape sequence'''
		while True:
			sequence_length = self.data[p:].index(TextRnn.escape_control)
			if sequence_length > 1:
				return p, sequence_length
			p += 2

	def randomSample(self,length):
		sample_ix = self.sample(random.randint(0,self.vocab_size-1), length)
		txt = ' '.join(self.ix_to_char[ix] for ix in sample_ix)
		return txt

	def step(self, p):
		'''Does the heavy lifting'''

		try:
			p, sequence_length = self.measure_sequence(p)
		except: # ValueError: escape_control is not in list
			p = 0 # go from start of data
			p, sequence_length = self.measure_sequence(p)
			self.hprev = np.zeros((self.hidden_size,1)) # reset RNN memory

		smooth_loss = -np.log(1.0/self.vocab_size)*sequence_length # loss at iteration 0
		# prepare inputs (we're sweeping from left to right in steps seq_length long)

		inputs = [self.char_to_ix[ch] for ch in self.data[p:p+sequence_length-1]]
		targets = [self.char_to_ix[ch] for ch in self.data[p+1:p+sequence_length]]

		# forward seq_length characters through the net and fetch gradient
		loss, dWxh, dWhh, dWhy, dbh, dby = self.lossFun(inputs, targets)
		smooth_loss = smooth_loss * 0.999 + loss * 0.001

		# perform parameter update with Adagrad
		for param, dparam, mem in zip([self.Wxh, self.Whh, self.Why, self.bh, self.by],
				[dWxh, dWhh, dWhy, dbh, dby],
				[self.mWxh, self.mWhh, self.mWhy, self.mbh, self.mby]):
			mem += dparam * dparam
			param += -self.learning_rate * dparam / np.sqrt(mem + 1e-8) # adagrad update

		return p + sequence_length + 1
