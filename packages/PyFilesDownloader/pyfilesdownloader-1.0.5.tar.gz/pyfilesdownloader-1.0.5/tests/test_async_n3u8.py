# coding: utf-8
from PyFilesDownloader.async_loader.async_m3u8 import AsyncM3U8Downloader

url = 'https://v.cdnlz22.com/20250101/10507_73949974/index.m3u8'
save_path = './download/上班族转生异世界当上了四天王不是很正常吗'
file_name = '第一集.mp4'
loader = AsyncM3U8Downloader(url, save_path, file_name)
loader.run()
