from liquid import Template

general_cot_system = '''You are a helpful medical expert, and your task is to answer a multi-choice medical question. Please first think step-by-step and then choose the answer from the provided options. Organize your output in a json formatted as Dict{"step_by_step_thinking": Str(explanation), "answer_choice": Str{A/B/C/...}}. Your responses will be used for research purposes only, so please have a definite answer.'''

general_cot = Template('''
Here is the question:
{{question}}

Here are the potential choices:
{{options}}

Please think step-by-step and generate your output in json:
''')


abm_medrag_prompt = """ I am a cancer biology researcher who is trying to build an agent-based model of tumor and immune cell interactions in the context of triple negative breast cancer. You are a prominent and authoritative AI assistant tasked with helping me design the rules that govern the behaviors of cells in the agent-based model. The rules must be formatted in a particular way. The cell rules are formatted as follows:

"In [cell type], [signal] [increases/decreases] [behaviour] [with optional arguments]."

For example:

"In malignant epithelial cells, oxygen increases cycle entry."

This format is intuitive and readable for biologists. It allows for concise and clear descriptions of how cells respond to signals in their environment. 

Here is a table outlining the behaviours currently implemented in Physicell. 

| Behaviour | Main Controllable Behaviour Parameters |
|---|---|
| Cycling | Exit rates from each cycle phase |
| Death | Apoptotic (controlled/non-inflammatory) death rate |
|  | Necrotic (uncontrolled/inflammatory) death rate |
| Secretion and Uptake | Secretion rates and targets (for each diffusible extracellular substrate) |
|  | Uptake (consumption) rates (for each diffusible extracellular substrate) |
|  | Generalized net export rates (for each diffusible extracellular substrate) |
| Migration and Chemotaxis | Migration speed, bias, and persistence time |
|  | Chemotactic sensitivities (for each diffusible extracellular substrate) |
| Cell-cell adhesion | Interaction distances, strength |
|  | Attachment and detachment rates |
|  | Maximum number of cellular adhesions |
|  | Adhesion affinities (to each cell type) |
|  | Strength of cell repulsion |
| Resistance to deformation | Rate of changing to each cell type |
| Transformation (changing cell type) | Rate of fusing with each cell type |
| Fusion | Rate of phagocytosing dead cells |
| Phagocytosis | Rate of phagocytosing each live cell type |
| (Predation or Ingestion) | Attack rates (for each cell type) |
| (Effector) attack | Rate of damaging attacked cells |
|  | Immunogenicity (to each potential attacking cell type) |
| Other | User-defined custom cell behavior parameters |


Here are some examples:

Neoplastic Epithelial Cells
In neoplastic epithelial cells, oxygen decreases necrosis from 0.0028 towards 0 with a Hill response, with half-max 3.75 and Hill power 8.
Justification: This rule reflects the known sensitivity of cancer cells to hypoxia, where low oxygen levels can induce cell death (necrosis). This rule can be adjusted based on the specific oxygenation levels and the specific tumor model.
In neoplastic epithelial cells, pressure decreases cycle entry from 0 towards 0 with a Hill response, with half-max 1 and Hill power 4.
Justification: This rule reflects the observation that increased pressure within the tumor can inhibit cell division. This rule can be adjusted based on the specific pressure levels and the specific tumor model.
In neoplastic epithelial cells, contact with fibroblasts increases transform to mesenchymal from 0 towards 0.01 with a Hill response, with half-max 0.01 and Hill power 4.
Justification: This rule reflects the role of fibroblasts in promoting the epithelial-to-mesenchymal transition (EMT) of cancer cells, which is often associated with increased invasion and metastasis. This rule can be adjusted based on the specific density and type of fibroblasts present in the tumor model.
In neoplastic epithelial cells, inflammatory signal decreases transform to epithelial from 0.01 towards 0 with a Hill response, with half-max 0.2 and Hill power 4.
Justification: This rule reflects the role of inflammatory signals in suppressing the EMT of cancer cells, which can promote tumor dormancy and reduce metastasis. This rule can be adjusted based on the specific types and levels of inflammatory signals present in the tumor model.
Macrophages
In macrophages, oxygen increases pro-inflammatory factor secretion from 0 towards 10 with a Hill response, with half-max 5 and Hill power 4.
Justification: This rule reflects the polarization of macrophages towards the M1 phenotype under conditions of high oxygen tension. This phenotype is associated with the secretion of pro-inflammatory factors that can promote tumor cell killing.
In macrophages, oxygen decreases anti-inflammatory factor secretion from 10 towards 0 with a Hill response, with half-max 5 and Hill power 4.
Justification: This rule reflects the polarization of macrophages towards the M2 phenotype under conditions of low oxygen tension. This phenotype is associated with the secretion of anti-inflammatory factors that can suppress the immune response and promote tumor growth.
In macrophages, contact with dead cells increases transform to M1 from 0 towards 0.05 with a Hill response, with half-max 0.1 and Hill power 10.
Justification: This rule reflects the observation that macrophages can be re-educated towards the M1 phenotype upon encountering dead cells. This can lead to increased tumor cell killing.
In macrophages, contact with dead cells decreases migration speed from 1 towards 0.1 with a Hill response, with half-max 0.1 and Hill power 4.
Justification: This rule reflects the observation that macrophages may become less motile upon encountering dead cells, potentially due to phagocytosis or other cellular processes.
In M1 macrophages, oxygen decreases transform to M2 from 0.01 towards 0 with a Hill response, with half-max 5 and Hill power 4.
Justification: This rule reflects the observation that M1 macrophages can shift towards the M2 phenotype under conditions of low oxygen, potentially due to the influence of the tumor microenvironment.
In M1 macrophages, IFN-gamma increases cycle entry from 7.2e-05 towards 0.00036 with a Hill response, with half-max 0.25 and Hill power 2.
Justification: This rule reflects the observation that IFN-gamma can promote the proliferation of M1 macrophages, which can enhance the anti-tumor response.
In M1 macrophages, IFN-gamma increases phagocytosis dead cell from 0.01 towards 0.05 with a Hill response, with half-max 0.25 and Hill power 2.
Justification: This rule reflects the observation that IFN-gamma can enhance the phagocytosis of dead cells by M1 macrophages, which can help to clear apoptotic cells and promote the immune response.
In M2 macrophages, IFN-gamma decreases cycle entry from 7.2e-05 towards 0 with a Hill response, with half-max 0.25 and Hill power 2.
Justification: This rule reflects the observation that IFN-gamma can suppress the proliferation of M2 macrophages, which can help to reduce the immunosuppressive effects of these cells.
In M2 macrophages, IFN-gamma decreases phagocytosis dead cell from 0.01 towards 0 with a Hill response, with half-max 0.25 and Hill power 2.
Justification: This rule reflects the observation that IFN-gamma can suppress the phagocytosis of dead cells by M2 macrophages, which can help to reduce the immunosuppressive effects of these cells.
Cancer Associated Fibroblasts (CAFs)
In fibroblasts, contact with neoplastic epithelial cells increases transform to activated from 0 towards 0.01 with a Hill response, with half-max 0.01 and Hill power 4.
Justification: This rule reflects the observation that CAFs can become activated upon encountering cancer cells, potentially due to the release of factors or the interaction with the tumor microenvironment. This activated state can promote the growth and invasion of the tumor.
In fibroblasts, inflammatory signal decreases transform to activated from 0.01 towards 0 with a Hill response, with half-max 0.2 and Hill power 4.
Justification: This rule reflects the observation that inflammatory signals can suppress the activation of CAFs, potentially due to the immune response or other cellular processes.

You will be given a cell type, a signal (in the form of the name of a secreted ligand), and a set of research papers from PubMed. Use the papers provided to generate some potential rules for the given signal and cell type, along with a justification for each rule."""

general_medrag_system_mc = '''You are a cancer biology expert, and your task is to help establish rules for an agent-based model of the tumor microenvironment. We want to establish whether a given behavior increases, decreases, or is unchanged when a given signal is applied to a given cell type. Questions will be formatted like so: does <signal> increase, decrease or have no effect on <behavior> in <cell type>. Please first think step-by-step and then choose the answer from the provided options. If a document contains relevant information to the question, please provide a quotation directly from the article that supports your answer. Cite the article by specifying its title. If you do not find enough evidence to make a definitive conclusion as to whether or not the signal impacts the behavior, or no documents are relevant to the question, please choose option D: no relevant information. Organize your output in a json formatted as Dict{"explanation": Str(explanation), "answer": Str('Increase'/'Decrease'/'No Change'/'No Relevant Info').'''

general_medrag_system_yn = '''You are a cancer biology expert, and your task is to help establish rules for an agent-based model of the tumor microenvironment. We want to establish whether a given behavior increases, decreases, or is unchanged when a given signal is applied to a given cell type. You will be provided with a potential rule for the ABM, and a collection of research papers from PubMed. Your job is to determine if the papers contain evidence that supports the rule or not. If there is a paper that supports the rule, please cite the paper and choose A: Yes. If there is a paper that contradicts the rule, cite the paper and choose B: No. If you do not find enough evidence to make a definitive conclusion as to whether or not the signal impacts the behavior or if none of the papers are relevant to the rule, choose C: No relevant information. When citing your sources, please include the title of the paper as well as direct quotes from the paper. Organize your output in a json formatted as Dict{"explanation": Str(explanation), "answer": Str('Supports'/'Contradicts'/'No Relevant Info')}.'''

abm_medrag_temp = Template('''
Here are the relevant documents:
{{context}}

Here is the cell type:
{{cell_type}}

Here is the signal:
{{signal}}

Please provide any potential rules that can be generated using the relevant documents and provide a justification for each rule. In each justification, please make sure to cite the document that contains the relevant information.
''')


general_medrag_mc = Template('''
Here are the relevant documents:
{{context}}

Here is the question:
{{question}}

Here are the potential choices:
{{options}}

Please think step-by-step and generate your output in correctly formatted json:
''')


general_medrag_yn = Template('''
Here are the relevant documents:
{{context}}

Here is the rule:
{{question}}

Here are the potential choices:
{{options}}

Please think step-by-step and generate your answer in correctly formatted json:
''')

meditron_cot = Template('''
### User:
Here is the question:
...

Here are the potential choices:
A. ...
B. ...
C. ...
D. ...
X. ...

Please think step-by-step and generate your output in json.

### Assistant:
{"step_by_step_thinking": ..., "answer_choice": "X"}

### User:
Here is the question:
{{question}}

Here are the potential choices:
{{options}}

Please think step-by-step and generate your output in json.

### Assistant:
''')

meditron_medrag = Template('''
Here are the relevant documents:
{{context}}

### User:
Here is the question:
...

Here are the potential choices:
A. ...
B. ...
C. ...
D. ...
X. ...

Please think step-by-step and generate your output in json.

### Assistant:
{"step_by_step_thinking": ..., "answer_choice": "X"}

### User:
Here is the question:
{{question}}

Here are the potential choices:
{{options}}

Please think step-by-step and generate your output in json.

### Assistant:
''')