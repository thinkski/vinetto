from distutils.core import setup
setup (name='vinetto',
    version='0.06alpha',
    scripts=['vinetto'],
    py_modules=['vinutils', 'vinreport'],
    data_files=[('/usr/share/vinetto', ['res/header', 'res/huffman', \
                                        'res/quantization', \
					'res/HtRepTemplate.html'])],
    description='vinetto : a forensics tool to examine Thumbs.db files.',
    author='Michel Roukine',
    author_email='rukin@users.sf.net',
    url='http://vinetto.sourceforge.net/',
    license='GNU GPL',
    platforms='LINUX',
)
