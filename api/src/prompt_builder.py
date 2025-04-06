from database import main_flow
car_data_example = main_flow()["resultList"][:10]


def prompt_builder(user_input: dict) -> str:
    prompt = f"""
                ## Role: Car situation Reporter

                ### Context:
                You are an experienced car reporter that answers question about cars from a given data, each car id identified by a unique id and you answer based on the user query.

                ### Required Output Format:
                you only give a discription of the car with the given Id, with no addtional information.
               
                ### User Query:
                {user_input}
                ### Car data:
                {car_data_example}"""
    return prompt