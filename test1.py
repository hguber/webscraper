import nltk
from nltk.corpus import words
def main():
    elist = list()
    x =  "and John and Molly Garone"
    namelist = x.split()
    # and John and Molly Garone
    if len(namelist) == 5 and (namelist[0] == "and" or namelist[0] == "AND"):
        elist.append(namelist[1] + " " + namelist[4])
        elist.append(namelist[3] + " " + namelist[4])
    print(elist)

if __name__ == "__main__":
    main()