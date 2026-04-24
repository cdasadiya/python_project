import pandas as pd

# Sample Data
print(f"Creating sample DataFrame")
df = pd.DataFrame({
    'A': [1, 2, None, 4],
    'B': [5, None, 7, 8],
    'C': ['x', 'y', 'z', 'x']
})
print(f"DataFrame:\n{df}\n")

# head
print(f"head():\n{df.head()}\n")

# info
print(f"info():")
df.info()

# describe
print(f"describe():\n{df.describe()}\n")

# fillna
filled = df.fillna(0)
print(f"fillna(0):\n{filled}\n")

# dropna
dropped = df.dropna()
print(f"dropna():\n{dropped}\n")

# drop_duplicates
print(f"drop_duplicates():\n{df.drop_duplicates()}\n")

# astype
try:
    print(f"astype(int) positive:\n{filled['A'].astype(int)}\n")
    print(f"astype(int) negative (error expected):")
    print(df['C'].astype(int))
except Exception as e:
    print(f"Error: {e}\n")

# groupby
grouped = df.groupby('C').sum(numeric_only=True)
print(f"groupby sum:\n{grouped}\n")

# sort_values
sorted_df = df.sort_values(by='A')
print(f"sort_values:\n{sorted_df}\n")

# merge
left = pd.DataFrame({'key': [1,2], 'val': ['a','b']})
right = pd.DataFrame({'key': [1,3], 'val2': ['c','d']})
merged = pd.merge(left, right, on='key', how='inner')
print(f"merge inner:\n{merged}\n")

# concat
concat_df = pd.concat([left, right], axis=0)
print(f"concat:\n{concat_df}\n")

# pivot_table
pivot = pd.pivot_table(df, values='A', index='C', aggfunc='mean')
print(f"pivot_table:\n{pivot}\n")

# apply
applied = df['A'].fillna(0).apply(lambda x: x*2)
print(f"apply *2:\n{applied}\n")

# isin
print(f"isin(['x']):\n{df[df['C'].isin(['x'])]}\n")

# rename
renamed = df.rename(columns={'A':'A_new'})
print(f"rename:\n{renamed}\n")

# to_csv (not saving file, just showing intent)
print(f"to_csv would save the DataFrame to a file")
