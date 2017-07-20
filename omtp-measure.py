import statistics

# Open files from the two runs

runs = [
  {
    "name": "Stock",
    "file": open("stock.txt", "r"),
    "flushTimes": [],
    "renderTimes": [],
    "paintCallbackTimes": []
  },
  {
    "name": "Direct2D Disabled",
    "file": open("d2d-disabled.txt", "r"),
    "flushTimes": [],
    "renderTimes": [],
    "paintCallbackTimes": []
  },
  {
    "name": "Direct2D Disabled OMTP Enabled Force Sync False",
    "file": open("d2d-disabled-omtp-enabled-force-sync-false.txt"),
    "flushTimes": [],
    "renderTimes": [],
    "paintCallbackTimes": []
  },
  {
    "name": "Direct2D Enabled OMTP Enabled Force Sync False",
    "file": open("d2d-enabled-omtp-enabled-force-sync-false.txt"),
    "flushTimes": [],
    "renderTimes": [],
    "paintCallbackTimes": []
  }
]

numTimesToDelete = 50

# Parse data to fill out the above structure

accum = 0.0
for run in runs:
  for line in run["file"]:
    if "OMTP" not in line: continue # Not an OMTP log message that we're about to parse

    # Determine what kind of line it is? Options
    #   FlushAsyncPaint time
    #   RenderLayers time
    #   PaintCallback time (either time spent capturing or rasterizing on the main thread per layer)
    #   ----EndFrame line indicating a new frame, so we should reset the
    #           accumulator that accumulates values gathered from each layer's PaintCallback time

    if len(line.split(":")) > 1: theTime = float(line.split(":")[1])

    if line.startswith("FlushAsyncPaint"):
      run["flushTimes"].append(theTime)
    elif line.startswith("RenderLayer"):
      run["renderTimes"].append(theTime)
    elif line.startswith("PaintedLayerCallback"):
      accum += theTime
    elif line.startswith("----End"):
      if accum is 0: continue
      run["paintCallbackTimes"].append(accum)
      accum = 0

  # Clean up data by deleting the first & last
  # `numTimesToDelete` measurements
  del run["flushTimes"][:numTimesToDelete]
  del run["renderTimes"][:numTimesToDelete]
  del run["paintCallbackTimes"][:numTimesToDelete]
  run["flushTimes"] = run["flushTimes"][:-numTimesToDelete]
  run["renderTimes"] = run["renderTimes"][:-numTimesToDelete]
  run["paintCallbackTimes"] = run["paintCallbackTimes"][:-numTimesToDelete]

for run in runs:
  print("Statistics for", run["name"], "run")
  print("AVG FlushPaint Time:", statistics.mean(run["flushTimes"]))
  print("AVG RenderLayer Time:", statistics.mean(run["renderTimes"]))
  print("AVG PaintCallback Time:", statistics.mean(run["paintCallbackTimes"]))

  print("STD-DEV of FlushPaint Times:", statistics.stdev(run["flushTimes"]))
  print("STD-DEV of RenderLayer Times:", statistics.stdev(run["renderTimes"]))
  print("STD-DEV of PaintCallback Times:", statistics.stdev(run["paintCallbackTimes"]))

  print("Variance of FlushPaint Times:", statistics.variance(run["flushTimes"]))
  print("Variance of RenderLayer Times:", statistics.variance(run["renderTimes"]))
  print("Variance of PaintCallback Times:", statistics.variance(run["paintCallbackTimes"]))

  print("----------------------------------")
