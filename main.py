from PIL import Image
im = Image.open('tst.png')
data = list(im.getdata())
# print(data)
def noir_blanc() :
	global data
	for i in range(len(data)):
		p=data[i]
		r=int((p[0]+p[1]+p[2])/3)
		p=(r, r, r)
		data[i]=p
noir_blanc()
# print(data)
im.putdata(data)
im.save("final.png", "PNG")
