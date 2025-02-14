import spacy
import json
from spacy.training import Example

TRAIN_DATA_FILE = "train_data.json"
OUTPUT_MODEL_DIR = "ner_model"

def load_train_data():
    with open(TRAIN_DATA_FILE, "r", encoding="utf-8") as f:
        train_data = json.load(f)
    return train_data

def train_ner():
    nlp = spacy.blank("en")  
    ner = nlp.add_pipe("ner", last=True)

    train_data = load_train_data()
    
    for entry in train_data:
        for _, _, label in entry["entities"]:
            ner.add_label(label)

    optimizer = nlp.begin_training()
    examples = []

    for entry in train_data:
        text = entry["text"]
        entities = [(start, end, label) for start, end, label in entry["entities"]]
        examples.append(Example.from_dict(nlp.make_doc(text), {"entities": entities}))

    for _ in range(30):  # Train for 30 epochs
        losses = {}
        nlp.update(examples, drop=0.3, losses=losses)
        print(f"Losses: {losses}")

    nlp.to_disk(OUTPUT_MODEL_DIR)
    print(f"Model saved to {OUTPUT_MODEL_DIR}")

if __name__ == "__main__":
    train_ner()
