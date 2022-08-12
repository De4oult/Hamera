from write import video, photo
from virtualcam import camera
from matrix import matrix_bg
from render import render

import sys

args = sys.argv

if len(args) == 1:
    print("Err! Need more args")

elif args[1] == "-r":
    render()

elif args[1] == "-c":
    camera()

elif args[1] == "-v":
    if len(args) <= 2:
        print("Err! Need file name arg")
    else:
        video(14, str(args[2]))

elif args[1] == "-p":
    if len(args) <= 2:
        print("Err! Need file name arg")
    else:
        photo(args[2])

else:
    print("Err!")