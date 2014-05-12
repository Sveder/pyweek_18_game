from PIL import Image

pic = Image.open("simple.png")

for i in xrange(365):
    new_pic = pic.rotate(i)
    new_pic.save("simple_%s.png" % i)