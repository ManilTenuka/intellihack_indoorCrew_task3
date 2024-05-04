import tensorflow as tf
from utils.data_utils import load_loan_products, load_faq, load_application_process
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

# Load data
loan_products = load_loan_products('data/loan_products.json')
faq = load_faq('data/faq.json')
application_process = load_application_process('data/application_process.json')

# Preprocess data
# Combine data from all sources into a single list of texts
texts = []
for product in loan_products:
    texts.append(product['name'])
    texts.extend(product['features'])
    texts.extend([str(product['eligibility'][key]) for key in product['eligibility']])

for faq_item in faq:
    texts.append(faq_item['question'])
    texts.append(faq_item['answer'])

texts.extend(application_process['required_documents'])
texts.extend(application_process['steps'])
texts.append(application_process['timeline'])

# Tokenize and pad sequences
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
MAX_SEQUENCE_LENGTH = max(len(seq) for seq in sequences)
X = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH, padding='post')

# Prepare labels (assuming a binary classification task)
y = [0] * len(loan_products) + [1] * (len(faq) + len(application_process))

# Split data into train and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Define model architecture
model = tf.keras.Sequential([
  
])

# Compile and train the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_val, y_val))

# Save the trained model
model.save('models/loan_support_model.h5')
