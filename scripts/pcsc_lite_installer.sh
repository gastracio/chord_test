echo Installing pcsc-light
sudo apt-get install -y autoconf libtool libsystemd-dev libudev-dev flex

echo
git clone https://salsa.debian.org/rousseau/PCSC.git
cd PCSC
./bootstrap
./configure
make
cd ../
sudo rm -rf PCSC
echo
echo
