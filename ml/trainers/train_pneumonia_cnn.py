"""Train Pneumonia CNN — Custom small CNN in Keras, 150x150 grayscale."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
import numpy as np
from pathlib import Path
from utils import save_metrics, update_registry, ARTIFACTS_DIR

DATASETS = Path(__file__).parent.parent / "datasets" / "pneumonia"

def train():
    print("\n[TRAIN] Pneumonia CNN Detector")
    train_dir = DATASETS / "train"
    if not train_dir.exists():
        print(f"  [SKIP] Dataset not found: {train_dir}")
        return

    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
    import tensorflow as tf
    from tensorflow.keras import layers, models, callbacks

    IMG_SIZE = (150, 150)
    BATCH = 32

    # Load data using image_dataset_from_directory
    train_ds = tf.keras.utils.image_dataset_from_directory(
        str(train_dir), image_size=IMG_SIZE, color_mode="grayscale",
        batch_size=BATCH, label_mode="binary", seed=42, validation_split=0.2, subset="training"
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        str(train_dir), image_size=IMG_SIZE, color_mode="grayscale",
        batch_size=BATCH, label_mode="binary", seed=42, validation_split=0.2, subset="validation"
    )

    # Normalize
    norm = layers.Rescaling(1.0 / 255)
    train_ds = train_ds.map(lambda x, y: (norm(x), y)).prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.map(lambda x, y: (norm(x), y)).prefetch(tf.data.AUTOTUNE)

    # 3-conv-block CNN
    model = models.Sequential([
        layers.Input(shape=(150, 150, 1)),
        layers.Conv2D(32, 3, activation="relu"), layers.MaxPooling2D(),
        layers.Conv2D(64, 3, activation="relu"), layers.MaxPooling2D(),
        layers.Conv2D(128, 3, activation="relu"), layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(128, activation="relu"),
        layers.Dense(1, activation="sigmoid"),
    ])
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    model.summary()

    early_stop = callbacks.EarlyStopping(patience=3, restore_best_weights=True)
    model.fit(train_ds, validation_data=val_ds, epochs=10, callbacks=[early_stop], verbose=1)

    # Evaluate
    y_true, y_pred_prob = [], []
    for x_batch, y_batch in val_ds:
        preds = model.predict(x_batch, verbose=0)
        y_true.extend(y_batch.numpy().flatten().astype(int))
        y_pred_prob.extend(preds.flatten())
    
    y_pred = (np.array(y_pred_prob) > 0.5).astype(int)
    y_true = np.array(y_true)

    save_metrics("pneumonia", y_true, y_pred, ["image_pixels"], str(DATASETS))

    model_path = ARTIFACTS_DIR / "pneumonia_v1.h5"
    model.save(str(model_path))
    
    indices = {"NORMAL": 0, "PNEUMONIA": 1}
    with open(ARTIFACTS_DIR / "pneumonia_class_indices.json", "w") as f:
        json.dump(indices, f)
    
    update_registry("pneumonia", "pneumonia_v1.h5", 1)
    print(f"  [OK] Saved to {model_path}")

if __name__ == "__main__":
    train()
