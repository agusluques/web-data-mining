import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

df = pd.read_csv("./bank-data.csv")
del df["id"]
df["income"] = pd.cut(df["income"],10)
dataset = []
for index, row in df.iterrows():
    row = [col+"="+str(row[col]) for col in list(df)]
    dataset.append(row)


te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_ary, columns=te.columns_)
frequent_itemsets = apriori(df, min_support=0.3, use_colnames=True)
print("Frequent Itemset:\n")
print(frequent_itemsets)

rules_confidence = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
print("\nConfidence 0.7:\n")
print(rules_confidence)

rules_support = association_rules(frequent_itemsets, metric="support", min_threshold=0.4)
print("\nSupport 0.4:\n")
print(rules_support)

rules_lift = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
print("\nLift 1:\n")
print(rules_lift)