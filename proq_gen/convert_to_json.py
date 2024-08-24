import json

def data_to_json(questions):
    questions_json = []

    for doc in questions:
        question_obj = {
            "question": doc.page_content,
            "question_template" : doc.metadata.get("question_template"),
            "data_formats": doc.metadata.get("data_formats", ""),
            # "solution": doc.metadata.get("solution", ""),
            "tags": doc.metadata.get("tags", ""),
            "testcases": json.loads(doc.metadata.get("testcases", "[]")),
            "testcasetype": doc.metadata.get("testcasetype", "")
            
        }
        questions_json.append(question_obj)

    # Convert the list to a JSON string
    json_output = json.dumps(questions_json, indent=2)

    return json_output