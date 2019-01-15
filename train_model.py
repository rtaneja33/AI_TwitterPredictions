import numpy as np
import seaborn as sns
sns.set(style='whitegrid')
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from datetime import datetime

## function taken from tutorial at https://towardsdatascience.com/experimenting-with-twitter-data-using-tensorflow-ea88a8078fd
## calculates day since last post
def get_days_quan_after(created_at):
    splitted_created_at = created_at.split()
    month = splitted_created_at[1]
    day = splitted_created_at[2]
    year = created_at[-4:]

    concated_date = (' '.join([month, day, year]))
    datetime_object = datetime.strptime(concated_date, '%b %d %Y')
    today = datetime.now()
    diff = today - datetime_object
    diff_days = diff.days
    return diff_days

df = pd.read_csv('users_data.csv')

#df = df[df['days_after_last_post'].notnull()]

x_data = df[['favourites_count','followers_count','friends_count','statuses_count']]
y_labels = df['follows_me']

## 30% of data for test set and 70% for training set
X_train, X_test, y_train, y_test = train_test_split(x_data,y_labels,test_size=0.3,random_state=101)

favourites_count = tf.feature_column.numeric_column("favourites_count",normalizer_fn=lambda x: tf.subtract(x, tf.reduce_mean(x)))
followers_count = tf.feature_column.numeric_column("followers_count",normalizer_fn=lambda x: tf.subtract(x, tf.reduce_mean(x)))
friends_count = tf.feature_column.numeric_column("friends_count",normalizer_fn=lambda x: tf.subtract(x, tf.reduce_mean(x)))
statuses_count = tf.feature_column.numeric_column("statuses_count",normalizer_fn=lambda x: tf.subtract(x, tf.reduce_mean(x)))

feat_cols = [favourites_count, followers_count, friends_count,  statuses_count]

#training input function :
# Can also do .pandas_input_fn
input_func = tf.estimator.inputs.pandas_input_fn(x=X_train,y=y_train,batch_size=100,num_epochs=None,shuffle=True)

#testing input function
eval_fn = tf.estimator.inputs.pandas_input_fn(x=X_test,
      y=y_test,
      batch_size=10,
      num_epochs=1,
      shuffle=False)

model = tf.estimator.LinearClassifier(feature_columns=feat_cols, n_classes=2)

model.train(input_fn = input_func, steps=1000)

eval_metrics = model.evaluate(input_fn=eval_fn,steps=1000)

print(eval_metrics)

pdf = pd.read_csv('users_data.csv')
pdf.count()

p_data = pdf[['favourites_count', 'followers_count', 'friends_count', 'statuses_count']]  # 'statuses_count',
pred_fn = tf.estimator.inputs.pandas_input_fn(x=p_data, batch_size=10, num_epochs=1, shuffle=False)
predictions = list(model.predict(input_fn=pred_fn))

final_preds = []
for pred in predictions:
    final_preds.append(pred['class_ids'][0])

result = p_data
print(result)
print(final_preds)
print("FINALPRED" + str(final_preds))
new_col = pd.DataFrame({'prediction':final_preds})
print("NEWCOL" + str(new_col))
result['prediction'] = new_col

final_id = []
for idnum in pdf[['id']]:
    final_id.append(idnum)
print(final_id)
new_col2 = pd.DataFrame({'id': final_id})
print("NEWCOL2" + str(new_col2))
result['id'] = new_col2
print(result)
# result[:10]
#
# users_who_will_follow_me = result.loc[result['prediction'] == 1]
# print(list(users_who_will_follow_me['id']))