import json
file_name = r"D:\temp\data\c3\d-dev.json"


def uniform(file):
    with open(file, "r", encoding="utf-8") as f:
        examples = json.load(f)
        print(len(examples))
        print(examples[0])
        for example in examples:
            if len(example) != 3:
                print("length of example not equal 3: -------------------", example)
            if len(example[1]) > 1:
                print("question numbers greater than 1: -----------------", example)

if __name__ == "__main__":
    uniform(file_name)