from durable.lang import *

with ruleset('web_test'):

    # Button 태그 테스트
    @when_all((m.tag == 'button') & (m.text != None))
    def button_test(c):
        print(f'Button 테스트: 텍스트 "{c.m.text}"를 포함하는 버튼이 있습니다.')

    # Form 태그 테스트
    @when_all((m.tag == 'form') & (m.action != None))
    def form_test(c):
        print(f'Form 테스트: action 속성이 "{c.m.action}"인 폼이 있습니다.')

    # A 태그 (링크) 테스트
    @when_all((m.tag == 'a') & (m.href != None))
    def link_test(c):
        print(f'Link 테스트: href 속성이 "{c.m.href}"인 링크가 있습니다.')

# 테스트 케이스 예시
assert_fact('web_test', {'tag': 'button', 'text': '클릭하세요'})
assert_fact('web_test', {'tag': 'form', 'action': '/submit'})
assert_fact('web_test', {'tag': 'a', 'href': 'https://example.com'})