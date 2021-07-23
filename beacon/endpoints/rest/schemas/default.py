from beacon.utils.json import jsonb
import logging
import re
import json

from .... import conf

under_pat = re.compile(r'_([a-z])')

LOG = logging.getLogger(__name__)

def remove_nulls(j):
    if isinstance(j, list):
        jj = [remove_nulls(v) for v in j]
        return jj if jj else None
    elif isinstance(j, dict):
        jj = {}
        for k, v in j.items():
            vv = remove_nulls(v)
            if vv:
                jj[k] = vv
        return jj if jj else None
    elif isinstance(j, jsonb):
        jj = json.loads(j)
        return remove_nulls(jj)
    else:
        return j if j else None

def snake_case_to_camelCase(j):
    return j if j is None else json.loads(under_pat.sub(lambda x: x.group(1).upper(), j))

def beacon_info_v30(datasets, authorized_datasets=[]):
    return remove_nulls({
        'id': conf.beacon_id,
        'name': conf.beacon_name,
        'apiVersion': conf.api_version,
        'environment': conf.environment,
        'organization': {
            'id': conf.org_id,
            'name': conf.org_name,
            'description': conf.org_description,
            'address': conf.org_adress,
            'welcomeUrl': conf.org_welcome_url,
            'contactUrl': conf.org_contact_url,
            'logoUrl': conf.org_logo_url,
            'info': conf.org_info,
        },
        'description': conf.description,
        'version': conf.version,
        'welcomeUrl': conf.welcome_url,
        'alternativeUrl': conf.alternative_url,
        'createDateTime': conf.create_datetime,
        'updateDateTime': conf.update_datetime,
        'serviceType': conf.service_type,
        'serviceUrl': conf.service_url,
        'entryPoint': conf.entry_point,
        'open': conf.is_open,
        'datasets': [beacon_dataset_info_v30(row, authorized_datasets) for row in datasets],
        'info': None,
    })


def beacon_dataset_info_v30(row, authorized_datasets=[]):
    dataset_id = row['stable_id']
    is_authorized = dataset_id in authorized_datasets

    return remove_nulls({
        'id': dataset_id,
        # TODO: Remove default
        'name': row['name'] if row['name'] else 'Default name',
        'description': row['description'],
        'assemblyId': row['reference_genome'],
        'createDateTime': row['created_at'].strftime(conf.datetime_format) if row['created_at'] else None,
        'updateDateTime': row['updated_at'].strftime(conf.datetime_format) if row['updated_at'] else None,
        'dataUseConditions': None,
        'version': None,
        'variantCount': row['variant_count'],
        'callCount': row['call_count'],
        'sampleCount': row['sample_count'],
        'externalURL': None,
        'handovers': row['handovers'],
        'info': {
            'accessType': row['access_type'],
            'authorized': True if row['access_type'] == 'PUBLIC' else is_authorized,
            'datasetSource': row['dataset_source'],
            'datasetType': row['dataset_type']
        }
    })


def beacon_variant_v30(row):
    return remove_nulls({
            'variantId': str(row['variant_id']),
            'assemblyId': row['assembly_id'],
            # TODO: Remove default
            'refseqId': row['refseq_id'] if row['refseq_id'] else 'Unknown',
            'start': [row['start']] if isinstance(row['start'], int) else row['start'],
            'end': [row['end']] if isinstance(row['end'], int) else row['end'],
            'ReferenceBases': row['reference'],
            'AlternateBases': row['alternate'],
            'variantType': row['variant_type'],
        })


def beacon_variant_annotation_v30(row):
    genomic_features_ontology = json.loads(row['genomic_features_ontology'])
    for gf in genomic_features_ontology:
        if gf['class'] == 'ENSGLOSSARY:0000002':
            gf['class'] = 'gene'
        elif gf['class'] == 'ENSGLOSSARY:0000003':
            gf['class'] = 'protein coding transcript'
        elif gf['class'] == 'ENSGLOSSARY:0000029':
            gf['class'] = 'non-coding transcript'
        elif gf['class'] == 'ENSGLOSSARY:0000077':
            gf['class'] = 'untranslated region'

    return remove_nulls({
            'variantId': str(row['variant_id']),
            'variantAlternativeId': [row['alternative_id']],
            'genomicHGVSId': row['genomic_hgvs_id'],
            'transcriptHGVSId': row['transcript_hgvs_ids'],
            'proteinHGVSId': row['protein_hgvs_ids'],
            'genomicRegion': row['genomic_regions'],
            'genomicFeatures': genomic_features_ontology,
            'annotationToolVersion': 'SnpEffVersion=5.0d (build 2021-01-28 11:39)',
            'molecularEffect': row['molecular_effects'],
            #'molecularConsequence': row['molecular_consequence'],
            'aminoacidChange': row['aminoacid_changes'],
            'info': {
                'aaref': row['aaref'],
                #'aapos': row['aapos'],
                'aaalt': row['aaalt'],
                'aa_pos_aa_length': row['functional_classes'],
                'rank': row['exon_ranks'],
                'annotation_impact': row['genomic_regions']
            }
        })

def beacon_biosample_v30(row):
    return remove_nulls( {
        'biosampleId': row['biosample_stable_id'],
        'individualId': row['individual_stable_id'],
        'description': row['description'],
        # TODO: Remove default
        'biosampleStatus': row['biosample_status_ontology'] if row['biosample_status_ontology'] else 'EFO:0009655',
        'collectionDate':  str(row['collection_date']) if row['collection_date'] else None,
        'subjectAgeAtCollection': row['individual_age_at_collection'],
        'sampleOriginType': json.loads(row['sample_origins_ontology'])[0]['sampleOriginType'],
        'sampleOriginDetail': json.loads(row['sample_origins_ontology'])[0]['sampleOriginDetail'],
        'obtentionProcedure': row['obtention_procedure_ontology'],
        'cancerFeatures': {
            'tumorProgression': row['tumor_progression_ontology'],
            'tumorGrade': row['tumor_grade_ontology'],
        },
        'handovers': row['handovers'],
        'info': {
            'alternativeIds': row['alternative_ids'],
            'studyId': row['study_id'],
            'bioprojectId': row['bioproject_id'],
            'files': row['files'],
        }
    } )

def beacon_individual_v30(row):
    return remove_nulls({
        'individualId': row['individual_stable_id'],
        'taxonId': row['taxon_id'],
        'sex': 'NCIT:C46113' if row['sex_ontology'] == 'PATO:0000384' else 'NCIT:C46112',
        'ethnicity': row['ethnicity_ontology'],
        'geographicOrigin': row['geographic_origin_ontology'],
        'phenotypicFeatures': row['phenotypic_features'],
        'diseases': row['diseases'],
        'pedigrees': row['pedigrees'],
        'handovers': row['handovers'],
        'treatments': None,
        'interventions': row['interventions'],
        'measures': row['measures'],
        'exposures': row['exposures'],
        'info': {
            'sraFamilyId': row['sra_family_id'],
            'alternativeIds': row['alternative_ids'],
            'race': row['race'],
            'weightKg': row['weight_kg'],
            'heightCm': row['height_cm'],
            'bloodType': row['blood_type'],
            'medications': row['medications'],
            'procedures': row['procedures'],
        },
    })


def beacon_cohort_v31(row):
    return remove_nulls ({
        'cohortId': str(row['id']),
        'cohortName': row['cohort_name'],
        'cohortType': row['cohort_type'],
        'cohortDesign': row['cohort_design'],
        'cohortInclusionCriteria': row['cohort_inclusion_criteria'],
        'cohortExclusionCriteria': row['cohort_exclusion_criteria'],
        'cohortLicense': row['cohort_license'],
        'cohortContact': row['cohort_contact'],
        'cohortRights': row['cohort_rights'],
        'cohortSize': row['cohort_size'],
        'cohortDataTypes': row['cohort_data_types'],
        'collectionEvents': row['collection_events'],
    })

def beacon_run_v40(row):
    return remove_nulls({
        'runId': str(row['run_id']),
        'biosampleId': row['biosample_id'],
        'runDate': row['run_date'],
        'librarySource': row['library_source'],
        'libraryStrategy': row['library_strategy'],
        'librarySelection': row['library_selection'],
        'libraryLayout': row['library_layout'],
        'platform': row['platform'],
        'platformModel': row['platform_model']
    })

def beacon_analysis_v40(row):
    return remove_nulls({
        'analysisId': row['id'],
        'runId': row['run_id'],
        'analysisDate': row['analysis_date'],
        'pipelineName': row['pipeline_name'],
        'pipelineRef': row['pipeline_ref'],
        'aligner': row['aligner'],
        'variantCaller': row['variant_caller']
    })

def beacon_variant_in_sample_v40(row):
    return remove_nulls({
        'variantId': row['id'],
        'analysisId': row['analysis_id'],
        'biosampleId': row['biosample_id'],
        'variantFrequency': row['variant_frequency'],
        'zigosity': row['zigosity'],
        'alleleOrigin': row['allele_origin'],
        'phenotypicEffects': row['phenotypic_effects'],
        'clinicalRelevances': row['clinical_relevances']
    })

def beacon_variant_interpretation_v40(row):
    return remove_nulls({
        'variantId': row['variant_id'],
        'datasetId': row['dataset_id'],
        'phenotypicEffects': row['phenotypic_effects'],
        'clinicalRelevances': row['clinical_relevances']
    })

def beacon_interactor_v40(row):
    result = remove_nulls({
        'individualId': row['stable_id'],
        'taxonId': row['taxon_id'],
        'sex': row['sex'],
        'ethnicity': row['ethnicity'],
        'geographicOrigin': row['geographic_origin'],
        'phenotypicFeatures': None,
        'diseases': None,
        'pedigrees': None,
        'handovers': None,
        'treatments': None,
        'interventions': None, 
        'measures': None,
        'exposures': None,
        'info': {
            'sraFamilyId': row['sra_family_id'],
            'alternativeIds': row['alternative_ids'],
            'race': row['race'],
            'weightKg': row['weight_kg'],
            'heightCm': row['height_cm'],
            'bloodType': row['blood_type'],
            'medications': row['medications'],
            'procedures': row['procedures'],
        },
    })
    result['relationType'] = row['relation_type']
    return result
