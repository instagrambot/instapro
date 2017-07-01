import argparse
from instabot import User

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('user', type=str, help="username")
parser.add_argument('password', type=str, help="password")
args = parser.parse_args()

_ = User(args.user, args.password)