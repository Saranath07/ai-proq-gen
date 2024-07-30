from .equal_check import equal_check_chain
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda

extract_text_metadata_chain = {
    "texts": RunnableLambda(itemgetter("statement")).map(),
    "metadatas": RunnableParallel({
        "solution":itemgetter("solution"),
        "tags": lambda x: ",".join(x.get("tags", [])),
        "data_formats":lambda x: ",".join(x.get("data_formats", [])),
    }).map()
}

def get_generator_chain(ideation_chain, db_store):
    single_item_retriever = db_store.as_retriever(search_kwargs={"k": 1})
    duplicate_check_chain = (
        RunnableParallel(
            {
                "problem": RunnablePassthrough(),
                "statement1": itemgetter("statement"),
                "statement2": itemgetter("statement")
                | single_item_retriever
                | (lambda x: x[0].page_content),
            }
        )
        | RunnablePassthrough.assign(
            is_equal=RunnablePassthrough().pick(["statement1", "statement2"])
            | equal_check_chain
        )
    )

    return (
        ideation_chain
        | duplicate_check_chain.map()
        | {
            "new_problems": (
                lambda problems: [
                    problem for problem in problems if not problem["is_equal"]
                ]
            )
            | RunnablePassthrough().pick("problem").map()
            | extract_text_metadata_chain
            | (lambda x: db_store.add_texts(**x)),
            "duplicate_problems": (
                lambda problems: [
                    problem for problem in problems if problem["is_equal"]
                ]
            ),
        }
    )
