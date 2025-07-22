import requests
import random
import json
import time

# --------------------------
# Utility to get categories
# --------------------------
def get_categories():
    url = "https://opentdb.com/api_category.php"
    data = requests.get(url).json()
    categories = data["trivia_categories"]
    return {c["id"]: c["name"] for c in categories}

# --------------------------
# Fetch questions
# --------------------------
def fetch_questions(amount=5, difficulty=None, category=None):
    base_url = "https://opentdb.com/api.php?"
    params = f"amount={amount}&type=multiple"
    if difficulty:
        params += f"&difficulty={difficulty}"
    if category:
        params += f"&category={category}"
    url = base_url + params
    response = requests.get(url)
    data = response.json()
    return data.get("results", [])

# --------------------------
# Ask a single question
# --------------------------
def ask_question(q, timer_enabled=False, time_limit=15):
    question_text = q['question']
    correct = q['correct_answer']
    options = q['incorrect_answers'] + [correct]
    random.shuffle(options)

    print(f"\n{question_text}")
    for i, opt in enumerate(options, start=1):
        print(f"{i}. {opt}")

    start_time = time.time()
    while True:
        try:
            answer = input("Your answer (1-4): ")
            if not answer.isdigit():
                print("Enter a number!")
                continue
            ans_num = int(answer)
            if ans_num not in [1,2,3,4]:
                print("Enter a number between 1-4!")
                continue
            # Timer check
            if timer_enabled:
                elapsed = time.time() - start_time
                if elapsed > time_limit:
                    print("⏳ Time's up!")
                    print(f"✅ Correct answer was: {correct}")
                    return False
            if options[ans_num-1] == correct:
                print("✅ Correct!")
                return True
            else:
                print(f"❌ Wrong! Correct answer: {correct}")
                return False
        except Exception as e:
            print("Invalid input. Try again.")

# --------------------------
# Main game loop
# --------------------------
def main():
    print("🎮 Welcome to the Quiz Game!")
    # Choose number of questions
    while True:
        try:
            num = int(input("How many questions do you want? "))
            if num <= 0:
                print("Enter a positive number.")
                continue
            break
        except:
            print("Enter a valid number.")

    # Difficulty selection
    difficulty = input("Select difficulty (easy/medium/hard or leave blank): ").strip().lower()
    if difficulty not in ['easy','medium','hard']:
        difficulty = None

    # Category selection
    cats = get_categories()
    print("\nAvailable Categories:")
    for cid, name in list(cats.items())[:20]:  # show first 20 for brevity
        print(f"{cid}: {name}")
    cat_choice = input("Enter category id or leave blank: ").strip()
    if cat_choice.isdigit() and int(cat_choice) in cats:
        category = int(cat_choice)
    else:
        category = None

    # Timer choice
    timer_opt = input("Enable timer? (y/n): ").strip().lower()
    timer_enabled = timer_opt == 'y'
    time_limit = 15  # seconds

    # Fetch and play
    questions = fetch_questions(num, difficulty, category)
    score = 0
    for q in questions:
        if ask_question(q, timer_enabled, time_limit):
            score += 1

    print(f"\n🎯 Final Score: {score}/{len(questions)}")

    # Save result
    with open("quiz_scores.json", "a") as f:
        entry = {"score": score, "total": len(questions), "difficulty": difficulty, "category": category}
        f.write(json.dumps(entry) + "\n")
    print("✅ Your score has been saved to quiz_scores.json")

if __name__ == "__main__":
    main()
