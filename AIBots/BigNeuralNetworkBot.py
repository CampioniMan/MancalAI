from AIBots.BaseNeuralNetworkBot import BaseNeuralNetworkBot
import keras


class BigNeuralNetworkBot(BaseNeuralNetworkBot):
	def __init__(self, file_path=None):
		if file_path is None:
			self.model = keras.models.Sequential([
				keras.layers.Input(shape=(15,)),
				keras.layers.Dense(256, activation='relu'),
				keras.layers.Dropout(0.5),
				keras.layers.Dense(512, activation='relu'),
				keras.layers.Dropout(0.5),
				keras.layers.Dense(512, activation='relu'),
				keras.layers.Dropout(0.5),
				keras.layers.Dense(256, activation='relu'),
				keras.layers.Dropout(0.3),
				keras.layers.Dense(128, activation='relu'),
				keras.layers.Dense(6, activation='softmax')
			])
			self.model.compile(optimizer='adam',
								loss='sparse_categorical_crossentropy',
								metrics=['accuracy'])
		else:
			self.model = keras.models.load_model(file_path)

	def get_title(self):
		return f"BigNeuralNetworkBot"
