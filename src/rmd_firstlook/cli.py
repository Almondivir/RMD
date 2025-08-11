import typer
import pandas as pd
from .core import compute_rmd

app = typer.Typer()

@app.command()
def main(expr: str, meta: str, A: str, B: str, by: str = None, out: str = 'rmd.csv'):
    expr_df = pd.read_csv(expr).set_index('sample_id')
    meta_df = pd.read_csv(meta)
    res = compute_rmd(expr_df, meta_df, A, B, by=by)
    res.to_csv(out, index=False)
    typer.echo(f'Wrote results to {out}')
if __name__ == '__main__':
    app()
