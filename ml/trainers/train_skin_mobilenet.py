"""Train Skin Disease Classifier — MobileNetV2 transfer learning, 128x128 RGB."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
import numpy as np
import pandas as pd
from pathlib import Path
from utils import save_metrics, update_registry, ARTIFACTS_DIR

DATASETS = Path(__file__).parent.parent / "datasets" / "skin_ham10000"

def train():
    print("\n[TRAIN] Skin Disease Classifier (MobileNetV2)")
    if not DATASETS.exists():
        print(f"  [SKIP] Dataset not found: {DATASETS}")
        return

    # Check for metadata and images
    meta_files = list(DATASETS.glob("*metadata*.csv"))
    img_files = list(DATASETS.glob("*.jpg"))
    if len(img_files) < 50:
        print(f"  [SKIP] Only {len(img_files)} images found (need 50+)")
        return

    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
    import tensorflow as tf
    from tensorflow.keras import layers, models, callbacks
    from tensorflow.keras.applications import MobileNetV2
    import cv2

    IMG_SIZE = 128
    BATCH = 32

    # Load metadata
    if meta_files:
        meta = pd.read_csv(meta_files[0])
        meta.columns = [c.strip().lower() for c in meta.columns]
        # Find image_id and dx columns
        id_col = [c for c in meta.columns if "image" in c and "id" in c]
        dx_col = [c for c in meta.columns if c in ["dx", "diagnosis", "label"]]
        
        if not id_col or not dx_col:
            print("  [WARN] Cannot parse metadata columns, using directory structure")
            return
        
        id_col, dx_col = id_col[0], dx_col[0]
        classes = sorted(meta[dx_col].unique())
        class_to_idx = {c: i for i, c in enumerate(classes)}
        
        # Load images
        X, y = [], []
        for _, row in meta.iterrows():
            img_name = str(row[id_col])
            label = row[dx_col]
            
            img_path = DATASETS / f"{img_name}.jpg"
            if not img_path.exists():
                continue
            
            img = cv2.imread(str(img_path))
            if img is None:
                continue
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            img = img.astype("float32") / 255.0
            X.append(img)
            y.append(class_to_idx[label])
            
            if len(X) >= 2000:  # Limit to 2000 images
                break
        
        X = np.array(X)
        y = np.array(y)
    else:
        print("  [SKIP] No metadata CSV found")
        return

    print(f"  Loaded {len(X)} images, {len(classes)} classes: {classes}")

    from sklearn.model_selection import train_test_split
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    num_classes = len(classes)
    
    # MobileNetV2 transfer learning
    base = MobileNetV2(weights="imagenet", include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))
    base.trainable = False  # Freeze base

    model = models.Sequential([
        base,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.3),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation="softmax"),
    ])
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

    early_stop = callbacks.EarlyStopping(patience=3, restore_best_weights=True)
    model.fit(X_train, y_train, validation_data=(X_val, y_val),
              epochs=10, batch_size=BATCH, callbacks=[early_stop], verbose=1)

    y_pred = model.predict(X_val, verbose=0).argmax(axis=1)

    # Convert back to class names for metrics
    idx_to_class = {v: k for k, v in class_to_idx.items()}
    y_val_names = [idx_to_class[i] for i in y_val]
    y_pred_names = [idx_to_class[i] for i in y_pred]

    save_metrics("skin", y_val_names, y_pred_names, classes, str(DATASETS))

    model_path = ARTIFACTS_DIR / "skin_v1.h5"
    model.save(str(model_path))
    
    with open(ARTIFACTS_DIR / "skin_class_indices.json", "w") as f:
        json.dump(class_to_idx, f)
    
    update_registry("skin", "skin_v1.h5", 1)
    print(f"  [OK] Saved to {model_path}")

if __name__ == "__main__":
    train()
