import json
import os
import pandas as pd


def get_data(path):
    try:
        with open(f"benchmark/{path}") as file:
            quiz = json.load(file)
            average_question_similarity = (quiz['semantic_diversity']['average_question_similarity'])
            similarity_variation = (quiz['semantic_diversity']['similarity_variation'])
            is_diverse = (quiz['semantic_diversity']['is_diverse'])
    except:
        pass
    return average_question_similarity, similarity_variation, is_diverse


files = os.listdir("benchmark")
average_question_similarity = []
similarity_variation = []
is_diverse = []

for file in files:
    avg_sim, sim_var, is_sim = get_data(file)
    average_question_similarity.append(avg_sim)
    similarity_variation.append(sim_var)
    is_diverse.append(is_sim)

dicti = {
    "average_question_similarity": average_question_similarity,
    "similarity_variation": similarity_variation,
    "is_diverse": is_diverse
}

pd.DataFrame(dicti).to_csv("benchmark_data.csv", index=False)