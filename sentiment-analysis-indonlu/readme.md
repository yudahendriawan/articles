---
title: In-depth Sentiment Analysis with Deep Learning (Study Case: IndoNLU Dataset)
---

## Introduction: Why is Sentiment Important in the Digital Age?

In the midst of the rapid flow of digital information, the ability to understand what people feel and think has become crucial. Sentiment analysis, often referred to as opinion mining, is a field within Natural Language Processing (NLP) that enables computers to automatically identify and categorize the emotions or attitudes expressed in a piece of text. This includes classifying sentiment into categories such as positive, negative, or neutral.

Every day, billions of text data are generated from various sources, ranging from social media posts, product reviews, to customer service emails. In this massive digital ecosystem, sentiment analysis allows organizations to automatically and at scale gain insights into public opinion, customer feedback, market sentiment, or even detect potential reputation crises.

To achieve this advanced level of language understanding, this project leverages artificial intelligence (AI), specifically Deep Learning. Deep Learning (DL) is a subset of Machine Learning (ML) that uses artificial neural network architectures with many hidden layers, enabling them to learn highly complex data representations. This capability makes Deep Learning a much more efficient and powerful approach, especially for unstructured data like text, where patterns and nuances of meaning can be very intricate.

## Getting to Know IndoBERT: A Revolutionary Language Model for the Indonesian Context

To understand sentiment in Indonesian text, this project utilizes an advanced language model called IndoBERT. This model is built upon a revolutionary architecture known as BERT.

### What is BERT? (Bidirectional Encoder Representations from Transformers)

BERT, short for Bidirectional Encoder Representations from Transformers, is one of the most innovative language models in the field of NLP. Its primary goal is to help computers understand the ambiguous meaning of language in text in a deeper way, similar to how humans interpret language.

BERT's main uniqueness lies in its "bidirectional" nature. Unlike previous language models that only read text from one direction (e.g., left to right), BERT has the unique ability to process context from both directions simultaneously. This allows BERT to build a rich contextual understanding of the relationships between words in a sentence.

### IndoBERT-base-p1: Adaptation for Indonesian Language

In this project, we specifically utilize a pre-trained model called **IndoBERT-base-p1**. This is a version of BERT that has been specifically adapted and trained on a large corpus of Indonesian text.

The **IndoBERT-base-p1** model has **124.5 million** parameters, a number that indicates the complexity and capacity of the model to capture highly intricate language patterns and subtle nuances of meaning. The core architecture of the `BertForSequenceClassification` model used in this project, which is built on top of **IndoBERT**, broadly consists of:
- `bert` (model core): The main part responsible for understanding text, including embeddings and an `encoder` with an `attention` mechanism.
- `pooler`: Summarizes relevant information from the model core.
- `classifier`: The final linear layer that maps the summarized information to 3 sentiment labels (positive, neutral, negative).

The use of pre-trained models like IndoBERT is a very smart and efficient strategy, saving significant time and computational resources.

## Data Preparation: Foundation for Effective Learning

The quality and preparation of data are the main foundations for the success of any Deep Learning project.

### SMSA Dataset: Source of Indonesian Sentiment Data

The main dataset used is `smsa_doc_sentiment_prosa` from the IndoNLU collection. This dataset is divided into three main parts:
- `train_preprocess.tsv`: Training data.
- `valid_preprocess.tsv`: Validation data.
- `test_preprocess_masked_label.tsv`: Test data.

### Utilizing PyTorch Dataset and DataLoader

To prepare raw data for efficient use by Deep Learning models, PyTorch provides two key abstractions: Dataset and DataLoader.

- `Dataset`: Functions as a "storage" for data samples, loading and processing each sample individually (including tokenization and conversion to numerical IDs).

- `DataLoader`: Wraps the `Dataset` and allows easy access to data samples in "mini-batches". It handles batching, shuffling (randomizing data order), and multiprocessing to speed up data loading. In this project, `batch_size` is set to 32, `num_workers` to 16, and `max_seq_len` is 512 tokens.

## Model Training and Fine-Tuning Process: Improving Sentiment Understanding Accuracy

Once the data is prepared, the model is trained for the sentiment analysis task.

### Model Initialization and Configuration

A random seed is set to `19072021` for reproducibility. The `BertForSequenceClassification` model is loaded with `num_labels=3`. The Adam optimizer is used with a small initial learning rate of `3e-6`. The model is moved to the GPU for computational acceleration.

### Fine-Tuning Strategy: Optimizing IndoBERT for Sentiment Analysis Tasks

The fine-tuning process is carried out for 5 epochs. Each epoch involves:

1. **Model Training and Parameter Update**: The model calculates the loss, computes gradients, and updates its weights.

2. **Training Metric Calculation**: Performance metrics (Accuracy, F1-score, Recall, Precision) are calculated on the training data.

3. **Evaluation on Validation Data**: The model is evaluated on validation data to monitor performance and detect overfitting.

### Performance Evaluation Metrics
- **Accuracy**: The proportion of correct classifications.

- **Precision**: The proportion of positive predictions that are actually positive.

- **Recall (True Positive Rate)**: The proportion of actual positives that are successfully identified.

- **F1-Score**: The harmonic mean of Precision and Recall, providing a good balance for datasets with imbalanced classes.

### Model Training and Validation Results

Here is a summary of the model's performance over 5 epochs of training and validation:

**Table 1: Summary of Training and Validation Metrics per Epoch**

| Epoch | Train Loss | Train Acc | Train F1 | Train Rec | Train Pre | Valid Loss | Valid Acc | Valid F1 | Valid Rec | Valid Pre |
|-------|------------|-----------|----------|-----------|-----------|------------|-----------|----------|-----------|-----------|
| 1     | 0.3488     | 0.87      | 0.82     | 0.79      | 0.86      | 0.1947     | 0.93      | 0.90     | 0.89      | 0.90      |
| 2     | 0.1581     | 0.95      | 0.93     | 0.93      | 0.93      | 0.1780     | 0.93      | 0.90     | 0.91      | 0.90      |
| 3     | 0.1184     | 0.96      | 0.95     | 0.95      | 0.95      | 0.1662     | 0.94      | 0.91     | 0.90      | 0.92      |
| 4     | 0.0881     | 0.97      | 0.97     | 0.96      | 0.97      | 0.1800     | 0.93      | 0.91     | 0.90      | 0.92      |
| 5     | 0.0656     | 0.98      | 0.98     | 0.97      | 0.98      | 0.2070     | 0.93      | 0.89     | 0.88      | 0.92      |

## Application and Results Analysis: Unpacking the Meaning Behind Words

This section demonstrates the model's ability to differentiate sentiment and handle ambiguous text.

### Sentiment Prediction Demonstration

Before fine-tuning, the model predicted a "positive" sentiment for the sentence: "Bahagia hatiku melihat pernikahan putri sulungku yang cantik jelita" (My heart is happy seeing the wedding of my beautiful eldest daughter) with only 39.380% confidence. After fine-tuning, the confidence dramatically increased to 99.592%. This clearly demonstrates the success of the fine-tuning process.

### Model's Contextual Intelligence: Handling Ambiguous Text

The model shows remarkable ability in handling ambiguous text:

1. Example 1: "Sayang, aku marah" (Darling, I'm angry)

    - Model Prediction: Negative (99.763%)
    - The model successfully captures the shift in sentiment from the positive word "sayang" (darling) to the negative word "marah" (angry).

2. Example 2: "Merasa kagum dengan toko ini tapi berubah menjadi kecewa setelah transaksi" (Felt amazed by this store but became disappointed after the transaction)

    - Model Prediction: Negative (99.697%)
    - The model accurately weighs the conjunction "tapi" (but) and identifies the dominant negative sentiment.

3. Example 3: "Aku padahal bangga banget sama kamu, tapi aku kecewa kenapa kamu memilih jalan yang salah pada akhirnya" (I was so proud of you, but I'm disappointed why you chose the wrong path in the end)

    - Model Prediction: Negative (99.759%)
    - The model correctly predicts a negative sentiment despite the word "bangga" (proud), demonstrating complex contextual understanding.

## Project Implementation Guide: Step-by-Step with Code

This section provides a practical guide to replicate and understand the workflow of this sentiment analysis project, complete with relevant Python code snippets.

### 1. Initial Setup

The first step is to set up the working environment and import the necessary libraries, as well as define helper functions.

```Python
# Clone IndoNLU Repository (run in terminal/notebook)
# git clone https://github.com/indobenchmark/indonlu

# Import Libraries
import random
import numpy as np
import pandas as pd
import torch
from torch import optim
import torch.nn.functional as F
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore') # Disable warnings
from transformers import BertForSequenceClassification, BertConfig, BertTokenizer
from indonlu.utils.forward_fn import forward_sequence_classification
from indonlu.utils.metrics import document_sentiment_metrics_fn
from indonlu.utils.data_utils import DocumentSentimentDataset, DocumentSentimentDataLoader

# Helper Functions
def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)

def count_param(module, trainable=False):
    if trainable:
        return sum(p.numel() for p in module.parameters() if p.requires_grad)
    else:
        return sum(p.numel() for p in module.parameters())

def get_lr(optimizer):
    for param_group in optimizer.param_groups:
        return param_group['lr']

def metrics_to_string(metric_dict):
    string_list = []
    for key, value in metric_dict.items():
        string_list.append(f"{key}:{value:.2f}")
    return " ".join(string_list)

# Set random seed
set_seed(19072021)
```

### 2. Loading Pre-trained Model and Configuration

The IndoBERT-base-p1 model is loaded along with its tokenizer and configuration.

```Python
# Load tokenizer and config
tokenizer = BertTokenizer.from_pretrained('indobenchmark/indobert-base-p1')
config = BertConfig.from_pretrained('indobenchmark/indobert-base-p1')
# Assume DocumentSentimentDataset.NUM_LABELS is already defined (e.g., 3)
config.num_labels = 3 # Or DocumentSentimentDataset.NUM_LABELS

# Instantiate model
model = BertForSequenceClassification.from_pretrained('indobenchmark/indobert-base-p1', config=config)
if torch.cuda.is_available():
    model.cuda() # Move model to GPU if available

```

### Dataset Preparation

The `smsa_doc_sentiment_prosa` dataset is prepared using PyTorch's `Dataset` and `DataLoader` classes. Ensure the file paths match your location.

```Python
# Adjust these paths to your dataset location after cloning the IndoNLU repository
train_dataset_path = './indonlu/dataset/smsa_doc-sentiment-prosa/train_preprocess.tsv'
valid_dataset_path = './indonlu/dataset/smsa_doc-sentiment-prosa/valid_preprocess.tsv'
test_dataset_path = './indonlu/dataset/smsa_doc-sentiment-prosa/test_preprocess_masked_label.tsv'

# Instantiate DocumentSentimentDataset objects
train_dataset = DocumentSentimentDataset(train_dataset_path, tokenizer, lowercase=True)
valid_dataset = DocumentSentimentDataset(valid_dataset_path, tokenizer, lowercase=True)
test_dataset = DocumentSentimentDataset(test_dataset_path, tokenizer, lowercase=True)

# Instantiate DocumentSentimentDataLoader objects
train_loader = DocumentSentimentDataLoader(dataset=train_dataset, max_seq_len=512,
                                           batch_size=32, num_workers=16, shuffle=True)
valid_loader = DocumentSentimentDataLoader(dataset=valid_dataset, max_seq_len=512,
                                           batch_size=32, num_workers=16, shuffle=False) # Usually shuffle is False for validation
test_loader = DocumentSentimentDataLoader(dataset=test_dataset, max_seq_len=512,
                                          batch_size=32, num_workers=16, shuffle=False)

# Define label mappings
w2i, i2w = DocumentSentimentDataset.LABEL2INDEX, DocumentSentimentDataset.INDEX2LABEL

print("Label Mapping (Word to Index):", w2i)
print("Label Mapping (Index to Word):", i2w)

```

### Fine-Tuning and Evaluation Process

The model is trained for several epochs using the training data and evaluated on the validation data.

```Python
optimizer = optim.Adam(model.parameters(), lr=3e-6)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(device) # Ensure model is on the correct device

n_epochs = 5

for epoch in range(n_epochs):
    # Training Phase
    model.train()
    torch.set_grad_enabled(True)
    total_train_loss = 0
    list_hyp, list_label = [], []

    train_pbar = tqdm(train_loader, leave=True, total=len(train_loader))
    for i, batch_data in enumerate(train_pbar):
        # forward_sequence_classification is a function from indonlu.utils.forward_fn
        # that returns loss, predictions, and true labels
        loss, batch_hyp, batch_label = forward_sequence_classification(model, batch_data[:-1], i2w=i2w, device=device)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        tr_loss = loss.item()
        total_train_loss = total_train_loss + tr_loss

        list_hyp.extend(batch_hyp)
        list_label.extend(batch_label)

        train_pbar.set_description(f"(Epoch {epoch+1}) TRAIN LOSS: {total_train_loss/(i+1):.4f} LR: {get_lr(optimizer):.8f}")

    metrics = document_sentiment_metrics_fn(list_hyp, list_label) # Function from indonlu.utils.metrics
    print(f"(Epoch {epoch+1}) TRAIN LOSS: {total_train_loss/(i+1):.4f} {metrics_to_string(metrics)} LR:{get_lr(optimizer):.8f}")

    # Validation Phase
    model.eval()
    torch.set_grad_enabled(False)
    total_loss_val = 0.0 # Using a different variable name for validation loss
    list_hyp_val, list_label_val = [], []

    pbar_val = tqdm(valid_loader, leave=True, total=len(valid_loader))
    for i, batch_data in enumerate(pbar_val):
        loss_val, batch_hyp_val, batch_label_val = forward_sequence_classification(model, batch_data[:-1], i2w=i2w, device=device)

        valid_loss = loss_val.item()
        total_loss_val = total_loss_val + valid_loss

        list_hyp_val.extend(batch_hyp_val)
        list_label_val.extend(batch_label_val)

        metrics_val = document_sentiment_metrics_fn(list_hyp_val, list_label_val)
        pbar_val.set_description(f"VALID LOSS: {total_loss_val/(i+1):.4f} {metrics_to_string(metrics_val)}")

    metrics_val = document_sentiment_metrics_fn(list_hyp_val, list_label_val)
    print(f"(Epoch {epoch+1}) VALID LOSS:{total_loss_val/(i+1):.4f} {metrics_to_string(metrics_val)}")

```

### Making New Predictions

Once the model is trained, you can use it to predict the sentiment of new text.

```Python
def prediction(text, model, tokenizer, i2w, device):
    model.eval() # Ensure model is in evaluation mode
    subwords = tokenizer.encode(text, truncation=True, max_length=512) # Add truncation and max_length
    subwords_torch = torch.LongTensor(subwords).view(1, -1).to(device)
    
    with torch.no_grad(): # Disable gradient calculation for inference
       logits = model(subwords_torch)[0] # Access logits from model output
    
    label_id = torch.topk(logits, k=1, dim=-1)[1].squeeze().item()
    confidence = F.softmax(logits, dim=-1).squeeze()[label_id].item() * 100
    
    print(f'Text: {text} | Label: {i2w[label_id]} ({confidence:.3f}%)')

# Example usage (after model, tokenizer, i2w, and device are defined from previous steps)
# Ensure you have the model, tokenizer, i2w, and device objects ready from the training process above.
# Example:
# prediction(text1, model, tokenizer, i2w, device)

text1 = 'Bahagia hatiku melihat pernikahan putri sulungku yang cantik jelita'
# Expected Output: Text: Bahagia hatiku melihat pernikahan putri sulungku yang cantik jelita | Label: positive (99.592%)

text2 = "Ronaldo pergi ke Mall Grand Indonesia membeli cilok"
# Expected Output: Text: Ronaldo pergi ke Mall Grand Indonesia membeli cilok | Label: neutral (98.332%)

text3 = "Sayang, aku marah"
# Expected Output: Text: Sayang, aku marah | Label: negative (99.763%)

text4 = "Merasa kagum dengan toko ini tapi berubah menjadi kecewa setelah transaksi"
# Expected Output: Text: Merasa kagum dengan toko ini tapi berubah menjadi kecewa setelah transaksi | Label: negative (99.697%)

text5 = "Aku padahal bangga banget sama kamu, tapi aku kecewa kenapa kamu memilih jalan yang salah pada akhirnya"
# Expected Output: Text: Aku padahal bangga banget sama kamu, tapi aku kecewa kenapa kamu memilih jalan yang salah pada akhirnya | Label: negative (99.759%)

```

## Conclusion and Future Development

### Summary of Project Achievements

This project successfully developed a Deep Learning-based sentiment analysis model using the IndoBERT-base-p1 architecture. This model effectively classifies Indonesian text sentiment into positive, neutral, and negative categories with high accuracy. Through careful fine-tuning on the smsa_doc_sentiment_prosa dataset, the model showed significant improvement in contextual understanding. This is evident from its ability to handle ambiguous or mixed-connotation sentences with high precision, as demonstrated in the text examples "Sayang, aku marah" and "Merasa kagum... kecewa". The model achieved strong performance metrics on validation data (e.g., Accuracy around 93% and F1-Score around 90-91%), proving its effectiveness and generalization capability.

### Future Development and Further Enhancements

Although the developed model has shown excellent performance, there are several avenues for further development and enhancement that can be explored to expand its capabilities and increase its application value:

- **Dataset Enhancement**: Exploring the use of larger and more diverse datasets will improve the model's generalization capabilities across various domains and language styles. Richer datasets will help the model learn more complex sentiment patterns and broader linguistic nuances.

- **Aspect-Based Sentiment Analysis (ABSA)**: Currently, the model identifies the overall sentiment of a text. Future development could involve enabling the model to not only identify overall sentiment but also sentiment towards specific aspects mentioned in the text. For example, in a phone review, the model could differentiate positive sentiment towards the "camera" but negative sentiment towards "battery life." This capability would provide much more granular and specific insights.

- **Intent Sentiment Analysis**: In addition to sentiment polarity, analyzing the intent behind user messages is also highly valuable. The model could be developed to identify whether the text is a complaint, a suggestion, a question, or an expression of appreciation. This would provide a deeper understanding of user needs and desires.

- **More Specific Emotion Detection**: Developing the model to differentiate more granular emotions such as happiness, sadness, anger, surprise, etc., could provide a richer understanding of users' emotional responses. This is a step forward from simple polarity sentiment classification towards a deeper understanding of emotions.

- **Real-time Implementation**: Integrating the trained model into applications that require real-time sentiment analysis, such as customer service chatbots or real-time social media monitoring systems. This would allow organizations to respond to user sentiment more quickly and effectively.

By exploring these development directions, this sentiment analysis project can continue to innovate, moving from general sentiment understanding to more granular and applicable insights, demonstrating foresight and continuous learning in the field of NLP.