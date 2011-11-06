#!/bin/bash
while [ 1 ]; do
        for afbeelding in `grep -e "img" -e "video" broadcast.smil | sed -r "s/.*(img|video).*src=\"(.*\.png|.*\.m3u)\".*dur=\"(.*)s\".*/\\1\*\\2*\\3/g"`; do
                type=`echo $afbeelding | awk '{split($0,a,"*" ); print a[1]}'`
                file=`echo $afbeelding | awk '{split($0,a,"*" ); print a[2]}'`
                delay=`echo $afbeelding | awk '{split($0,a,"*" ); print a[3]}'`
                #echo $file
                #echo $delay
                if [ $type == "img" ]; then
                        #echo  "xloadimage $file sleep $delay"
                        xloadimage -global -fullscreen -global -onroot $file 2>&1 1>/home/tv/errors && sleep $delay;
                fi
                if [ $type == "video" ]; then
                        #echo "vlc $file"
                        #make sure we don't interrupt bima
                        if [ `ps aux | grep -c -e vlc -e gst-launch` -le 1 ]; then
                                TIJD=`date --iso-8601=seconds`
                                export DISPLAY=:0
                                screen -D -m /usr/bin/vlc -vvv --no-audio --extraintf logger --logfile /home/tv/log/vlc-${TIJD}.txt --file-caching 600 -f --vout-filter deinterlace:logo --deinterlace-mode blend --logo-file=/home/tv/programmalogo.png --logo-x=40 --logo-y=48 "$file"
                        fi
                fi
        done
done
