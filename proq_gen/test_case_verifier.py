
from .generators.test_case import get_test_case_chain
import json
def verify_testcases(problems, db_store, id_docs):
    for i in range(len(problems['ids'])):
        problem = db_store.get(id_docs[i]["document_id"])
        question = problem['documents'][0]
        solution = problem['metadatas'][0]['solution']
        test_case_chain = get_test_case_chain(
        lang="Python",
        n_testcases=4
    )


        result = test_case_chain.invoke({"problem_statement":question, "solution":solution})
        test_case_json = json.dumps(result, indent=2)
        # testcases = json.loads(problem["metadatas"][0]['testcases'])

        suffix = """
        import sys
        exec(sys.stdin.read())
        """
        with open("test.py", "w") as f:
            f.write(solution+suffix)

        import subprocess
        for testcase in result:
            output  = subprocess.run(["python", "test.py"], input=testcase["input"],text=True,capture_output=True).stdout.strip()
            if output != testcase['output']:
                testcase['output'] = output
            # print(output, testcase["output"])
        id_docs[i]["document"].metadata["testcasetype"] = "function"
        id_docs[i]["document"].metadata["testcases"] = test_case_json
        db_store.update_document(**id_docs[i])
    return db_store
        