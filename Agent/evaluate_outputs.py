import csv
from sklearn.metrics import f1_score
from rouge_score import rouge_scorer
import sys

def normalize_colname(name):
    return name.strip().lower()

# Read outputs and references from a CSV file, robust to large files and flexible headers
def read_outputs(filename):
    outputs = []
    references = []
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # Flexible header matching
        fieldnames = [normalize_colname(c) for c in reader.fieldnames]
        try:
            output_col = fieldnames.index('output')
            ref_col = fieldnames.index('reference')
        except ValueError:
            print("ERROR: CSV must have columns named 'output' and 'reference' (case-insensitive, no extra spaces).", file=sys.stderr)
            sys.exit(1)
        for i, row in enumerate(reader):
            row_values = list(row.values())
            outputs.append(row_values[output_col])
            references.append(row_values[ref_col])
            if (i+1) % 1000 == 0:
                print(f"Processed {i+1} rows...")
    return outputs, references

def compute_rouge(outputs, references):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    scores = [scorer.score(ref, out) for ref, out in zip(references, outputs)]
    avg_rouge1 = sum([s['rouge1'].fmeasure for s in scores]) / len(scores)
    avg_rougeL = sum([s['rougeL'].fmeasure for s in scores]) / len(scores)
    return avg_rouge1, avg_rougeL

def compute_f1(outputs, references):
    f1s = []
    for out, ref in zip(outputs, references):
        out_set = set(out.lower().split())
        ref_set = set(ref.lower().split())
        common = out_set & ref_set
        if len(out_set) == 0 or len(ref_set) == 0:
            f1s.append(0.0)
            continue
        precision = len(common) / len(out_set)
        recall = len(common) / len(ref_set)
        if precision + recall == 0:
            f1s.append(0.0)
        else:
            f1s.append(2 * precision * recall / (precision + recall))
    return sum(f1s) / len(f1s)

if __name__ == "__main__":
    try:
        outputs, references = read_outputs("outputs_vs_refs.csv")
    except Exception as e:
        print(f"ERROR: Failed to read or process CSV: {e}", file=sys.stderr)
        sys.exit(1)
    if not outputs or not references:
        print("ERROR: No data found in CSV.", file=sys.stderr)
        sys.exit(1)
    avg_rouge1, avg_rougeL = compute_rouge(outputs, references)
    avg_f1 = compute_f1(outputs, references)
    print(f"Average ROUGE-1: {avg_rouge1:.2f}, ROUGE-L: {avg_rougeL:.2f}, F1: {avg_f1:.2f}") 