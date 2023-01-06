from Queries import queryPeopleForGene

available_genes = ['APC', 'ATM', 'BMPR1A', 'BRCA1', 'BRCA2', 'CDK4',
    'CDKN2A', 'CREBBP', 'EGFR', 'EP300', 'ETV6', 'FHIT', 'FLT3',
    'HRAS', 'KIT', 'MET', 'MLH1', 'NTRK1', 'PAX8', 'PDGFRA',
    'PPARG', 'PRCC', 'PRKAR1A', 'PTEN', 'RET', 'STK11',
    'TFE3', 'TGFB1', 'TGFBR2', 'TP53', 'WWOX']

available_humans = ['NA12878', 'NA12892', 'NA12877', 'NA12889', 'NA12890']

def find_people_for_gene(gene):
    matches = queryPeopleForGene(gene)
    people_matches = {}
    for m in matches:
        call_name = m['call_name']
        if call_name in people_matches:
            people_matches[call_name] = people_matches[call_name] + 1
        else:
            people_matches[call_name] = 1
    
    if len(people_matches) > 0:
        print("Matches for " + gene + " found in:")
        for call, count in people_matches.items():
            print("\t" + call + ", Count: " + str(count))
    else:
        print("No matches found for " + gene + "!")

    