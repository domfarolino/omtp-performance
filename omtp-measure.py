import statistics

# Open files from the two runs

runs = [
  {
    "name": "Stock",
    "file": open("stock.txt", "r"),
    "flushTimes": [],
    "renderTimes": []
  }, 
  {
    "name": "Direct2D Disabled",
    "file": open("d2d-disabled.txt", "r"),
    "flushTimes": [],
    "renderTimes": []
  },
  {
    "name": "Direct2D Disabled OMTP Enabled Force Sync False",
    "file": open("d2d-disabled-omtp-enabled-force-sync-false.txt"),
    "flushTimes": [],
    "renderTimes": []
  },
  {
    "name": "Direct2D Enabled OMTP Enabled Force Sync False",
    "file": open("d2d-enabled-omtp-enabled-force-sync-false.txt"),
    "flushTimes": [],
    "renderTimes": []
  }
]

numTimesToDelete = 50

# Parse data to fill out the above structure

for run in runs:
  for line in run["file"]:
    if len(line.split(":")) < 2: continue
    timeType = line.split(":")[0]
    theTime = line.split(":")[1]

    if timeType == "FlushAsyncPaint":
      run["flushTimes"].append(float(theTime))
    elif timeType == "RenderLayer":
      run["renderTimes"].append(float(theTime))

  # Delete the first & last `numTimesToDelete` measurements
  del run["flushTimes"][:numTimesToDelete]
  del run["renderTimes"][:numTimesToDelete]
  run["flushTimes"] = run["flushTimes"][:-numTimesToDelete]
  run["renderTimes"] = run["renderTimes"][:-numTimesToDelete]

for run in runs:
  print("Statistics for", run["name"], "run")
  print("AVG FlushPaint Time:", statistics.mean(run["flushTimes"]))
  print("AVG RenderLayer Time:", statistics.mean(run["renderTimes"]))

  print("STD-DEV of FlushPaint Times:", statistics.stdev(run["flushTimes"]))
  print("STD-DEV of RenderLayer Times:", statistics.stdev(run["renderTimes"]))

  print("Variance of FlushPaint Times:", statistics.variance(run["flushTimes"]))
  print("Variance of RenderLayer Times:", statistics.variance(run["renderTimes"]))

  print("----------------------------------")
