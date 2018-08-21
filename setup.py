import setuptools

setuptools.setup(
    name="helper_kits",
    version="1.0.0",
    author="Kauê Mendes",
    author_email="kauemendes@kauemendes.com",
    description="Canivete Suiço Python based on Flask",
    long_description="Pacotes para ajudar algu",
    long_description_content_type="text/markdown",
    url="https://github.com/kauemendes/helper_kits",
    install_requires=[
          'flask', 'flask_sqlalchemy', 'itsdangerous', 'Crypto', 'boto3', 'libmagic', 'pymysql'
      ]
)