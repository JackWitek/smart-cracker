import itertools
import time
import subprocess

#########################################

possibleStartTerms = ['','0','start']
possibleMiddleTerms = ['','one','two','three','four','4',]
combos = 3 # How many middle terms to be grouped together (For x number of empty strings in midTerms, list will also include [combos - x] combos)
possibleEndTerms = ['','0','1','2','3']
ignoreStrings = ['fourone','fourtwo']

generatedPasswordList = "words.txt"

zipFile = 'C:/Users/Jack/Documents/Test.7z'
exeFile = 'C:/Program Files/7-Zip/7z.exe'

#########################################
# Longer passwords, take longer to check!
# 4 char passwords = 17 passwords/s
# 10 char passwords = 11 passwords/s
# 15 char passwords = 9 passwords/s
# 20 char passwords = 7 passwords/s


permList = list(itertools.permutations(possibleMiddleTerms,combos))

print(len(permList) , 'middle term permutations')
textfile = open(generatedPasswordList, "w")
for perm in permList:
    permStr = ''.join(perm)
    for start in possibleStartTerms:
        for ending in possibleEndTerms:
            line = start + permStr + ending + "\n"
            for stop in ignoreStrings:
                if stop not in line:
                    continue
            textfile.write(line)
textfile.close()

with open(generatedPasswordList) as f:
    words = f.read().splitlines()

passwordsToTry = len(words)

print(passwordsToTry, 'passwords to try')
print()
realstart = time.time()
start = time.time()
current = 0
with open(generatedPasswordList, "r") as file:
  for line in file:
    word = line.strip()
    cmd = [exeFile, 't', zipFile, '-P' + word]
    sp = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    out, err = sp.communicate()
    current +=1
    if current %100 == 0:
        print("Currently at password #",current)
        end = time.time()
        rate = 100 /(end - start)
        start = time.time()
        print("Speed:" , "{:.2f}".format(rate), "passwords/s")
        print("Estimated time left:","{:.0f}".format((passwordsToTry-current)/rate), "seconds")
        print()
    if "Wrong password" not in out.decode("utf-8") :
        if "Everything is Ok" in out.decode("utf-8"):
            print("FOUND PASSWORD:", word)
            end = time.time()
            print("Total speed:" , "{:.2f}".format(current /(end - realstart)), "passwords/s")
            print("Total time:" , "{:.2f}".format(end - realstart), "s")
            exit()
        else:
            print("Got unexpected output from 7zip:", out.decode("utf-8"))
            print("Current word:", word)
            input("Press enter to continue...")


end = time.time()
print("No correct password found :(")
print("Average speed:" , "{:.2f}".format(passwordsToTry /(end - realstart)), "passwords/s")
print("Total time:" , "{:.2f}".format((end - realstart)), "seconds")