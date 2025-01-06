import setuptools

setuptools.setup(
    name="pyCDM4F",
    version="0.0.3",
    license='MIT',
    author="Songwon Kim",
    author_email="kimsongwon10@korea.ac.kr",
    description="Package for Predicting Plant Phenology with ChillDay-Model(CDM), which has Parameter Examination, Visualization, Clustering and so on... with Phenology & Meteorological Data.",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/CSBL-urap/2024-summer-swkim",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)
