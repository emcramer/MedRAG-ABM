from src.medrag import MedRAG
import ast
import re

medrag = MedRAG(llm_name="Google/gemini-1.5-flash-latest", rag=True, retriever_name="RRF-2", corpus_name="PubMed")

cell_types = ['cancer associated fibroblasts (CAFs)', 'Macrophages', 'Monocytes', 'CD4+ T Cells', 'CD8+ T Cells', 'Neoplastic Epithelium']
signals = ['Ncam1',
 'Col4a2',
 'Thbs3',
 'Vegfb',
 'Ccl6',
 'ITGA4_ITGB1',
 'Tnxb',
 'Lamb1',
 'Lama2',
 'Col9a3',
 'Lgals9',
 'Osm',
 'Pdgfa',
 'Sema3d',
 'Tgfb2',
 'Icam1',
 'Ccl2',
 'Ccl3',
 'Tnn',
 'Postn',
 'Tnc',
 'ITGAV_ITGB1',
 'Cdh1',
 'Vegfa',
 'Ccl9',
 'App',
 'Lamb2',
 'Ccl7',
 'Pros1',
 'Ccl8',
 'Ptprc',
 'Hspg2',
 'Tnf',
 'Nectin3',
 'Wnt5a',
 'Sema5a',
 'Tgfb3',
 'Fgf7',
 'Col6a2',
 'Sema3c',
 'Cxcl12',
 'Ptn',
 'Cxcl16',
 'Nampt',
 'Cd55',
 'Igf1',
 'Lama4',
 'C3',
 'Mdk',
 'Ccl12',
 'Csf1',
 'Igfbp3',
 'Thbs2',
 'F11r',
 'Col6a1',
 'Thy1',
 'Angptl4',
 'Efnb2',
 'Jam3',
 'Sdc2',
 'Cldn3',
 'Apoe',
 'Col1a1',
 'Col4a5',
 'Agrn',
 'Cadm1',
 'Mpzl1',
 'Efna5',
 'Angptl2',
 'Lair1',
 'Hbegf',
 'Sema3b',
 'Cd6',
 'Fn1',
 'Lpar1',
 'Jag1',
 'Gja1',
 'Gas6',
 'Areg',
 'Tenm3',
 'Sdc1',
 'Efnb1',
 'Cdh2',
 'Col4a1',
 'Thbs1',
 'Lamb3',
 'Mif',
 'Flrt2',
 'Ccl4',
 'Tnfsf12',
 'Tgfb1',
 'Lamc1',
 'Kitl',
 'Spp1',
 'Col6a3',
 'Cd86',
 'Col1a2']

                           
def add_pmids(explanation, snippets):
    doc_refs = re.findall('Document \[[0-9][0-9]?\]', explanation)
    if len(doc_refs) > 0:
        for doc_ref in doc_refs:
            idx = int(doc_ref[doc_ref.index('[')+1:doc_ref.index(']')])
            try:
                explanation = explanation.replace(doc_ref, f"PMID={snippets[idx]['PMID']}")
            except IndexError:
                print(f"tried to retrieve document [{idx}] PMID, but got list out of range, num_snippets={len(snippets)}")
                print(explanation)
    return explanation
    
                            
for cell_type in cell_types:
    for signal in signals:
        query = f"functional experiments of uptake of {signal} in {cell_type} in triple negative breast cancer"
        answer, snippets, scores = medrag.answer(question=query, k=75, abm=True, cell_type=cell_type, signal=signal, save_dir='abm-rules')
            
        
        

