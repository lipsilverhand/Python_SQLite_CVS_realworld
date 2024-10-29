import pandas as pd
import sqlite3
import ssl
import matplotlib.pyplot as plt
import seaborn as sb

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

con = sqlite3.connect("social_economic.db")
df = pd.read_csv('https://data.cityofchicago.org/resource/jcxq-k9xf.csv')
df.to_sql("chicago_socioeconomic_data", con, if_exists='replace', index=False, method="multi")
print("Data has been converted into the database")

con.commit()
print(df)

# Execute a query to count the records in the table
problem1 = '''SELECT COUNT(*) FROM chicago_socioeconomic_data'''
exe1 = con.execute(problem1).fetchone()[0]
print("Prob_1: Number of records in the database:", exe1)

# Count areas that have a hardship index > 50.0
problem2 = '''SELECT COUNT(*) FROM chicago_socioeconomic_data
				WHERE hardship_index > 50.0
'''
exe2 = con.execute(problem2).fetchone()[0]
print("Prob_2: Counted areas which have hardship index larger than 50.0:", exe2)


# Maximum value of harship index
problem3 = '''SELECT MAX(hardship_index) FROM chicago_socioeconomic_data'''
exe3 = con.execute(problem3).fetchone()[0]
print("Prob_3: Maximum value of harship index:", exe3)

# Area which has highest hardship index value
problem4 = '''SELECT community_area_name FROM chicago_socioeconomic_data
			  WHERE hardship_index = (SELECT MAX(hardship_index) FROM chicago_socioeconomic_data)'''
exe4 = con.execute(problem4).fetchone()[0]
print("Prob_4: Area that has highest hardship index:", exe4)

# Areas which have capital income higher than $60k
problem5 = '''SELECT community_area_name FROM chicago_socioeconomic_data
			  WHERE per_capita_income_ > 60000
'''
exe5 = con.execute(problem5).fetchall()
area_names = [name[0] for name in exe5]
print("Prob_5: Areas with capital income more than $60k: ", ', '.join(area_names))

# Scatter plot using the variables per_capita_income_ and hardship_index
problem6 = '''SELECT per_capita_income_, hardship_index FROM chicago_socioeconomic_data'''
data = con.execute(problem6).fetchall()
df2 = pd.DataFrame(data, columns=['per_capita_income_', 'hardship_index'])
plot = sb.jointplot(x='per_capita_income_',y='hardship_index', data=df2)
plt.show()

# Close the connection
con.close()

