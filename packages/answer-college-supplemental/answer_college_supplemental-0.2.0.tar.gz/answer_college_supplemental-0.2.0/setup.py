from setuptools import setup, find_packages

setup(
    name="answer_college_supplemental",
    version="0.2.0",
    description="A CLI tool for gaining inspiration for college supplementals. Do NOT submit these generated essays to colleges.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Vishy Gopal",
    author_email="vishy1290@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "answer-college-supplemental=answer_college_supplemental.main:main",
        ],
    },
)
