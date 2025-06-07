from AIBots.BaseNeuralNetworkBot import BaseNeuralNetworkBot
import keras


class SmallNeuralNetworkBot(BaseNeuralNetworkBot):
	def __init__(self, file_path=None):
		if file_path is None:
			self.model = keras.models.Sequential([
				keras.layers.Dense(15, activation='relu'),
				keras.layers.Dropout(0.2),
				keras.layers.Dense(30, activation='relu'),
				keras.layers.Dense(6, activation='softmax')
			])
			self.model.compile(optimizer='adam',
								loss='sparse_categorical_crossentropy',
								metrics=['accuracy'])
		else:
			self.model = keras.models.load_model(file_path)

	def get_title(self):
		return f"SmallNeuralNetworkBot"
