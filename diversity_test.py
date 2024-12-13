import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json


def analyze_question_diversity(generated_questions):
    # Use TF-IDF to capture important keywords
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(generated_questions)

    # Determine topic clusters
    num_clusters = min(5, len(generated_questions))
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(tfidf_matrix)

    # Analyze cluster distribution
    cluster_distribution = np.unique(kmeans.labels_, return_counts=True)

    # Get representative questions for each cluster
    cluster_representatives = {}
    for cluster_id in range(num_clusters):
        cluster_mask = (kmeans.labels_ == cluster_id)
        cluster_questions = [q for q, mask in zip(generated_questions, cluster_mask) if mask]
        cluster_representatives[cluster_id] = cluster_questions

    result = {
        'total_questions': len(generated_questions),
        'num_clusters': num_clusters,
        'cluster_distribution': dict(zip(*cluster_distribution)),
        'cluster_representatives': cluster_representatives
    }

    # Convert all NumPy types to standard Python types
    return result


def evaluate_quiz_coverage(generated_questions):
    # Keyword extraction
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(generated_questions)

    # Get top keywords across all questions
    feature_names = vectorizer.get_feature_names_out()
    tfidf_sum = tfidf_matrix.sum(axis=0).A1
    top_keywords = sorted(zip(feature_names, tfidf_sum), key=lambda x: x[1], reverse=True)[:10]

    return {
        'diversity_analysis': analyze_question_diversity(generated_questions),
        'top_keywords': top_keywords
    }



def measure_semantic_diversity(generated_questions):
    # Use sentence embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(generated_questions)

    # Compute pairwise similarities
    similarity_matrix = cosine_similarity(embeddings)

    # Calculate diversity metrics
    avg_similarity = np.mean(similarity_matrix)
    similarity_std = np.std(similarity_matrix)

    return {
        'average_question_similarity': avg_similarity,
        'similarity_variation': similarity_std,
        'is_diverse': (avg_similarity > 0.4) & (avg_similarity < 0.6)
        # lower similarity suggest questions are not co-related at all
        # higher similarity suggest questions are focusing on a specifi part only
        # medium similarity suggest fair diversity and co-related questions

    }


def comprehensive_quiz_analysis(generated_questions):
    return {
        'topic_coverage': evaluate_quiz_coverage(generated_questions),
        'semantic_diversity': measure_semantic_diversity(generated_questions)
    }

# Getting list of questions from all the questions file
def get_qusetions(path):
    questions = []
    try:
        with open(f"quiz_json/{path}") as file:
            quiz = json.load(file)
        for question in quiz:
            questions.append(question['Question'])
    except:
        pass
    return questions

# Converting keys(of a dictionary) to valid suppoted data type for json files
def convert_keys_recursive(data):
    if isinstance(data, dict):
        return {str(k): convert_keys_recursive(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_keys_recursive(item) for item in data]
    elif isinstance(data, (np.integer, np.floating, np.bool_)):  # Added np.bool_
        return str(data)  # Convert to string
    else:
        return data


def get_result_for_all_quiz():
    files = os.listdir("quiz_json")
    for file in files:
        print("getting result for ", file)
        questions = get_qusetions(file)
        analysis_results = comprehensive_quiz_analysis(questions)
        print(analysis_results)
        analysis_results = convert_keys_recursive(analysis_results)
        with open(f"benchmark/{file}", 'w') as f:
            json.dump(analysis_results, f, indent=4)

get_result_for_all_quiz()