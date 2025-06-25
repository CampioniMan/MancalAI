from Game.Player import Player
from Game.GameLogicClasses import Game
from AIBots.BaseNeuralNetworkBot import RangedClampNormalization
import keras
import numpy as np
import random


class CompoundNeuralNetworkBot(Player):
	def __init__(self, models_path, sample_percentage):
		self.sample_percentage = sample_percentage
		self.models = []
		for model_path in models_path:
			self.models.append(keras.models.load_model(model_path, custom_objects={'RangedClampNormalization': RangedClampNormalization}))

	def play(self, board):
		state_vector = board.get_board_state_vector()
		state_vector.append(self.player_id)
		reshaped_input_data = np.array(state_vector).reshape(1, 15)

		possibilities = Game.get_possible_moves(board, self.player_id)
		answers = [0, 0, 0, 0, 0, 0]
		chosen_models = random.sample(self.models, max(int(len(self.models) * self.sample_percentage), 1))
		for model in chosen_models:
			predictions = model.predict(reshaped_input_data, verbose=0)[0]
			for _ in predictions:
				best_play = np.argmax(predictions)
				if best_play + 1 in possibilities:
					answers[best_play] += 1
					break
				predictions[best_play] = -1
		possible_answers = CompoundNeuralNetworkBot.find_multiple_max_indices_numpy(answers)
		return random.choice(possible_answers) + 1

	@staticmethod
	def find_multiple_max_indices_numpy(arr):
		if len(arr) == 0:
			return np.array([])
		max_value = np.max(arr)
		return np.where(arr == max_value)[0]

	def get_title(self):
		return f"CompoundNeuralNetworkBot"
