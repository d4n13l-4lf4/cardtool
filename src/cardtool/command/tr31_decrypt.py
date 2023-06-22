import click


@click.command(name="decrypt-tr31")
@click.option("--kbpk", "-kbpk", type=str, required=True)
@click.option("--kcv", "-kcv", type=str, required=True)
@click.argument("kblock")
def decrypt_tr31(kbpk, kcv, kblock):
    click.echo("Plaintext Key: 0123456789ABCDEFFEDCBA9876543210")
