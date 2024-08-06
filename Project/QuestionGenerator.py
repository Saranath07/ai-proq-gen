import json
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_groq import ChatGroq
import os

with open("apiKeys.json", "r", encoding='utf-8') as f:
    apiKeys = json.load(f)





os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = apiKeys['LANGCHAIN_API_KEY']
os.environ["GROQ_API_KEY"] = apiKeys['GROQ_API_KEY']

class PythonQuestionGenerator:
    def __init__(self, model_name="llama-3.1-70b-versatile", temperature=1, max_tokens=1024):
        self.model = ChatGroq(model=model_name, temperature=temperature, max_tokens=max_tokens)
        self.theme = ""
        self.topic = ""
        self.result = {}

    def set_theme_and_topic(self, theme, topic):
        self.theme = theme
        self.topic = topic

    def generate_problem_name(self):
        messages = [
            SystemMessage(content="Give a name for a python programming question based on the theme and the topic. JUST OUTPUT THE TITLE AND NOTHING ELSE"),
            HumanMessage(content=f"topic : cricket, theme : functions"),
            AIMessage(content="Scores of the batsman in his two innings"),
            HumanMessage(content=f"topic : {self.topic}, theme : {self.theme}")
        ]
        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | self.model | StrOutputParser()
        self.result['problem_name'] = chain.invoke({})

    def generate_description(self):
        messages = [
            SystemMessage(content="Give a proper 5 to 10 line paragraph description for the problem title. JUST GIVE THE PROBLEM DESCRIPTION WITHOUT ANY OTHER MESSAGES"),
            HumanMessage(content=f"topic : cricket, theme : functions, problem_statement : Scores of the batsman in his two innings"),
            AIMessage(content="""Write a Python program that defines a function to calculate and display the total and average score of a batsman in two innings. The function should take the scores of the two innings as parameters.
            Define a function named calculate_scores that takes two parameters: score_innings1 and score_innings2.
            The function should print the total and average scores.
            
            Example Output:
            Enter the score of the batsman in the first innings: 45
            Enter the score of the batsman in the second innings: 67
            Total score of the batsman: 112
            Average score of the batsman: 56.0
            Hints:
            Use the input() function to get user input.
            Use int() to convert the input from string to an integer.
                                    """),
            HumanMessage(content=f"topic : {self.topic}, theme : {self.theme}, problem_statement : {self.result['problem_name']}")
        ]
        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | self.model | StrOutputParser()
        self.result['description'] = chain.invoke({})

    def generate_function_info(self):
        messages = [
            SystemMessage(content="Give a function name and parameters for the following problem statement and description. JUST OUTPUT A SINGLE JSON WITHOUT ANY OTHER SENTANCES"),
            HumanMessage(content=f"""topic : cricket, theme : functions, problem_statement : Scores of the batsman in his two innings, description : A batsman has scored runs in two innings of a cricket match. Write a Python program that:
                                    1. Prompts the user to enter the scores of the batsman in the first and second innings.
                                    2. Calculates the total score by adding the scores of both innings.
                                    3. Calculates the average score by dividing the total score by 2.
                                    4. Displays the total and average scores.
                                    Example Output:
                                    Enter the score of the batsman in the first innings: 45
                                    Enter the score of the batsman in the second innings: 67
                                    Total score of the batsman: 112
                                    Average score of the batsman: 56.0
                                    
                                    Hint:
                                    You can use the input() function to get user input.
                                    Use int() to convert the input from string to an integer.
                                    Use basic arithmetic operations to calculate the total and average scores."""),
            AIMessage(content='{"function_name" : "compute_total_score", "parameters" : ["score1", "score2"]}'),
            HumanMessage(content=f"topic : {self.topic}, theme : {self.theme}, problem_statement : {self.result['problem_name']}, description : {self.result['description']}")
        ]
        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | self.model | JsonOutputParser()
        self.result['function_info'] = chain.invoke({})

    def generate_function_template(self):
        messages = [
            SystemMessage(content="Give a function name and parameters, give the function template. JUST GIVE THE TEMPLATE AND NO OTHER SENTANCES"),
            HumanMessage(content=f"function_name : compute_total_score, parameters : [score1, score2]"),
            AIMessage(content="def compute_total_score(score1, score2):\\n # Write your code here\\n return"),
            HumanMessage(content=f"function_name : {self.result['function_info']['function_name']}, parameters : {self.result['function_info']['parameters']}")
        ]
        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | self.model | StrOutputParser()
        self.result['function_template'] = chain.invoke({})

    def generate_input_output_description(self):
        messages = [
            SystemMessage(content="Give only explainaton for one of the input output sample. It should be just a small description in 5 to 10 lines. NO CODE TO BE PROVIDED."),
            HumanMessage(content=f"""function_name : compute_total_score, parameters : [score1, score2], description :
            Write a Python program that defines a function to calculate and display the total and average score of a batsman in two innings. The function should take the scores of the two innings as parameters.
            Define a function named calculate_scores that takes two parameters: score_innings1 and score_innings2.
            The function should print the total and average scores.
            Example Output:
            Enter the score of the batsman in the first innings: 45
            Enter the score of the batsman in the second innings: 67
            Total score of the batsman: 112
            Average score of the batsman: 56.0
            Hints:
            Use the input() function to get user input.
            Use int() to convert the input from string to an integer."""),
            AIMessage(content="""
        Input :
        Enter the score of the batsman in the first innings: 45
        Enter the score of the batsman in the second innings: 67
        Output:
        Total score of the batsman: 112
        Average score of the batsman: 56.0
        Explanation:
        The program first prompts the user to enter the score for the first innings. In this case, the user enters 45.
        Then, it prompts for the score of the second innings. The user enters 67.
        The calculate_scores function takes these two scores as parameters.
        Inside the function:
        It calculates the total score by adding the two innings scores: 45 + 67 = 112
        It calculates the average score by dividing the total by 2 (since there are two innings): 112 / 2 = 56.0
        The function then prints the results:
        The total score (112)
        The average score (56.0)
        The average is displayed with a decimal point to show that it's a floating-point number, which allows for more precise averages in cases where the total isn't evenly divisible by 2."""),
            HumanMessage(content=f"function_name : {self.result['function_info']['function_name']}, parameters : {self.result['function_info']['parameters']}, description : {self.result['description']}")
        ]
        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | self.model | StrOutputParser()
        self.result['input_output_description'] = chain.invoke({})

    def generate_input_output_pairs(self):
        messages = [
            SystemMessage(content="Give a minimum of 4 INPUT OUTPUT Pairs for the given problem statement and description. OUTPUT ONLY JSON PARSABLE OBJECT WITHOUT ANY OTHER STATEMENTS"),
            HumanMessage(content=f"""problem_statement : Scores of the batsman in his two innings, description : Write a Python function that calculates the total score of a batsman across two innings. The function should take two arguments representing the scores of the batsman in the two innings and return the total score
            input_output_description :
        Input :
        Enter the score of the batsman in the first innings: 45
        Enter the score of the batsman in the second innings: 67
        Output:
        Total score of the batsman: 112
        Average score of the batsman: 56.0
        Explanation:
        The program first prompts the user to enter the score for the first innings. In this case, the user enters 45.
        Then, it prompts for the score of the second innings. The user enters 67.
        The calculate_scores function takes these two scores as parameters.
        Inside the function:
        It calculates the total score by adding the two innings scores: 45 + 67 = 112
        It calculates the average score by dividing the total by 2 (since there are two innings): 112 / 2 = 56.0
        The function then prints the results:
        The total score (112)
        The average score (56.0)
        The average is displayed with a decimal point to show that it's a floating-point number, which allows for more precise averages in cases where the total isn't evenly divisible by 2."""),
            AIMessage(content='[{"input" : [10, 20], "output" : 30}, {"input" : [15, 89], "output" : 104}]'),
            HumanMessage(content=f"problem_statement : {self.result['problem_name']}, description : {self.result['description']}, input_output_description : {self.result['input_output_description']}")
        ]
        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | self.model | JsonOutputParser()
        self.result['input_output_pairs'] = chain.invoke({})

    def generate_solution(self):
        messages = [
            SystemMessage(content="Generate a neat python solution with appropriate variable names and comments which can make the students understand the solution. JUST OUTPUT THE PYTHON CODE AND NO EXTRA SENTANCES. USE SIMPLE IN_BUILT FUNCTIONS OR AVOID IT UNLESS SPECIFIED."),
            HumanMessage(content=f"""problem_statement : Scores of the batsman in his two innings, description : Write a Python function that calculates the total score of a batsman across two innings. The function should take two arguments representing the scores of the batsman in the two innings and return the total score
            function_template : def compute_total_score(score1, score2):\\n # Write your code here\\n return
            input_output_description :
        Input :
        Enter the score of the batsman in the first innings: 45
        Enter the score of the batsman in the second innings: 67
        Output:
        Total score of the batsman: 112
        Average score of the batsman: 56.0
        
        Explanation:
        
        The program first prompts the user to enter the score for the first innings. In this case, the user enters 45.
        Then, it prompts for the score of the second innings. The user enters 67.
        The calculate_scores function takes these two scores as parameters.
        Inside the function:
        
        It calculates the total score by adding the two innings scores: 45 + 67 = 112
        It calculates the average score by dividing the total by 2 (since there are two innings): 112 / 2 = 56.0
        
        
        The function then prints the results:
        
        The total score (112)
        The average score (56.0)
        
        
        
        The average is displayed with a decimal point to show that it's a floating-point number, which allows for more precise averages in cases where the total isn't evenly divisible by 2."""),
            AIMessage(content="""
            def compute_total_score(score1, score2):
               # Calculate the total score by adding the scores from both innings
               total_score = score1 + score2
               
               # Return the total score
               return total_score
            """),
            HumanMessage(content=f"problem_statement : {self.result['problem_name']}, description : {self.result['description']}, function_template : {self.result['function_template']}, input_output_description : {self.result['input_output_description']}")
        ]
        
        prompt = ChatPromptTemplate.from_messages(messages)
        
        chain = prompt | self.model | StrOutputParser()
        
        self.result["solution"] = chain.invoke({})
        

    def generate_problem(self):
        self.generate_problem_name()
        self.generate_description()
        self.generate_function_info()
        self.generate_function_template()
        self.generate_input_output_description()
        self.generate_input_output_pairs()
        self.generate_solution()

    def get_json_result(self):
        return json.dumps(self.result, indent=2)

