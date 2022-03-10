#!/usr/local/bin python
import numpy as np
import os
import sys
import time
import csv
import glob
from PIL import Image,ImageDraw,ImageFont

ttfontname = "hiragino.ttc"
backgroundRGB = (45, 51, 69)
textRGB       = (231, 228, 115)

tmp_dir = "tmp"
out_dir = "out"

canvasW = 1920
canvasH = 1080
top = 200
left = 100
right = 100
bottom = 100
margin = 20
textHeight = 30
lineOffset = 5

def makeSpecialThanks(pngList):
    print("png num",len(pngList))
    canvas = Image.new('RGB', (canvasW, canvasH), backgroundRGB)
    posX = left
    posY = top
    pageNum = 0
    imgBuffer = []
    for i in pngList:
        print(i)
        img = Image.open(i)
        imgW,imgH = img.size
        resizeH = textHeight
        resizeW = int(textHeight * imgW / imgH)
        img = img.resize((resizeW,resizeH))
        if (posX + resizeW) > (canvasW - right):

            #make mod margin            
            totalW = 0
            for img_ in imgBuffer:
                totalW += img_[2]
            hosei = 1.0 * (canvasW - left - right - totalW - margin * (len(imgBuffer) - 1)) / (len(imgBuffer) - 1)
            #paste
            for idx,img_ in enumerate(imgBuffer):
                canvas.paste(img_[0],(img_[1]+int(hosei*idx),posY))
            imgBuffer = []                
            posX = left
            posY += (textHeight + lineOffset)
            if (posY + textHeight) > (canvasH - bottom):
                canvas.save(os.path.join(out_dir,str(pageNum)+".png"))
                pageNum += 1
                canvas = Image.new('RGB', (canvasW, canvasH), backgroundRGB)
                posX = left
                posY = top
        imgBuffer.append([img,posX,resizeW])
        posX += (resizeW + margin)
    for idx,img_ in enumerate(imgBuffer):
        canvas.paste(img_[0],(img_[1],posY))
    return

def getPngList():
    return glob.glob(os.path.join(tmp_dir,"*.png"))

def main(argv):
    pList = getPngList()
    makeSpecialThanks(pList)
    #makeImg("暗黙の型宣言",36)

def makePokeImg():
    poke = getPokeList()
    print(len(poke))
    for text in poke:
        print(text)
        img = makeImg(text,36)
        img.save(os.path.join(tmp_dir,text+".png"))

def makeImg(text,fontsize):
    img  = Image.new('RGB', (1,1), backgroundRGB)
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(ttfontname, fontsize)
    textWidth, textHeight = draw.textsize(text,font=font)

    img  = Image.new('RGB', (textWidth, textHeight), backgroundRGB)
    draw = ImageDraw.Draw(img)
    draw.text((0,0), text, fill=textRGB, font=font)
    return img

def getPokeList():
    f = open('poke.csv',encoding='shift_jis')
    reader = csv.reader(f)
    l = []
    for row in reader:
        if "" != row[1]:
            l.append(row[1])
    return l

def test():
    # 使うフォント，サイズ，描くテキストの設定
    fontsize = 36
    text = "暗黙の型宣言"
    # 画像サイズ，背景色，フォントの色を設定
    canvasSize    = (300, 150)
    
    # 文字を描く画像の作成
    img  = Image.new('RGB', canvasSize, backgroundRGB)
    draw = ImageDraw.Draw(img)

    # 用意した画像に文字列を描く
    font = ImageFont.truetype(ttfontname, fontsize)
    textWidth, textHeight = draw.textsize(text,font=font)
    textTopLeft = (canvasSize[0]//6, canvasSize[1]//2-textHeight//2) # 前から1/6，上下中央に配置
    draw.text(textTopLeft, text, fill=textRGB, font=font)

    img.save("image.png")
    return

if __name__ == "__main__":
    print(sys.argv)
    main(sys.argv)