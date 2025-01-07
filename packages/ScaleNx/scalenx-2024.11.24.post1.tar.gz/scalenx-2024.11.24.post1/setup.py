import setuptools

with open("README.md") as file:
    read_me_md = file.read()

setuptools.setup(
    name="ScaleNx",
    version="2024.11.24.post1",
    author="Ilya Razmanov",
    author_email="ilyarazmanov@gmail.com",
    description="Image resizing using Scale2x and Scale3x algorithms, in pure Python.",
    long_description=read_me_md,
    long_description_content_type="text/markdown",
    url="https://github.com/Dnyarri/PixelArtScaling",
    py_modules=['scalenx'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    keywords=[
        'scale2x',
        'scale3x',
        'pixel',
        'resize',
        'rescale',
        'image',
        'bitmap',
        'python'
    ],
    python_requires='>=3.10',
)
