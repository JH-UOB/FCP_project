def main(*arguments):
    if arguments[0] == 'GUI':
        print('yes')
        import GUI
        GUI.main()

if __name__ == "__main__":
    import sys
    arguments = sys.argv[1:]
    print(arguments)
    main(*arguments)