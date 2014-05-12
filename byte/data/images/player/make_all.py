from PIL import Image

pic = Image.open("player.png")

for i in xrange(365):
    new_pic = pic.rotate(i)
    new_pic.save("player_%s.png" % i)