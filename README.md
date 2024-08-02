# 2DCuttingStock
The overall goal of this project is to minimize wood stud cut waste, a material optimization problem.


There are several stages to this project.
1 -- Input Data Ingestion and Preprocessing
2 -- Cutting Stock Algorithm/s Testing
3 -- Algorithm performance comparison and Output File Generation

1 -- Input Data Ingestion and Preprocessing

The initial inputs are the following:
-the standard stud lengths to be cut/evaluated against each other(ex. 8ft, 12ft, 16ft)
-The set of required cuts and their respective quantities

The approach for dealing with input files will be to parse them all so all of the inputs have standard naming of widthxdepthxlength and are list of lists, meaning for example
if I need 3 of 24inch cut, 4 of 31inch cut, and 8 of 12inch cut, my LoL would be:
[[3,24],[4,31],[8,12]]

But, I will be adding in blade cut lengths to all the cuts(which is ex. 0.125 inches) so the LoL will be:
[[3,24.125],[4,31.125],[8,12.125]]

The inputs for now will all come from three excel files of the same format(sheet names and content) the only difference is they pertain to 3 different standard studs and the only relavent sheet within them is 'Stud - Wastage Calc'. They have results from one algorithm already listed in each of the files, so that will be parsed as well.

2 -- Cutting Stock Algorithm/s Testing


There will be different material optimization algorithms tested for this project, and their links/sources will be listed below as used:

The project will be organized with an overall main.py file from which everything is run, and a folder for inputfiles, a folder for the outputfiles, and a folder for the functions.

The aim is to generalize the running of this as much as possible so that it is dynamic and easy to run. 

Now, many algorithms require integer programming, so these will either need to be slightly rounded or multiplied by 1000, the latter being preferable but may not always work due to runtime. These processings will be performed in the algorithm function file due to that algorithm causing the constraint. 






3 -- Algorithm performance comparison and Output File Generation

The final output file will be an excel file with 2 different sheets: one for the summary of the results and one for the actual cuts and quantities for each of the standard lengths and configurations.


