import os
import sys
import time
import requests
import eyed3
from ytmusicapi import YTMusic

if __name__ == "__main__":

    local_folder = r"E:\Music"
    local_list = []

    try:
        eyed3.log.setLevel("ERROR")
        for dirpath, dirnames, filenames in os.walk(local_folder):
            for filename in filenames:
                if "mp3" in filename:
                    audiofile = eyed3.load(dirpath + os.sep + filename)
                    if audiofile.tag.album != "":
                        local_list.append((audiofile.tag.album, audiofile.tag.album_artist, dirpath))
                        local_list = list(set(local_list))
                        break
    except Exception as E:
        print(E)

    album_list, album_artist_list, path_list= [e[0] for e in local_list], [e[1] for e in local_list], [e[2] for e in local_list]

    f = open('headers_auth_raw.txt', 'r+')
    f_raw = f.read()
    f.close()

    YTMusic.setup(filepath='headers_auth.json', headers_raw=f_raw)
    ytmusic = YTMusic('headers_auth.json')

    yt_albums = ytmusic.get_library_upload_albums(limit=999, order='a_to_z')
    ytmusic_list = []

    for item in yt_albums:
        ytmusic_list.append(item["title"])

    diff = list(set(album_list).difference(set(ytmusic_list)))

    upload_path_list = []
    for album, artist, path in local_list:
        for item in diff:
            if item == album:
                print(artist, "-", album)
