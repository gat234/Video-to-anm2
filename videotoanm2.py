from PIL import Image
from ffprobe import FFProbe
import ffmpeg
import math
fileName = input("What is your file called?\n")
while True:
    try:
        metadata=FFProbe(fileName)
    except:
        fileName = input("Incorrect file, try again.\n")
    else:
        break
desiredFPS = input("Desired fps: ")
while True:
    try:
        desiredFPS = int(desiredFPS)
    except:
        desiredFPS = input("Not a number.\n")
    else:
        break
videoData = []

for stream in metadata.streams:
    if stream.is_video():
        videoData.append((desiredFPS/(stream.frames()/float(stream.duration))*stream.frames())+1)
        videoData.append(int(stream.width))
        videoData.append(int(stream.height))
        # print(videoData)
file = ffmpeg.input(fileName)
# got this from wikipedia didnt know there were so many lol
formats = [
    '.webm',
    '.mp4',
    '.flv',
    '.vob',
    '.ogv',
    '.ogg',
    '.drc',
    '.gif',
    '.gifv',
    '.mng',
    '.avi',
    '.MTS',
    '.M2TS',
    '.TS',
    '.mov',
    '.qt',
    '.wmv',
    '.yuv',
    '.rm',
    '.rmvb',
    '.viv',
    '.asf',
    '.amv',
    '.m4p',
    '.m4v',
    '.mpg',
    '.mp2',
    '.mpeg',
    '.mpe',
    '.mpv',
    '.m2v',
    '.m4v',
    '.svi',
    '.3gp',
    '.3g2',
    '.mxf',
    '.roq',
    '.nsv',
    '.f4v',
    '.f4p',
    '.f4a',
    '.f4b'
]
for i in formats:
    fileName = fileName.replace(i,'')
video = file.video.filter('fps', fps=desiredFPS, round='up')
audio = file.audio
out = ffmpeg.output(video, 'image-%07d.png',f="image2")
print("Video processing complete!")
out2 = ffmpeg.output(audio, f'{fileName}.ogg',f="ogg")
print("Audio successfully exported!")

valuesX = []
valuesY = []
number = videoData[0]
n = 1
while math.ceil(math.sqrt(number / n))*videoData[1] > 14000:
    n = n + 1
    # print(math.ceil(math.sqrt(number / n))*videoData[1])
valuesF = []
while (number > 0 and n > 0):
    a = math.ceil(number / n)
    number -= a
    n = n - 1
    valuesF.append(a)
for x in valuesF:
    valuesX.append(math.ceil(math.sqrt(x))*videoData[1])
    valuesY.append(math.ceil(math.sqrt(x))*videoData[2])

# print(valuesX,valuesY)
length = len(valuesX)
for i in range(length):
    img = Image.new('RGBA', (valuesX[i], valuesY[i]), (255, 0, 0, 0))
    img.save(f'canvas{i}_{fileName}.png', 'PNG')
    print(f'canvas{i}_{fileName}.png Created!')


ffmpeg.run(out)
ffmpeg.run(out2)



offset = 2
saveToErase = ['image-0000001.png']
for i in range(len(valuesX)):
    locationList = []
    multiplierX = 0
    multiplierY = 0
    canvas = Image.open(f'canvas{i}_{fileName}.png')
    for _ in range(valuesF[i]):
        if _+offset < 10:
            zero = "000000"
        if _+offset > 9 and _+offset < 100:
            zero = "00000"
        if _+offset > 99 and _+offset < 1000:
            zero = "0000"
        if _+offset > 999 and _+offset < 10000:
            zero = "000"
        if _+offset > 9999 and _+offset < 100000:
            zero = "00"
        if _+offset > 99999 and _+offset < 1000000:
            zero = "0"
        if _+offset > 999999 and _+offset < 10000000:
            zero = ""
        if _+offset > videoData[0]:
            break
        saveToErase.append(f"image-{zero}{_+offset}.png")
        locationList.insert(0,f"image-{zero}{_+offset}.png")

    locationList.reverse()
    offset = offset + valuesF[i]
    if i < 1:
        image = Image.open("image-0000001.png")
    canvas.paste(image, (0,0))
    # print(locationList)
    for x in range(len(locationList)):
        image = Image.open(locationList[x])
        multiplierX = multiplierX + videoData[1]
        print("Saved: ",locationList[x],f' IN: canvas{i}_{fileName}.png')
        if multiplierX == valuesX[i]:
            multiplierX = 0
            multiplierY = multiplierY + videoData[2]
        canvas.paste(image, (0+multiplierX,0+multiplierY))
    canvas.save(f'canvas{i}_{fileName}.png', quality=100)




txt1 = '<AnimatedActor>\n	<Info CreatedBy="Unknown" CreatedOn="14-Dec-23 3:56:17 PM" Version="4" Fps="30"/>\n	<Content>\n		<Spritesheets>'
txt2 = ''
for i in range(length):
    txt2 = txt2 + f'\n			<Spritesheet Path="canvas{i}_{fileName}.png" Id="{i}"/>'
txt2 = txt2 + '\n		</Spritesheets>\n		<Layers>'
txt3 = ''
for i in range(length):
    txt3 = txt3 + f'\n			<Layer Name="sheet{i}" Id="{i}" SpritesheetId="{i}"/>'
txt3 = txt3 + '\n		</Layers>\n		<Nulls/>\n		<Events/>\n	</Content>\n	<Animations DefaultAnimation="sheet0">'
txt4 = ''
for i in range(len(valuesF)):
    txt4 = txt4 + f'\n		<Animation Name="sheet{i}" FrameNum="{valuesF[i]+1}" Loop="false">'
    txt4 = txt4 + f'\n			<RootAnimation>\n				<Frame XPosition="0" YPosition="0" XScale="100" YScale="100" Delay="1" Visible="true" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="false"/>\n			</RootAnimation>\n			<LayerAnimations>'
    for c in range(i+1):
        txt4 = txt4 + f'\n				<LayerAnimation LayerId="{c}" Visible="true"/>'
    else:
        txt4 = txt4.replace(f'\n				<LayerAnimation LayerId="{c}" Visible="true"/>','')
        txt4 = txt4 + f'\n 				<LayerAnimation LayerId="{c}" Visible="true">'
    yCrop = 0
    xCrop = 0
    txt4 = txt4 + f'\n					<Frame XPosition="0" YPosition="0" XPivot="16" YPivot="16" XCrop="{xCrop}" YCrop="{yCrop}" Width="{videoData[1]}" Height="{videoData[2]}" XScale="100" YScale="100" Delay="1" Visible="true" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="false"/>'
    for x in range(valuesF[i]):
        xCrop = xCrop + videoData[1]
        if xCrop == valuesX[i]:
            xCrop = 0
            yCrop = yCrop + videoData[2]
        txt4 = txt4 + f'\n					<Frame XPosition="0" YPosition="0" XPivot="16" YPivot="16" XCrop="{xCrop}" YCrop="{yCrop}" Width="{videoData[1]}" Height="{videoData[2]}" XScale="100" YScale="100" Delay="1" Visible="true" RedTint="255" GreenTint="255" BlueTint="255" AlphaTint="255" RedOffset="0" GreenOffset="0" BlueOffset="0" Rotation="0" Interpolated="false"/>'
    for n in range(len(valuesF)+1):
        # print(n,i)
        if(n==0):
            txt4 = txt4 + f'\n				</LayerAnimation>'
            # print(i,n,"1")
        if(n>i):
            txt4 = txt4 + f'\n				 <LayerAnimation LayerId="{n}" Visible="true"/>'
            # print(i,n,"2")
    txt4 = txt4 + '\n			</LayerAnimations>\n			<NullAnimations/>\n			<Triggers/>\n		</Animation>'
txt4 = txt4 + '\n	</Animations>\n</AnimatedActor>'
f = open("animfile.txt","a")
anm2txt = txt1+txt2+txt3+txt4
f.write(anm2txt)
f.close()
import os
try:
    os.remove(f'{fileName}.anm2')
except:
    print("")
os.rename('animfile.txt', f'{fileName}.anm2')
for i in saveToErase:
    os.remove(i)
os.mkdir("output")
os.rename(f'{fileName}.anm2',f'output/{fileName}.anm2')
os.rename(f'{fileName}.ogg',f'output/{fileName}.ogg')
for i in range(len(valuesF)):
    os.rename(f'canvas{i}_{fileName}.png',f'output/canvas{i}_{fileName}.png')
