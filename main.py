import sqlite3

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver

from agent import create_agent


DB_PATH = "memory.db"


def get_projects():

    try:

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.execute("SELECT DISTINCT thread_id FROM checkpoints")
        
        projects = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        
        return projects
   
    except:

        return []


def select_project():

    projects = get_projects()

    if projects:

        print("Существующие проекты: ")

        for i, name in enumerate(projects, 1):

            print(f"{i}. {name}")

        print()

    name = input("Название проекта (Enter = новый): ").strip()

    if not name:

        name = input("Введите название нового проекта: ").strip()

    return name


def main():

    project = select_project()

    print(f"Проект: {project}")

    with SqliteSaver.from_conn_string(DB_PATH) as memory:

        agent = create_agent(memory)

        config = {"configurable": {"thread_id": project}}

        while True:

            user_input = input("You: ")

            if user_input.lower() in ["exit", "quit", "выход"]:
                return
 
            if not user_input.strip():
                continue

            response = agent.invoke(
                {"messages": [HumanMessage(content=user_input)]},
                config=config
            )

            messages = response["messages"]

            for msg in reversed(messages):

                if hasattr(msg, "type") and msg.type == "ai" and msg.content:

                    print(f"S-code: {msg.content}")

                    break


if __name__ == "__main__":

    main()
