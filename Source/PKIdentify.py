import aiohttp
import numpy as np
import tensorflow as tf

class Pokefier:
    def __init__(self):
        self.labels = eval(open('Source/Names.txt', 'r').read())
        self.interpreter_pool = [self._initialize_interpreter() for _ in range(5)]

    def _remove_alpha_channel(self, image):
        return image[:, :, :3]

    def _preprocess_input_image(self, image):
        img = tf.image.resize(image, [224, 224]) / 255.0
        return img

    async def _prepare_image_for_prediction(self, image_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                image_data = await response.read()

        image = tf.image.decode_image(image_data, channels=3).numpy()
        preprocessed_image = self._preprocess_input_image(image)

        return preprocessed_image

    async def predict_pokemon_from_url(self, image_url):
        interpreter = self._get_interpreter_from_pool()

        # Preprocess And Prepare Image For Prediction
        preprocessed_image = await self._prepare_image_for_prediction(image_url)

        # Predict Teh Pokemon Lable
        predicted_pokemon = await self._predict_pokemon(interpreter, [preprocessed_image.numpy()])

        # Return The Interpreter To The Pool
        self._return_interpreter_to_pool(interpreter)

        return predicted_pokemon

    def _initialize_interpreter(self):
        tflite_model_path = 'src/pokefier.tflite'
        interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
        interpreter.allocate_tensors()
        return interpreter

    def _get_interpreter_from_pool(self):
        return self.interpreter_pool.pop()

    def _return_interpreter_to_pool(self, interpreter):
        self.interpreter_pool.append(interpreter)

    async def _predict_pokemon(self, interpreter, image):
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        input_data = tf.convert_to_tensor(image, dtype=tf.float32)
        interpreter.set_tensor(input_details[0]['index'], input_data)

        interpreter.invoke()

        output_data = interpreter.get_tensor(output_details[0]['index'])
        predicted_class_index = np.argmax(output_data)
        predicted_label = self.labels[predicted_class_index]

        # Get Prediction Score And Create Tuple
        prediction_scores = output_data[0]
        predictions = [(self.labels[i], round(score * 100, 1)) for i, score in enumerate(prediction_scores)]

        # Sort Predictions By Score
        predictions.sort(key=lambda x: x[1], reverse=True)

        # Return Predictions ( Top 3 )
        return predictions[:3]
