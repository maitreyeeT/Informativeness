# Informativeness
Here we present the implementation of two metrics: syntactic cohesion and informativeness for our recent project.

## Folder description
1. Code has the necessary code for computing the metrics. The code sub-directory consists of a python file which parses, cleans and transforms the data.

2. Data folder has three files: cleaned_inst1 used for calculations, exploded_id_nullvals2 raw dataset, parsed_tree_data has depedency graphs for each instruction segment.

3. data_metrics consists of the final dataset with dependency graphs and cohesion and informativeness scores. 

***Later we will add the analysis part.

### The libraries used are as follows, 
### install libraries using pip and use virtual environment to keep things clean:
```
pip install -U spacy
pip install pandas
pip install copy
```
### Don't forget to change the folder path in cohesion_specificity.py for dir and home_dir

The format of the data is tab delimited csv files with index (below trans_info) and instructions (instruction_segment) 
where, each of it is expanded to consequitive rows with segments as indicated in the example below. 

trans_info	instruction_segment

0	 mok move right 

0	 move four feet 

0	 turn left 

0	 move seven feet 

### After this we apply dependency parsing using SPACY. 
### Then we calculate cohesion and informativeness equations. 

### Usage 
As a loss function for generating informative natural language and to analyse syntactically cohesive instances of natural language.

