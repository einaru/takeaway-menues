#!/usr/bin/env bash
#
# Copyright (c) Einar Uvsløkk 2011 <einar.uvslokk@linux.com>
#
# Utility script for bumping the version of the Luma application.
# Uses `sed` to update the version variable in the version file.
# The version string should be on the format:
#  
#     VERSION = 'version'
#
# Where version typically is made up of version.release.modification,
# i.e. 3.0.6.

application="takeaway-menues"

srcfolder="src"
versionfile="info.py"

usage()
{
	echo "Bump the version of the application!"
	echo
	echo "usage: $0 [VERSION]"
	echo
	echo "If VERSION is missing you will be asked for the version."
	echo "NOTE: There will be now validation on the version you choose"
	echo
	echo "options:"
	echo
	echo "-h, --help    Prints usage and help."
}

ask_for_version()
{
	echo "Current version of $application:"
	echo "  $(sed -n "/VERSION = '\(.*\)'/p" $srcfolder/$versionfile)"
	echo "Bump $application version: "
	read version
	bump_version $version
}

bump_version()
{
	sed -i  "s/VERSION = '\(.*\)'/VERSION = '$1'/g" $srcfolder/$versionfile
}

if [[ "$1" == "" ]];
then
	ask_for_version
else
	case $1 in
		-h|--help)
			usage
			;;
		*)
			bump_version $1
			;;
	esac
fi
