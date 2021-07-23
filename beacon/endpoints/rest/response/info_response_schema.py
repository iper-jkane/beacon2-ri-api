import logging

from .... import conf

LOG = logging.getLogger(__name__)

def build_response_summary(exists, num_total_results):
    return {
        'exists': exists,
        'numTotalResults': num_total_results
    }

def build_beacon_handovers():
    return conf.beacon_handovers

def build_beacon_resultset_response(data,
                          num_total_results,
                          qparams_converted,
                          func_response_type,
                          authorized_datasets):
    """"
    Transform data into the Beacon response format.
    """

    beacon_response = {
        'meta': build_meta(qparams_converted),
        'responseSummary': build_response_summary(bool(data), num_total_results),
        # TODO: 'extendedInfo': build_extended_info(),
        'beaconHandovers': build_beacon_handovers(),
        'resultSets': build_response(data, num_total_results, qparams_converted, func_response_type)
    }
    return beacon_response

def build_beacon_info_response(data, qparams_converted, func_response_type, authorized_datasets=[]):
    """"Fills the `results` part with the format for BeaconInfo"""

    meta = build_meta(qparams_converted)

    response = func_response_type(data, qparams_converted, authorized_datasets)

    beacon_response = {
        'meta': meta,
        'response': response,
    }

    return beacon_response

# def build_beacon_response(data, qparams_converted, func_response_type, authorized_datasets=[]):
#     """"
#     Transform data into the Beacon response format.
#     """

#     beacon_response = {
#         'meta': build_meta(qparams_converted),
#         'response': build_response(data, qparams_converted, func_response_type, authorized_datasets)
#     }
#     return beacon_response

def build_meta(qparams):
    """"Builds the `meta` part of the response

    We assume that receivedRequest is the evaluated request (qparams) sent by the user.
    """

    meta = {
        'beaconId': conf.beacon_id,
        'apiVersion': conf.api_version,
        'receivedRequest': build_received_request(qparams),
        'returnedSchemas': [qparams.requestedSchema[0]]
    }
    return meta


def build_received_request(qparams):
    """"Fills the `receivedRequest` part with the request data"""

    request = {
        'meta': {
            'requestedSchemas' : [qparams.requestedSchema[0]],
            'apiVersion' : qparams.apiVersion,
        },
    }

    return request

def build_response(data, num_total_results, qparams, func):
    """"Fills the `response` part with the correct format in `results`"""

    # LOG.debug('Calling f= %s', func)
    results = func(data, qparams)

    response = {
        'id': '',
        'setType': '',
        'exists': str(bool(data)).lower(),
        'resultsCount': len(results),
        'results': results,
        'info': None,
        'resultsHandover': None, # build_results_handover
    }

    # if non_accessible_datasets:
    #     response['error'] = build_error(non_accessible_datasets)

    return response

def build_response_info(data, qparams, func, authorized_datasets=[]):
    """"Fills the `response` part with the correct format in `results`"""

    response = {
            'results': func(data, qparams, authorized_datasets),
            'info': None,
            # 'resultsHandover': None, # build_results_handover
            # 'beaconHandover': None, # build_beacon_handover
        }

    # build_error(qparams)

    return response


def build_service_info_response(datasets, qparams, authorized_datasets=[]):
    """"Fills the `results` part with the format for ServiceInfo"""

    func = qparams.requestedSchema[1]

    return func(datasets, authorized_datasets)


def build_dataset_info_response(data, qparams, authorized_datasets=[]):
    """"Fills the `results` part with the format for Dataset"""

    func = qparams.requestedSchema[1]
    return [func(row, authorized_datasets) for row in data]
