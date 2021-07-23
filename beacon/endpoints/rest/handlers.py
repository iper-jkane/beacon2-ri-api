from ...utils import db
from .response.response_schema import (build_variant_response,
                                       build_biosample_or_individual_response, 
                                       build_cohort_response,
                                       build_run_response,
                                       build_analysis_response,
                                       build_variant_in_sample_response,
                                       build_variant_interpretation_response,
                                       build_interactor_response,
                                       build_variant_annotation_response,
                                       BeaconEntity)
from . import AnalysesParameters, BiosamplesParameters, GVariantsParameters, IndividualsParameters, CohortParameters, RunsParameters, VariantsInSampleParameters, VariantsInterpretationParameters, InteractorsParameters, generic_handler

biosamples_proxy = BiosamplesParameters()
gvariants_proxy = GVariantsParameters()
individuals_proxy = IndividualsParameters()
cohorts_proxy = CohortParameters()
runs_proxy = RunsParameters()
analyses_proxy = AnalysesParameters()
variants_in_sample_proxy = VariantsInSampleParameters()
variants_interpretation_proxy = VariantsInterpretationParameters()
interactors_proxy = InteractorsParameters()

individuals_by_biosample = generic_handler('individuals', BeaconEntity.BIOSAMPLE, individuals_proxy, db.fetch_individuals_by_biosample, db.count_individuals_by_biosample, build_biosample_or_individual_response)
biosamples_by_biosample = generic_handler('biosamples' , BeaconEntity.BIOSAMPLE, biosamples_proxy , db.fetch_biosamples_by_biosample , db.count_biosamples_by_biosample, build_biosample_or_individual_response)
gvariants_by_biosample = generic_handler('gvariants'  , BeaconEntity.BIOSAMPLE, gvariants_proxy  , db.fetch_variants_by_biosample   , db.count_variants_by_biosample, build_variant_response)
runs_by_biosample = generic_handler('runs' , BeaconEntity.BIOSAMPLE, runs_proxy, db.fetch_runs_by_biosample, db.count_runs_by_biosample, build_run_response)
variants_in_sample_by_biosample = generic_handler('variants in sample', BeaconEntity.BIOSAMPLE, variants_in_sample_proxy, db.fetch_variants_in_sample_by_biosample, db.count_variants_in_sample_by_biosample, build_variant_in_sample_response)

individuals_by_variant = generic_handler('individuals', BeaconEntity.VARIANT, individuals_proxy, db.fetch_individuals_by_variant, db.count_individuals_by_variant, build_biosample_or_individual_response)
biosamples_by_variant = generic_handler('biosamples' , BeaconEntity.VARIANT, biosamples_proxy , db.fetch_biosamples_by_variant , db.count_biosamples_by_variant, build_biosample_or_individual_response)
gvariants_by_variant = generic_handler('gvariants'  , BeaconEntity.VARIANT, gvariants_proxy  , db.fetch_variants_by_variant   , db.count_variants_by_variant, build_variant_response)
variants_in_sample_by_variant = generic_handler('variants in sample', BeaconEntity.VARIANT, variants_in_sample_proxy, db.fetch_variants_in_sample_by_variant, db.count_variants_in_sample_by_variant, build_variant_in_sample_response)
variants_interpretations_by_variant = generic_handler('variants interpretation', BeaconEntity.VARIANT, variants_interpretation_proxy, db.fetch_variants_interpretation_by_variant, db.count_variants_interpretation_by_variant, build_variant_interpretation_response)

variants_annotation_by_variant = generic_handler('gvariants'  , BeaconEntity.VARIANT, gvariants_proxy  , db.fetch_variants_by_variant   , db.count_variants_by_variant, build_variant_annotation_response)

individuals_by_individual = generic_handler('individuals', BeaconEntity.INDIVIDUAL, individuals_proxy, db.fetch_individuals_by_individual, db.count_individuals_by_individual, build_biosample_or_individual_response)
biosamples_by_individual = generic_handler('biosamples' , BeaconEntity.INDIVIDUAL, biosamples_proxy , db.fetch_biosamples_by_individual , db.count_biosamples_by_individual, build_biosample_or_individual_response)
gvariants_by_individual = generic_handler('gvariants'  , BeaconEntity.INDIVIDUAL, gvariants_proxy  , db.fetch_variants_by_individual   , db.count_variants_by_individual, build_variant_response)
cohorts_by_individual = generic_handler('cohorts'  , BeaconEntity.INDIVIDUAL, cohorts_proxy  , db.fetch_cohorts_by_individual   , db.count_cohorts_by_individual, build_cohort_response)
interactors_by_individual = generic_handler('interactors'  , BeaconEntity.INDIVIDUAL, interactors_proxy  , db.fetch_interactors_by_individual   , db.count_interactors_by_individual, build_interactor_response)

runs_by_run = generic_handler('runs'  , BeaconEntity.RUN, runs_proxy  , db.fetch_runs_by_run   , db.count_runs_by_run, build_run_response)
biosamples_by_run = generic_handler('biosamples'  , BeaconEntity.RUN, biosamples_proxy  , db.fetch_biosamples_by_run   , db.count_biosamples_by_run, build_biosample_or_individual_response)
analyses_by_run = generic_handler('analyses'  , BeaconEntity.RUN, analyses_proxy  , db.fetch_analyses_by_run   , db.count_analyses_by_run, build_analysis_response)

analyses_by_analysis = generic_handler('analyses'  , BeaconEntity.ANALYSIS, analyses_proxy  , db.fetch_analyses_by_analysis   , db.count_analyses_by_analysis, build_analysis_response)
runs_by_analysis = generic_handler('runs'  , BeaconEntity.ANALYSIS, runs_proxy  , db.fetch_runs_by_analysis   , db.count_runs_by_analysis, build_run_response)

variants_in_sample_by_analysis = generic_handler('variants in sample', BeaconEntity.ANALYSIS, variants_in_sample_proxy, db.fetch_variants_in_sample_by_analysis, db.count_variants_in_sample_by_analysis, build_variant_in_sample_response)
variants_in_sample_by_variants_in_sample = generic_handler('variants in sample', BeaconEntity.VARIANT_IN_SAMPLE, variants_in_sample_proxy, db.fetch_variants_in_sample_by_variants_in_sample, db.count_variants_in_sample_by_variants_in_sample, build_variant_in_sample_response)

variants_interpretations_by_variants_interpretation = generic_handler('variants interpretation', BeaconEntity.VARIANT_INTERPRETATION, variants_interpretation_proxy, db.fetch_variants_interpretations_by_variants_interpretation, db.count_variants_interpretations_by_variants_interpretation, build_variant_interpretation_response)

interactors_by_interactor = generic_handler('interactors', BeaconEntity.INTERACTOR, interactors_proxy, db.fetch_interactors_by_interactor, db.count_interactors_by_interactor, build_interactor_response)
individuals_by_interactor = generic_handler('individuals', BeaconEntity.INTERACTOR, individuals_proxy, db.fetch_individuals_by_interactor, db.count_individuals_by_interactor, build_biosample_or_individual_response)

cohorts_by_cohort = generic_handler('cohorts'  , BeaconEntity.COHORT, cohorts_proxy  , db.fetch_cohorts_by_cohort   , db.count_cohorts_by_cohort, build_cohort_response)
individuals_by_cohort = generic_handler('individuals', BeaconEntity.COHORT, individuals_proxy, db.fetch_individuals_by_cohort, db.count_individuals_by_cohort, build_biosample_or_individual_response)
