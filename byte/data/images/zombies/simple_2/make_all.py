from PIL import Image

pic = Image.open("simple2.png")

for i in xrange(365):
    new_pic = pic.rotate(i)
    new_pic.save("simple2_%s.png" % i)