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
        for l in layers_informations:
            self.layers.append(self.Layer(l, self))
        #TODO amount estimate

    def __create_element_id(self) -> str:
        id = ""
        for layer in self.layers:
            id += str(random.randrange(0, layer.size, 1))
        return id
        #TODO fix double
    
    def generate_set(self, n: int):
        for x in range(n):
            id = self.__create_element_id()
            self.generate_image(id)

    def generate_image(self, id) -> None:
        result = Image.new(mode="RGBA", size=(32, 32))
        for layer_index, image_index in enumerate(id):
            image_index = int(image_index)
            image = self.layers[layer_index].images[image_index]
            result.paste(image, (0, 0), image)
        Path(self.output_path).mkdir(parents=True, exist_ok=True)
        result.save(self.output_path + id + ".png")


ImageSet("set-config.json").generate_set(1000)
