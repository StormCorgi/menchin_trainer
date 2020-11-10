# definition
import collections
import copy
import random


def serialize_tiles(tiles):
    # 1-9牌カウント ex.[2,3,3] => [0,1,2,0,0,0,0,0,0]
    s_tiles = [0]*9
    for i in range(9):
        s_tiles[i] = tiles.count(i + 1)
    return s_tiles


def deserialize_tiles(s_tiles):
    # 1-9牌カウント ex.[0,1,2,0,0,0,0,0,0] => [2,3,3]
    tiles = []
    for i in range(9):
        for j in range(s_tiles[i]):
            tiles.append(i + 1)
    return tiles

# 刻子(pong)


def find_pong(t):
    for i in range(9):
        if t[i] >= 3:
            t[i] -= 3
    return t

# 順子(chow)


def find_chow_descend(s_tiles):
    t = copy.deepcopy(s_tiles)
    cursor = [7, 6, 5, 4, 3, 2, 1]
    for i in cursor:
        # n=2,3,4,5,6,7,8のとき n-1, n, n+1 の個数が全て１以上なら順子
        if t[i + 1] >= 1 and t[i] >= 1 and t[i - 1] >= 1:
            t[i + 1] -= 1
            t[i] -= 1
            t[i - 1] -= 1
            cursor.insert(7-i, i)
    return t


def find_chow_ascend(s_tiles):
    t = copy.deepcopy(s_tiles)
    cursor = [1, 2, 3, 4, 5, 6, 7]
    for i in cursor:
        # n-1, n, n+1 の個数が全て１以上なら順子
        if t[i - 1] >= 1 and t[i] >= 1 and t[i + 1] >= 1:
            t[i - 1] -= 1
            t[i] -= 1
            t[i + 1] -= 1
            cursor.insert(i-1, i)
    return t

# 雀頭


def find_eyes(s_tiles):
    eyes_pattern = []
    for i in range(9):
        if s_tiles[i] >= 2:
            eyes_pattern.append(i+1)
    return eyes_pattern

# n面子探索 :　刻子優先 / 順子優先 (昇順 / 降順)


def find_meld(s_tiles, search_desc=True, pref_chow=True):
    t = copy.deepcopy(s_tiles)
    if pref_chow:
        # 順子優先探索
        if search_desc:
            t = find_chow_descend(t)
            t = find_pong(t)
        else:
            t = find_chow_ascend(t)
            t = find_pong(t)
    else:
        # 刻子優先探索
        t = find_pong(t)
        if search_desc:
            t = find_chow_descend(t)
        else:
            t = find_chow_ascend(t)

    # 1-9牌が全て0枚=面子
    if t.count(0) == 9:
        return True
    else:
        return False


def hola_finder(hand):
    hand.sort()
    s_tiles = serialize_tiles(hand)
    hola_tile = []
    for i in range(9):
        # 既に4枚持っている牌はツモれないため飛ばす
        if s_tiles[i] >= 4:
            continue
        # 1牌ずつ数牌を足す
        array_adding_one = copy.deepcopy(s_tiles)
        array_adding_one[i] += 1

        # すべての対子(刻子からも抜き取る)を列挙、雀頭候補として探索のキーとする
        eyes_pattern_list = find_eyes(array_adding_one)
        # 雀頭なし＝ノーテン
        if len(eyes_pattern_list) == 0:
            continue

        # 雀頭あり雀頭候補を抜きとった手で4面子が作れるか
        for eye in eyes_pattern_list:
            headless_tiles = copy.deepcopy(array_adding_one)
            headless_tiles[eye - 1] -= 2
            # 4メンツが見つかった＝最初に足した牌は待ち牌だった
            if find_meld(headless_tiles, True, True):
                hola_tile.append(i+1)
                break
            elif find_meld(headless_tiles, True, False):
                hola_tile.append(i+1)
                break
            elif find_meld(headless_tiles, False, True):
                hola_tile.append(i+1)
                break
            elif find_meld(headless_tiles, False, False):
                hola_tile.append(i+1)
                break
            else:
                continue
            break
    # 待ち牌表示の重複排除
    unique_tile = list(set(hola_tile))
    unique_tile.sort()
    return unique_tile
