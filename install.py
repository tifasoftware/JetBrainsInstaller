#!/usr/bin/env python

import platform
import webbrowser
import sys
import subprocess

listingFile = open("listing.txt", "r")

supportedProducts = []

for product in listingFile.readlines():
    supportedProducts += [product.strip()]

unsupportedProducts = ['aqua']

# print(supportedProducts)

def safeSearch(array, value):
    try:
        return array.index(value)
    except ValueError:
        return -1

def verifyProduct(productName):
    if safeSearch(supportedProducts,productName) != -1:
        return True
    elif safeSearch(unsupportedProducts,productName) != -1:
        print("This product is unsupported by this script.")
        if checkArm():
            print("This product might not be compatible with ARM")
        return True
    else:
        print("Product does not exist")
        return False

def getCECode(productName):
    if productName == "idea":
        return "&code=IIC"
    elif productName == "pycharm":
        return "&code=PCC"
    else:
        print("There is no Community Edition for this product.")
    return ""


def checkArm():
    if platform.machine() == "aarch64":
        return True
    else:
        return False


def getProductDownloadLink(productName, isCE = False):
    if (verifyProduct(productName)):
        url = "https://www.jetbrains.com/" + productName + "/download/download-thanks.html?platform=linux"
        if checkArm():
            url = url + "ARM64"
        if isCE:
            url = url + getCECode(productName)
        # webbrowser.open(url)
        return url
    else:
        return "about:blank"

def installLinuxArchive(productName, archivepath, isCE = False):
    ceNum = 0
    if isCE:
        ceNum = 1

    subprocess.run(["sudo", "/usr/bin/env", "bash", "install_archive.sh", archivepath, productName, str(ceNum)])

def installProduct(productName, isCE):
    url = (getProductDownloadLink(productName, isCE))
    print("URL: " + url + "")
    if url != "about:blank":
        if input("Is File Already Downloaded [y/N]: ").lower() != "y":

            webbrowser.open(url)
        tarF = input("Drag & Drop JetBrains tar.gz file to install: ").strip().strip("'").strip('"')
        print("Installing " + tarF)
        installLinuxArchive(productName, tarF, isCE)

def interactive():
    print("JetBrains Installer Interactive")
    print("ls to list supported products, quit to leave interactive")
    if checkArm():
        print("Processor: ARM64")
    else:
        print("Processor: x86_64")

    test = ""
    while test != "quit":
        test = input("Enter JetBrains Product Name: ")
        if test == "quit":
            break

        if (test != "ls") and (verifyProduct(test)):
            rce = input("Select Edition: [P] for professional, or [C] for community (Default = P): ")
            ce = False
            if rce.lower() == "c":
                ce = True
            installProduct(test, ce)
        elif test == "ls":
            printListing()


def printListing():
    print("Supported Products: ")
    for product in supportedProducts:
        print(product)
    print()
    print("Unsupported Product: ")
    print("aqua - IDE in beta, doesn't support ARM Linux")


args = list(sys.argv)
#print(len(args))
if len(args) == 1:
    args = args + ['-h']

if args[1] == "-h":
    print("Syntax: install.py [-hli] [-e PATH_TO_ARCHIVE] PRODUCT [-c]")
elif args[1] == "-l":
    printListing()
elif args[1] == "-i":
    interactive()
elif args[1] == "-e":
    if len(args) == 4:
        args = args + [""]
    if len(args) == 5:
        if verifyProduct(args[3]):
            installLinuxArchive(args[3], args[2], args[4] == "-c")
    else:
        print("Invalid Arguments")
else:
    if len(args) == 2:
        args = args + [""]
    if verifyProduct(args[1]):
        installProduct(args[1], args[2] == "-c")

