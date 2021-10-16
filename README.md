
# Install Library
### pypi
```
$ pip3 install xremovebg
```
### github
```bash
$ pip install git+https://github.com/krypton-byte/removebg
```
# Library
```python
from removebg import RemoveBg
rb=RemoveBg()
res=rb.upload('images.png')
res.save('saved.png')
```

# Run server
```bash
$ python -m removebg -p 8000
```

# Command Line
## without session
```bash
$ python -m removebg --file=3.jpg --json 2>/dev/null
{
    "url": "https://o.remove.bg/downloads/47b11d7f-3157-4dea-88ba-a47632c348a2/3-removebg-preview.png",
    "filename": "3-removebg-preview.png",
    "width": 500,
    "height": 500,
    "foreground_type": "product",
    "rated": false
}

```
## save session

```bash
$ python -m removebg --file=3.jpg --save-session=session --json 2>/dev/null
{
    "url": "https://o.remove.bg/downloads/47b11d7f-3157-4dea-88ba-a47632c348a2/3-removebg-preview.png",
    "filename": "3-removebg-preview.png",
    "width": 500,
    "height": 500,
    "foreground_type": "product",
    "rated": false
}

```

## load session
```bash
$ python -m removebg --file=3.jpg --load-session=session --json 2>/dev/null
{
    "url": "https://o.remove.bg/downloads/47b11d7f-3157-4dea-88ba-a47632c348a2/3-removebg-preview.png",
    "filename": "3-removebg-preview.png",
    "width": 500,
    "height": 500,
    "foreground_type": "product",
    "rated": false
}

```
## get histories removebg
```bash
$ python -m removebg --get-histories --json 2>/dev/null
[{
    "url": "https://o.remove.bg/downloads/47b11d7f-3157-4dea-88ba-a47632c348a2/3-removebg-preview.png",
    "filename": "3-removebg-preview.png",
    "width": 500,
    "height": 500,
    "foreground_type": "product",
    "rated": false
}]

```