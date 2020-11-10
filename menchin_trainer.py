import random
import cv2
import jongg_machi as jm


def is_tehai_valid(tehai):
    for i in supai:
        if tehai.count(i) > 4:
            return False
    return True


def gen_tehai():
    tehai = [0]*7
    for i in range(7):
        tehai[i] = supai[random.randint(0, len(supai)-1)]
    while is_tehai_valid(tehai) is False:
        tehai = gen_tehai()
    return tehai


# main
supai = [3, 4, 5, 6, 7]
all_pisyu = ["man", "pin", "sou"]
pisyu = all_pisyu[random.randint(0, 2)]
filename_suffix = "-66-90-l.png"

tehai = gen_tehai()
print(tehai)


paisi = None
ripi_paisi = None

# 問題用の牌姿
for i in range(len(tehai)):
    tmp_img = cv2.imread('./pai-images/' + pisyu +
                         str(tehai[i]) + '-66-90-l.png')
    # flip 50%
    if random.randint(0, 1) == 1:
        tmp_img = cv2.flip(tmp_img, -1)
    # write image
    if i == 0:
        paisi = tmp_img
    else:
        paisi = cv2.hconcat([paisi, tmp_img])

cv2.imwrite('./question.jpg', paisi)


# 回答用の牌姿
tehai.sort()
for i in range(len(tehai)):
    tmp_img = cv2.imread('./pai-images/' + pisyu +
                         str(tehai[i]) + '-66-90-l.png')
    # write image
    if i == 0:
        ripi_paisi = tmp_img
    else:
        ripi_paisi = cv2.hconcat([ripi_paisi, tmp_img])

cv2.imwrite('./ripi.jpg', ripi_paisi)
print(tehai)
machi = jm.hola_finder(tehai)
print(machi)

if len(machi) == 0:
    str = "ノーテン"
else:
    strcast = map(str, machi)
    str = ','.join(strcast)
    str += "待ち"

with open('answer.txt', 'w', encoding="utf-8") as f:
    f.write(str)

