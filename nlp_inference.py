from tensorflow.keras.preprocessing.sequence import pad_sequences
import matplotlib.pyplot as plt
import pickle
from tensorflow.keras.models import load_model

def predict(text, model_path, token_path):
    # 该方法输入指定的模型h5文件的地址以及指定的tokenizer的地址

    model = load_model(model_path)


    with open(token_path, 'rb') as f:
        tokenizer = pickle.load(f)

    sequences = tokenizer.texts_to_sequences([text])
    x_new = pad_sequences(sequences, maxlen=50)
    predictions = model.predict([x_new, x_new])

    emotions = {0: 'anger', 1: 'neutral', 2: 'joy', 3:'sadness'}

    probs = list(predictions[0])
    prediction = probs.index(max(probs))

    return emotions[prediction]