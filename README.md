# SIF-Profiler

Enhanced tool to profiler methods. Can be used to profile function/line timings/memory usage, and create intuitive visualizations from it

## Overview

All encompassing profiler meant to trace a multitude of different performance analytics of the profiled function. Can be used to calculate overall function timings, isolated function timings, line timings, memory usage calculations, etc. Based on certain parameters inputted into the Profiler, it analyzes that specific datapoint. Either prints the output to standard output, or dumps it into an output.json file, which can then be ran with the Analytics tool. This tool takes in this json file and creates dynamic graphs of the overall execution of the profiled method to be visualized.

## Installation

```
pip install sif-profiler
```

Now that you've installed the profiler, here are the steps to start profiling your method. To import it into your code, use

```
from sif-profiler import Profiler, Analytics
```

## Usage

### Calling it
Once you have it installed, you can start using it to trace your code. Simply start by calling 

```
newProfiler = Profiler()
```

### Specifying Tracing Information
Now that it's created, we need to start by specifying what values we want to trace with our function. Depending on what we specify, the profiler will track information about this, and dump it to the json file. Here are the current values that can be specified

- test_lines
  - True/False value that specifies if we want to obtain analytics information about individual lines as well as overall function information
- test_timing
  - True/False value that specifies if we want to time execution time.
- test_memory
  - True/False value that specifies if we want to calculate memory usage
- timing_isolation
  - True/False value that tells if we want to isolate function timing. For example, if function B calls function A, then the execution time of function A won't be reflected in function B's execution time
- timing_function
  - List of function names to be analyzed. If a function exists in this list, then information about it will be collected. If we're tracing lines, then only if a line exists in one of these functions will it be analyzed. If nothing is passed into this variable, then every function/line will be analyzed

Now to specify information about which variable we want to utilized, you can use code like this

```
newProfiler.test_timing = True
newProfiler.test_lines = True
newProfiler.timing_isolation = True
newProfiler.timing_functions = ['getReport', 'parseReport']
```

### Profiling a Function
To 
