import pandas as pd
import matplotlib.pyplot as plt

# Data
data = {
    "average_question_similarity": [0.64932144, 0.45950112, 0.5653297, 0.3988551, 0.64333606, 0.47275418,
                                     0.5427977, 0.5769779, 0.47690544, 0.43154797, 0.3483602, 0.5169278,
                                     0.37672693, 0.53171366, 0.42598698, 0.44798255, 0.45648843, 0.5862167,
                                     0.41465387, 0.46018898],
    "similarity_variation": [0.22681357, 0.30662295, 0.23953542, 0.2922515, 0.25688645, 0.24135922,
                              0.2510093, 0.26528051, 0.2615546, 0.30928865, 0.33317012, 0.31499323,
                              0.31227776, 0.24637622, 0.25345013, 0.34596506, 0.32756647, 0.3004706,
                              0.21588857, 0.26772317],
    "is_diverse": [False, True, True, False, False, True, True, True, True, True, False, True,
                    False, True, True, True, True, True, True, True]
}
# Create DataFrame
df = pd.DataFrame(data)

# Count True vs False in is_diverse
counts = df["is_diverse"].value_counts()
labels = ["Diverse and Related\n(40% - 60%)", "Less Diverse or Less Related\n(0% - 40% and 60% to 100%)"]

# Plotting
plt.figure(figsize=(8, 8))
plt.pie(counts, labels=labels, autopct="%1.1f%%", startangle=90, colors=["lightskyblue", "lightcoral"])
plt.title("Question Diversity and Afinity", fontsize=14)

# Show plot
plt.tight_layout()
plt.savefig("diversity.png")
plt.show()


