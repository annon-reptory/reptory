# Reptory
This repository provides a dataset along with a framework to assist comparative experimental studies on learning-based automated program repair.

## Dataset:
- Dataset is based upon Deepbugs. The following files in the create-dataset/ folder that are in charge of data extraction are borrowed from DeepBugs although we changed them accordingly:
    - extractFromJS.js
    - extractorOfBinOps.js
    - extractorOfCalls.js
    - fileIDs.json
    - jsExtractionUtil.js
    - Util.py

- Dataset comprises of named based bug patterns:
    - Swapped function arguments
    - Wrong binary operator
    - Wrong operand in binary operation

Framework:
    - A framework where researchers can incorporate additional context and use on the existing dataset.

# Prerequisites

- Install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html)
    ```
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O ~/miniconda.sh
    bash ~/miniconda.sh -b -p $HOME/miniconda
    conda init
    source ~/miniconda/bin/activate
    source ~/.bash_profile
    ```

- Setup environment 
   
  - Install conda:
    ```
    conda create -n context_ml python=3.6 
    conda activate context_ml
    conda install -y python=3.6    
    ```
  - Install tensorflow using `pip`: `pip install tensorflow==1.5` 
  - Install tensorflow using `conda`: `conda install -y -c conda-forge tensorflow=1.5.1`
  
  - Required `python` packages for embedding generation: 
    ```
       conda install -c anaconda nltk
       conda install -c anaconda gensim
    ```
    Detailed:
    ```
      conda install -c anaconda nltk
            
      import nltk
      nltk.download('punkt')
      [nltk_data] Downloading package punkt to /Users/UserName/nltk_data...
      [nltk_data]   Unzipping tokenizers/punkt.zip.
    ```
    
  - Install `nvm` and `npm`:
    ```
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
        source .bashrc
        nvm install --lts
        nvm use --lts
    ```
  - Install node dependencies:
    ```
      cd src
      npm install
    ```

### Dataset
- Download [dataSet](http://www.mediafire.com/file/4slt3qi90jabfre/dataset.zip/file)

# Dataset

# Code Representations
| ID    |Buggy                                                                                       | Fixed                                                                                                             | Dataset Generation Script                                                                                      |
|-------|--------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| 1a    | Word tokenization                                                                          | Word tokenization                                                                                                 | data_word_level_esprima.sh                                                                                     |
| 1b    | Word tokenization Enhanced                                                                 | Word tokenization Enhanced                                                                                        | data_word_level_word_tokenization_enhanced.sh                                                                                     |
| 2     | Deepbugs Representation                                                                    | Deepbugs Representation                                                                                           | data_word_level_deepbugs.sh                                                                                    |
| 3     | Deepbugs Representation (with Types Incomplete with variable value)                        | Deepbugs Representation (with Types Incomplete with variable value)                                               | data_word_level_deepbugs_with_type_and_variable.sh                                                             |
| 4     | Deepbugs Representation (with Types Incomplete without variable value)                     | Deepbugs Representation (with Types Incomplete without variable value)                                            | data_word_level_deepbugs_with_type.sh                                                                          |
| 5     | Code Simplification (Signatures)                                                           | Code Simplification (Signatures)                                                                                  | data_word_level_synthesized.sh                                                                                 |
| 6     | Code Simplification (Signatures with position anchor)                                      | Code Simplification (Signatures with position anchor)                                                             | data_word_level_synthesized_with_anchor.sh                                                                     |
| 7     | Code Simplification (Signatures with LIT/ID)                                               | Code Simplification (Signatures with LIT/ID)                                                                      | data_word_level_synthesized_with_ID_LIT.sh                                                                     |
| 8     | Code Simplification (Signatures with position anchor and LIT/ID)                           | Code Simplification (Signatures with position anchor and LIT/ID)                                                  | data_word_level_synthesized_with_anchor_with_ID_LIT.sh                                                         |
| 9     | AST (of original code)	                                                                 | AST (of original code)                                                                                            | data_word_level_ast.sh                                                                                         |
| 10    | AST (of code simplification -> Type with variable value)	                                 | AST (of code simplification -> Type with variable value)                                                          | data_word_level_synthesized_with_variable_ast.sh                                                               |
| 11    | AST (of code simplification -> Types without variable value)	                             | AST (of code simplification -> Types without variable value)                                                      | data_word_level_synthesized_without_variable_ast.sh                                                            |
| 12    | Preorder AST (of original code)                                                            | Preorder AST (of original code)                                                                                   | prepare_calls_ast_preorder.sh                                                                                  |
| 13    | Abstraction - Tufano                                                                       | Abstraction - Tufano                                                                                              | prepare_calls_abstraction.sh                                                                                   |

# Mixed Representations
| Buggy                                                                                      | Fixed                                                                                                             | Dataset Generation Script                                                                                      |
|--------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
|Code Simplification (function signatures with LIT/ID)                                       |AST (of code simplification -> Types without variable value)                                                       |data_word_level_synthesized_with_ID_LIT_to_data_word_level_synthesized_without_variable_ast.sh                  |
|AST (of code simplification -> Types without variable value)                                |Code Simplification (function signatures with LIT/ID)                                                              |data_word_level_synthesized_without_variable_ast_to_data_word_level_synthesized_with_ID_LIT.sh                  | 
|Word tokenization                                                                           |AST                                                                                                                |data_word_level_esprima_to_data_word_level_ast.sh                                                               |
|AST                                                                                         |Word tokenization                                                                                                  |data_word_level_ast_to_data_word_level_esprima.sh                                                               |


| Buggy                                                                                      | Fixed                                                                                                             | Dataset Generation Script                                                                                      |
|--------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
|                                                                                            |                                                                                                                   |prepare_calls_tufano_abstraction_to_code_simplification_signatures_with_position_anchor.sh                      |
|                                                                                            |                                                                                                                   |prepare_code_simplification_signatures_with_position_anchor_to_calls_tufano_abstraction.sh                      |

# Generate Embedding
| Embedding           | Script                                               |
|---------------------|------------------------------------------------------|
| word2Vec-CBOW       | getEmbeddings.sh                                     |
| word2Vec-SkipGram   | get-embedding-final-skipgram.sh                      |
| fastText            | get-embedding-fasttext-final.sh                      |
| gloVe               | cd glove && make && getEmbeddings_glove.sh           |

# Experiments for Embedding
| Embedding           | Script                                                                                                                                            |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| word2Vec-SkipGram   | prepare_calls_abstraction_word2vec_skipgram.sh                                                                                                    |
| fastText            | prepare_calls_abstraction_fasttext.sh                                                                                                             |
| gloVe               | run `prepare_calls_abstraction_glove.sh` and then `cd GloVe && make && getEmbeddings_glove.sh`. Finally run `./train-final-save-log.sh`           |

# How to calculate Accuracy and Rank?
`python calculate_accuracy_and_rank.py test.correct test.buggy model.output`

# Raw Results for Swapped Arguments, Wrong Binary Operator, Wrong Binary Operands.

- [Table 5 - Swapped Arguments](./results/Swapped&#32;Arguments.xlsx)
- [Table 6 - Wrong Binary Operator](./results/Wrong&#32;Binary&#32;Operator.xlsx)
- [Table 7 - Wrong Binary Operands](./results/Wrong&#32;Binary&#32;Operands.xlsx)
