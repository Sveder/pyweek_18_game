from PIL import Image

pic = Image.open("simple3.png")

for i in xrange(365):
    new_pic = pic.rotate(i)
    new_pic.save("simple3_%s.png" % i)