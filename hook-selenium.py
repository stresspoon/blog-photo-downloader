"""
PyInstaller hook for selenium package
selenium의 모든 모듈을 강제로 포함시키는 hook 파일
"""

from PyInstaller.utils.hooks import collect_all, collect_submodules

# selenium 관련 모든 모듈 수집
datas, binaries, hiddenimports = collect_all('selenium')

# 추가로 누락될 수 있는 모듈들 명시적 포함
additional_imports = [
    'selenium',
    'selenium.webdriver',
    'selenium.webdriver.chrome',
    'selenium.webdriver.chrome.webdriver',
    'selenium.webdriver.chrome.service',
    'selenium.webdriver.chrome.options',
    'selenium.webdriver.chromium',
    'selenium.webdriver.chromium.webdriver',
    'selenium.webdriver.chromium.service',
    'selenium.webdriver.chromium.options',
    'selenium.webdriver.common',
    'selenium.webdriver.common.by',
    'selenium.webdriver.common.keys',
    'selenium.webdriver.common.options',
    'selenium.webdriver.common.service',
    'selenium.webdriver.common.utils',
    'selenium.webdriver.remote',
    'selenium.webdriver.remote.webdriver',
    'selenium.webdriver.support',
    'selenium.common',
    'selenium.common.exceptions',
]

# 기존 hiddenimports에 추가
hiddenimports.extend(additional_imports)

# selenium 하위 모듈 모두 수집
hiddenimports.extend(collect_submodules('selenium.webdriver'))
hiddenimports.extend(collect_submodules('selenium.common'))
hiddenimports.extend(collect_submodules('selenium.webdriver.chrome'))
hiddenimports.extend(collect_submodules('selenium.webdriver.chromium'))
hiddenimports.extend(collect_submodules('selenium.webdriver.common'))
hiddenimports.extend(collect_submodules('selenium.webdriver.remote'))
hiddenimports.extend(collect_submodules('selenium.webdriver.support'))

# 중복 제거
hiddenimports = list(set(hiddenimports)) 