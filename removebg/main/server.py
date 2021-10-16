from PIL import Image,UnidentifiedImageError
import json
from flask import Flask, request
from ..removebg import RemoveBg, RequestError, CaptchaError
from io import BytesIO
app = Flask(__name__)
captcha: int = 1
download:int = 1
@app.route('/')
def running():
    try:
        print(captcha)
        img=request.files.get('image')
        if not img:
            return json.dumps({'status':False,'msg':'image not found'})
        img_=BytesIO(img.stream.read())
        Image.open(img_)
        result=RemoveBg().upload(img_, img.filename, captcha, download)
        result.download()
        return json.dumps({'status':True, 'url':result.url})
    except UnidentifiedImageError:
        return json.dumps({'status':False,'msg':'Invalid Image'})
    except RequestError:
        return json.dumps({'status':False, 'msg':'max request'})
    except CaptchaError:
        return json.dumps({'status':False, 'msg':'captcha error'})
