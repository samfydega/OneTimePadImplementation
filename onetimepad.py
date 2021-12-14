# average words in an email: 434
# average characters per word: ~5
# bits per character: 8
# bits for an average encrypted message sent using one-time pad cypher: 17,360 (2170 bytes) (2.17 KB)
# bits for private key: 17,360 (2.17KB)
# 1 million messages a day stores 2.17GB

import data
import random

def encryptedandkeytodecrypted(encryptedmessage, key):

    encryptedinascii = ""
    privatekeyinascii = ""
    decryptedmessageinascii = ""

    for x in encryptedmessage:
        encryptedinascii = encryptedinascii + data.asciiprintablecharacterslibrary[x] + " "

    for x in key:
        privatekeyinascii = privatekeyinascii + data.asciiprintablecharacterslibrary[x] + " "

    x = 0
    while x < len(encryptedinascii):
        if encryptedinascii[x] == " ":
            decryptedmessageinascii = decryptedmessageinascii + " "
            x += 1
        else:
            decryptedmessageinascii = decryptedmessageinascii + str(XOR(int(encryptedinascii[x]), int(privatekeyinascii[x])))
            x += 1


    finaldecrypted = binarytotext(decryptedmessageinascii)
    return finaldecrypted

def texttobinary(phrasetoparse):

    final = ""

    for x in phrasetoparse:
        final = final + str(data.asciiprintablecharacterslibrary[x]) + " "

    return final

def binarytotext(phrasetoconvert):

    final = ""
    temp = ""

    #01101100 01110001 01111010

    for x in phrasetoconvert:

        if x != " ":
            temp = temp + x

        else:
            add = ""
            for y in data.asciiprintablecharacterslibrary:
                if data.asciiprintablecharacterslibrary[y] == temp:
                    add = y

            if add != "":
                final = final + add
                temp = ""
            else:
                final = final + "?"
                temp = ""


    return final

def XOR(num1, num2):
    if str(num1) == str(num2):
        return 0
    else:
        return 1

def binarygeneratingkey2(binary):

    #01110000 01101110 01100011 01100101 00100000 01110101 01110000

    count = 0
    key = ""
    message = ""

    for x in binary:

        # start of string -> first digit must be 0, so 0 XOR 0 will give 0 in encrypted message
        if count == 0:
            key = key + "0"
            message = message + "0"
            count += 1

        # either key, message, or both must be 1
        elif count == 1:
            flip = random.random()

            if flip <= 0.50000000000:
                if x == "1":
                    key = key + "1"
                    message = message + "0"
                    count += 1
                elif x == "0":
                    key = key + "1"
                    message = message + "1"
                    count += 1

            else:
                if x == "1":
                    key = key + "0"
                    message = message + "1"
                    count += 1
                elif x == "0":
                    key = key + "1"
                    message = message + "1"
                    count += 1

        # key/message must be 1 if previously 0. if not, one/both can be random
        elif count == 2:

            # both are 1
            if key[-1] == "1" and message[-1] == "1":

                num2 = 0
                temprand = random.random()

                if temprand >= 0.5000000:
                    num2 = 1

                key = key + str(num2)
                message = message + str(XOR(int(x), num2))
                count += 1

            #key is 1, message is 0
            elif key[-1] == "1" and message[-1] == "0":

                if x == "1":
                    key = key + "0"
                    message = message + "1"
                    count += 1
                elif x == "0":
                    key = key + "1"
                    message = message + "1"
                    count += 1

            # key is 0, message is 1
            elif key[-1] == "0" and message[-1] == "1":
                key = key + "1"
                message = message + str(XOR(x, 1))
                count += 1

        # end of that character
        elif count == 8:
            key = key + " "
            message = message + " "
            count = 0

        # randomness for remaining decimal places
        else:

            num2 = 0
            temprand = random.random()

            if temprand >= 0.5000000:
                num2 = 1

            key = key + str(num2)
            message = message + str(XOR(int(x), num2))
            count += 1


    return key, message

# not using
def binarygeneratingkey(binary):

    finalKey = ""
    finalMessage = ""
    lastBlank = True
    count = 0
    currentstring = ""

    for x in binary:

        if x == " ":

            if currentstring == "01111111":

                if finalKey[-1] == 1:
                    finalKey[-1] = 0
                else:
                    finalKey[-1] = 1

                finalMessage[-1] = 0
                finalKey = finalKey + " "
                finalMessage = finalMessage + " "

            else:
                finalKey = finalKey + " "
                finalMessage = finalMessage + " "

            lastBlank = True
            count = 0
            currentstring = ""

        else:
            if lastBlank == True:
                finalMessage = finalMessage + "0"
                finalKey = finalKey + "0"
                lastBlank = False
                count += 1

            elif count == 2:
                finalMessage = finalMessage + "1"
                finalKey = finalKey + "1"
                count += 1

            else:
                num1 = x
                num2 = 0

                randomnum = random.random()

                if randomnum <= 0.50000000:
                    num2 = 1

                finalKey = finalKey + str(num2)

                newvalue = XOR(num1, num2)
                finalMessage = finalMessage + str(newvalue)
                count+=1

    return finalKey, finalMessage


if __name__ == '__main__':

    # Step 0: Print the phrase we want to encrypt
    phrase = "Potatoes were introduced to Europe from the Americas in the second half of the 16th century by the Spanish. " \
             "Today they are a staple food in many parts of the world and an integral part of much of the world's food supply. " \
             "As of 2014, potatoes were the world's fourth-largest food crop after maize (corn), wheat, and rice."

    print("##################")
    print("We are encrypting the phrase: '" + phrase + "'")
    print("##################")

    # Step 1: Take the text, turn it into ASCII binary
    originalmessageinbinary = texttobinary(phrase)
    print("##################")
    print("This phrase ASCII encoded is: " + originalmessageinbinary)
    print("Back to English: " + binarytotext(originalmessageinbinary))
    print("##################")

    # Step 2: Encrypt the binary (###################################################)
    privatekey, encryptedtext = binarygeneratingkey2(originalmessageinbinary)
    encryptedtext = encryptedtext + " "
    privatekey = privatekey + " "
    print("##################")
    print("The encrypted text is: " + encryptedtext)
    print("The private key (do not share) is: " + privatekey)
    print("##################")

    # Step 3/4: Pretend to be an adversary and read the encrypted message sent over an unsecured channel
    backtoasciimessage = binarytotext(encryptedtext)
    backtoasciikey = binarytotext(privatekey)
    print("##################")
    print("As the message receiver, I see the following.")
    print("My private key is:" + backtoasciikey)
    print("The encrypted message I've received is:" + backtoasciimessage)
    print("##################")

    # Step 4: Decrypt the binary
    finaldecrypted = encryptedandkeytodecrypted(backtoasciimessage, backtoasciikey)
    print("##################")
    print("The original message was: " + finaldecrypted)
    print(":D")
    print("##################")



