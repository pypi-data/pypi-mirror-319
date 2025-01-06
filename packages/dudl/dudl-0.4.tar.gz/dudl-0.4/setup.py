from setuptools import find_packages, setup

setup(
    name='DUDL',
    version='0.4.0',    
    description='The DUDL Game',
    package_dir={"": "src"},
    url='https://github.com/v0rtex20k/DUDL/',
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": [
            "start-dudl=dudl_app:start_server",  # Adjust to match your structure
        ],
    },
)

