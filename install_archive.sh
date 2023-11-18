#!/usr/bin/env bash

# $1 - archive path
# $2 - general product name

export jbiDir="$(pwd)"
mkdir /opt/jetbrains/
mkdir /opt/jetbrains/tmp
tar xvf $1 -C /opt/jetbrains/tmp
rawarchDir="${1%".tar.gz"}"
archDir="${rawarchDir%%-*}"
progDir="$(basename $archDir)"
# rm $1
cd /opt/jetbrains/tmp

commonName=$2

if [ -d "./$commonName" ]; then
  echo "Removing old version"
  yes | rm -r $commonName
fi

export progDirL=$(echo "$progDir" | sed -e 's/\(.*\)/\L\1/')

mv * ../$commonName
cd ..
rm -r tmp

cd $commonName/bin || exit 1

cp -u *.svg /usr/share/pixmaps/$2.svg
cp -u $jbiDir/$commonName.desktop /usr/share/applications/

echo "Software Installed"