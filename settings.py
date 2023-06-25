
from bin.urls import Url

ROUTER = [
    Url('index', [
        Url('blog')
    ])
]

# register anything you want to use
STATIC_REGISTER = {
    'image1':'image1.png',
    'txt': 'read.txt'
}

# where to scan html files
SCAN_DIRS = [
    'views',
    'static'
]

# charset of encode
ENCODING = 'utf8'

# base dir used to store html files
BASE_DIR = 'src/'

# static dir
STATIC_RESOURCE_DIR = 'static/'

# jump root
ROOT_HTML = 'index.html'

# scanning file types
FILE_TYPES = ['.html', '.png', 'jpg', 'webp']