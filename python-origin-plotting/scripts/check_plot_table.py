"""Read-only semantic checks for precomputed Origin plot tables; no fitting or cleaning."""
import argparse
import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd


SCHEMAS = {
    'reliability': ['bin_left', 'bin_right', 'mean_probability', 'event_frequency', 'n'],
    'fdc': ['exceedance_pct', 'discharge'],
    'composite': ['lag', 'estimate', 'lo', 'hi', 'n'],
    'portrait': ['model', 'metric', 'reference', 'value', 'better', 'status'],
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def numeric(data, columns):
    return data[columns].apply(pd.to_numeric, errors='raise').to_numpy(dtype=float)


def finite(values, label):
    require(np.isfinite(values).all(), label + ': finite values required')


def counts(data):
    n = numeric(data, ['n'])[:, 0]
    finite(n, 'n')
    require(((n >= 0) & (n == np.floor(n))).all(), 'n must contain nonnegative integer counts')
    return n


def check(data, kind):
    require(kind in SCHEMAS, 'Unknown schema')
    require(len(data) > 0, 'Table must not be empty')
    require(data.columns.is_unique, 'Duplicate column names')
    missing = set(SCHEMAS[kind]) - set(data.columns)
    require(not missing, 'Missing columns: ' + ', '.join(sorted(missing)))
    report = {'schema': kind, 'rows': len(data), 'status': 'TABLE_CHECKS_PASSED',
              'scope': 'No statistical inference, metadata or Origin rendering validation.'}
    if kind == 'reliability':
        bounds = numeric(data, ['bin_left', 'bin_right'])
        finite(bounds, 'Bin bounds')
        left, right = bounds.T
        require(((0 <= left) & (left < right) & (right <= 1)).all(), 'Invalid probability bins')
        require((left[1:] >= right[:-1]).all(), 'Bins must be ordered and non-overlapping')
        n = counts(data)
        values = numeric(data, ['mean_probability', 'event_frequency'])
        present = n > 0
        finite(values[present], 'Populated bins')
        require(((values[present] >= 0) & (values[present] <= 1)).all(), 'Probabilities outside [0, 1]')
        require(((values[present, 0] >= left[present]) &
                 (values[present, 0] <= right[present])).all(), 'Mean probability outside its bin')
        require(np.isnan(values[~present]).all(), 'Empty bins must have missing probabilities, not zero')
        report['empty_bins'] = int((~present).sum())
        report['samples'] = int(n.sum())
    elif kind == 'fdc':
        values = numeric(data, ['exceedance_pct', 'discharge'])
        finite(values, 'FDC')
        probability, discharge = values.T
        require(((probability > 0) & (probability < 100)).all(), 'Exceedance must be strictly between 0 and 100 percent')
        require((np.diff(probability) > 0).all(), 'Exceedance probability must strictly increase')
        require((discharge >= 0).all(), 'This discharge schema does not accept negative flow')
        require((np.diff(discharge) <= 0).all(), 'Discharge must not increase with exceedance probability')
        report['zero_flow_rows'] = int((discharge == 0).sum())
        report['log_y_compatible'] = bool((discharge > 0).all())
    elif kind == 'composite':
        lag = numeric(data, ['lag'])[:, 0]
        finite(lag, 'Lag')
        require((np.diff(lag) > 0).all(), 'Lag must strictly increase; one series per table')
        n = counts(data)
        values = numeric(data, ['estimate', 'lo', 'hi'])
        present = n > 0
        finite(values[present], 'Supported lags')
        require((values[present, 1] <= values[present, 2]).all(), 'Reversed interval endpoints')
        require(np.isnan(values[~present]).all(), 'Unsupported lags must have missing estimate and interval')
        # Percentile/bootstrap intervals can exclude the point estimate. Never alter it.
        report['unsupported_lags'] = int((~present).sum())
    elif kind == 'portrait':
        keys = ['model', 'metric', 'reference']
        require(data[keys].notna().all().all(), 'Missing portrait identifier')
        require(data[keys].astype(str).apply(lambda col: col.str.strip().ne('')).all().all(), 'Blank portrait identifier')
        require(not data.duplicated(keys).any(), 'Duplicate model/metric/reference cells; do not silently aggregate')
        require(data['better'].isin(['higher', 'lower']).all(), 'better must be higher or lower')
        require((data.groupby('metric')['better'].nunique() == 1).all(), 'Metric direction changes between rows')
        require(data['status'].isin(['available', 'missing']).all(), 'status must be available or missing')
        values = numeric(data, ['value'])[:, 0]
        present = data['status'].eq('available').to_numpy()
        finite(values[present], 'Available skill values')
        require(np.isnan(values[~present]).all(), 'Missing cells must not contain a numeric value')
        report['missing_cells'] = int((~present).sum())
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kind', required=True, choices=SCHEMAS)
    parser.add_argument('--csv', required=True, type=Path)
    args = parser.parse_args()
    try:
        with args.csv.open(encoding='utf-8-sig', newline='') as stream:
            header = next(csv.reader(stream), [])
        require(len(header) == len(set(header)), 'Duplicate CSV column names')
        # String fields stay literal, including legitimate model names such as "NA".
        data = pd.read_csv(args.csv, encoding='utf-8-sig', keep_default_na=False, na_values=[''], dtype=str)
        result = check(data, args.kind)
    except (ValueError, OSError) as error:
        parser.exit(2, 'Table check failed: ' + str(error) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
