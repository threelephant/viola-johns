from PIL import Image

mn = 5

image = Image.open("pictures/man{}/man{}.png".format(mn, mn))
cropped_image = image.crop((0, 0, 292, image.size[1]))
cropped_image.save("pictures/man{}/man{}_1.png".format(mn, mn))

cropped_image2 = image.crop((293, 0, 293+290, image.size[1]))
cropped_image2.save("pictures/man{}/man{}_2.png".format(mn, mn))


for i in range(1, 9):
    cropped_image_ = image.crop((293 + 290 * i + 1, 0, 293 + 290*(i + 1), image.size[1]))
    cropped_image_.save("pictures/man{}/man{}_{}.png".format(mn, mn, i + 2))
