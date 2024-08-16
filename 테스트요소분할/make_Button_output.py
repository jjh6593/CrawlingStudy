import json
import rule_set
from json_process import load_processed_data


# 예측 문장을 생성하는 함수
def generate_prediction(data):
    predictions = []
    for item in data:
        tag = item.get('tag')
        xPath = item.get('xPath')
        input_value = item.get('value')
        role = item.get('role')
        disabled = item.get('disabled')
        btn_form = item.get('btn_form')

        # 예측 문장 생성
        result = f"해당 버튼은 '{role}'의 역할, "
        if disabled:
            result += "클릭할 수 없는 상태"
        else:
            result += "클릭할 수 있는 상태"
        if input_value:  # input_value가 None이 아니고 빈 문자열이 아닐 때
            result += f", '{input_value}' 값을 서버로 전송"
        if btn_form:
            result += f", '{btn_form}'과 관련된 행동을 해야함"
        result += "."

        prediction = {
            'Type': 'Button Click',
            'Tag': tag,
            'Target': f'XPath: {xPath}',
            'Input': input_value if input_value else "None",
            'Result': result
        }

        predictions.append(prediction)

    return predictions

# 예시: JSON 파일에서 데이터를 읽고 예측 문장을 생성
filename = 'reset_button_data.json'
data = load_processed_data(filename, encoding='utf8')  # utf8로 인코딩 명시
predictions = generate_prediction(data)

# 예측 문장을 파일로 저장
output_filename = 'button_output.json'
with open(output_filename, 'w', encoding='utf8') as outfile:
    for prediction in predictions:
        outfile.write(json.dumps(prediction, ensure_ascii=False) + '\n')

# 예: 파일에서 처리된 데이터를 읽어 출력
with open(output_filename, 'r', encoding='utf8') as file:
    for line in file:
        print(json.loads(line))
