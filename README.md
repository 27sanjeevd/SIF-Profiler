# SIF-Profiler

Enhanced tool to profiler methods. Can be used to profile function/line timings/memory usage, and create intuitive visualizations from it

## Overview

All encompassing profiler meant to trace a multitude of different performance analytics of the profiled function. Can be used to calculate overall function timings, isolated function timings, line timings, memory usage calculations, etc. Based on certain parameters inputted into the Profiler, it analyzes that specific datapoint. Either prints the output to standard output, or dumps it into an output.json file, which can then be ran with the Analytics tool. This tool takes in this json file and creates dynamic graphs of the overall execution of the profiled method to be visualized.

## Installation

```
pip install sif-profiler
```

Now that you've installed the profiler, here are the steps to start profiling your method.
