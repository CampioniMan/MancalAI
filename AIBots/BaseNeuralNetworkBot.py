from Game.Player import Player
from Game.GameLogicClasses import Game
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping
import numpy as np
import json
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


class BaseNeuralNetworkBot(Player):
	model = None  # Defined in each inherited class
	verbose = 0

	def get_title(self):
		pass

	def play(self, board):
		state_vector = board.get_board_state_vector()
		state_vector.append(self.player_id)
		reshaped_input_data = np.array(state_vector).reshape(1, 15)
		predictions = self.model.predict(reshaped_input_data, verbose=self.verbose)[0]

		possibilities = Game.get_possible_moves(board, self.player_id)
		for _ in predictions:
			best_play = np.argmax(predictions)
			if best_play+1 in possibilities:
				return best_play+1
			predictions[best_play] = -1
		return None

	def train(self, epoch_count, train_x_data, train_y_data, test_x_data, test_y_data):
		early_stopping_callback = EarlyStopping(
			monitor='val_loss',
			patience=35,
			verbose=1,
			restore_best_weights=True
		)
		return self.model.fit(train_x_data, train_y_data,
							epochs=epoch_count,
							validation_data=(test_x_data, test_y_data),
							callbacks=early_stopping_callback)

	def evaluate(self, test_x_data, test_y_data) -> (float, float):  # loss and accuracy
		return self.model.evaluate(test_x_data, test_y_data, verbose=2)


class Trainer:
	def __init__(self):
		self.test_data_percentage = 0.2
		self.all_data_x = []
		self.all_data_y = []

	def load_data(self, file_paths: list[str]):
		for file_path in file_paths:
			with open(file_path, 'r') as file:
				for line in file:
					data_s = json.loads(line)
					x = data_s["sv"]
					x.append(data_s["p"])
					self.all_data_x.append(x)
					self.all_data_y.append(data_s["m"]-1)
		print(f"Loaded {len(self.all_data_x)} data points")

	def get_training_data_split(self):
		return train_test_split(
			np.array(self.all_data_x), np.array(self.all_data_y), test_size=self.test_data_percentage, random_state=42)

	def train_model(self, bot: BaseNeuralNetworkBot, epoch_count):
		x_train, x_test, y_train, y_test = self.get_training_data_split()
		return bot.train(epoch_count, x_train, y_train, x_test, y_test)
