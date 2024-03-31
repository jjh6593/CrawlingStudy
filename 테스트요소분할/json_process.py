import json

def initialize_file(input_filename):
    with open(input_filename, 'w') as file:
        pass  # 파일을 열고 즉시 닫아서 내용을 초기화

def reset_indexes_in_json_file(input_filename, output_filename):
    # 입력 파일을 열고 JSON 데이터를 읽습니다.
    with open(input_filename, 'r') as file:
        data = [json.loads(line) for line in file]

    # index 값을 재설정합니다.
    for i, item in enumerate(data, start=1):
        item['index'] = i

    # 결과를 출력 파일에 저장합니다.
    with open(output_filename, 'w') as file:
        for item in data:
            json.dump(item, file)
            file.write('\n')  # 각 객체를 새로운 줄에 저장

# 함수를 호출하여 index를 재설정하고 결과를 저장합니다.
reset_indexes_in_json_file('processed_data.json', 'reset_index_data.json')
# 예: 파일에서 처리된 데이터를 읽어 출력
with open('reset_index_data.json', 'r') as file:
    for line in file:
        print(json.loads(line))