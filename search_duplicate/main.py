import os
import time
from dotenv import load_dotenv
import db
import gpt


ENV_FILE = "../.env"
env_loaded = load_dotenv(ENV_FILE)
if not env_loaded:
    exit(f"Не удалось прочитать переменные окружения в файле: {ENV_FILE}")


def main():
    while True:
        success = process_skill()
        if not success:
            break


def process_skill():
    pair = db.get_skill_pair()
    print(pair)
    if not pair:
        return False

    is_duplicate = gpt.check_skills_similarity(pair)
    while is_duplicate is None:
        time.sleep(60)
        is_duplicate = gpt.check_skills_similarity(pair)

    pair.IsDuplicate = is_duplicate
    db.update_row(pair)
    print(pair)
    time.sleep(20)
    return True


if __name__ == "__main__":
    main()

