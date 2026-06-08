from dotenv import load_dotenv

import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

from langgraph.prebuilt import create_react_agent

from tools import get_directory, create_file, run_code, read_file, delete_file, install_package, list_directory


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))


def create_agent(memory):

    llm = ChatOpenAI(

        model="gpt-5",
        openai_api_key=os.getenv("API_KEY"),
        openai_api_base="https://apinet.cloud/v1",
        temperature=0.3,
        timeout=120,

    )

    tools = [get_directory, create_file, run_code, read_file, delete_file, install_package, list_directory]

    prompt = SystemMessage(content="""
        Ты ИИ агент S-code для создания приложений по текстовому описанию.
        Когда ты получил задачу от пользователя нужно сделать шаги:
            1) сначала спроси в какую директорию и в какое название папки надо сделать проект
                БЕЗ ЭТОЙ ИНФОРМАЦИИ НЕ ИДИ ДАЛЬШЕ СПРАШИВАЙ ПОКА НЕ ПОЛУЧИШЬ ОТВЕТ
            2) далее разбей программу на компаненты где и что должно быть
            3) затем СОЗДАВАЙ КАЖДЫЙ ФАЙЛ ПО ОТДЕЛЬНОСТИ
            4) после запусти и собери ошибки
            5) в случаи ошибок перепиши не работающие фалы
            6) ДЕБАГ КОДА ДЕЛАЙ МАКСИМУМ 3 РАЗА ПОСЛЕ ВЫДАВАЙ ТО ЧТО ЕСТЬ

        Tools:
            для получения основной директории используй - get_directory()
            для создания файла используй - create_file()
            для запуска файла используй - run_code()
            для получения содержимого файла используй - read_file()
            для удаления файла используй - delete_file()
            для установки пакета используй - install_package()
            для просмотра содержимого директории используй - list_directory()

        КРИТИЧЕСКИ ВАЖНО:
            НИКОГДА не пиши код в ответе пользователю — только через инструмент create_file.
            НИКОГДА не проси пользователя самому создавать файлы или устанавливать пакеты — делай это сам через инструменты.
            НИКОГДА не выдумывай путь — сначала вызови get_directory() чтобы узнать рабочий стол.
            Инструмент create_file автоматически создаёт все папки по пути.
            Пример пути: C:/Users/Дмитрий/Desktop/snake_game/main.py
            При создании файла передавай ТОЛЬКО чистый код без markdown блоков и кавычек.
            Если tool вернул текст содержащий "Error" или "Warning" — это проблема.
            Успех только если tool вернул "Done!".
    """)

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=prompt,
        checkpointer=memory
    )

    return agent