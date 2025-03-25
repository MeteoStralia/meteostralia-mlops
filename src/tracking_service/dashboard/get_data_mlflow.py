experiment_id = get_experiment_id(experiment_name)


# last ten runs data
runs = mlflow.search_runs(experiment_ids=experiment_id)
runs.head(10)

# best last run for a specific metric
runs = mlflow.search_runs(experiment_ids=experiment_id,
                          order_by=['metrics.f1_score'], 
                          max_results=50)
runs.loc[0]

# recent runs and best run per day
earliest_start_time = (datetime.datetime.now() - timedelta(days=50)).strftime('%Y-%m-%d')
recent_runs = runs[runs.start_time >= earliest_start_time]
recent_runs['Run Date'] = recent_runs.start_time.dt.floor(freq='D')

best_runs_per_day_idx = recent_runs.groupby(
  ['Run Date']
)['metrics.f1_score'].idxmin()
best_runs = recent_runs.loc[best_runs_per_day_idx]

display(best_runs[['Run Date', 'metrics.f1_score']])

sns.boxplot(x=recent_runs['Run Date'], 
         y=recent_runs['metrics.f1_score'])

plt.ylim(0,1)
plt.xlabel('Run Date')
plt.ylabel('metrics.f1_score')
plt.title("Run f1_score per day")
plt.xticks(rotation=45)

sns.lineplot(x=best_runs['Run Date'], 
         y=best_runs['metrics.f1_score'],
         marker='H')
plt.ylim(0,1)
plt.xlabel('Run Date')
plt.ylabel('metrics.f1_score')
plt.title("Best run per day")
plt.xticks(rotation=45)

# number of run per day
earliest_start_time = (datetime.datetime.now() - timedelta(days=50)).strftime('%Y-%m-%d')
recent_runs = runs[runs.start_time >= earliest_start_time]

recent_runs['Run Date'] = recent_runs.start_time.dt.floor(freq='D')

runs_per_day = recent_runs.groupby(
  ['Run Date']
).count()[['run_id']].reset_index()
runs_per_day['Run Date'] = runs_per_day['Run Date'].dt.strftime('%Y-%m-%d')
runs_per_day.rename({ 'run_id': 'Number of Runs' }, axis='columns', inplace=True)

display(runs_per_day)

sns.barplot(x = runs_per_day['Run Date'],
            y = runs_per_day['Number of Runs'])
plt.xlabel('Run Date')
plt.ylabel('Number of Runs')
plt.title("Number of runs per day")
plt.xticks(rotation=45)
