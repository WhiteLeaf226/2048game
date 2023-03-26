import canshu
from game import game
 
def main(opt):

    screen_width = opt.width
    screen_height = opt.height
    block_jiange = opt.block_jiange
    block_size = opt.block_size
 
    game_2048 = game(screen_width, screen_height, block_jiange, block_size)
    game_2048.Form()
 
 
if __name__ == '__main__':
    opt = canshu.parse_args()
    main(opt)
