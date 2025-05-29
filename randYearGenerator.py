import random

def random_year(year):
    year = int(year)
    min=1900
    max=2000
    a=year
    b=random.randint(year-20,year+20)
    while b>max or b<min:
        b = random.randint(year - 20, year + 20)
    c=random.choice([random.randint(a - 20, a+ 20),random.randint(b - 20, b + 20)])
    while c>max or c<min:
        c = random.choice([random.randint(a - 20, a + 20), random.randint(b - 20, b + 20)])
    d=random.choice([random.randint(a - 20, a+ 20),random.randint(b - 20, b + 20), random.randint(c - 20, c + 20)])
    while d>max or d<min:
        d = random.choice([random.randint(a - 20, a + 20), random.randint(b - 20, b + 20), random.randint(c - 20, c + 20)])
    options = [a, b, c, d]
    random.shuffle(options)
    if len(set(options))==4:
        return options
    else:
        return random_year(year)
