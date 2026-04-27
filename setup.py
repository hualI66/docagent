from setuptools import setup, find_packages

setup(
    name="docagent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask>=3.0.0",
        "langchain>=0.1.0",
        "langchain-openai>=0.0.5",
        "werkzeug>=3.0.0",
        "pyppeteer>=1.0.0",
        "reportlab>=4.0.0",
    ],
)
