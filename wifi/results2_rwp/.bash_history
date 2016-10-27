cd ~/ && mkdir -p .ssh && chmod 700 .ssh && cd .ssh && touch authorized_keys2 && chmod 600 authorized_keys2 && cat ../id_rsa.pub >> authorized_keys2 && rm ../id_rsa.pub && cd ..
sudo visudo
sudo ps axu
sudo visudo
sudo ps axu
sudo visudo
sudo ps axu
ls
sudo apt-get install git
git clone https://github.com/intrig-unicamp/mininet-wifi
cd mininet-wifi
sudo util/install.sh -Wnfv 
sudo apt clean
sudo apt clear
sudo apt-get clean
sudo apt-get install build-essentials
sudo apt-get install build-essential 
vim /etc/apt/sources.list
sudo vim /etc/apt/sources.list
sudo apt update
sudo util/install.sh -Wnfv 
sudo apt-get update
sudo px axu
ps
sudo ps
sudo visudo
ls
visudo 
sudo visudo 
sudo ps
sudo apt-get update
sudo apt-get -y install autoconf automake build-essential libass-dev libfreetype6-dev   libsdl1.2-dev libtheora-dev libtool libva-dev libvdpau-dev libvorbis-dev libxcb1-dev libxcb-shm0-dev   libxcb-xfixes0-dev pkg-config texinfo zlib1g-dev
mkdir ~/ffmpeg_sources
sudo apt-get install yasm
sudo apt-get install libx264-dev
sudo apt-get install cmake mercurial
cd ~/ffmpeg_sources
hg clone https://bitbucket.org/multicoreware/x265
cd ~/ffmpeg_sources/x265/build/linux
PATH="$HOME/bin:$PATH" cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$HOME/ffmpeg_build" -DENABLE_SHARED:bool=off ../../source
make
sudo reboot
htop
sudo apt install htop
cd ~/ffmpeg_sources
hg clone https://bitbucket.org/multicoreware/x265
cd ~/ffmpeg_sources/x265/build/linux
PATH="$HOME/bin:$PATH" cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$HOME/ffmpeg_build" -DENABLE_SHARED:bool=off ../../source
make
cd ~
ls
cd ffmpeg_sources/
ls
cd ..
cd ffmpeg_sources/
rm -rf x265/
cd ~
cd ~/ffmpeg_sources
hg clone https://bitbucket.org/multicoreware/x265
cd ~/ffmpeg_sources/x265/build/linux
PATH="$HOME/bin:$PATH" cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$HOME/ffmpeg_build" -DENABLE_SHARED:bool=off ../../source
make
make install
make distcleanmake distclean
make distclean
sudo apt-get install libfdk-aac-dev
sudo apt-get install libmp3lame-dev
sudo apt-get install libopus-dev
cd ~/ffmpeg_sources
wget http://storage.googleapis.com/downloads.webmproject.org/releases/webm/libvpx-1.5.0.tar.bz2
tar xjvf libvpx-1.5.0.tar.bz2
cd libvpx-1.5.0
PATH="$HOME/bin:$PATH" ./configure --prefix="$HOME/ffmpeg_build" --disable-examples --disable-unit-tests
PATH="$HOME/bin:$PATH" make
make install
make clean
cd ~/ffmpeg_sources
wget http://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2
tar xjvf ffmpeg-snapshot.tar.bz2
cd ffmpeg
PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure   --prefix="$HOME/ffmpeg_build"   --pkg-config-flags="--static"   --extra-cflags="-I$HOME/ffmpeg_build/include"   --extra-ldflags="-L$HOME/ffmpeg_build/lib"   --bindir="$HOME/bin"   --enable-gpl   --enable-libass   --enable-libfdk-aac   --enable-libfreetype   --enable-libmp3lame   --enable-libopus   --enable-libtheora   --enable-libvorbis   --enable-libvpx   --enable-libx264   --enable-libx265   --enable-nonfree
PATH="$HOME/bin:$PATH" make
#Jo
cp ~/ffplay.c .
ls
git st
git status
cd ..
ls
find . -name "ffplay.c"
cd ffmpeg/
ls
ls -la
ls -la ffplay.c
PATH="$HOME/bin:$PATH" make ffplay
PATH="$HOME/bin:$PATH" make
make install
make disclean
hash -r
htop
ifconfig 
htop
ls
ps axu | grep mininet
ps axu | grep simple-mob-scanario.py
ps axu | grep "sudo ./simple-mob-scanario.py"
ps axu | grep "^sudo ./simple-mob-scanario.py"
ps axu | grep "sudo ./simple-mob-scanario.py" | grep "root"
ps axu | grep "sudo ./simple-mob-scanario.py" | grep "root" | awk {2}
ps axu | grep "sudo ./simple-mob-scanario.py" | grep "root" | awk {"print $2"}}
ps axu | grep "sudo ./simple-mob-scanario.py" | grep "root" | awk {"print $2" }}
ps axu | grep "sudo ./simple-mob-scanario.py" | grep "root" | awk '{print $2}'
kill $(ps axu | grep "sudo ./simple-mob-scanario.py" | grep "root" | awk '{print $2}')
sudo kill $(ps axu | grep "sudo ./simple-mob-scanario.py" | grep "root" | awk '{print $2}')
htop 
sudo kill $(ps axu | grep "sudo ./simple-mob-scanario.py" | grep "root" | awk '{print $2}')
ls
sudo kill $(ps axu | grep "sudo ./simple-mob-scanario.py" | grep "root" | awk '{print $2}')
ls
sudo kill $(ps axu | grep "sudo ./simple-mob-scanario.py" | grep "root" | awk '{print $2}')
[A
sudo kill $(ps axu | grep "sudo ./simple-mob-scanario.py" | grep "root" | awk '{print $2}')
source ~/.profile 
ls
pwd
cd ffmpeg_sources/
ls
rm ffmpeg
rm  -r ffmpeg
ls
git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg
ls
cd ffmpeg/
ls
cd ~
ls
cp ffplay.c ffmpeg_sources/ffmpeg/
cd ffmpeg_sources/ffmpeg/
ls
ls -la ffplay.c
cat ffplay.c | grep "UFRGS"
PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure   --prefix="$HOME/ffmpeg_build"   --pkg-config-flags="--static"   --extra-cflags="-I$HOME/ffmpeg_build/include"   --extra-ldflags="-L$HOME/ffmpeg_build/lib"   --bindir="$HOME/bin"   --enable-gpl   --enable-libass   --enable-libfdk-aac   --enable-libfreetype   --enable-libmp3lame   --enable-libopus   --enable-libtheora   --enable-libvorbis   --enable-libvpx   --enable-libx264   --enable-libx265   --enable-nonfree
PATH="$HOME/bin:$PATH" make
make install
make distclean
hash -r
source ~/.profile 
ls
ld
ls
ffplay
source ~/.profile 
cd ~
cd bin/
ls
cd ~/ffmpeg_sources/
ls
cd ffmpeg/
ls
PATH="$HOME/bin:$PATH" make ffplay
cat Makefile 
PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure   --prefix="$HOME/ffmpeg_build"   --pkg-config-flags="--static"   --extra-cflags="-I$HOME/ffmpeg_build/include"   --extra-ldflags="-L$HOME/ffmpeg_build/lib"   --bindir="$HOME/bin"   --enable-gpl   --enable-libass   --enable-libfdk-aac   --enable-libfreetype   --enable-libmp3lame   --enable-libopus   --enable-libtheora   --enable-libvorbis   --enable-libvpx   --enable-libx264   --enable-libx265   --enable-nonfree
sudo apt-get -y install autoconf automake build-essential libass-dev libfreetype6-dev   libsdl1.2-dev libtheora-dev libtool libva-dev libvdpau-dev libvorbis-dev libxcb1-dev libxcb-shm0-dev   libxcb-xfixes0-dev pkg-config texinfo zlib1g-dev
PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure   --prefix="$HOME/ffmpeg_build"   --pkg-config-flags="--static"   --extra-cflags="-I$HOME/ffmpeg_build/include"   --extra-ldflags="-L$HOME/ffmpeg_build/lib"   --bindir="$HOME/bin"   --enable-gpl   --enable-libass   --enable-libfdk-aac   --enable-libfreetype   --enable-libmp3lame   --enable-libopus   --enable-libtheora   --enable-libvorbis   --enable-libvpx   --enable-libx264   --enable-libx265   --enable-nonfree --enable-ffplay
.mak, config.h, and doc/config.texi...
config.asm is unchanged
libavutil/avconfig.h is unchanged
libavcodec/bsf_list.c is unchanged
libavformat/protocol_list.c i.mak, config.h, and doc/config.texi...
config.asm is unchanged
libavutil/avconfig.h is unchanged
libavcodec/bsf_list.c is unchanged
libavformat/protocol_list.c i
sudo apt-get install libsdl-dev
which sdl-config
cat config.log | grep ffplay
PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure   --prefix="$HOME/ffmpeg_build"   --pkg-config-flags="--static"   --extra-cflags="-I$HOME/ffmpeg_build/include"   --extra-ldflags="-L$HOME/ffmpeg_build/lib"   --bindir="$HOME/bin"   --enable-gpl   --enable-libass   --enable-libfdk-aac   --enable-libfreetype   --enable-libmp3lame   --enable-libopus   --enable-libtheora   --enable-libvorbis   --enable-libvpx   --enable-libx264   --enable-libx265   --enable-nonfree --enable-ffplay
apt-cache search libsdl2
sudo apt-get install libsdl2-dev
PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure   --prefix="$HOME/ffmpeg_build"   --pkg-config-flags="--static"   --extra-cflags="-I$HOME/ffmpeg_build/include"   --extra-ldflags="-L$HOME/ffmpeg_build/lib"   --bindir="$HOME/bin"   --enable-gpl   --enable-libass   --enable-libfdk-aac   --enable-libfreetype   --enable-libmp3lame   --enable-libopus   --enable-libtheora   --enable-libvorbis   --enable-libvpx   --enable-libx264   --enable-libx265   --enable-nonfree --enable-ffplay
cat ffplay.c | grep UFRGS
PATH="$HOME/bin:$PATH" make
make install
make distclean
hash -r
ffplay
source ~/.profile 
make install
make
PATH="$HOME/bin:$PATH" make ffplay
PATH="$HOME/bin:$PATH" make ffplay.c
ls
./configure 
PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure   --prefix="$HOME/ffmpeg_build"   --pkg-config-flags="--static"   --extra-cflags="-I$HOME/ffmpeg_build/include"   --extra-ldflags="-L$HOME/ffmpeg_build/lib"   --bindir="$HOME/bin"   --enable-gpl   --enable-libass   --enable-libfdk-aac   --enable-libfreetype   --enable-libmp3lame   --enable-libopus   --enable-libtheora   --enable-libvorbis   --enable-libvpx   --enable-libx264   --enable-libx265   --enable-nonfree
PATH="$HOME/bin:$PATH" make
git status
git diff HEAD ffplay.c
git st
git status
git checkout -- ffplay.c
PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure   --prefix="$HOME/ffmpeg_build"   --pkg-config-flags="--static"   --extra-cflags="-I$HOME/ffmpeg_build/include"   --extra-ldflags="-L$HOME/ffmpeg_build/lib"   --bindir="$HOME/bin"   --enable-gpl   --enable-libass   --enable-libfdk-aac   --enable-libfreetype   --enable-libmp3lame   --enable-libopus   --enable-libtheora   --enable-libvorbis   --enable-libvpx   --enable-libx264   --enable-libx265   --enable-nonfree
PATH="$HOME/bin:$PATH" make
ffplay
make install
make distclean
has -t
hash -r
ffplay 
cd ..
ls
cd 
cd ~
ls
cd ~
wget http://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2
tar xjvf ffmpeg-snapshot.tar.bz2
ls
git mergetool 
vimdiff ffplay.c ffmpeg/ffplay.c 
vimdiff ffplay.c ffmpeg_sources/ffmpeg/ffplay.c 
cd ffmpeg_sources/ffmpeg/
ls
git diff HEAD ffplay.c
PATH="$HOME/bin:$PATH" make
PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure   --prefix="$HOME/ffmpeg_build"   --pkg-config-flags="--static"   --extra-cflags="-I$HOME/ffmpeg_build/include"   --extra-ldflags="-L$HOME/ffmpeg_build/lib"   --bindir="$HOME/bin"   --enable-gpl   --enable-libass   --enable-libfdk-aac   --enable-libfreetype   --enable-libmp3lame   --enable-libopus   --enable-libtheora   --enable-libvorbis   --enable-libvpx   --enable-libx264   --enable-libx265   --enable-nonfree
PATH="$HOME/bin:$PATH" make
make install
make distclean
hash -r
ffplay http://video.webmfiles.org/big-buck-bunny_trailer.webm
ls
sudo kill $(ps axu | grep "sudo ./simple-mob-scanario.py" | grep "root" | awk '{print $2}')
ls
"sudo ./simple-mob-scanario.py" | grep "root" | awk '{print $2}')
mininet@mininet:~$ sudo kill $(ps axu | grep "sudo ./simple-mob-scanario.py" | grep "root" | awk '{print $2}')
ls *SEVEN.log"
ls *SEVEN.log
ls *SEVEN.log | wc -l
ls
ls *SEVEN.log
mkdir LOGS_SEVEN
mv *SEVEN.log LOGS_SEVEN/
ls
mininet@mininet:~$ sudo kill $(ps axu | grep "sudo ./simple-mob-scanario.py" | grep "root" | awk '{print $2}')
sudo
sudo kill $(ps axu | grep "sudo ./simple-mob-scanario.py" | grep "root" | awk '{print $2}')
mv *SEVEN.log LOGS_SEVEN/
sudo kill $(ps axu | grep "sudo ./simple-mob-scanario.py" | grep "root" | awk '{print $2}')
mv *SEVEN.log LOGS_SEVEN/
ls
ls *SEVEN.log
mv *SEVEN.log LOGS_SEVEN/
ls
ls *SEVEN.log
rm -rf *.log
ls
cd LOGS_SEVEN/
ls
cd ..
ls
sudo kill $(ps axu | grep "sudo ./simple-mob-scanario.py" | grep "root" | awk '{print $2}')
ls
ls *EIGHT.log
EIGHT.log
log_sta9_h2642250_rep20161011_154227_EIGHT.log
log_sta9_h2642250_rep20161011_154407_EIGHT.log
log_sta9_h2642250_rep20161011_154644_EIGHT.log
log_sta9_h2642250_rep20161011_155200_EIGHT.log
log_sta9_h2642250_rep20161011_155340_EIGHT.log
log_sta9_h2642250_rep20161011_155520_EIGHT.log
log_sta9_h2642250_rep20161011_160226_EIGHT.log
log_sta9_h2642250_rep20161011_160546_EIGHT.log
log_sta9_h2642250_rep20161011_160727_EIGHT.log
log_sta9_h2642250_rep20161011_162856_EIGHT.log
log_sta9_h2642250_rep20161011_163059_EIGHT.log
log_sta9_h2642250_rep20161011_163243_EIGHT.log
ls
mkdir LOGS_EIGHT
mv *EIGHT.log LOGS_EIGHT/
ls
mkdir LOGS_NINE
mv *NINE.log LOGS_NINE/
ls
htop
sudo mn -c
htop
ls
clear
ls
ls -l
sudo mn -c
ls
ffplay -autoexit http://10.0.0.1:8001/h2642250 2>&1 | tee log_sta1_h2642250_rep00_ONE.log
sudo kill $(ps axu | grep "sudo ./simple-mob-scanario.py" | grep "root" | awk '{print $2}')
l
ls
mkdir LOGS_SIX
cp *_SIX.log LOGS_SIX/
mv *_SIX.log LOGS_SIX/
ls
mkdir LOGS_FIVE
ls
cp *_FIVE.log LOGS_FIVE
mv *_FIVE.log LOGS_FIVE
ls
ls -l
ls -la
sudo reboot
sudo kill $(ps axu | grep "sudo ./simple-mob-scanario.py" | grep "root" | awk '{print $2}')
ls
mkdir LOGS_FOUR
mkdir LOGS_THREE
mkdir LOGS_TWO
mkdir LOGS_ONE
mv *FOUR.log LOGS_FOUR/
mv *THREE.log LOGS_THREE/
mv *TWO.log LOGS_TWO/
mv *ONE.log LOGS_ONE/
ls
ls -l
ls
python ls
ls
mv *ONE.log LOGS_ONE/
sudo kill $(ps axu | grep "sudo ./simple-mob-scenario.py" | grep "root" | awk '{print $2}')
reboot
sudo reboot
ls
ls *TWO.LOG
ls *TWO.log
ls *TWO.log | wc -l
sudo kill $(ps axu | grep "sudo ./simple-mob-scenario.py" | grep "root" | awk '{print $2}')
cat simple-mob-scenario.py 
reboot
sudo reboot
users
who
sudo who
sudo who --help
sudo who -t
sudo kill $(ps axu | grep "sudo ./simple-mob-scenario.py" | grep "root" | awk '{print $2}')
ls
sudo kill $(ps axu | grep "sudo ./simple-mob-scenario.py" | grep "root" | awk '{print $2}')
ls
ream over ream over ream over ream over ream over ream over ls *_SEVEN.log
ls
ls *_SEVEN.log
ls *_SEVEN.log | wc -l
mkdir logs_rwp
mv *.log logs_rwp/
ls
sudo kill $(ps axu | grep "sudo ./simple-mob-scenario.py" | grep "root" | awk '{print $2}')
ls
sudo kill $(ps axu | grep "sudo ./simple-mob-scenario.py" | grep "root" | awk '{print $2}')
zcrhupm1
sudo kill $(ps axu | grep "sudo ./simple-mob-scenario.py" | grep "root" | awk '{print $2}')
ls
ls *_NINE.log | wc -l
sudo kill $(ps axu | grep "sudo ./simple-mob-scenario.py" | grep "root" | awk '{print $2}')
ls *_NINE.log | wc -l
sudo reboot
ifconfig 
ping 10.0.0.91
ping 10.0.0.1
ifconfig 
iw 
iw list
iw info
iw wlan0 info
ifconfig 
ping 10.0.0.1
ping 10.0.0.91
ls
chmod +x simple-mob-scenario.py 
rm -rf *.log
ls
ls -la
chmod +x simple-mob-scenario2.py 
sudo mn -c && sudo ./simple-mob-scenario2.py 
./simple-mob-scenario2.py -n 1 -m h2642250 -c 9
sudo ./simple-mob-scenario2.py -n 1 -m h2642250 -c 9
sudo mn -c && sudo ./simple-mob-scenario2.py -n 1 -m h2642250 -c 9
sudo mn -c
sudo mn -c && sudo ./simple-mob-scenario2.py -n 1 -m h2642250 -c 9
sudo mn -c
./simple-mob-scenario2.py -n 1 -m h2642250 -c 9
sudo mn -c && ./simple-mob-scenario2.py -n 1 -m h2642250 -c 9
sudo mn -c && sudo ./simple-mob-scenario2.py -n 1 -m h2642250 -c 9
ls
tail *.log
sudo mn -c && sudo ./simple-mob-scenario2.py -n 1 -m h2642250 -c 9
ls
rm -rf *.log
ls
sudo mn -c && sudo ./simple-mob-scenario2.py -n 1 -m h2642250 -c 9
user
users
killall -u minient
killall -u mininet
sudo reboot
sudo mn -c
sudo kill $(ps axu | grep "sudo ./simple-mob-scenario.py" | grep "root" | awk '{print $2}')
sudo kill $(ps axu | grep "sudo ./simple-mob-scenario2.py" | grep "root" | awk '{print $2}')
ls
sudo kill $(ps axu | grep "sudo ./simple-mob-scenario2.py" | grep "root" | awk '{print $2}')
sudo reboot
ls
sudo mn -c
