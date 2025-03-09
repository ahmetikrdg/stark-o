import json


def write_results_to_json(y_test, y_pred, y_probs, output_file='results.json'):
    results = {
        "y_test": y_test.tolist() if hasattr(y_test, 'tolist') else y_test,
        "y_pred": y_pred.tolist() if hasattr(y_pred, 'tolist') else y_pred,
        "y_probs": y_probs.tolist() if hasattr(y_probs, 'tolist') else y_probs,
    }

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"Results written to {output_file}")