from __future__ import annotations
from sys import stderr
from io import BytesIO
import pickle
from time import time
from PIL import Image
from json import loads
from base64 import b64decode
import re
from typing import Generator, Union
from requests import Session
import requests

class CaptchaError(Exception):
    pass
    
class APIError(Exception):
    pass

class RequestError(Exception):
    pass

class UploadError(Exception):
    pass

class ResultModel:
    def __init__(self, url:str, filename:str, width:int, height:int, foreground_type:str, **kwargs) -> None:
        self.url      = url
        self.filename = filename
        self.width    = width
        self.height   = height
        self.foreground_type=foreground_type
        self.json = {'url':url,'filename':filename, 'width':width, 'height':height, 'foreground_type':foreground_type, **kwargs}
        pass
    def __str__(self) -> str:
        return self.filename
    def __repr__(self) -> str:
        return self.__str__()
    def download(self, filename=False)->Union[BytesIO, int]:
        '''
        param: filename: Image output path


        `show image example`
        ```
        from PIL import Image
        Image.open(<ResultModel Object>.download())
        ```
        
        `save image as file`
        ```
        <ResultModelObject>.download('saved.png')
        '''
        binary = requests.get(self.url).content
        return open(filename, 'wb').write(binary) if isinstance(filename, str) else BytesIO(binary)

class RemoveBg(Session):
    '''
    RemoveBg Scrapper With Request Library
    
    `Example`
    ```python
    from removebg import RemoveBg
    rb=RemoveBg()
    #From File
    im=rb.upload('image.png')
    #From Bytes object
    im=rb.upload(BytesIO(open('images.png','rb).read()), filename='images.png')
    #Download
    im.download('result.png')
    #download from Histories
    for i in rb.histories:
        i.download(i.filename)
    ```
    '''
    def __init__(self) -> None:
        super().__init__()
        self.headers.update({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'})
    def filename_object_png(self, image:Union[str, BytesIO], filename)->tuple:
        '''
        :param image :path image/bytes object of image
        :param filename: save image name
        '''
        filename=re.findall('(.+?)(\.[^.]*$|$)', (image if isinstance(image, str) else filename))[0][0]+'.png'
        res=BytesIO()
        Image.open(image).save(res, format='png')
        return (filename, res.getvalue())

    def get_token(self, token_retrying: int=1)->Union[None, str]:
        '''
        :param token_retrying: force get trust token
        '''
        not 'x-csrf-token' in self.headers.keys() and self.headers.update({'x-csrf-token':self.post('https://www.remove.bg/trust_tokens').json()['csrf_token']})
        n=self.post('https://www.remove.bg/trust_tokens').text
        x=re.search('useToken\(\'(.*?)\'',n)
        if x:
            return x.group(1)

    @property
    def histories(self)->Generator:
        for i in self.get('https://www.remove.bg/images').json()['data']:
            try:
                yield ResultModel(**loads(b64decode(i['pl']))['result'])
            except TypeError:
                raise TypeError('a')

    def __iter__(self)->Generator:
        yield from self.histories

    def download(self, resp: dict, max:int)->ResultModel:
        '''
        :param resp: json response
        :param max: retryng image url
        '''
        for i in range(max):
            try:
                resp=self.get(f'https://www.remove.bg{resp["url"]}?_={time.__str__()[:-3]}').json()
                base=loads(b64decode(resp['pl']))
                if 'result' in base.keys() and 'url' in base['result'].keys():
                    break
                stderr.write(f'Retrying Download [{i}]\n')
                stderr.flush()
            except requests.exceptions.SSLError:
                stderr.write('[SSL ERROR]\n')
                stderr.flush()
            except requests.exceptions.ConnectionError:
                stderr.write('[Connection Error]\n')
                stderr.flush()
        else:
            raise RequestError('max requests')
        try:
            return ResultModel(**base['result'])
        except KeyError:
            raise APIError(base['result']['error_message'])

    def upload(self, img:Union[str, BytesIO], filename='nobg.png',trust_token_retrying:int=1,download_retrying=12, retryng_upload=5)->ResultModel:
        '''
        :param img: image path/Bytes object of image
        :param filename: alias image name
        :param trust_token_retrying: force get trust token
        :param download_retrying: force get download object
        :param upload_retrying: force upload image

        `upload from file`
        ```
        <Removebg Object>.upload('image.png')
        ```
        `upload from bytes object`
        ```
        byte=BytesIO(open('image.png','rb').read())
        <RemoveBg Object>.upload(byte, filename='image.png')
        '''
        for i in range(retryng_upload):
            try:
                stderr.write(f'Retrying Upload [{i+1}]\n')
                stderr.flush()
                up = self.post('https://www.remove.bg/images', data={'trust_token':self.get_token(token_retrying=trust_token_retrying)}, files={'image[original]':self.filename_object_png(img, filename)}).json()
                if up:
                    return self.download(up,download_retrying)
            except requests.exceptions.SSLError:
                stderr.write('[SSL ERROR]\n')
                stderr.flush()
            except requests.exceptions.ConnectionError:
                stderr.write('[Connection Error]\n')
                stderr.flush()
        else:
            raise UploadError('Response Empty')
            
    def save_session(self, filename: Union[BytesIO,bool, str])->Union[int, BytesIO, bytes,None]:
        '''
        :param filename: session filename
        '''
        if isinstance(filename, str):
            open(filename, 'wb').write(pickle.dumps(self))
        elif isinstance(filename,BytesIO):
            return BytesIO(pickle.dumps(self))
        else:
            return pickle.dumps(self)

    def load_session(self, session: Union[BytesIO, bytes, str])->RemoveBg:
        '''
        :param session: session binary|object

        `Example`
        ```
        >>> from removebg import RemoveBg
        >>> rb=RemoveBg()
        >>> rb.upload('images.png')
        images-removebg-prefiew.png
        >>> list(rb)
        [images-removebg-prefiew.png]
        >>> new_rb=RemoveBg().load_session(rb.load_session())
        >>> list(new_rb)
        [images-removebg-prefiew.png]
        ```
        '''
        if isinstance(session, str):
            return pickle.loads(open(session, 'rb').read())
        elif isinstance(session,BytesIO):
            return pickle.loads(session.getvalue())
        else:
            return pickle.loads(session)