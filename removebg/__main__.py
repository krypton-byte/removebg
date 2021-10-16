import os
import argparse
from . import RemoveBg
import json
arg = argparse.ArgumentParser()
arg.add_argument('--host',default='127.0.0.1')
arg.add_argument('--port',default='8000')
arg.add_argument('--force-captcha',type=int, default=5, help='looping for get captcha')
arg.add_argument('--force-download', default=5, help='looping for get download')
arg.add_argument('--force-upload', default=10, help='looping for upload image')
arg.add_argument('--server', action='store_true', help='run as server')
arg.add_argument('--json', action='store_true', help='json result')
arg.add_argument('--file', help='image path')
arg.add_argument('--save-session',help='save session file')
arg.add_argument('--load-session',help='load session file')
arg.add_argument('--get-histories', action='store_true', help='get histories result')
parse = arg.parse_args()

if parse.server:
    from .main import server
    server.download = parse.force_download
    server.captcha = parse.force_captcha
    server.app.run(host=parse.host, port=parse.port)
elif parse.file:
    rb = RemoveBg()
    if parse.save_session:
        up=rb.upload(parse.file, trust_token_retrying=parse.force_captcha, download_retrying=parse.force_download, retryng_upload=parse.force_download)
        print(json.dumps(up.json, indent=4) if parse.json else up.url)
        rb.save_session(parse.save_session)
    elif parse.load_session:
        up=rb.load_session(parse.load_session).upload(parse.file, trust_token_retrying=parse.force_captcha, download_retrying=parse.force_download,retryng_upload=parse.force_download)
        print(json.dumps(up.json, indent=4) if parse.json else up.url)
elif parse.get_histories and parse.load_session:
    rb = RemoveBg()
    rb=rb.load_session(parse.load_session)
    if parse.json:
        print(json.dumps(list(map(lambda x:x.json, rb)), indent=4))
    else:
        for i in rb:
            print(i.url)
else:
    os.system('python3 -m removebg --help')