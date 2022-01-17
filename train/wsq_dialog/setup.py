from distutils.core import setup
import py2exe
import glob

opts = {
    'py2exe': {
        "includes": ["matplotlib.backends",
                     "matplotlib.figure",
                     "pylab",
                     "numpy",
                     "matplotlib.backends.backend_tkagg"],
        'excludes': ['_gtkagg',
                     '_tkagg',
                     '_agg2',
                     '_cairo',
                     '_cocoaagg',
                     '_fltkagg',
                     '_gtk',
                     '_gtkcairo', ],
        'dll_excludes': ['libgdk-win32-2.0-0.dll',
                         'libgobject-2.0-0.dll']
    }
}

data_files = [(r'mpl-data', glob.glob(r'C:\Anaconda\Lib\site-packages\matplotlib\mpl-data\*.*')),
              (r'mpl-data', [r'C:\Anaconda\Lib\site-packages\matplotlib\mpl-data\matplotlibrc']),
              (r'mpl-data\images', glob.glob(r'C:\Anaconda\Lib\site-packages\matplotlib\mpl-data\images\*.*')),
              (r'mpl-data\fonts', glob.glob(r'C:\Anaconda\Lib\site-packages\matplotlib\mpl-data\fonts\*.*'))]

setup(
    # options=options,
    zipfile=None,
    windows=[{"script": "quotedlg.py"}],
    data_files=data_files,
    version='Wind 1.0',
    name='WindAPI Demo --- WSQ Subscribe',
    options=opts,
)
