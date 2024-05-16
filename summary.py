from entity.problem import Problem
from database import get_db_conn

needed_to_summarize = [
    "1008_E. Guess two numbers",
    "1023_G. Pisces",
    "1033_E. Hidden Bipartite Graph",
    "1033_F. Boolean Computer",
    "1033_G. Chip Game",
    "1044_A. The Tower is Going Home",
    "1044_B. Intersecting Subtrees",
    "1044_D. Deduction Queries",
    "1062_F. Upgrading Cities",
    "107_C. Arrangement",
    "107_E. Darts",
    "1080_D. Olya and magical square",
    "1091_G. New Year and the Factorisation Collaboration",
    "1118_F2. Tree Cutting (Hard Version)",
    "1153_E. Serval and Snake",
    "1163_F. Indecisive Taxi Fee",
    "1172_C2. Nauuo and Pictures (hard version)",
    "1174_F. Ehab and the Big Finale",
    "1178_H. Stock Exchange",
    "1185_G2. Playlist for Polycarp (hard version)",
    "1190_F. Tokitsukaze and Powers",
    "1205_C. Palindromic Paths",
    "1205_E. Expected Value Again",
    "1253_F. Cheap Robot",
    "1263_F. Economic Difficulties",
    "1279_F. New Year and Handle Change",
    "1293_D. Aroma's Search",
    "1304_F2. Animal Observation (hard version)",
    "1326_G. Spiderweb Trees",
    "1332_G. No Monotone Triples",
    "1355_F. Guess Divisors Count",
    "1359_C. Mixing Water",
    "1359_F. RC Kaboom Show",
    "1372_F. Omkar and Modes",
    "1375_H. Set Merging",
    "1375_I. Cubic Lattice",
    "1383_D. Rearrange",
    "1389_G. Directing Edges",
    "138_C. Mushroom Gnomes - 2",
    "1392_E. Omkar and Duck",
    "1392_F. Omkar and Landslide",
    "1392_G. Omkar and Pies",
    "1407_E. Egor in the Republic of Dagestan",
    "1420_E. Battle Lemmings",
    "1425_I. Impressive Harvesting of The Orchard",
    "1427_C. The Hard Work of Paparazzi",
    "1427_F. Boring Card Game",
    "1427_G. One Billion Shades of Grey",
    "1442_F. Differentiating Games",
    "1450_G. Communism",
    "1450_H2. Multithreading (Hard Version)",
    "1454_F. Array Partition",
    "1474_E. What Is It?",
    "1474_F. 1 2 3 4 ...",
    "1491_I. Ruler Of The Zoo",
    "1498_E. Two Houses",
    "1514_E. Baby Ehab's Hyper Apartment",
    "1517_H. Fly Around the World",
    "1521_C. Nastia and a Hidden Permutation",
    "1525_F. Goblins And Gnomes",
    "1526_F. Median Queries",
    "1534_E. Lost Array",
    "1539_E. Game with Cards",
    "1541_E1. Converging Array (Easy Version)",
    "1545_F. AquaMoon and Potatoes",
    "1550_F. Jumping Around",
    "226_E. Noble Knight's Path",
    "251_E. Tree and Table",
    "327_C. Magic Five",
    "327_E. Axis Walking",
    "340_E. Iahub and Permutations",
    "360_E. Levko and Game",
    "384_D. Volcanoes",
    "384_E. Propagating tree",
    "391_C3. The Tournament",
    "391_D2. Supercollider",
    "391_E2. Three Trees",
    "391_F1. Stock Trading",
    "391_F2. Stock Trading",
    "391_F3. Stock Trading",
    "430_C. Xor-tree",
    "471_E. MUH and Lots and Lots of Segments",
    "533_A. Berland Miners",
    "538_H. Summer Dichotomy",
    "549_E. Sasha Circle",
    "553_E. Kyoya and Train",
    "566_C. Logistical Questions",
    "611_G. New Year and Cake",
    "639_F. Bear and Chemistry",
    "671_E. Organizing a Race",
    "678_F. Lena and Queries",
    "710_F. String Set Queries",
    "724_G. Xor-matic Number of the Graph",
    "725_D. Contest Balloons",
    "758_C. Unfair Poll",
    "788_D. Finding lines",
    "807_D. Dynamic Problem Scoring",
    "853_D. Michael and Charging Stations",
    "917_A. The Monster",
    "950_F. Curfew",
    "991_F. Concise and clear"
]

def get_problem(name: str) -> Problem:
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT p.name, p.description, p.cf_tags, p.cf_rating, e.content
    FROM problems p JOIN editorials e ON p.name = e.name
    WHERE p.name = %s
""", (name,))
    problem = cursor.fetchone()
    cursor.close()
    conn.close()
    if problem is None:
        return None
    return Problem(name = problem[0], description = problem[1], tags = problem[2], rating = problem[3], editorial = problem[4], source="codeforces")

for name in needed_to_summarize:
    problem = get_problem(name)
    print(problem.name)
    with open('tmp_des.txt', 'w') as f:
        f.write(f"""Summarize the following editorial in bullet points format.
The summary MUST be long and detailed, about 10-15 bullet points for each solution.
Must contain all the reasonings, logics, math-works, facts, observations, and explanations in the editorial.
Must fix any vocabulary, grammar errors in the editorial.
Must not contain any code.
Must not have any unnecessary details. 
Must be able to solve the problem with the summary alone.
Must not have any formatting.
Answer in markdown format like this:
```md
- sentence 1
- sentence 2
    - sentence 3
- sentence 4
```             
Here is the problem description:
# Problem {problem.name}
# Description:
// start of problem description
{problem.description}
// end of problem description
Here is the editorial:
# Editorial:
// start of editorial
{problem.editorial}
// end of editorial
""")
    while True:
        c = input()
        c = c.strip()
        if c == 'save':
            with open('tmp_ed.txt', 'r') as f:
                content = f.read()
            with open(f'gemini/{name}.txt', 'w') as f:
                f.write(content)
            break
            
                

