import json

def initialize_file(input_filename):
    with open(input_filename, 'w', encoding='utf8') as file:
        pass  # 파일을 열고 즉시 닫아서 내용을 초기화

def reset_indexes_in_json_file(input_filename, output_filename, input_encoding='utf8', output_encoding='utf8'):
    # 입력 파일을 열고 JSON 데이터를 읽습니다.
    with open(input_filename, 'r', encoding=input_encoding) as file:
        data = [json.loads(line) for line in file]

    # index 값을 재설정합니다.
    for i, item in enumerate(data, start=1):
        item['index'] = i

    # 결과를 출력 파일에 저장합니다.
    with open(output_filename, 'w', encoding=output_encoding) as file:
        for item in data:
            json.dump(item, file, ensure_ascii=False)
            file.write('\n')  # 각 객체를 새로운 줄에 저장

def load_processed_data(filename, encoding='utf8'):
    with open(filename, 'r', encoding=encoding) as file:
        data = [json.loads(line) for line in file]
    return data

# 테스트 코드 (실제 사용 시 주석 처리하거나 삭제)
if __name__ == "__main__":
    initialize_file('processed_data.json')
    reset_indexes_in_json_file('processed_data.json', 'reset_index_data.json')
    with open('reset_index_data.json', 'r', encoding='utf8') as file:
        for line in file:
            print(json.loads(line))
