import pandas as pd

def compute_rmd(expr_df, meta_df, A, B, by=None):
    expr_df = expr_df.copy()
    meta_df = meta_df.copy()
    if by:
        results = []
        for level, sub_meta in meta_df.groupby(by):
            sub_expr = expr_df.loc[sub_meta['sample_id']]
            res = _compute_rmd_basic(sub_expr, sub_meta, A, B)
            res[by] = level
            results.append(res)
        return pd.concat(results, ignore_index=True)
    else:
        return _compute_rmd_basic(expr_df, meta_df, A, B)

def _compute_rmd_basic(expr_df, meta_df, A, B):
    A_ids = meta_df.loc[meta_df['condition'] == A, 'sample_id']
    B_ids = meta_df.loc[meta_df['condition'] == B, 'sample_id']
    mean_A = expr_df.loc[A_ids].mean(axis=0)
    mean_B = expr_df.loc[B_ids].mean(axis=0)
    rmd = mean_A - mean_B
    out = pd.DataFrame({
        'gene': rmd.index,
        f'{A}_mean': mean_A.values,
        f'{B}_mean': mean_B.values,
        'RMD': rmd.values,
        'abs_RMD': rmd.abs().values,
        'sign': rmd.apply(lambda x: '+' if x > 0 else '-')
    }).sort_values('abs_RMD', ascending=False)
    return out.reset_index(drop=True)
