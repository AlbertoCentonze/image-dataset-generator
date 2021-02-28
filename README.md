# pixelart-dataset-generator
A simple python scripts that allows you to create procedurally a greate amount of images by overlaying layers 

## How to install
1. Clone the repository
2. From the repository folder open the terminal
```shell
  pip install -r requirements.txt
```

## How to use
To start working on the project you'll need to import the ImageSet library first.
```python
from generator import ImageSet 
```

Create then your own .json configuration file using set-config.json as a model and save it inside the project folder
### Generate a set
From the Python shell write
```python
ImageSet("yourjson.json").generate_set(set_size)
```
### Generate a specific element
From the Python shell write
```python
ImageSet("yourjson.json").generate_image(image_id)
```
 
