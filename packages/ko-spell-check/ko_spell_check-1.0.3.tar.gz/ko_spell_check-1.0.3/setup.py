from setuptools import setup, find_packages

setup(
    name="ko-spell-check",  # PyPI에 등록할 패키지 이름
    version="1.0.3",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python package for Korean spell checking using Naver API",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ko-spell-check",  # GitHub URL
    packages=find_packages(exclude=["tests*"]),  # 테스트 폴더 제외
    install_requires=["requests"],  # 의존 패키지
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"kospellcheck": "kospellcheck"},  # import 시 사용할 이름
)
