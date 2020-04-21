import spacy
nlp = spacy.load('en_core_web_sm')
import matplotlib.pyplot as plt
from spacy.tokenizer import Tokenizer
import re
import glob, os
import pandas as pd
from copy import deepcopy


class CohesionFromDepTree():

    def __init__(self):
        self.dir = '/home/maitreyee/Development/informativeness/data_metrics'
        self.home_dir = '/home/maitreyee/Development/informativeness/data/'
        self.all_lefts = []
        self.all_rights = []
        self.total_words = []


    def merge_all_corpora(self, filepath):
        coded_files = glob.glob(os.path.join(filepath + "P*S*C*d.txt"))
        ntcoded_files = glob.glob(os.path.join(filepath + "P*S*y.txt"))
        all_files = coded_files + ntcoded_files
        li = []
        for filename in all_files:
            df = pd.read_csv(filename, index_col =None, header = None, sep='\r')
            li.append(df)
        frame = pd.concat(li, axis=0, ignore_index=True)
        frame.columns = ['Instruction']
        infrmtvnss_data = 'Teamtalk.csv'
        frame.to_csv(os.path.join(self.dir+infrmtvnss_data))


    def clean_inst(self):
    # read the file, define the home directory and the filename
        filename = 'exploded_id_nullvals2.csv'
        exploded = pd.read_csv(os.path.join(self.home_dir,filename), sep = '\t')
        #select the pandas columns that are important
        selected_data = deepcopy(exploded.loc[:, ['trans_info',
                                                  'instruction_segment']])
    # clean the dataset remove null columns,
    # remove characters between # <>,
    # remove special characters and symbols \ls\.
        clean_df = selected_data.dropna(thresh=2)
        cleaned_df = pd.DataFrame()
        cleaned_df['cleaned_inst_segment'] = clean_df['instruction_segment']\
            .astype(str).str.lstrip().str.rstrip().\
            str.replace(r"\<[^)]*\>", "", regex=True).\
            str.replace(r"\#[^)]*\#", "", regex=True).\
            str.replace("\/[^)]*\/","", regex=True).\
            str.replace(r'[^\s\w]','',regex=True)
        cleaned_df['index'] = clean_df['trans_info']
        cleaned_df.to_csv(os.path.join(self.home_dir,'cleaned_inst1.csv'), sep = '\t')


    def parseDepLTree(self):

        children = []
        df = pd.read_csv(os.path.join(self.home_dir,'cleaned_inst1.csv'),sep = '\t')
        instruct = list(filter(None, df['cleaned_inst_segment'].astype(
            str).str.lstrip().str.rstrip().values))
        print(instruct[0:10])
        for inst in instruct:
            doc2 = nlp(inst)
            for sent in doc2.sents:
                tmp1, tmp2, tmp4, tmp5, posK, posP = [], [], [], [], [], []
                tmp3, tmp6, tmp8, tmp9 = [], [], [], []
                for sent2 in sent:
                    info = [child for child in sent2.children]
                    if len(info) > 1:
                        tmp1.append(len(set(info)))  # depK_count
                        tmp4.append(set(info))  # depK
                        tmp3.append(sent2.head.text)  # headK
                        head = [sent2.head.text]
                        tmp8.append(len(set(head)))  # headK_count
                        posK = [sent2.head.pos_]
                    elif len(info) == 1:
                        tmp2.append(len(set(info)))  # depP_count
                        tmp5.append(set(info))  # depP
                        tmp6.append(sent2.head.text)  # headP
                        head1 = [sent2.head.text]
                        tmp9.append(len(set(head1)))  # headP_count
                        # head = [sent2.head.text]
                        posP = [sent2.head.pos_]
                children.append(
                    [sent, len(sent), tmp1, tmp4, tmp3, tmp8, posK, tmp2, tmp5,
                     tmp6, tmp9, posP])
        parsedTree = pd.DataFrame(children, columns=[
            'segments', 'length_segment', 'dep_count_k',
            'dependents_k', 'head_k', 'head_kLength',
            'posK', 'dep_count_p', 'dependents_p', 'head_p',
            'head_pLength', 'posP'])
        parsedTree.to_csv(os.path.join(
            self.home_dir,'parsed_tree_data.csv'), sep='\t')
        return children


    def cohesionCalculate(self):
 #       cleandf = self.clean_inst()
        treedf = self.parseDepLTree()
        parsedTree = pd.DataFrame(treedf)
        parsedTree.columns=['segments', 'length_segment',
                             'dep_count_k','dependents_k', 'head_k',
                             'head_kLength',
                             'posK', 'dep_count_p', 'dependents_p',
                             'head_p','head_pLength', 'posP']
        df_index = pd.read_csv(os.path.join(self.home_dir,
                                            'cleaned_inst1.csv'), sep = '\t')
        parsedTree['index'] = df_index['index']
        parsedLtree = deepcopy(parsedTree)
        print(parsedLtree.info())
        parsedLtree['depSum_p'] = parsedLtree.dep_count_p.apply(lambda x: sum(x))
        parsedLtree['depSum_k'] = parsedLtree.dep_count_k.apply(lambda x: sum(x))
        parsedLtree['headSum_p'] = parsedLtree.head_pLength.apply(lambda x: sum(x))
        parsedLtree['headSum_k'] = parsedLtree.head_kLength.apply(lambda x: sum(x))
        ####pervious version of the cohesion metric
        parsedLtree['cohesion_V1'] = (((parsedLtree['depSum_k'])*(parsedLtree['headSum_k']))
                                      - ((parsedLtree['depSum_p'])*(parsedLtree['headSum_p'])))
        #####current and simplified version of cohesion metric
        parsedLtree['cohesion'] = (
        (parsedLtree['depSum_k']) - (parsedLtree['depSum_p']))
        ######for finding out below we can use any of the version of cohesion above
        parsedLtree['cohesion_norm'] = round(
        parsedLtree.cohesion / (parsedLtree['length_segment']), 2)

        parsedLtree['ifmt'] = parsedLtree.groupby('index')['cohesion'].sum()
        parsedLtree['inst_len'] = parsedLtree.groupby('index')['length_segment'].sum()
        parsedLtree['ifmt_norm'] = round((parsedLtree['ifmt'])/(parsedLtree['inst_len']),2)


        df_cohesion = deepcopy(parsedLtree)

        df_cohesion.to_csv(os.path.join(self.dir + '/dfCohInf_allMet.csv'), sep='\t')


if __name__ == "__main__":
    depTree = CohesionFromDepTree()
    findCohesion = depTree.cohesionCalculate()
