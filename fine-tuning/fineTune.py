from transformers import DistilBertTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer, DataCollatorWithPadding
from datasets import Dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

if __name__ == "__main__":

    df = pd.read_csv("../scraper-to-train/cleaned.csv")
    df['rating'] = df['rating'].astype('float32')

    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = AutoModelForSequenceClassification.from_pretrained(
        "distilbert-base-uncased",
        num_labels=1
    )
    # Make it into a data set which transformers can work with
    dataset = Dataset.from_pandas(df)
    

    def tokenize_dataset(dataset):
        return tokenizer(dataset["content"], truncation = True)
    #Minimize rmse (root mean squared error)
    def compute_metrics(eval_pred):
        predications, labels = eval_pred
        mse = mean_squared_error(labels, predications)
        rmse = np.sqrt(mse)
        return {"rmse": rmse}
    #Tokenize the content field
    tokenized_dataset = dataset.map(tokenize_dataset, batched=True)

    #The regression can only work with a column named labels for some reason
    tokenized_dataset = tokenized_dataset.rename_column("rating", "labels")

    dataset_split = tokenized_dataset.train_test_split(test_size=0.2, seed=42)
    #Split traina and test
    train_dataset = dataset_split["train"]
    eval_dataset = dataset_split["test"]

    #pad sequences to maximum length in the batch
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    training_args = TrainingArguments(
        output_dir="opinionation_model",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=7,
        eval_strategy="epoch", 
        save_strategy="epoch",
        load_best_model_at_end=True,
    )

    trainer = Trainer(
        model = model,
        args = training_args,
        train_dataset = train_dataset,
        eval_dataset = eval_dataset,
        compute_metrics=compute_metrics,
        data_collator=data_collator,
    )

    trainer.train()