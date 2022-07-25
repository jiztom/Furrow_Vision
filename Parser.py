import pathlib
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source', help='setting the source folder')
parser.add_argument('-d', '--dest', help='setting the destination folder')
parser.add_argument('square', type=int, help='squaring the values')
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
args = parser.parse_args()

answer = args.square**2

if args.verbose:
    print("the square of {} equals {}".format(args.square, answer))
else:
    print(answer)