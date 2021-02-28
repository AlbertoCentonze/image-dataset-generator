import json
from PIL import Image
from pathlib import Path
import glob
import random


class ImageSet:
    class Layer:
        def __init__(self, name, set_ref) -> None:
            self.name = name
            self.set = set_ref
            self.path = Path(set_ref.resource_path + name)
            self.images = []
            if (self.path.exists() and self.path.is_dir()):
                pngs = glob.glob(set_ref.resource_path + name + "/*.png")
                for image_path in pngs:
                    with Image.open(image_path) as image:
                        if image.width == self.set.width and image.height == self.set.height:
                            image = image.convert("RGBA")
                            self.images.append(image)
                        else:
                            raise Exception("Size of file " +
                                            image_path + "is not correct")
                self.size = len(pngs)
            else:
                raise Exception("Directory " + name +
                                " specified in json does not exist")

    def __init__(self, json_file: str) -> None:
        config = json.load(open(json_file))
        self.height = config["size"]["height"]
        self.width = config["size"]["width"]
        self.output_path = "./output/" + config["name"] + "/"
        self.resource_path = config["resDirectory"]
        layers_informations = config["layers"]
        self.layers = []
        self.set_elements = []
        for l in layers_informations:
            self.layers.append(self.Layer(l, self))
        self.max_size = self.__compute_max_set_size()
        print(f"With the current set you can generate up to {self.max_size} elements")

    def __create_element_id(self) -> str:
        id = ""
        for layer in self.layers:
            id += str(random.randrange(0, layer.size, 1)) + "-"
        id = id[:-1]
        while id in self.set_elements:
            return self.__create_element_id()
        self.set_elements.append(id)
        return id

    def __check_output_size(self, correct_size, message):
        output_list = glob.glob(self.output_path + "*.png")
        if (len(output_list) != correct_size):
            raise Exception(message)

    def __compute_max_set_size(self):
        size = 1
        for layer in self.layers:
            size *= layer.size
        return size
    
    def generate_set(self, set_size: int):
        if set_size > self.max_size:
            raise Exception(f"Invalid set size, the maximum value with the current set is {self.max_size}")
        self.__check_output_size(0, "Don't forget to delete the output folder before generating a new set")
        self.set_elements = []
        for x in range(set_size):
            id = self.__create_element_id()
            self.generate_image(id)
        self.__check_output_size(set_size, "An error has occured, please contact the developer")

    def generate_image(self, id) -> None:
        result = Image.new(mode="RGBA", size=(32, 32))
        for layer_index, image_index in enumerate(id.split("-")):
            image_index = int(image_index)
            image = self.layers[layer_index].images[image_index]
            result.paste(image, (0, 0), image)
        Path(self.output_path).mkdir(parents=True, exist_ok=True)
        result.save(self.output_path + id + ".png")


ImageSet("set-config.json").generate_set(10)
