import joblib

model = joblib.load('model.pkl')

def classify_packet(features):
    prediction = model.predict([features])
    return prediction[0]