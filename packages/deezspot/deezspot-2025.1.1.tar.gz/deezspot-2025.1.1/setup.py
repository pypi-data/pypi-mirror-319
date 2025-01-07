from setuptools import setup

README = open("README.md", "r")
readmed = README.read()
README.close()

setup(
    name="deezspot",
    version="2025.01.01",
    description="Downloads songs, albums, episode or playlists from deezer and spotify with this packages! (clone from https://pypi.org/project/deezloader/)",
    long_description=readmed,
    long_description_content_type="text/markdown",
    license="GNU Affero General Public License v3",
    python_requires=">=3.10",
    author="farihdzakyy",
    author_email="farihmuhammad75@gmail.com",
    url="https://github.com/farihdzkyy/deezspot",
    packages=[
        "deezspot",
        "deezspot.models", 
        "deezspot.spotloader",
        "deezspot.deezloader", 
        "deezspot.libutils"
    ],
    install_requires=[
        "mutagen",
        "pycryptodome",
        "requests",
        "spotipy",
        "tqdm",
        "fastapi",
        "uvicorn[standard]",
        "spotipy-anon",
        "librespot"
    ],
    entry_points={
        'console_scripts': [
            'deez-dw=deezspot.bin.deez_dw:main',
            'deez-web=deezspot.bin.deez_web:main',
        ],
    }
)