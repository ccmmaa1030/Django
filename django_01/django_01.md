# Django_01



## Django 개발 환경 설정 가이드

- 가상환경 생성/실행

  - 위치 이동

  ```bash
  $ cd ~
  ```

  - 파일 생성

  ```bash
  $ cd 파일이름/
  $ cd server/
  ```

  - 가상환경 생성

  ```bash
  $ python -m venv 가상환경이름
  $ python -m venv server-venv
  ```

  - 생성 확인

  ```bash
  $ ls
  ```

  - 가상환경 실행

  ```bash
  $ source 가상환경이름/Scripts/activate
  $ source server-venv/Scripts/activate
  ```

  - 가상환경 종료

  ```bash
  $ deactivate
  ```

- Django LTS 버전 설치

  - LTS 설치

  ```bash
  $ pip install django==3.2.13
  ```

  - 설치 확인

  ```bash
  $ pip list
  ```

- Django 프로젝트 생성

  - 프로젝트 생성

  ```bash
  $ django-admin startproject 프로젝트이름 시작경로
  $ django-admin startproject serverpjt .
  ```

  - 생성 확인

  ```bash
  $ ls
  ```

  - VS code 실행

  ```bash
  $ code .
  ```

- Django 실행

  - 실행

  ```bash
  $ python manage.py runserver
  ```

  - web에서 확인

  ```http
  http://localhost:8000/
  ```

  - 종료

  ```bash
  ctrl + c 눌러서 종료
  ```




## 서버 기초

- Q. IP와 도메인은 무엇일까요?

  > https://developer.mozilla.org/ko/docs/Learn/Common_questions/How_does_the_Internet_work

  - 네트워크에 연결된 모든 컴퓨터에는 인터넷 프로토콜을 나타내는 고유한 주소인 IP 주소를 가지고 있다. IP 주소는 점으로 구분 된 네 개의 숫자로 구성된다. 이러한 주소를 이용해서 다른 컴퓨터를 찾을 수 있다.
  -  IP 주소는 기억하기 어렵고 시간이 지나면서 변경될 수 있기 때문에 IP 주소에 도메인 이름을 지정한다. 웹 브라우저에서 웹을 탐색 할 때 일반적으로 도메인 이름을 사용하여 웹 사이트에 접속할 수 있다. (ex. `173.194.121.32` -> `'google.com'`) 



- Q. 클라이언트와 서버는 무엇일까요?

  > https://developer.mozilla.org/ko/docs/Learn/Getting_started_with_the_web/How_the_Web_works
  >
  > https://developer.mozilla.org/ko/docs/Learn/Common_questions/What_is_a_web_server

  - 클라이언트는 다른 프로그램에게 서비스를 요청하는 프로그램이다. 일반적인 웹 사용자의 인터넷이 연결된 장치들과 이런 장치들에서 이용가능한 웹에 접근하는 소프트웨어를 말한다.
  - 서버는 웹페이지, 사이트, 또는 앱을 저장하는 컴퓨터이다. 클라이언트의 장비가 웹페이지에 접근하길 원할 때, 서버로부터 클라이언트의 장치로 사용자의 웹 브라우저에서 보여지기 위한 웹페이지의 사본이 다운로드 된다.



- Q. 정적 웹 사이트와 동적 웹 사이트의 차이점은 무엇일까요? Django는 무엇을 위한 도구인가요?

  > https://developer.mozilla.org/ko/docs/Learn/Server-side/First_steps/Introduction

  - 정적 웹 사이트는 특별한 리소스 요청이 들어올 때 서버에서 하드 코딩된 동일한 콘텐츠를 반환한다. 서버에 미리 저장된 HTML 파일 그대로 내용이 변하지 않고 모든 사용자에게 동일한 정보를 표시한다. 사용자가 페이지를 탐색하거나, 브라우저가 지정된 URL에 HTTP "GET" 요청을 보낼 때 서버는 파일 시스템에서 요청한 문서를 검색하고 문서와 HTTP 응답을 반환한다.
  - 동적 웹 사이트는 필요할 때 동적으로 응답 콘텐츠가 생성된다. 보통 HTML 템플릿에 있는 자리 표시자에 데이터베이스에서 가져온 데이터를 넣어 생성된다. 사용자 또는 지정된 환경을 기반으로 URL에 대해 다른 데이터를 반환 할 수 있으며, 응답을 반환하는 과정에서 다른 작업을 수행할 수 있다. 
  - Django는 파이썬으로 작성된 오픈 소스 서버-사이드 웹 프레임워크로, MTV(Model-Templete-View) 패턴을 따르고 있다. 데이터베이스 기반 웹사이트를 작성하는 데 있어서 컴포넌트의 재사용성과 플러그인화 가능성 향상, 빠른 개발을 위해 사용된다.



- Q. HTTP는 무엇이고 요청과 응답 메시지 구성은 어떻게 되나요?

  > https://developer.mozilla.org/ko/docs/Web/HTTP/Overview

  - HTTP는 웹에서 이루어지는 모든 데이터 교환의 기초이며, HTML 문서와 같은 리소스들을 가져올 수 있도록 하는 클라이언트-서버 프로토콜이다. 클라이언트-서버 프로토콜은 수신자 측에 의해 요청이 초기화되는 프로토콜을 의미한다. HTTP는 사용이 쉬운 확장 가능한 프로토콜로 헤더를 쉽게 추가할 수 있는 클라이언트-서버 구조이다.
  - 클라이언트에 의해 전송되는 메시지를 요청이라고 하며, 이에 대한 서버로부터 전송되는 메시지를 응답이라고 한다. 요청은 하나의 개체, 사용자 에이전트 또는 프록시에 의해 전송된다. 각각의 개별적인 요청들은  서버로 보내지며, 서버는 요청을 처리하고 응답을 제공한다. 
  - 요청은 HTTP 메서드, 가져오려는 리소스 경로, HTTP 프로토콜 버전, 서버에 대한 추가 정보를 전달하는 선택적 헤더, 선택적인 전송된 리소스를 포함하는 응답의 본문과 유사한 본문으로 구성된다.
  - 응답은 HTTP 프로토콜 버전, 요청의 성공 여부와 이유를 나타내는 상태코드, 상태 메시지, HTTP 헤더, 선택적인 가져온 리소스가 포함되는 본문으로 구성된다.



- Q. 프레임워크는 무엇일까요?(외부 자료 조사)
  - 서비스 개발에 필요한 기능들을 미리 구현해서 모아 놓은 것을 프레임워크라고 한다. 특정 프로그램을 개발하기 위한 여러 도구들과 규약을 제공하기 때문에 프레임워크를 잘 사용하면 웹 서비스 개발에 있어서 모든 것들을 직접 개발할 필요가 없어 소프트웨어의 생산성과 품질을 높일 수 있다.
  - 웹 프레임워크는 웹 서비스 개발을 위한 프레임워크로 웹 개발 작업을 단순화 하는 도구와 라이브러리를 제공한다. Django는 파이썬으로 작성된 프레임워크의 한 종류이다.