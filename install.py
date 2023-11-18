#!/usr/bin/env python

import platform
import os
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

def getProductDownloadLink(productName):
    if (verifyProduct(productName)):
        url = productListing[productName]
        return url
    else:
        return "about:blank"


def installLinuxArchive(productName, archivepath):
    ceNum = 0

    return subprocess.run(["sudo", "/usr/bin/env", "bash", "install_archive.sh", archivepath, productName, str(ceNum)]).returncode


def urlretrieve(url, filename):
    return subprocess.run(["wget", "-O", filename, url]).returncode == 0


def getProductList(arguments):
    productList = []
    if (safeSearch(arguments, "@all") != -1):
        productList = supportedProducts
    else:
        for x in range(1, len(arguments)):
            productList = productList + [arguments[x].lower()]
    #print(productList)
    return productList

def installProduct(productName):
    url = (getProductDownloadLink(productName))
    print("URL: " + url + "")
    tarF = "./"+productName+".tar.gz"
    if url != "about:blank":
        if urlretrieve(url, tarF):
            print("Installing " + productName)
            if installLinuxArchive(productName, tarF) == 0:
                os.remove(tarF)
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
            installProduct(test)
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
            installLinuxArchive(args[3], args[2].lower())
    else:
        print("Invalid Arguments")
else:
    for product in getProductList(args):
        if verifyProduct(product):
            #print(product)
            installProduct(product)

