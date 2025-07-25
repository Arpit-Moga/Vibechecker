def greet(name):
    for i in range(5):
        print("Hello " + name)
        name = name + str(i)

def main():
    greet(123)
    greet(None)
    greet([1,2,3])

if __name__ == "__main__":
    main()
