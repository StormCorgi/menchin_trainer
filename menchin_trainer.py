import random
import cv2
import jongg_machi as jm


def is_tehai_valid(target_hand):
    """validate array, mahjong use same 4 pi. not 5 or 6...
    """
    for i in supai:
        if target_hand.count(i) > 4:
            return False
    return True


def gen_tehai(gen_hand):
    """gen_tehai inputs 7 length array, and return mahjong hand (random)
    """
    for i in range(7):
        gen_hand[i] = supai[random.randint(0, len(supai)-1)]
    while is_tehai_valid(gen_hand) is False:
        gen_hand = gen_tehai(gen_hand)
    return tehai


def gen_hand_pict(hands, is_sorted):
    """input hand, sorted(bool), and generate image file.
    """
    for i, hand in enumerate(hands):
        tmp_img = cv2.imread('./pai-images/' + pisyu +
                             str(hand) + FILENAMESUFFIX)
        # flip 50%
        if is_sorted is False and random.randint(0, 1) == 1:
            tmp_img = cv2.flip(tmp_img, -1)

        # write image
        if i == 0:
            paisi = tmp_img
        else:
            paisi = cv2.hconcat([paisi, tmp_img])

    if is_sorted is True:
        cv2.imwrite('./ripi.jpg', paisi)
    else:
        cv2.imwrite('./question.jpg', paisi)


# main
supai = [3, 4, 5, 6, 7]
all_pisyu = ["man", "pin", "sou"]
pisyu = all_pisyu[random.randint(0, 2)]
FILENAMESUFFIX = "-66-90-l.png"

tehai = [0]*7
gen_tehai(tehai)
print(tehai)

# 問題用の牌姿
gen_hand_pict(tehai, False)
# 回答用の牌姿
tehai.sort()
gen_hand_pict(tehai, True)

print(tehai)
machi = jm.hola_finder(tehai)
print(machi)

if len(machi) == 0:
    STR = "ノーテン"
else:
    strcast = map(str, machi)
    STR = ','.join(strcast)
    STR += "待ち"

with open('answer.txt', 'w', encoding="utf-8") as f:
    f.write(STR)
