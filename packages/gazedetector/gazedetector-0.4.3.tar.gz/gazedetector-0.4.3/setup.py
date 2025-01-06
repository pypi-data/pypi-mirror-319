from setuptools import setup, find_packages

setup(
    name='gazedetector',
    version='0.4.3',  # Ensure the version number is updated
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-cors',
        'opencv-python',  # Use the regular version of OpenCV
    ],
    entry_points={
        'console_scripts': [
            'gazedetector = gazedetector.server:run_server',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
)
