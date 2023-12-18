# Domain Scraper

## Python Script (`domain.py`)

### Dependencies
- Python 3.x
- Requests
- BeautifulSoup4
- Tornado
- Pillow
- Numpy
- Sniffio

### Pasang project
1. Copy repo ini ke folder baru:
   ```bash
    git clone https://github.com/miftah06/domainscraper.git
   cd domainscraper
	```

### Instalasi untuk domain.py
1. Install dependencies using pip:
   ```bash
   pkg install python3
   pkg install python-pip
   pip install requests beautifulsoup4 tornado pillow numpy sniffio
   pip install -r requirements.txt
   python domain.py
	```
	
#### Penggunaan untuk melakukan Dorking
#### Penggunaan untuk melakukan google.py
1. -- untuk GOOGLE tolong cantumkan kata kunci dan input.txt secukupnya agar tidak terkena ban

2. Menjalankan skrip dengan google:
```bash
pip install -r requirements.txt
python3 google.py
  ```

#### Penggunaan untuk melakukan dork.py
1. Menjalankan skrip dengan bing dan yahoo:
```bash
pip install -r requirements.txt
python3 dork.py
  ```

##### Untuk Menggunakan termux.py/ TERMUX
```bash
pkg install python3
pkg install python-requests
pkg install python-pandas
pip install -r requirements.txt
pkg install nodejs
npm install -g appium-doctor
pip install Appium-Python-Client==0.45
python3 termux.py
```

##### Untuk Hasil atau output nya
```bash
mv ouput.csv hasil.csv
nano output.csv
  ```
-- lalu isi dengan tanda pagar (#) lalu exit

### Ganti hal ini pada script termux.py
--- 
from appium import webdriver

def setup_appium():
    desired_caps = {
        ##'platformName': 'Android',
        ##'platformVersion': 'YOUR_ANDROID_VERSION',
        'deviceName': 'YOUR_DEVICE_NAME',
        'appPackage': 'com.brave.browser',
        'appActivity': '.MainActivity',
        'noReset': True,
    }
---
### Dengan versi hape kalian masing-masing
	
## jangan lupa jalankan appium dengan menuliskan di termux

```bash
appium
```