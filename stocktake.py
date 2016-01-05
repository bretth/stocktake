import csv

import click

KEY_MAP = {}  # Map the external record to an internal primary key


def _csv_to_dict(click_file, name, get_pk=False):
    total = 0
    filed = {}
    csvfile = csv.reader(click_file)
    for lineno, row in enumerate(csvfile, start=1):
        if get_pk or (lineno == 1 and len(row) > 2):
            get_pk = True
        pk = row[2] if get_pk else None
        sku = row[0]

        if sku:
            try:
                qty = int(row[1])
                filed[row[0]] = qty
                total += qty
            except ValueError:
                if lineno == 1 and row[1]:  # assume header row
                    pass
                else:
                    click.echo("Warning: No valid quantity for %s row %i" % (name, lineno))
        if pk and sku:
            KEY_MAP[sku] = pk
    click.echo('%i total for %s' % (total, name))
    return filed, total


@click.command()
@click.argument('inventory', type=click.File("rb"))
@click.argument('stockcount', type=click.File("rb"))
@click.argument('adjustments', type=click.File('wb'))
def cli(inventory, stockcount, adjustments):
    """Takes an inventory csv file with sku, qty that is compared
    against a csv file with 'actual' counts and outputs an adjustments file.

    stocktake inventory.csv count.csv adjustments.csv

    By default a negative quantity is a negative adjustment to inventory
    """
    inv, inv_total = _csv_to_dict(inventory, 'inventory')
    count, count_total = _csv_to_dict(stockcount, 'stock count')
    adj_total = count_total - inv_total
    adj_written = 0
    click.echo('--------------')
    click.echo('%i nett adjustments to make' % adj_total)
    skus = set(inv.keys()) | set(count.keys())
    adjwriter = csv.writer(adjustments)
    for sku in skus:
        adj = count.get(sku, 0) - inv.get(sku, 0)
        if KEY_MAP:
            try:
                pk = KEY_MAP[sku]
            except KeyError:
                click.echo('Warning: No primary key for %s' % sku)
                continue
        else:
            pk = sku
        if adj:
            adjwriter.writerow([pk, adj])
            adj_written += adj
    click.echo('%i nett adjustments written' % adj_written)
