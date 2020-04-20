# Informativeness
Here we present the implementation of two metrics: syntactic cohesion and informativeness.

The repository also consists of the dataset used.

***Later we will add the analysis part.

The code sub-directory consists of a python file which parses, cleans and transforms the data.

The transformed data is then used to generate dependency graphs for segments of a corpus of instructions.

The dependency graph elements are then used to calculate cohesion scores and their cumulative sum to generate informativeness.

The libraries used are as follows:
Spacy for generating dependency graphs
Pandas for reading, transforming and writing the data.

The format of the data is tab delimited csv files with index (below trans_info) and instructions (instruction_segment) 
where, each of it is expanded to consequitive rows with segments as indicated in the example below. 

trans_info	instruction_segment

0	 mok move right 

0	 move four feet 

0	 turn left 

0	 move seven feet 

After this we apply dependency parsing using SPACY. 

Then we calculate informativeness equations. 

