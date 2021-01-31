# Telegram-Crawler
Crawl Text Messages for Telegram Channel & Groups.

## Installation
This project can only run under Linux distribution. Ubuntu 18.04 is tested.

The following step shows that how to install `Telegram-Crawler` in Ubuntu 18.04.

1. Install [TDLib](https://github.com/tdlib/td). Follow the installation step of TDLib: [TDLib build instructions generator](https://tdlib.github.io/td/build.html).
```
Programming Language: Python;
Operating System: Linux
Linux distro: Ubuntu 18
Enable Link Time Optimization (requires CMake >= 3.9.0). It can significantly reduce binary size and increase performance, but sometimes it can lead to build failures: No
Build the debug binary. Debug binaries are much larger and slower than the release one: No
Install built TDLib to /usr/local instead of placing the files to td/tdlib: Yes
Choose which compiler you want to use to build TDLib: G++
```
Once you have chosen all the options, the install commands will be shown on the page. The following is an example bash commands for Ubuntu 18.04.
```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install make git zlib1g-dev libssl-dev gperf php-cli cmake g++
git clone https://github.com/tdlib/td.git
cd td
rm -rf build
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX:PATH=/usr/local ..
cmake --build . --target install
cd ..
cd ..
ls -l /usr/local
```

2. Install python-telegram by running the following commands:
```bash
sudo apt install python3-pip
pip3 install python-telegram
```

3. Clone this repo:
```bash
git clone https://github.com/bjrjk/Telegram-Crawler.git
cd Telegram-Crawler
```

## Configuration
1. Go to [Telegram Delete Account or Manage Apps](https://my.telegram.org/apps) to apply for a API ID & API Hash.

2. Run the following commands in your bash or add them to you `.bashrc`.
```bash
export TG_API_ID="Your API ID Here"
export TG_API_HASH="Your API Hash Here"
export TG_PHONE="Your Telegram Phone Account Here"
export TG_DB_ENCRYPTION_KEY="An arbitrary password for tdlib database encryption"
```

3. Modify `tg_crawler.py` to set options:
```python
if __name__ == '__main__':
    main(
        groupTitle='Group/Channel Title', # Fill in Your Group Title Here
        limit=100000, # Message number You want to retrieve, -1 to retrieve all
        fileName='chatMessages.log' # Where to store your crawled data
    )
```

4. Run the crawler by following command:
```bash
sh crawler.sh
```