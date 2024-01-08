import pandas as pd
import random

def random_array(n, max_value):
  a = [0] * n
  for i in range(n):
    a[i] = random.randint(1, max_value)
  return a


for i in range(1, 10):
  size = 10_000_000
  data = {
       'c1': random_array(size, 1000),
       'c2': random_array(size, 10)
  }
  df = pd.DataFrame(data)
  file_id = random.randint(1,10000000)
  print("Writing file...")
  df.to_parquet('data/output' + str(file_id) + '.parquet')
