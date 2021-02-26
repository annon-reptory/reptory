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

 - Dataset comprises of named based bug patterns
    - Swapped function arguments
    - Wrong binary operator
    - Wrong operand in binary operation
  
Framework:
 - A framework where researchers can incorporate additional context and use on the existing dataset.

### Prerequisites

- Install conda
    ```
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O ~/miniconda.sh
    bash ~/miniconda.sh -b -p $HOME/miniconda
    conda init
    source ~/miniconda/bin/activate
    source ~/.bash_profile
    ```

- Setup environment

    ```
    conda create -n reptory python=3.6` 
    conda activate reptory
    pip install tensorflow==1.5

- Install node dependencies:
    ```
    cd src
    node install
    ```    

### Dataset
You can download DataSet from http://www.mediafire.com/file/4slt3qi90jabfre/dataset.zip/file

| Buggy                                                                                      | Fixed                                                                                                             | Dataset Generation Script                                                                                      |
|--------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| Word tokenization                                                                          | Word tokenization                                                                                                 | data_word_level_esprima.sh                                                                                     |
| Deepbugs Representation                                                                    | Deepbugs Representation                                                                                           | data_word_level_deepbugs.sh                                                                                    |
| Deepbugs Representation (with Types Incomplete with variable value)                        | Deepbugs Representation (with Types Incomplete with variable value)                                               | data_word_level_deepbugs_with_type_and_variable.sh                                                             |
| Deepbugs Representation (with Types Incomplete without variable value)                     | Deepbugs Representation (with Types Incomplete without variable value)                                            | data_word_level_deepbugs_with_type.sh                                                                          |
| Code Simplification (Signatures)                                                           | Code Simplification (Signatures)                                                                                  | data_word_level_synthesized.sh                                                                                 |
| Code Simplification (Signatures with position anchor)                                      | Code Simplification (Signatures with position anchor)                                                             | data_word_level_synthesized_with_anchor.sh                                                                     |
| Code Simplification (Signatures with LIT/ID)                                               | Code Simplification (Signatures with LIT/ID)                                                                      | data_word_level_synthesized_with_ID_LIT.sh                                                                     |
| Code Simplification (Signatures with position anchor and LIT/ID)                           | Code Simplification (Signatures with position anchor and LIT/ID)                                                  | data_word_level_synthesized_with_anchor_with_ID_LIT.sh                                                         |
| AST (of original code)	                                                                 | AST (of original code)                                                                                            | data_word_level_ast.sh                                                                                         |
| AST (of code simplification -> Type with variable value)	                                 | AST (of code simplification -> Type with variable value)                                                          | data_word_level_synthesized_with_variable_ast.sh                                                               |
| AST (of code simplification -> Types without variable value)	                             | AST (of code simplification -> Types without variable value)                                                      | data_word_level_synthesized_without_variable_ast.sh                                                            |

### Mixed Representations
| Buggy                                                                                      | Fixed                                                                                                             | Dataset Generation Script                                                                                      |
|--------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
|Code Simplification (function signatures with LIT/ID)                                       |AST (of code simplification -> Types without variable value)                                                       |data_word_level_synthesized_with_ID_LIT_to_data_word_level_synthesized_without_variable_ast.sh                  |
|AST (of code simplification -> Types without variable value)                                |Code Simplification (function signatures with LIT/ID)                                                              |data_word_level_synthesized_without_variable_ast_to_data_word_level_synthesized_with_ID_LIT.sh                  | 
|Word tokenization                                                                           |AST                                                                                                                |data_word_level_esprima_to_data_word_level_ast.sh                                                               |
|AST                                                                                         |Word tokenization                                                                                                  |data_word_level_ast_to_data_word_level_esprima.sh                                                               |

### Generate Embedding
| Embedding       | Script                          |
|-----------------|---------------------------------|
| word2Vec        | getEmbeddings.sh                |
| fastText        | getEmbeddingsFastText.sh        |

#### How to calculate Accuracy and Rank

python parse_results_1_beam.py test.correct test.buggy model.output



