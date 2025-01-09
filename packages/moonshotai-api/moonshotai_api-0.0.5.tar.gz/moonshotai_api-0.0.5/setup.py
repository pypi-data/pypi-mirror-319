from setuptools import setup

setup(
    name='moonshotai_api',
    packages=[
        'MoonshotAI_Api',
        'MoonshotAI_Api.utils'
    ],
    version='0.0.5',
    description='LTV API SDK',
    author='Tomer Efr',
    install_requires=[
        "requests==2.31.0"
    ],
    zip_safe=False,
    license='MIT',
    classifiers=[],
    package_data={'': ['LICENSE', 'README.md']}
)
