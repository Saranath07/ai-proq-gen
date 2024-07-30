from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser
from langchain_groq import ChatGroq



model = ChatGroq(temperature=1.2,model="llama3-70b-8192")

prompt = ChatPromptTemplate.from_messages([
    ('system', """
Given a word generate 10 related words for that it as a comma seperated list.
Generate only the list of words and nothing else
"""),
    ('human','''education'''),
    ('ai',"""school,classes,exam,library,homework"""),
    ('human','''movie'''),
    ('ai',"""production,cast,box-office,genre,grossing"""),
    ('human',"{word}")
])

get_related =  prompt | model | CommaSeparatedListOutputParser()

