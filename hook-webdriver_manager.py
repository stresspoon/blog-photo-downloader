"""
PyInstaller hook for webdriver_manager package
webdriver_manager의 모든 모듈을 강제로 포함시키는 hook 파일
"""

from PyInstaller.utils.hooks import collect_all, collect_submodules

# webdriver_manager 관련 모든 모듈 수집
datas, binaries, hiddenimports = collect_all('webdriver_manager')

# 추가로 누락될 수 있는 모듈들 명시적 포함
additional_imports = [
    'webdriver_manager',
    'webdriver_manager.chrome',
    'webdriver_manager.core',
    'webdriver_manager.core.utils',
    'webdriver_manager.core.download_manager',
    'webdriver_manager.core.driver_cache',
    'webdriver_manager.core.config_manager',
    'webdriver_manager.driver',
    'webdriver_manager.utils',
    'webdriver_manager.firefox',
    'webdriver_manager.microsoft',
    'webdriver_manager.opera',
]

# 기존 hiddenimports에 추가
hiddenimports.extend(additional_imports)

# webdriver_manager 하위 모듈 모두 수집
hiddenimports.extend(collect_submodules('webdriver_manager'))

# 중복 제거
hiddenimports = list(set(hiddenimports)) 