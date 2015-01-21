#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
        name = "holepunch",
        version = "1.0.0",
        description = "P2P Communication Across NAT/Firewall Hole Punching Server",
        author = "Emmanouil Matsis",
        author_email = "emmanouilmatsis@gmail.com",
        url = "https://www.emmanouilmatsis.com",
        classifiers = [
            "Environment :: Console",
            "Programming Language :: Python :: 3.4.0",
            "Operating System :: OS Independent",
            "Intended Audience :: Software Developers",
            "Topic :: Networks and Distributed Systems",
            ],
        packages = [
            "holepunch"
            ],
        test_suite = "test",
        entry_points = {
            "console_scripts": [
                "holepunch = holepunch.__main__:main"
                ],
            },
        )
