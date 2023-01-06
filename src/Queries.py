from google.cloud import bigquery


client = bigquery.Client()

createIntervalTableQuery = """
    CREATE TABLE `genomics.geneIntervalTable` AS (
    SELECT
    Gene,
    Chr,
    MIN(Start) AS gene_start,
    MAX(`End`) AS gene_end,
    MIN(Start)-100000 AS region_start,
    MAX(`End`)+100000 AS region_end
    FROM
    `silver-wall-555.TuteTable.hg19`
    WHERE
    Gene IN ('APC', 'ATM', 'BMPR1A', 'BRCA1', 'BRCA2', 'CDK4',
    'CDKN2A', 'CREBBP', 'EGFR', 'EP300', 'ETV6', 'FHIT', 'FLT3',
    'HRAS', 'KIT', 'MET', 'MLH1', 'NTRK1', 'PAX8', 'PDGFRA',
    'PPARG', 'PRCC', 'PRKAR1A', 'PTEN', 'RET', 'STK11',
    'TFE3', 'TGFB1', 'TGFBR2', 'TP53', 'WWOX')
    GROUP BY
    Chr,
    Gene );
"""

def _intervalTableExists():
    from google.cloud.exceptions import NotFound
    try:
        client.get_table(client.dataset("genomics").table("geneIntervalTable"))
        return True
    except NotFound:
        return False

def createIntervalTable():
    if not _intervalTableExists():
        result = client.query(createIntervalTableQuery)
        print("Table created")
        print(result.result())
    else:
        print("Table already exists, proceeding")
    
def queryPeopleForGene(gene):
    geneQuery = prepareDatasets + peopleForGene.replace("$x", gene)
    result = client.query(geneQuery)
    return result.result()

prepareDatasets = """
#standardSQL
WITH

  variants AS (
  SELECT
    REPLACE(reference_name, 'chr', '') as reference_name,
    call[OFFSET(0)].name AS call_name,
    start_position,
    end_position,
    reference_bases,
    alternate_bases.alt AS alt,
    (SELECT COUNTIF(gt = alt_offset+1) FROM v.call call, call.genotype gt) AS num_variant_alleles,
    (SELECT COUNTIF(gt >= 0) FROM v.call call, call.genotype gt) AS total_num_alleles
  FROM
    `bigquery-public-data.human_genome_variants.platinum_genomes_deepvariant_variants_20180823` v,
    UNNEST(v.alternate_bases) alternate_bases WITH OFFSET alt_offset ),

  gene_variants AS (
  SELECT
    call_name,
    reference_name,
    start_position,
    reference_bases,
    alt,
    num_variant_alleles,
    total_num_alleles,
    Gene
  FROM
    variants
  INNER JOIN
    `genomics.geneIntervalTable` AS intervals ON
    variants.reference_name = intervals.Chr
    AND intervals.region_start <= variants.start_position
    AND intervals.region_end >= variants.end_position )
"""

peopleForGene = """
SELECT DISTINCT
  call_name,
  Chr,
  annots.Start AS Start,
  Ref,
  annots.Alt,
  Func,
  vars.Gene,
  PopFreqMax,
  ExonicFunc,
  num_variant_alleles,
  total_num_alleles
FROM
  `silver-wall-555.TuteTable.hg19` AS annots
INNER JOIN
  (SELECT * FROM gene_variants WHERE gene_variants.Gene = '$x') AS vars
ON
  vars.reference_name = annots.Chr
  AND vars.start_position = annots.Start
  AND vars.reference_bases = annots.Ref
  AND vars.alt = annots.Alt
ORDER BY
  Chr,
  Start;
"""