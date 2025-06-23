from AIBots.BaseNeuralNetworkBot import BaseNeuralNetworkBot
from AIBots.BaseNeuralNetworkBot import RangedClampNormalization
import keras


class BigNeuralNetworkBot(BaseNeuralNetworkBot):
	def __init__(self, file_path=None):
		if file_path is None:
			self.model = keras.models.Sequential([
				keras.layers.Input(shape=(15,)),
				RangedClampNormalization(44, range(0, 14)),
				keras.layers.Dense(512, activation='relu'),
				keras.layers.Dropout(0.1),
				keras.layers.Dense(1024, activation='relu'),
				keras.layers.Dropout(0.1),
				keras.layers.Dense(2048, activation='relu'),
				keras.layers.Dense(2048, activation='relu'),
				keras.layers.Dense(6, activation='softmax')
			])
			self.model.compile(optimizer='adam',
								loss='sparse_categorical_crossentropy',
								metrics=['accuracy'])
		else:
			self.model = keras.models.load_model(file_path)

	def get_title(self):
		return f"BigNeuralNetworkBot"
