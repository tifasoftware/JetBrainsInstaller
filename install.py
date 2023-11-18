#!/usr/bin/env python

import platform
#from urllib.request import urlretrieve
import sys
import subprocess
import json


def checkArm():
    if platform.machine() == "aarch64":
        return True
    else:
        return False


fileName = "listing.json"
if checkArm():
    fileName = "listing-arm.json"

listingFile = open(fileName, "r")

productListing = json.loads(listingFile.read())

supportedProducts = list(productListing.keys())

listingFile.close()

#unsupportedProducts = ['aqua']

# print(supportedProducts)

def safeSearch(array, value):
    try:
        return array.index(value)
    except ValueError:
        return -1

def verifyProduct(productName):
    if safeSearch(supportedProducts,productName) != -1:
        return True
    else:
        print("Product does not exist")
        return False

def getProductDownloadLink(productName, isCE = False):
    if (verifyProduct(productName)):
        url = productListing[productName]
        if isCE:
            url = productListing[productName + "-ce"]
        return url
    else:
        return "about:blank"


def installLinuxArchive(productName, archivepath, isCE = False):
    ceNum = 0
    if isCE:
        ceNum = 1

    subprocess.run(["sudo", "/usr/bin/env", "bash", "install_archive.sh", archivepath, productName, str(ceNum)])


def urlretrieve(url, filename):
    return subprocess.run(["wget", "-O", filename, url]).returncode == 0


def getProductList(arguments):
    productList = []
    if (safeSearch(arguments, "@all") != -1):
        productList = supportedProducts
    else:
        for x in range(1, len(arguments) - 1):
            productList = productList + [arguments[x].lower()]
    #print(productList)
    return productList

def installProduct(productName, isCE):
    url = (getProductDownloadLink(productName, isCE))
    print("URL: " + url + "")
    tarF = "./"+productName+".tar.gz"
    if url != "about:blank":
        if urlretrieve(url, tarF):
            print("Installing " + productName)
            installLinuxArchive(productName, tarF, isCE)
        else:
            print("Download Failed!")

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
    #print("Unsupported Product: ")
    #print("aqua - IDE in beta, doesn't support ARM Linux")


args = list(sys.argv)
#print(len(args))
if len(args) == 1:
    args = args + ['-h']

if args[1] == "-h":
    print("Syntax: install.py [-hli] [-e PATH_TO_ARCHIVE] PRODUCT(s) [-c]")
elif args[1] == "-l":
    printListing()
elif args[1] == "-i":
    interactive()
elif args[1] == "-e":
    if len(args) == 4:
        args = args + [""]
    if len(args) == 5:
        if verifyProduct(args[3]):
            installLinuxArchive(args[3], args[2].lower(), args[4] == "-c")
    else:
        print("Invalid Arguments")
else:
    if args[-1] != "-c":
        args = args + [""]
    for product in getProductList(args):
        if verifyProduct(product):
            print(product)
            installProduct(product, args[-1] == "-c")

