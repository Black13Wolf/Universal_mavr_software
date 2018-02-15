import sys

class main:
    def __init__(self):
        msg = """\tExample of using:
            mavr-control -w : for windowed version
            mavr-control -c : for console version
            """
        if len(sys.argv) == 1:
            print(msg)
        else:
            if sys.argv[1] == '-c':
                print('console')
            elif sys.argv[1] == '-w':
                print('windowed')
            else:
                print(msg)

if __name__ == '__main__':
    q = main()