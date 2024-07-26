import json
import rule_set
from json_process import load_processed_data


# 예측 문장을 생성하는 함수
def generate_prediction(data):
    target_info = {
        "_blank": "새 창이나 탭에서 열립니다.",
        "_self": "같은 프레임이나 창에서 열립니다.",
        "_parent": "부모 프레임에서 열립니다.",
        "_top": "전체 창에서 열립니다."
    }

    rel_info = {
        "alternate": "대체 버전 링크",
        "author": "저자 링크",
        "bookmark": "북마크",
        "external": "외부 링크",
        "help": "도움말 링크",
        "license": "라이선스 링크",
        "next": "다음 문서",
        "nofollow": "링크 따라가지 않음",
        "noreferrer": "referrer 정보 전송하지 않음",
        "noopener": "새 창에서 열리지만 opener 속성 없음",
        "prev": "이전 문서",
        "search": "검색 링크",
        "tag": "태그 링크"
    }

    predictions = []
    for item in data:
        tag = item.get('tag')
        xPath = item.get('xPath')
        href = item.get('href', 'None')
        text = item.get('text', 'None')
        role = item.get('role')
        target = item.get('target', '_self')
        rel = item.get('rel', '기본 동작')
        download = item.get('download', '0')

        # 예측 문장 생성
        target_desc = target_info.get(target, "알 수 없음")
        rel_desc = rel_info.get(rel, "기본 동작")

        result = f"해당 링크는 '{role}' 역할을 하며, target은 '{target_desc}', rel은 '{rel_desc}'입니다."

        prediction = {
            'Type': 'Link Click',
            'Tag': tag,
            'Target': f'XPath: {xPath}',
            'Input': href,
            'Result': result
        }

        predictions.append(prediction)

    return predictions


# 예시: JSON 파일에서 데이터를 읽고 예측 문장을 생성
filename = 'reset_a_data.json'
data = load_processed_data(filename, encoding='utf8')  # utf8로 인코딩 명시
predictions = generate_prediction(data)

# 예측 문장을 파일로 저장
output_filename = 'link_output.json'
with open(output_filename, 'w', encoding='utf8') as outfile:
    for prediction in predictions:
        outfile.write(json.dumps(prediction, ensure_ascii=False) + '\n')

# 예: 파일에서 처리된 데이터를 읽어 출력
with open(output_filename, 'r', encoding='utf8') as file:
    for line in file:
        print(json.loads(line))