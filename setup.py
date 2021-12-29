import os
import setuptools

print('this is in [setup] module###############')
os.system('pwd')
os.system('ls')
print('this is in [setup] module###############')
try:
    os.makedirs('./TaichiGAME/packaged-examples')
except FileExistsError:
    pass

os.system('ls ./TaichiGAME/packaged-examples')
os.system("echo 'hello!!!!!!!!!' ")
os.system('cp ./examples/testbed.py ./TaichiGAME/packaged-examples/')
os.system('cp ./examples/ti_testbed.py ./TaichiGAME/packaged-examples/')
os.system('ls ./TaichiGAME/packaged-examples')

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TaichiGAME",
    version="0.0.1",
    author="maksyuki",
    author_email="maksyuki@126.com",
    description="GPU Accelerated Motion Engine based on Taichi Lang",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maksyuki/TaichiGAME",
    project_urls={
        'Documentation': 'https://github.com/maksyuki/TaichiGAME',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/maksyuki/TaichiGAME',
        'Tracker': 'https://github.com/maksyuki/TaichiGAME/issues',
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License', 'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Framework :: Robot Framework :: Library',
        'Topic :: Games/Entertainment :: Simulation',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
    license='MIT',
    keywords=['phyics engine', 'dynamics simulation', 'robot motion control'],
    packages=setuptools.find_packages(exclude=['examples', 'tests']),
    include_package_data=True,
    package_data={'examples': ['testbed.py']},
    install_requires=['taichi'],
    python_requires=">=3.7,<3.10",
)
