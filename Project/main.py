from QuestionGenerator import PythonQuestionGenerator

generator = PythonQuestionGenerator()
generator.set_theme_and_topic("tamil movies", "basic functions")
generator.generate_problem()
print(generator.get_json_result())