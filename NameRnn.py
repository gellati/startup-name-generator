from rnn import Rnn
import numpy as np
import random

class NameRnn(Rnn):
	'''
	RNN which learns from a list of names
	'''

	def __init__(self):
		super(NameRnn, self).__init__('names.txt')
		self.minimum_name_length = 3
		self.maximum_name_length = 12
		self.iterations_per_log = 1000

	def validate(self,name):
		'''Validate that the first char and length are appropriate'''
		return (self.is_letter(name[0]) and self.is_acceptable_length(name))

	def is_letter(self, character):
		return ord(character) in range(65,90)

	def is_acceptable_length(self, name):
		return self.meets_maximum_length(name) and self.meets_minimum_length(name)

	def meets_minimum_length(self, name):
		return len(name) >= self.minimum_name_length

	def meets_maximum_length(self, name):
		return len(name) <= self.maximum_name_length

	def get(self,num):
		'''Gets a list of generated names'''
		names = []
		while len(names) < num:
			start_char_id = random.randint(0, len(self.char_to_ix)-1)
			start = self.ix_to_char[start_char_id]

			self.hprev = np.random.randn(len(self.hprev), 1)
			sample_ix = self.sample(self.char_to_ix[start], 30, training=False)
			txt = ''.join(self.ix_to_char[ix] for ix in sample_ix)

			# Clean up
			for name in txt.split():
				if self.validate(name):
					names.append(name.capitalize())
		self.saveParameters()
		return names

	def print_names(self, rows, columns):
		for name in [self.get(columns) for i in range(rows)]:
			out = ''
			for x in name:
				out += x.ljust(15)
			print(out)

	def step(self,p):
		'''Does the heavy lifting'''
		smooth_loss = -np.log(1.0/self.vocab_size)*self.seq_length # loss at iteration 0
		# prepare inputs (we're sweeping from left to right in steps seq_length long)
		if p+self.seq_length+1 >= len(self.data):
			self.hprev = np.zeros((self.hidden_size,1)) # reset RNN memory
			p = 0 # go from start of data

		inputs = [self.char_to_ix[ch] for ch in self.data[p:p+self.seq_length]]
		targets = [self.char_to_ix[ch] for ch in self.data[p+1:p+self.seq_length+1]]

		# forward seq_length characters through the net and fetch gradient
		loss, dWxh, dWhh, dWhy, dbh, dby = self.lossFun(inputs, targets)
		smooth_loss = smooth_loss * 0.999 + loss * 0.001

		# perform parameter update with Adagrad
		for param, dparam, mem in zip([self.Wxh, self.Whh, self.Why, self.bh, self.by],
				[dWxh, dWhh, dWhy, dbh, dby],
				[self.mWxh, self.mWhh, self.mWhy, self.mbh, self.mby]):
			mem += dparam * dparam
			param += -self.learning_rate * dparam / np.sqrt(mem + 1e-8) # adagrad update

		next_ind = p + self.data[p:p+self.seq_length].index(' ')+1 # move data pointer
		#print(self.data[p:next_ind])
		return next_ind
