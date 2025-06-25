from AIBots.BaseNeuralNetworkBot import BaseNeuralNetworkBot
from AIBots.BaseNeuralNetworkBot import RangedClampNormalization
import keras


class BigNeuralNetworkBot(BaseNeuralNetworkBot):
	def __init__(self, file_path=None):
		if file_path is None:
			self.model = keras.models.Sequential([
				keras.layers.Input(shape=(15,)),
				RangedClampNormalization(48, range(0, 14)),
				keras.layers.Dense(256, activation=keras.activations.relu),
				keras.layers.Dropout(0.15),
				keras.layers.Dense(512, activation=keras.activations.relu),
				keras.layers.Dropout(0.25),
				keras.layers.Dense(1024, activation=keras.activations.relu),
				keras.layers.Dropout(0.35),
				keras.layers.Dense(4096, activation=keras.activations.relu),
				keras.layers.Dense(6, activation=keras.activations.softmax)
			])
			self.model.compile(optimizer='adam',
								loss='sparse_categorical_crossentropy',
								metrics=['accuracy'])
		else:
			self.model = keras.models.load_model(file_path, custom_objects={'RangedClampNormalization': RangedClampNormalization})

	def get_title(self):
		return f"BigNeuralNetworkBot"
