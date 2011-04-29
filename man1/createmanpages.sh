#!/bin/bash

ending=".rst"

for i in *$ending;
do
	rst2man $i > `basename $i .rst`
done

nroff_em()
{
	for i in *".1 ";
	do
		$1 $i
	done
}

case $1 in
	gz)
		nroff_em gzip
		;;
	bz2)
		nroff_em bzip2
		;;
	*)
		echo "nroff manpage extension not recognized: $1"
		echo "Supported extenstions is: 'gz' and 'bz2'" 
		;;
esac
