# Cognitron 

Easy-to-use model inference for the digital humanities.

The library's central goals are:

    * ease of use, esp. in a marimo notebook context
    * maintainability by reduction of dependencies

## Installation

```bash
pip install cognitron
```

## Usage

```py
# detect all faces in an image.
import cognitron as cg
im = cg.Image.open("path/to/image")
pipeline = cg.pipeline("face-detection")
faces = pipeline(im).top
print(faces)
```

## License

Cognitron is licensed under GPLv3. See the LICENSE file.
