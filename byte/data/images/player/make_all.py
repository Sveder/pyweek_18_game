from PIL import Image

for i in xrange(15):
    pic = Image.open("player_%s.png" % i)
    new_pic = pic.resize((200, 51))
    new_pic.save("player_small_%s.png" % i)

