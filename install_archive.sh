#!/usr/bin/env bash

# $1 - archive path
# $2 - general product name
# $3 - isCE

if [ $3 == "1" ]; then
  echo "Installing as CE Distribution"
fi

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
if [ $3 == "1" ]; then
  commonName="$commonName-ce"
fi

if [ -d "./$commonName" ]; then
  echo "Removing old version"
  yes | rm -r $commonName
fi

ceE="0"

if [ -e "$2-ce" ] && [ $3 == "0" ]; then
  mv $2-ce hold-ce
  ceE="1"
fi

export progDirL=$(echo "$progDir" | sed -e 's/\(.*\)/\L\1/')

mv * ../$commonName
cd ..
rm -r tmp

cd $commonName/bin || exit 1

if [ $3 == "1" ]; then
  cp $2.svg $commonName.svg
fi
cp -u $commonName.svg /usr/share/pixmaps/
cp -u $jbiDir/$commonName.desktop /usr/share/applications/

if [ $ceE == "1" ]; then
  mv hold-ce $2-ce
fi

echo "Software Installed"