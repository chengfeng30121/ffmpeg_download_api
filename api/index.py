## vars

debug = 0

## Libs

import requests
import json
import os

def _get_info() -> dict:
    if os.path.exists("info.json") and debug:
        return json.loads(open("info.json").read())
    url = "https://api.github.com/BtbN/FFmpeg-Builds/releases/latest"
    response = requests.get(url)
    json_data = response.json()
    print(json_data)
    return json_data

def progress_version(filenames: [(str, str), ...]) -> list:
    data = []
    for filename, url in filenames:
        d = {}
        if filename.endswith(".zip"):
            filename = filename[:-4]
        elif filename.endswith(".tar.xz"):
            filename = filename[:-7]
        else:
            d = None
            data.append(d)
            continue
        for part in filename.split("-"):
            if part == "ffmpeg":
                continue
            if part.lower() in ["linuxarm64", "linux64", "win64"]:
                d["sys"] = "linux" if part.lower()[:5] == "linux" else "win"
                d["arch"] = "x86_64" if part[-3:] != "m64" else "aarch64"
                continue
            if part == "N":
                d["version"] = "N"
                continue
            if part.startswith("n"):
                d["version"] = part[1:]
                continue
            if part.isdigit():
                continue
            if part.lower().startswith("g") and len(part) == 11:
                d["commit_id"] = part.lower()[1:]
                continue
            if part.lower() in ["gpl", "lgpl"]:
                if "license" in d:
                    d["license"] = f'{part.lower()}-{d["license"]}'
                else:
                    d["license"] = part.lower()
                continue
            if part.lower() =="shared":
                if "license" in d:
                    d["license"] = f'{d["license"]}-{part.lower()}'
                else:
                    d["license"] = part.lower()
                continue
        d["download_url"] = "https://github.moeyy.xyz/" + url
        data.append(d)
    return data

## Main_Script

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    return "使用说明(目前暂不支持浏览器, 请使用爬虫查看)\n\n本api仅收录最新版本的ffmpeg, 如要老版本请自行下载(也许以后会...?)\n本项目完全公益, 未收任何人的一针一线, 开发费用全由我个人承担, 请不要盗刷流量, 谢谢\nGithub: https://github.com/chengfeng30121/ffmpeg_download_api\n\n====================\nURL: /list_version/\nMethods: (GET)\nUsage: 返回一个ffmpeg列表\n====================\n"

@app.route("/list_version")
def list_version():
    json_data = _get_info()
    return json_data
    raw_datas = []
    for raw_data in json_data["assets"]:
        raw_datas.append((raw_data["name"], raw_data["browser_download_url"]))
    datas = progress_version(raw_datas)
    datas = {"Code": 200, "Release Name": json_data["name"], "data": datas}
    return datas

if debug:
    app.run(host="0.0.0.0", port=5001, debug=debug)
