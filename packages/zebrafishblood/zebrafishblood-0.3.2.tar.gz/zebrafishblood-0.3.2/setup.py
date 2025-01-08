from setuptools import setup, find_packages

requirements = [
    'scikit-build','torch','torchvision','numpy',
    'ultralytics','opencv-python','openslide-python==1.3.1',
    # 'openslide-bin==4.0.0.2',
    'joblib'
]

setup(
    name='zebrafishblood',
    version='0.3.2',
    description='Zebrafish blood smear cell counter',
    long_description='For python>=3.8',
    author=['Eunhye Yang'],
    author_email='eunhye@connect.hku.hk',
    packages=find_packages(),
    install_requires=requirements
)