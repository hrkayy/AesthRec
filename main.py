import os
import glob
import matplotlib.pyplot as plt
from PIL import Image
from sentence_transformers import SentenceTransformer, util

# --- CONFIGURATION ---
# Use r'' for Windows paths to avoid escape character errors
CATALOG_PATH = r'C:\Users\raviv\Documents\HRK\Presidency University\Crackathon-GDG\AesthRec\catalogues'
TEST_IMAGE_PATH = r'C:\Users\raviv\Documents\HRK\Presidency University\Crackathon-GDG\AesthRec\test_inputs\t2.jpg'

# --- 1. INITIALIZE MODEL ---
print("Loading CLIP model... (This may take a minute on first run)")
model = SentenceTransformer('clip-ViT-B-32')

# --- 2. LOAD & PREPARE DATA ---
# Get all jpg, jpeg, and png files
image_paths = []
for ext in ['*.jpg', '*.jpeg', '*.png']:
    image_paths.extend(glob.glob(os.path.join(CATALOG_PATH, ext)))

if not image_paths:
    raise FileNotFoundError(f"No images found in {CATALOG_PATH}. Check your path!")

# Get clean names for display
image_names = [os.path.basename(p) for p in image_paths]
print(f"Successfully indexed {len(image_paths)} images.")

# --- 3. ENCODE CATALOG ---
print("Encoding catalog aesthetics... (Generating vectors)")
# We convert to RGB to ensure consistency
catalog_images = [Image.open(p).convert('RGB') for p in image_paths]
catalog_embeddings = model.encode(catalog_images, show_progress_bar=True)

# --- 4. RECOMMENDATION LOGIC ---
def get_recommendations(query_path, top_k=3):
    if not os.path.exists(query_path):
        print(f"Query image not found: {query_path}")
        return

    # Encode query image
    query_img = Image.open(query_path).convert('RGB')
    query_embedding = model.encode(query_img)

    # Compute cosine similarities
    # util.semantic_search returns a list of results (score and corpus_id)
    hits = util.semantic_search(query_embedding, catalog_embeddings, top_k=top_k)[0]

    # --- 5. VISUALIZATION ---
    fig, axes = plt.subplots(1, top_k + 1, figsize=(15, 5))
    fig.suptitle(f"Aesthetic Recommendations for: {os.path.basename(query_path)}", fontsize=16)

    # Display Query
    axes[0].imshow(query_img)
    axes[0].set_title("Input 'Vibe'")
    axes[0].axis('off')

    # Display Top K matches
    print("\nTop Matches Found:")
    for i, hit in enumerate(hits):
        idx = hit['corpus_id']
        score = hit['score']
        img_path = image_paths[idx]
        
        print(f"{i+1}. {image_names[idx]} (Score: {score:.4f})")
        
        axes[i+1].imshow(Image.open(img_path))
        axes[i+1].set_title(f"Match {i+1}\nScore: {score:.2f}")
        axes[i+1].axis('off')

    plt.tight_layout()
    plt.show()

# --- EXECUTION ---
if __name__ == "__main__":
    # Call the function
    get_recommendations(TEST_IMAGE_PATH, top_k=3)