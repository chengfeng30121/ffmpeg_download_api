def progress_version(filenames: [str, str, ...]) -> list:
    data = []
    for filename in filenames:
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
        data.append(d)
    return data

if __name__ == "__main__":
    filenames = [
        "ffmpeg-n6.1.2-9-g4571c80b40-linuxarm64-lgpl-6.1.tar.xz",
        "ffmpeg-n7.1-7-g63f5c007a7-win64-lgpl-shared-7.1.zip",
        "ffmpeg-N-117414-gb9145fcab2-linux64-gpl-shared.tar.xz"
    ]

    for d in progress_version(filenames):
        print(d)

