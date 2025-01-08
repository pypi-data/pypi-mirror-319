from setuptools import setup, find_packages

requirements = [
    'scikit-build','torch','torchvision','numpy',
    'ultralytics','opencv-python','openslide-python',
    'joblib'
]
    # 'openslide-bin',

setup(
    name='zebrafishblood',
    version='0.3.1',
    description='Zebrafish blood smear cell counter',
    long_description='For python>=3.8',
    author=['Eunhye Yang'],
    author_email='eunhye@connect.hku.hk',
    packages=find_packages(),
    install_requires=requirements
)