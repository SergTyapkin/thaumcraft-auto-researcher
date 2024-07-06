![GithubCI](https://github.com/SergTyapkin/thaumcraft-auto-researcher/actions/workflows/auto-translate-readme.yml/badge.svg)

[![](https://img.shields.io/badge/русский-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/russian.md)
[![](https://img.shields.io/badge/english-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/english.md)
[![](https://img.shields.io/badge/中文(简体)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/chinese%20(simplified).md)
[![](https://img.shields.io/badge/中文(传统)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/chinese%20(traditional).md)
[![](https://img.shields.io/badge/arabic(العربية)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/arabic.md)
[![](https://img.shields.io/badge/español-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/spanish.md)
[![](https://img.shields.io/badge/italiano-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/italian.md)
[![](https://img.shields.io/badge/Deutsch-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/dutch.md)
[![](https://img.shields.io/badge/hindi(हिन्दी)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/hindi.md)
[![](https://img.shields.io/badge/korean(한국어)-_?style=for-the-badge&logo=readme&color=white)](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/README_TRANSLATIONS/korean.md)


# Автоматический исследователь для Thaumcraft 4
> _**Thaumcraft**_ - мод для игры _Minecraft_, часто устанавливавауЂйся в магические сборки модов на популярных серверах

프로그램 **автоматически решает и раскладывает** записки исследований в столе исследований.
Весь интерфейс взаимодействия полупрозрачный 및 показывается поверх всех окон.

프로그램 **니카크**에는 코드에 대한 보안이 없으며 해독제도 없습니다. 
Все что она делает - это смотрит на **пиксели на экране**, и imiтирует **действия мышьк и клавиатурой**, как если бы это делал человек.

---

## [Releases](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases)
[latest version `v1.0.0`](https://github.com/SergTyapkin/thaumcraft-auto-researcher/releases/tag/v1.0.0)
<details>
<summary>변경 로그:</summary>

- Улучшено качество решения цепочек а 안경
- 측면 체인의 해상도가 ~2배 가속화되었습니다.
- 실행 파일 .exe 내의 .log 파일에 로깅을 추가했습니다.
- 닫기 버튼이 추가되었습니다.
</details>


질문, 오류 또는 제안 사항이 있는 경우 다음 주소로 편지를 보내주세요. [t.me/tyapkin_s](https://t.me/tyapkin_s)

## 작동 절차
### 초기 설정
1. 십자선이 움직일 수 있다는 시연 및 검증. 
빨간색 점을 노란색 점으로 옮기면 됩니다.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/enroll.png?raw=true)
2. 연구 테이블 인터페이스가 어디에 있는지 프로그램에 알려주어야 합니다. 
이렇게 하려면 아래 스크린샷에 표시된 것처럼 노란색 직사각형의 모서리가 테이블의 외부 둘레를 따라 이동하도록 이동해야 합니다.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/find_table.png?raw=true)
3. 마법 부여대 내부에서 상호 작용 버튼이 어디에 있는지 더 자세히 프로그램에 알려줄 필요가 있습니다.
이렇게 하려면 아래 스크린샷에 표시된 대로 모든 점을 이동하세요.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_controls.png?raw=true)
4. Thaumcraft 버전과 설치된 모든 애드온을 선택하세요.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_version_and_addons.png?raw=true) 

이러한 모든 작업을 수행한 후 모든 사용자 선택 사항이 저장됩니다.
다음에 프로그램을 시작할 때 이를 수행할 필요는 없습니다. 다음 단계가 즉시 표시됩니다.
'백스페이스' 키를 누르면 언제든지 구성으로 돌아갈 수 있습니다.

### 측면 체인 해결
1. 왼쪽 상단 인벤토리 슬롯에 있는 연구 노트가 자동으로 연구 테이블에 배치됩니다.
필드의 기존 측면을 클릭하고 측면 목록에서 선택합니다.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects.png?raw=true)
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects_1.png?raw=true)
2. 다른 모든 측면에 대해서도 동일하게 수행하고 다음이 포함된 모든 셀을 표시합니다.
측면을 배치할 수 없습니다(비어 있음). 아래 스크린샷과 유사하게 보일 것입니다.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects_2.png?raw=true)
3. 측면 체인이 너무 크거나 갖고 있지 않은 측면을 사용하는 경우 'R'을 눌러 다시 생성하세요.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/setup_table_aspects_3.png?raw=true)
4. 시작하기 전에 잉크 탱크에 잉크가 충분한지 확인하십시오. 부족하면 측면 배치 알고리즘이 중단됩니다.
그런 다음 `Enter`를 누르면 결과 체인에 따라 테이블에 측면을 배치하는 프로세스가 시작됩니다.
5. 면모 배치가 완료되면 연구 노트가 인벤토리에 배치됩니다.
그리고 그 대신에 인벤토리에서 다음이 배치됩니다.
프로세스를 다시 시작할 수 있습니다. 이렇게 하면 인벤토리에 쌓여 있는 수많은 노트를 차례로 해결할 수 있습니다.
![image](https://github.com/SergTyapkin/thaumcraft-auto-researcher/blob/master/README_images/solving_done.png?raw=true)


## 향후 버전에서는
- 신경망을 사용하여 테이블의 측면을 자동으로 감지합니다.
- 테이블에서 사용 가능한 측면과 수량을 자동으로 감지하고 이 정보를 기반으로 체인을 구축합니다.
- 소스 구성 편집
- 초기 측면 결정의 정확성 확인
- 배치된 체인의 정확성을 확인합니다.
- 더 많은 지원 버전 및 애드온
- 잉크 탱크 상태 추적
- 애플리케이션 내에서 다른 언어로 번역

---
## 소스에서 실행:
1. 종속성을 설치합니다.
```shell
pip install -r requirements.txt
```

2. 프로젝트 루트에서 실행합니다(`Python 3.10` 이상 필요).
```shell
python ./src/main.py
```