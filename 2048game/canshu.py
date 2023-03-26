import argparse

def parse_args():
 
    parser = argparse.ArgumentParser(description='Game 2048')
 
    # Form
    parser.add_argument('--width', default=600)
    parser.add_argument('--height', default=800)
 
    # Block
    parser.add_argument('--block_jiange', default=20)
    parser.add_argument('--block_size', default=120)
 
    return parser.parse_args()