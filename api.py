import io
import json
import torch
import os
import logging

from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AdamW


app = Flask(__name__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# model specifications
config = \
    {
        "model_id": "distilbert-base-uncased",
        "model_name": "distilbert",
        "epochs": 4,
        "batch_size": 24,
        "lr": 2e-5,
        "labels": ["none", "negative", "neutral", "positive", "conflict"],
        "aspects": ["food", "service", "price", "ambience", "anecdotes"]
    }

model_id = config["model_id"]
labels = config["labels"]
num_labels = len(labels)
model_file_name = config["model_id"] + ".pth"
tokenizer = AutoTokenizer.from_pretrained(model_id)
aspects = config["aspects"]
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_dir=''

model = AutoModelForSequenceClassification.from_pretrained(model_id, num_labels=num_labels)
with open(os.path.join(model_dir, 'distilbert_base_uncased.pth'), 'rb') as f:
    model.load_state_dict(torch.load(f))


def get_prediction(input_data):
    logger.info(input_data)
    with torch.no_grad():
        input_ids = input_data["input_ids"].to(device)
        attention_mask = input_data["attention_mask"].to(device)

        output = model(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        logits = output["logits"]

        predicted = torch.softmax(logits, -1).argmax(-1)
        y_pred = predicted.cpu()

    return {a: labels[y_pred[i]] for i, a in enumerate(aspects)}

def transform_data(data):
    encoded = tokenizer(
        5 * [data],
        aspects,
        padding=True,
        truncation=True,
        max_length=512,
        return_tensors="pt"
    )
    return encoded


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        data = request.form['text']
        data = transform_data(data)
        prediction = get_prediction(data)
        return jsonify(prediction)


if __name__ == '__main__':
    app.run()