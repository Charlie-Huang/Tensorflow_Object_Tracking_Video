def code_to_class_string(argument):
    switcher = {
                    'n02691156': "airplane",
                    'n02419796': "antelope",
                    'n02131653': "bear",
                    'n02834778': "bicycle",
                    'n01503061': "bird",
                    'n02924116': "bus",
                    'n02958343': "car",
                    'n02402425': "cattle",
                    'n02084071': "dog",
                    'n02121808': "domestic_cat",
                    'n02503517': "elephant",
                    'n02118333': "fox",
                    'n02510455': "giant_panda",
                    'n02342885': "hamster",
                    'n02374451': "horse",
                    'n02129165': "lion",
                    'n01674464': "lizard",
                    'n02484322': "monkey",
                    'n03790512': "motorcycle",
                    'n02324045': "rabbit",
                    'n02509815': "red_panda",
                    'n02411705': "sheep",
                    'n01726692': "snake",
                    'n02355227': "squirrel",
                    'n02129604': "tiger",
                    'n04468005': "train",
                    'n01662784': "turtle",
                    'n04530566': "watercraft",
                    'n02062744': "whale",
                    'n02391049': "zebra"            }
    return switcher.get(argument, "nothing")

def class_string_to_comp_code(argument):
    switcher = {
                    'airplane': 1,
                    'antelope': 2,
                    'bear': 3,
                    'bicycle': 4,
                    'bird': 5,
                    'bus': 6,
                    'car': 7,
                    'cattle': 8,
                    'dog': 9,
                    'domestic_cat': 10,
                    'elephant': 11,
                    'fox': 12,
                    'giant_panda': 13,
                    'hamster': 14,
                    'horse': 15,
                    'lion': 16,
                    'lizard': 17,
                    'monkey': 18,
                    'motorcycle': 19,
                    'rabbit': 20,
                    'red_panda': 21,
                    'sheep': 22,
                    'snake': 23,
                    'squirrel': 24,
                    'tiger': 25,
                    'train': 26,
                    'turtle': 27,
                    'watercraft': 28,
                    'whale': 29,
                    'zebra': 30                 }
    return switcher.get(argument, "nothing")

class Classes_List(object):
        
    class_name_string_list= ['airplane','antelope','bear','bicycle','bird','bus','car','cattle','dog','domestic_cat','elephant','fox','giant_panda','hamster','horse','lion','lizard','monkey','motorcycle','rabbit','red_panda','sheep','snake','squirrel','tiger','train','turtle','watercraft','whale','zebra']

    class_code_string_list= ['n02691156','n02419796','n02131653','n02834778','n01503061','n02924116','n02958343','n02402425','n02084071','n02121808','n02503517','n02118333','n02510455','n02342885','n02374451','n02129165','n01674464','n02484322','n03790512','n02324045','n02509815','n02411705','n01726692','n02355227','n02129604','n04468005','n01662784','n04530566','n02062744','n02391049']


