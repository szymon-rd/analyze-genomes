from Queries import createIntervalTable
from Genomes import find_people_for_gene, available_genes
import inquirer

createIntervalTable()

query_gene_option = "Query for a gene in available human genomes"
list_genes_option = "List genes in a selected human genome"
exit_option = "Exit"


def cli_menu():
    menu_q = [
    inquirer.List('select_opt',
                    message="Select the task",
                    choices=[query_gene_option, list_genes_option, exit_option],
                ),
    ]
    menu_answer = inquirer.prompt(menu_q)['select_opt']
    if menu_answer == query_gene_option:
        query_for_gene()
        cli_menu()
    elif menu_answer == list_genes_option:
        list_genes()
        cli_menu()
    elif menu_answer == exit_option:
        exit()
    

def query_for_gene():
    questions = [
    inquirer.List('gene_name',
                    message="What gene do you want to query for? (n = " + str(len(available_genes)) + ")",
                    choices=available_genes,
                ),
    ]
    answer = inquirer.prompt(questions)

    find_people_for_gene(answer['gene_name'])

def list_genes():
    print("xd")

cli_menu()