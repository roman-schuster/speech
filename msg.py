from papirus import PapirusText
import argparse

def main(msg):
    display = PapirusText()
    display.write(msg)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'msg', help='/home/pi/msg.txt')
    args = parser.parse_args()
    main(args.msg)
