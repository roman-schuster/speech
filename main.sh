#!/bin/bash


###   Google Environment Variables   ###
########################################

export GOOGLE_APPLICATION_CREDENTIALS="/home/pi/speech/service_acct.json"
export GCLOUD_PROJECT="smartscale-rs"


###   Recording Audio   ###
###########################

# Checking if speech.wav already exists
CURRENTDIR=$(pwd)
CHECK4WAV=$(find $CURRENTDIR -name speech.wav | wc -l)

if [ $CHECK4WAV == 1 ]; then
    sudo python remove_old_wav.py
    sudo rm -rf speech.wav
fi

# Recording audio file
	# Filename	:	'speech.wav'
	# Sample Rate	:	16000 (16khz)
	# Precision	:	Signed 16-bit Little Endian Integer PCM
	# Duration	:	00:00:10.00 = 16000 samples ~ 750 CDDA sectors
	# File Size	:	650kb
	# Bit Rate	:	512k
	# VU-meter	:	mono (1 channel)

arecord -f cd -r 16000 -d 10 -t wav -c 1 -D plughw:1,0 speech.wav

# Making sure the reording saved properly
CHECK4WAV=$(find $CURRENTDIR -name speech.wav | wc -l)

if [ $CHECK4WAV == 1 ]; then
	sudo python recording_saved.py
else
	sudo python recording_not_saved.py
fi


########   Speech API    ########
#################################

python speech.py speech.wav
