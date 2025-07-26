# Optical Character Recognition(OCR) Using Tesseract

## Project Structure
- train_images: contains the original images from IAM Handwriting Database

- metadata: contains the metadata files of the images

- preprocess.py: extracts info from metadata files and preprocess the images

- generate_train_txt.py: generates .gt.txt files which are used to train the model

- main.py: the main Python script to run the OCR system

- test.png: a sample image that can be used to test the OCR system

- traineddata\ft.traineddata: the best model that we obtained via training.


## Process to train the model
### 1. Preprocess the images and metadata
```bash
python preprocess.py

python generate_train_txt.py
```

After this step, you should see three new folders:
- train_gt: temporary txt files (we don't need them)

- split_lines: .gt.txt files that we need to train the model

- processed_images: images after preprocessing, will be used to train the model


### 2. Clone and set up Tesstrain
Navigate to a desired directory and clone the repository:
```bash
git clone https://github.com/tesseract-ocr/tesstrain.git
```

Prepare language data:
```bash
cd tesstrain

make tesseract-langdata
```

Provide ground truth data:
```bash
cd data

mkdir ft-ground-truth
```

Copy the images from `processed_images/` to `tesstrain/data/ft-ground-truth`

Copy the .gt.txt from `split_lines/` to `tesstrain/data/ft-ground-truth`

### 3. Train the model
Under `tesstrain/`, run the following command to train a model from scratch with 20000 max iterations:
```bash
make training MODEL_NAME=ft PSM=7 MAX_ITERATIONS=20000
```

After training, you should obtain `ft.traineddata` under `tesstrain/data`

## Run the OCR System
### Setup Tesseract
Download Tesseract-OCR and add to the PATH, make sure you can run Tesseract via command line, use the following command to test:
```bash
tesseract --version
```

Next, navigate to the location of Tesseract, such as `D:\Tesseract-OCR\`, copy the `ft.traineddata` to the `tessdata` folder

### Run the OCR
```bash
python main.py D:\OCR-DL\test.png
```

You should obtain `output.png` and `output.txt` which show the OCR result.