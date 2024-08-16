import json
import rule_set
from json_process import load_processed_data



# 예측 문장을 생성하는 함수
def generate_prediction(data):
    predictions = []

    # target에 대한 설명 딕셔너리
    target_descriptions = {
        '_self': '현재 창에서 링크를 엽니다.',
        '_blank': '새 창에서 링크를 엽니다.',
        '_parent': '부모 프레임에서 링크를 엽니다.',
        '_top': '전체 창에서 링크를 엽니다.'
    }
    rel_descriptions = {
        'noopener': '새 창이 원본 창에 대한 참조를 가질 수 없게 합니다.',
        'noreferrer': 'HTTP Referer 헤더가 전송되지 않게 합니다.',
        'nofollow': '검색 엔진에게 이 링크를 따르지 말라고 지시합니다.',
        'noopener noreferrer': '새 창이 원본 창에 대한 참조를 가지지 않으며, HTTP Referer 헤더도 전송되지 않게 합니다.'
    }
    for item in data:
        tag = item.get('tag')
        xPath = item.get('xPath')
        href = item.get('href')
        role = item.get('role')
        result = item.get('result')

        # target 값을 추출
        target_value = result.split(',')[0].split(': ')[1]

        # rel 값을 추출
        rel_value = result.split(',')[1].split(': ')[1]

        # 예측 문장 생성
        result_description = f"해당 링크는 '{role}'의 역할, 클릭 시 이동할 URL은 '{href}'이며, "
        result_description += target_descriptions.get(target_value, '알 수 없는 target 값입니다.')
        result_description += f" '{rel_descriptions.get(rel_value, '기본 동작으로 rel을 설정하지 않습니다.')}"

        prediction = {
            'Type': 'Hyperlink Click',
            'Tag': tag,
            'Target': f'XPath: {xPath}',
            'Input': 'None',
            'Result': result_description
        }

        predictions.append(prediction)

    return predictions


# 예시: JSON 파일에서 데이터를 읽고 예측 문장을 생성
filename = 'reset_a_data.json'
data = load_processed_data(filename, encoding='utf8')
predictions = generate_prediction(data)

# 예측 문장을 파일로 저장
output_filename = 'a_output.json'
with open(output_filename, 'w', encoding='utf8') as outfile:
    for prediction in predictions:
        outfile.write(json.dumps(prediction, ensure_ascii=False) + '\n')

# 예: 파일에서 처리된 데이터를 읽어 출력
with open(output_filename, 'r', encoding='utf8') as file:
    for line in file:
        print(json.loads(line))
