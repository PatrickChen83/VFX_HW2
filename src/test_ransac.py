from match import *
from LimitedPriorityQueue import LimitedPriorityQueue
from itertools import product, starmap, groupby
from imgtools import *
from PIL import Image
import numpy as np
import random
import sys
focal = 300
#showcase_mask(np.array(list(range(255))))
#
mat1 = parse_mat("../grail/1.mat")
mat2 = parse_mat("../grail/2.mat")
mat3 = parse_mat("../grail/3.mat")
# mat71 = parse_mat("../data/71.mat")
# mat72 = parse_mat("../data/72.mat")

merger = Merger()


# img2 = cyl_mapping(Image.open("../grail/2.jpg"), 300, mat2).transpose(1, 0, 2)
# img1 = cyl_mapping(Image.open("../grail/1.jpg"), 300, mat1).transpose(1, 0, 2)

# mat12, q12 = match(mat1, mat2)
# mat23, q23 = match(mat2, mat3)
# for x in q3:
#     mark_point(img1, x.fp1.xy())
#     mark_point(img2, x.fp2.xy())
# img1.show()
# img2.show()
#showcase_pairing(img1, img2, q3).show()
#
# mat69_70, queue69_70 = match(mat69, mat70)
# mat70_71, queue70_71 = match(mat70, mat71)
# mat71_72, queue71_72 = match(mat71, mat72)

#for pp in queue69_70:
#    print(pp)
#    mark_pair_for_concat(con, pp, mapping)
#con.show()
# Show pairing performance
#print(mat69_70)
#print(mat70_71)

# merger.add_image(np.array(Image.open("../grail/1.jpg")).transpose((1, 0, 2)), "1")
# merger.add_image(np.array(Image.open("../grail/2.jpg")).transpose((1, 0, 2)), "2")
# merger.add_image(np.array(Image.open("../grail/3.jpg")).transpose((1, 0, 2)), "3")
# merger.add_matrix(mat12, "1", "2")
# merger.add_matrix(mat23, "2", "3")
# merger.add_image(np.array(Image.open("../data/71.jpg")).transpose((1, 0, 2)), "c")
# merger.add_image(np.array(Image.open("../data/72.jpg")).transpose((1, 0, 2)), "d")
matrices = dict()

end = 18
start = 0
for i in range(start, end):
    matrices[i] = parse_mat("../grail/{num}.mat".format(num=i))
    merger.add_image(np.array(Image.open("../grail/{num}.jpg".format(num=i))).transpose((1, 0, 2)), str(i))
    if i > start:
        merger.add_matrix(match(matrices[i-1], matrices[i]), str(i-1), str(i))

merger.merge("0").show()

