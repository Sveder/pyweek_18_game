from PIL import Image

pic = Image.open("simple4.png")

for i in xrange(365):
    new_pic = pic.rotate(i)
    new_pic.save("simple4_%s.png" % i)