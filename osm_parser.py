from PIL import Image, ImageDraw
import osmium
import random
import matplotlib.pyplot as plt

lat_max = 37.4971437
lat_min = 37.4952007
lon_min = 127.0517836
lon_max = 127.0540056


img = Image.open('gangnam.png')
width, height = img.size
draw = ImageDraw.Draw(img)

#위도, 경도를 x,y 좌표로 변환
def latlon_to_pixel(lat,lon):
    x = int((lon - lon_min) / (lon_max - lon_min) * width)
    y = int((lat_max - lat) / (lat_max - lat_min) * height)
    return x,y

class HighwayNodeRecorder(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        #키 : 웨이 id , 값 : (위도 경도) 리스트
        self.way_nodes = {}
    
    def way(self,w):
        # highway 태그가 있을 경우에만
        if 'highway' in w.tags:
            coords = []
            for n in w.nodes:
                if n.location.valid():
                    coords.append((n.location.lat,n.location.lon))
            self.way_nodes[w.id] = coords

handler = HighwayNodeRecorder()
handler.apply_file('map.osm', locations=True)

for way_id, coords in handler.way_nodes.items():
    #print(f"Way {way_id} : {coords}")
    pixels = [latlon_to_pixel(lat,lon) for lat,lon in coords]
    color = tuple(random.randint(0,255) for _ in range(3))
    draw.line(pixels, fill=color, width = 4)
    r = 4
    for x,y in pixels:
        draw.ellipse((x-r,y-r,x+r,y+r), fill=color,outline=None)


plt.figure(figsize=(8,8))
plt.imshow(img)
plt.axis('off')
plt.show()

img.save('gangnam_with_ways.png')
