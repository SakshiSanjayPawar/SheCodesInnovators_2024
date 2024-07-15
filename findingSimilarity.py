import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from sklearn.metrics.pairwise import cosine_similarity
import glob
import os
import shutil
import tensorflow as tf

# Ensure TensorFlow does not allocate the entire GPU memory at once
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if physical_devices:
    try:
        for device in physical_devices:
            tf.config.experimental.set_memory_growth(device, True)
    except:
        pass

# Load VGG16 model + higher level layers
base_model = VGG16(weights='imagenet', include_top=False, pooling='avg')
model = Model(inputs=base_model.input, outputs=base_model.output)

def load_and_preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    return img_data

def extract_features(img_path):
    img_data = load_and_preprocess_image(img_path)
    features = model.predict(img_data)
    return features.flatten()

# Load dataset images and extract features
dataset_features = []
dataset_images = glob.glob(r'C:\Users\garge\OneDrive\Desktop\Myntra New\image_dataset1\*.jpg')  # Adjust the path and file extension as needed

for img_path in dataset_images:
    features = extract_features(img_path)
    dataset_features.append(features)

dataset_features = np.array(dataset_features)

# Function to find the most similar image in the dataset
def find_most_similar_image(new_img_path, dataset_features, dataset_images):
    new_features = extract_features(new_img_path)
    similarities = cosine_similarity([new_features], dataset_features)
    most_similar_idx = np.argmax(similarities)
    return dataset_images[most_similar_idx], similarities[0][most_similar_idx]

# Test with a new image
new_image_path = r'C:\Users\garge\OneDrive\Desktop\Myntra New\ai-image-generator\public\images\generated_image.png'  # Replace with the path to the new image
most_similar_image, similarity_score = find_most_similar_image(new_image_path, dataset_features, dataset_images)

print(f"Most similar image in the dataset: {most_similar_image}")
print(f"Similarity score: {similarity_score}")

# Check similarity score and move to output_images folder if < 0.70
output_folder = r'C:\Users\garge\OneDrive\Desktop\Myntra New\output_folder'
if similarity_score < 0.70:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    shutil.move(new_image_path, os.path.join(output_folder, os.path.basename(new_image_path)))
    print(f"Image moved to {output_folder} due to low similarity score.")
else:
    print("Image similarity is above the threshold, no action taken.")

# Clear session to free memory
tf.keras.backend.clear_session()
